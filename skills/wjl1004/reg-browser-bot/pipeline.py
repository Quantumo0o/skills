#!/usr/bin/env python3
"""
pipeline.py - 自动化流水线架构

Phase 5 新增:
- Pipeline 流水线编排
- 预置流水线:LoginPipeline, CollectPipeline, PostPipeline
- 错误处理和状态管理
"""

import logging
from typing import Callable, Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from browser_manager import BrowserManager, BrowserContext
from browser_config import get_config

# Phase B: SQLite 存储支持
try:
    from models import DatabaseManager, PipelineExecution, get_database
except ImportError:
    import sys as _sys
    _sys.path.insert(0, str(__file__).rsplit('/', 1)[0] if '/' in __file__ else '.')
    from models import DatabaseManager, PipelineExecution, get_database


class PipelineState(Enum):
    """流水线状态"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PipelineStep:
    """流水线步骤"""
    name: str
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    retry: int = 3  # 重试次数
    retry_delay: float = 1.0  # 重试间隔(秒)
    required: bool = True  # 是否必需


@dataclass
class PipelineResult:
    """流水线执行结果"""
    success: bool
    state: PipelineState
    step_results: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


class Pipeline:
    """
    自动化流水线

    用法:
        pipeline = Pipeline("my_pipeline")
        pipeline.add_step(login_step, "登录")
        pipeline.add_step(collect_step, "采集")
        result = pipeline.execute(context={"account": "user1"})
    """

    @property
    def db(self) -> DatabaseManager:
        """懒加载数据库管理器"""
        if self._db is None:
            self._db = get_database()
        return self._db

    def __init__(self, name: str, logger: Optional[logging.Logger] = None):
        """
        初始化流水线

        Args:
            name: 流水线名称
            logger: 日志记录器,None时使用默认
        """
        self.name = name
        self.steps: List[PipelineStep] = []
        self.state = PipelineState.IDLE
        self.logger = logger or logging.getLogger(f"Pipeline.{name}")
        self._browser_manager = BrowserManager.get_instance()
        self._on_error_handlers: List[Callable] = []
        self._on_step_complete_handlers: List[Callable] = []
        # Phase B: SQLite 数据库管理器
        self._db: Optional[DatabaseManager] = None

    def add_step(self, step_func: Callable, name: str,
                 args: tuple = None, kwargs: Dict[str, Any] = None,
                 retry: int = 3, retry_delay: float = 1.0,
                 required: bool = True) -> 'Pipeline':
        """
        添加步骤

        Args:
            step_func: 步骤函数,签名: func(context, *args, **kwargs)
            name: 步骤名称
            args: 位置参数
            kwargs: 关键字参数
            retry: 重试次数
            retry_delay: 重试间隔
            required: 是否必需(失败时终止流水线)

        Returns:
            self: 支持链式调用
        """
        step = PipelineStep(
            name=name,
            func=step_func,
            args=args or (),
            kwargs=kwargs or {},
            retry=retry,
            retry_delay=retry_delay,
            required=required
        )
        self.steps.append(step)
        self.logger.debug(f"添加步骤: {name}")
        return self

    def on_error(self, handler: Callable[[str, Exception], None]) -> 'Pipeline':
        """
        注册错误处理函数

        Args:
            handler: 错误处理函数,签名: handler(step_name, error)

        Returns:
            self: 支持链式调用
        """
        self._on_error_handlers.append(handler)
        return self

    def on_step_complete(self, handler: Callable[[str, Any], None]) -> 'Pipeline':
        """
        注册步骤完成处理函数

        Args:
            handler: 处理函数,签名: handler(step_name, result)

        Returns:
            self: 支持链式调用
        """
        self._on_step_complete_handlers.append(handler)
        return self

    def execute(self, context: Dict[str, Any] = None) -> PipelineResult:
        """
        执行流水线

        Args:
            context: 执行上下文,会在步骤间传递

        Returns:
            PipelineResult: 执行结果
        """
        if not self.steps:
            return PipelineResult(
                success=True,
                state=PipelineState.COMPLETED,
                context=context or {}
            )

        self.state = PipelineState.RUNNING
        context = context or {}
        step_results = []

        # Phase B: 记录开始时间并保存初始状态到 SQLite
        import uuid
        from datetime import datetime
        execution_id = str(uuid.uuid4())
        started_at = datetime.now().isoformat()

        self.logger.info(f"流水线开始执行: {self.name} (共 {len(self.steps)} 个步骤)")

        for i, step in enumerate(self.steps):
            self.logger.info(f"执行步骤 [{i+1}/{len(self.steps)}]: {step.name}")

            result = self._execute_step(step, context, step_results)

            if not result['success']:
                self.state = PipelineState.FAILED
                error_msg = f"步骤 '{step.name}' 失败: {result.get('error')}"
                self.logger.error(error_msg)

                # 调用错误处理
                self._notify_error(step.name, result['error'])

                # 如果是必需步骤,终止流水线
                if step.required:
                    # Phase B: 保存失败状态到 SQLite
                    self._save_pipeline_execution(
                        execution_id=execution_id,
                        state='failed',
                        step_results=step_results,
                        context=context,
                        error=error_msg,
                        started_at=started_at
                    )
                    return PipelineResult(
                        success=False,
                        state=self.state,
                        step_results=step_results,
                        error=error_msg,
                        context=context
                    )

            # 调用步骤完成处理
            self._notify_step_complete(step.name, result.get('result'))

            step_results.append(result)

        self.state = PipelineState.COMPLETED
        self.logger.info(f"流水线执行完成: {self.name}")

        # Phase B: 保存执行结果到 SQLite
        self._save_pipeline_execution(
            execution_id=execution_id,
            state='completed',
            step_results=step_results,
            context=context,
            error=None,
            started_at=started_at
        )

        return PipelineResult(
            success=True,
            state=self.state,
            step_results=step_results,
            context=context
        )

    def _execute_step(self, step: PipelineStep, context: Dict,
                      step_results: List) -> Dict[str, Any]:
        """执行单个步骤(带重试)"""
        last_error = None

        for attempt in range(step.retry + 1):
            try:
                # 为步骤注入 browser_manager
                step_kwargs = dict(step.kwargs)
                if 'browser_manager' not in step_kwargs:
                    step_kwargs['browser_manager'] = self._browser_manager

                result = step.func(context, *step.args, **step_kwargs)

                return {
                    'success': True,
                    'name': step.name,
                    'result': result,
                    'attempts': attempt + 1
                }

            except Exception as e:
                last_error = e
                self.logger.warning(
                    f"步骤 '{step.name}' 执行失败 (尝试 {attempt + 1}/{step.retry + 1}): {e}"
                )

                if attempt < step.retry:
                    import time
                    time.sleep(step.retry_delay * (attempt + 1))  # 递增等待

        return {
            'success': False,
            'name': step.name,
            'error': str(last_error),
            'attempts': step.retry + 1
        }

    def _notify_error(self, step_name: str, error: Any):
        """通知错误处理"""
        for handler in self._on_error_handlers:
            try:
                handler(step_name, error)
            except Exception as e:
                self.logger.warning(f"错误处理函数执行失败: {e}")

    def _notify_step_complete(self, step_name: str, result: Any):
        """通知步骤完成"""
        for handler in self._on_step_complete_handlers:
            try:
                handler(step_name, result)
            except Exception as e:
                self.logger.warning(f"步骤完成处理函数执行失败: {e}")

    def _save_pipeline_execution(
        self,
        execution_id: str,
        state: str,
        step_results: List,
        context: Dict,
        error: Optional[str],
        started_at: str
    ) -> None:
        """
        Phase B: 保存流水线执行记录到 SQLite

        Args:
            execution_id: 执行ID
            state: 执行状态
            step_results: 步骤结果列表
            context: 执行上下文
            error: 错误信息
            started_at: 开始时间
        """
        try:
            from datetime import datetime
            completed_at = datetime.now().isoformat()
            duration = (datetime.now() - datetime.fromisoformat(started_at)).total_seconds()

            pe = PipelineExecution(
                id=execution_id,
                pipeline_name=self.name,
                state=state,
                context=context,
                step_results=step_results,
                error=error,
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration
            )
            self.db.save_task  # DatabaseManager doesn't have save_pipeline_execution, use generic approach
            # 直接用 SQL 保存（PipelineExecution 表结构与 Task 兼容但不相同）
            import json
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO pipeline_executions
                    (id, pipeline_name, state, context, step_results, error,
                     started_at, completed_at, duration_seconds)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pe.id, pe.pipeline_name, pe.state,
                    json.dumps(pe.context), json.dumps(pe.step_results),
                    pe.error, pe.started_at, pe.completed_at, pe.duration_seconds
                ))
                conn.commit()
            self.logger.debug(f"流水线执行记录已保存SQLite: {execution_id}")
        except Exception as e:
            self.logger.warning(f"SQLite保存流水线执行记录失败: {e}")

    def cancel(self):
        """取消流水线"""
        self.state = PipelineState.CANCELLED
        self.logger.warning(f"流水线已取消: {self.name}")

    def pause(self):
        """暂停流水线"""
        if self.state == PipelineState.RUNNING:
            self.state = PipelineState.PAUSED
            self.logger.info(f"流水线已暂停: {self.name}")

    def resume(self):
        """恢复流水线"""
        if self.state == PipelineState.PAUSED:
            self.state = PipelineState.RUNNING
            self.logger.info(f"流水线已恢复: {self.name}")


# =============================================================================
# 预置步骤函数
# =============================================================================

def login_step(context: Dict, account_name: str = None, **kwargs) -> Dict:
    """
    登录步骤

    Args:
        context: 执行上下文
        account_name: 账号名称

    Returns:
        Dict: 包含 cookies 的结果
    """
    from account import AccountManager

    account_name = account_name or context.get('account_name', 'default')
    manager = BrowserManager.get_instance()
    browser = manager.get_browser(profile_id=f"login_{account_name}")

    try:
        account_mgr = AccountManager()
        account = account_mgr.get_account(account_name)

        if not account:
            raise ValueError(f"账号不存在: {account_name}")

        # 访问登录页
        browser.navigate(account.get('login_url', 'https://www.example.com/login'))

        # TODO: 根据实际网站实现登录逻辑
        # 这里需要根据具体网站的登录表单实现

        cookies = browser.get_cookies()
        context['cookies'] = cookies
        context['account_name'] = account_name

        return {'success': True, 'cookies': cookies}

    finally:
        manager.release_browser(f"login_{account_name}")


def captcha_solve_step(context: Dict, captcha_type: str = 'slider', **kwargs) -> Dict:
    """
    验证码解决步骤

    Args:
        context: 执行上下文
        captcha_type: 验证码类型 ('slider', 'click', 'image')

    Returns:
        Dict: 验证码解决结果
    """
    from captcha import CaptchaSolver

    captcha_solver = CaptchaSolver()
    result = captcha_solver.solve(captcha_type)

    context['captcha_result'] = result
    return result


def collect_step(context: Dict, target: str = None, max_count: int = 10, **kwargs) -> Dict:
    """
    数据采集步骤

    Args:
        context: 执行上下文
        target: 采集目标关键词
        max_count: 最大采集数量

    Returns:
        Dict: 采集结果
    """
    from collector import DataCollector

    target = target or context.get('target', '')
    profile_id = context.get('account_name', 'default')

    manager = BrowserManager.get_instance()
    browser = manager.get_browser(profile_id=profile_id)

    try:
        collector = DataCollector()
        results = collector.collect(target, max_count)

        context['collected_data'] = results
        context['collect_count'] = len(results)

        return {'success': True, 'count': len(results), 'data': results}

    finally:
        manager.release_browser(profile_id)


def save_step(context: Dict, save_path: str = None, **kwargs) -> Dict:
    """
    数据保存步骤

    Args:
        context: 执行上下文
        save_path: 保存路径

    Returns:
        Dict: 保存结果
    """
    import json
    import os

    data = context.get('collected_data', [])
    save_path = save_path or context.get('save_path',
                                          os.path.expanduser('~/.openclaw/data/collection.json'))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    context['save_path'] = save_path
    return {'success': True, 'path': save_path, 'count': len(data)}


def post_step(context: Dict, content: str = None, **kwargs) -> Dict:
    """
    内容发布步骤

    Args:
        context: 执行上下文
        content: 发布内容

    Returns:
        Dict: 发布结果
    """
    from poster import AutoPoster

    content = content or context.get('post_content', '')
    profile_id = context.get('account_name', 'default')

    manager = BrowserManager.get_instance()
    browser = manager.get_browser(profile_id=profile_id)

    try:
        poster = AutoPoster()
        result = poster.post(content, browser)

        context['post_result'] = result
        return result

    finally:
        manager.release_browser(profile_id)


# =============================================================================
# 预置流水线
# =============================================================================

class LoginPipeline(Pipeline):
    """登录流水线:登录 → 保存Cookie"""

    def __init__(self, account_name: str = "default"):
        super().__init__(f"LoginPipeline_{account_name}")
        self.account_name = account_name
        self.add_step(
            login_step,
            "登录",
            kwargs={'account_name': account_name}
        )
        self.add_step(
            self._save_cookies,
            "保存Cookie",
            required=False
        )

    def _save_cookies(self, context: Dict, **kwargs) -> Dict:
        """保存Cookie到账号"""
        from account import AccountManager

        cookies = context.get('cookies', [])
        account_name = context.get('account_name', self.account_name)

        account_mgr = AccountManager()
        account_mgr.save_cookies(account_name, cookies)

        return {'success': True, 'cookies_count': len(cookies)}


class CollectPipeline(Pipeline):
    """采集流水线:登录 → 采集 → 保存"""

    def __init__(self, account_name: str = "default", target: str = "", max_count: int = 10):
        super().__init__(f"CollectPipeline_{account_name}")
        self.account_name = account_name
        self.target = target

        self.add_step(
            login_step,
            "登录",
            kwargs={'account_name': account_name}
        )
        self.add_step(
            collect_step,
            "采集数据",
            kwargs={'target': target, 'max_count': max_count}
        )
        self.add_step(
            save_step,
            "保存数据",
            required=False
        )


class PostPipeline(Pipeline):
    """发布流水线:登录 → 验证码 → 发布"""

    def __init__(self, account_name: str = "default", content: str = ""):
        super().__init__(f"PostPipeline_{account_name}")
        self.account_name = account_name
        self.content = content

        self.add_step(
            login_step,
            "登录",
            kwargs={'account_name': account_name}
        )
        self.add_step(
            captcha_solve_step,
            "解决验证码",
            kwargs={'captcha_type': 'slider'},
            required=False  # 如果没有验证码也继续
        )
        self.add_step(
            post_step,
            "发布内容",
            kwargs={'content': content}
        )


def create_pipeline(pipeline_type: str, **kwargs) -> Pipeline:
    """
    工厂函数:创建预置流水线

    Args:
        pipeline_type: 流水线类型 ('login', 'collect', 'post')
        **kwargs: 流水线参数

    Returns:
        Pipeline: 流水线实例
    """
    factories = {
        'login': LoginPipeline,
        'collect': CollectPipeline,
        'post': PostPipeline,
    }

    factory = factories.get(pipeline_type.lower())
    if not factory:
        raise ValueError(f"未知流水线类型: {pipeline_type}")

    return factory(**kwargs)
