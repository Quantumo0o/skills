#!/usr/bin/env python3
"""
task_scheduler.py - 任务调度器

Phase 5 新增:
- 基于 APScheduler 的后台调度器
- 支持 cron/interval/date 触发器
- 持久化任务配置
- 任务执行状态跟踪
"""

import logging
import json
import os
from typing import Callable, Any, Dict, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    from apscheduler.triggers.date import DateTrigger
    from apscheduler.jobstores.memory import MemoryJobStore
    from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
    APSCHEDULER_AVAILABLE = True
except ImportError:
    APSCHEDULER_AVAILABLE = False


class TriggerType(Enum):
    """触发器类型"""
    CRON = "cron"
    INTERVAL = "interval"
    DATE = "date"


@dataclass
class ScheduledTask:
    """调度任务定义"""
    id: str
    name: str
    func_name: str
    func_args: tuple = field(default_factory=tuple)
    func_kwargs: Dict[str, Any] = field(default_factory=dict)
    trigger_type: str = "interval"
    # cron 字段
    second: Optional[str] = None
    minute: Optional[str] = None
    hour: Optional[str] = None
    day: Optional[str] = None
    month: Optional[str] = None
    day_of_week: Optional[str] = None
    # interval 字段
    seconds: Optional[int] = None
    minutes: Optional[int] = None
    hours: Optional[int] = None
    # date 字段
    run_date: Optional[str] = None
    # 元数据
    enabled: bool = True
    max_instances: int = 1
    coalesce: bool = False
    next_run_time: Optional[str] = None
    last_run_time: Optional[str] = None
    run_count: int = 0


class TaskScheduler:
    """
    任务调度器
    
    功能：
    - 基于 APScheduler 的后台调度
    - 支持 cron/interval/date 触发器
    - 持久化任务配置
    - 任务执行状态跟踪
    
    用法:
        scheduler = TaskScheduler()
        scheduler.add_job(my_func, "interval", seconds=60, name="每分钟任务")
        scheduler.start()
    """
    
    def __init__(self, config_dir: str = None, jobs_file: str = None):
        """
        初始化调度器
        
        Args:
            config_dir: 配置目录，默认 ~/.openclaw/scheduler/
            jobs_file: 任务配置文件，默认 config_dir/jobs.json
        """
        if not APSCHEDULER_AVAILABLE:
            raise ImportError(
                "APScheduler 未安装。请运行: pip install apscheduler"
            )
        
        self._logger = logging.getLogger(self.__class__.__name__)
        self._config_dir = config_dir or os.path.expanduser("~/.openclaw/scheduler")
        self._jobs_file = jobs_file or os.path.join(self._config_dir, "jobs.json")
        
        # 初始化 APScheduler
        jobstores = {
            'default': MemoryJobStore()
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 1,
            'misfire_grace_time': 60
        }
        
        self._scheduler = BackgroundScheduler(
            jobstores=jobstores,
            job_defaults=job_defaults,
            timezone='Asia/Shanghai'
        )
        
        # 任务注册表（函数名 -> 函数）
        self._registered_funcs: Dict[str, Callable] = {}
        
        # 加载已保存的任务配置
        self._tasks: Dict[str, ScheduledTask] = {}
        self._load_tasks()
        
        # 注册事件监听器
        self._register_listeners()
    
    def register_func(self, name: str, func: Callable) -> None:
        """
        注册可调度的函数
        
        Args:
            name: 函数名称
            func: 函数对象
        """
        self._registered_funcs[name] = func
        self._logger.debug(f"注册函数: {name}")
    
    def add_job(self, func: Callable = None, trigger: str = "interval",
                name: str = None, job_id: str = None,
                **kwargs) -> Optional[str]:
        """
        添加定时任务
        
        Args:
            func: 任务函数，或函数名（字符串）
            trigger: 触发器类型 ('cron', 'interval', 'date')
            name: 任务名称
            job_id: 任务ID，默认使用函数名
            **kwargs: 触发器参数
                - cron: second, minute, hour, day, month, day_of_week
                - interval: seconds, minutes, hours, start_date, end_date
                - date: run_date
            
        Returns:
            str: 任务ID，或 None（失败时）
        
        用法:
            # 每分钟执行
            scheduler.add_job(my_func, "interval", seconds=60, name="每分钟任务")
            
            # 每天凌晨2点执行
            scheduler.add_job(my_func, "cron", hour=2, minute=0, name="每日任务")
            
            # 指定时间执行（一次性）
            scheduler.add_job(my_func, "date", run_date="2026-04-05 10:00:00", name="一次性任务")
            
            # 使用已注册的函数名
            scheduler.add_job("my_task_func", "interval", seconds=60, name="每分钟任务")
        """
        # 处理 func 参数
        if func is None:
            raise ValueError("func 不能为空")
        
        if isinstance(func, str):
            func_name = func
            if func_name not in self._registered_funcs:
                self._logger.error(f"函数未注册: {func_name}")
                return None
            func = self._registered_funcs[func_name]
        else:
            func_name = getattr(func, '__name__', str(func))
        
        # 生成 job_id
        job_id = job_id or func_name
        
        # 创建 ScheduledTask
        task = ScheduledTask(
            id=job_id,
            name=name or func_name,
            func_name=func_name,
            trigger_type=trigger,
            **self._extract_trigger_kwargs(trigger, kwargs)
        )
        
        # 构建 APScheduler 触发器
        apscheduler_trigger = self._create_trigger(task)
        
        try:
            self._scheduler.add_job(
                func=func,
                trigger=apscheduler_trigger,
                id=job_id,
                name=task.name,
                **self._get_job_defaults(task)
            )
            
            self._tasks[job_id] = task
            self._save_tasks()
            
            self._logger.info(f"添加任务: {task.name} (id={job_id}, trigger={trigger})")
            return job_id
            
        except Exception as e:
            self._logger.error(f"添加任务失败: {e}")
            return None
    
    def remove_job(self, job_id: str) -> bool:
        """
        移除任务
        
        Args:
            job_id: 任务ID
            
        Returns:
            bool: 是否成功
        """
        try:
            self._scheduler.remove_job(job_id)
            if job_id in self._tasks:
                del self._tasks[job_id]
                self._save_tasks()
            self._logger.info(f"移除任务: {job_id}")
            return True
        except Exception as e:
            self._logger.warning(f"移除任务失败: {e}")
            return False
    
    def pause_job(self, job_id: str) -> bool:
        """暂停任务"""
        try:
            self._scheduler.pause_job(job_id)
            if job_id in self._tasks:
                self._tasks[job_id].enabled = False
                self._save_tasks()
            self._logger.info(f"暂停任务: {job_id}")
            return True
        except Exception as e:
            self._logger.warning(f"暂停任务失败: {e}")
            return False
    
    def resume_job(self, job_id: str) -> bool:
        """恢复任务"""
        try:
            self._scheduler.resume_job(job_id)
            if job_id in self._tasks:
                self._tasks[job_id].enabled = True
                self._save_tasks()
            self._logger.info(f"恢复任务: {job_id}")
            return True
        except Exception as e:
            self._logger.warning(f"恢复任务失败: {e}")
            return False
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        获取任务信息
        
        Returns:
            Dict 或 None
        """
        job = self._scheduler.get_job(job_id)
        if job is None:
            return None
        
        task = self._tasks.get(job_id)
        return {
            'id': job.id,
            'name': job.name,
            'next_run_time': str(job.next_run_time) if job.next_run_time else None,
            'trigger': str(job.trigger),
            'enabled': task.enabled if task else True,
        }
    
    def get_jobs(self) -> List[Dict[str, Any]]:
        """获取所有任务列表"""
        jobs = []
        for job in self._scheduler.get_jobs():
            task = self._tasks.get(job.id)
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': str(job.next_run_time) if job.next_run_time else None,
                'trigger': str(job.trigger),
                'enabled': task.enabled if task else True,
            })
        return jobs
    
    def start(self, paused: bool = False):
        """
        启动调度器
        
        Args:
            paused: 是否以暂停状态启动
        """
        if self._scheduler.running:
            self._logger.warning("调度器已在运行")
            return
        
        self._scheduler.start(paused=paused)
        self._logger.info(f"调度器已启动 (paused={paused})")
    
    def shutdown(self, wait: bool = True):
        """
        关闭调度器
        
        Args:
            wait: 是否等待正在执行的任务完成
        """
        if not self._scheduler.running:
            self._logger.warning("调度器未运行")
            return
        
        self._scheduler.shutdown(wait=wait)
        self._save_tasks()
        self._logger.info("调度器已关闭")
    
    def run_job(self, job_id: str) -> bool:
        """
        手动触发执行任务
        
        Args:
            job_id: 任务ID
            
        Returns:
            bool: 是否成功触发
        """
        try:
            job = self._scheduler.get_job(job_id)
            if job:
                job.modify(next_run_time=datetime.now())
                self._logger.info(f"手动触发任务: {job_id}")
                return True
            return False
        except Exception as e:
            self._logger.error(f"触发任务失败: {e}")
            return False
    
    # =========================================================================
    # 内部方法
    # =========================================================================
    
    def _extract_trigger_kwargs(self, trigger_type: str, kwargs: Dict) -> Dict:
        """从 kwargs 提取触发器参数"""
        task_kwargs = {}
        
        if trigger_type == "cron":
            for field in ['second', 'minute', 'hour', 'day', 'month', 'day_of_week']:
                if field in kwargs:
                    task_kwargs[field] = kwargs.pop(field)
        
        elif trigger_type == "interval":
            for field in ['seconds', 'minutes', 'hours', 'start_date', 'end_date']:
                if field in kwargs:
                    task_kwargs[field] = kwargs.pop(field)
        
        elif trigger_type == "date":
            if 'run_date' in kwargs:
                task_kwargs['run_date'] = kwargs.pop('run_date')
        
        return task_kwargs
    
    def _create_trigger(self, task: ScheduledTask):
        """创建 APScheduler 触发器"""
        if task.trigger_type == "cron":
            return CronTrigger(
                second=task.second,
                minute=task.minute,
                hour=task.hour,
                day=task.day,
                month=task.month,
                day_of_week=task.day_of_week
            )
        elif task.trigger_type == "interval":
            return IntervalTrigger(
                seconds=task.seconds,
                minutes=task.minutes,
                hours=task.hours
            )
        elif task.trigger_type == "date":
            return DateTrigger(run_date=task.run_date)
        else:
            raise ValueError(f"未知触发器类型: {task.trigger_type}")
    
    def _get_job_defaults(self, task: ScheduledTask) -> Dict:
        """获取任务参数"""
        return {
            'max_instances': task.max_instances,
            'coalesce': task.coalesce
        }
    
    def _register_listeners(self):
        """注册事件监听器"""
        def on_job_executed(event):
            job = event.job
            if job.id in self._tasks:
                self._tasks[job.id].run_count += 1
                self._tasks[job.id].last_run_time = datetime.now().isoformat()
                self._tasks[job.id].next_run_time = str(job.next_run_time) if job.next_run_time else None
            self._logger.debug(f"任务执行完成: {job.id}")
        
        def on_job_error(event):
            job = event.job
            self._logger.error(f"任务执行错误: {job.id}, exception: {event.exception}")
        
        self._scheduler.add_listener(on_job_executed, EVENT_JOB_EXECUTED)
        self._scheduler.add_listener(on_job_error, EVENT_JOB_ERROR)
    
    def _save_tasks(self):
        """保存任务配置到文件"""
        try:
            os.makedirs(self._config_dir, exist_ok=True)
            
            tasks_data = {}
            for job_id, task in self._tasks.items():
                tasks_data[job_id] = asdict(task)
            
            with open(self._jobs_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
            
            self._logger.debug(f"任务配置已保存: {self._jobs_file}")
        except Exception as e:
            self._logger.error(f"保存任务配置失败: {e}")
    
    def _load_tasks(self):
        """从文件加载任务配置"""
        if not os.path.exists(self._jobs_file):
            return
        
        try:
            with open(self._jobs_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            for job_id, task_data in tasks_data.items():
                self._tasks[job_id] = ScheduledTask(**task_data)
            
            self._logger.info(f"加载了 {len(self._tasks)} 个任务配置")
        except Exception as e:
            self._logger.error(f"加载任务配置失败: {e}")


# =============================================================================
# 便捷函数
# =============================================================================

_default_scheduler: Optional[TaskScheduler] = None


def get_scheduler() -> TaskScheduler:
    """获取全局调度器实例"""
    global _default_scheduler
    if _default_scheduler is None:
        _default_scheduler = TaskScheduler()
    return _default_scheduler


def schedule_task(func: Callable = None, trigger: str = "interval", 
                  name: str = None, job_id: str = None,
                  **kwargs) -> Optional[str]:
    """
    快速添加任务的便捷函数
    
    用法:
        # 每分钟执行
        schedule_task(my_func, "interval", seconds=60, name="每分钟任务")
        
        # 每天凌晨2点执行
        schedule_task(my_func, "cron", hour=2, minute=0, name="每日任务")
    """
    scheduler = get_scheduler()
    return scheduler.add_job(func, trigger, name, job_id, **kwargs)


def remove_scheduled_task(job_id: str) -> bool:
    """移除定时任务"""
    return get_scheduler().remove_job(job_id)


def start_scheduler():
    """启动全局调度器"""
    scheduler = get_scheduler()
    scheduler.start()


def stop_scheduler():
    """停止全局调度器"""
    global _default_scheduler
    if _default_scheduler:
        _default_scheduler.shutdown()
        _default_scheduler = None
