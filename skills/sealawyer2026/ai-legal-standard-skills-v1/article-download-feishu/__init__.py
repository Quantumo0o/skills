#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 文章下载技能 - 飞书版

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class ArticleDownloadFeishu:
    """文章下载技能 - 飞书版"""
    
    def __init__(self):
        self.feishu_app_id = "cli_a91180a31238dcd2"
        self.feishu_app_secret = "hprX1KkMZuoFSN1G9awnjcDwxNTJKXCV"
        self.feishu_user_id = "ou_5701bdf1ba73fc12133c04858da7af5c"
        self.base_url = "https://open.feishu.cn/open-apis"
        
        # 技能目录
        self.skill_dir = Path(__file__).parent
        self.articles_dir = self.skill_dir / "articles"
        self.uploads_dir = self.skill_dir / "uploads"
        
        # 创建目录
        self.articles_dir.mkdir(exist_ok=True)
        self.uploads_dir.mkdir(exist_ok=True)
        
        # 预定义的文章模板
        self.article_templates = {
            "contract_breach": {
                "title": "合同违约责任详解",
                "content": """# 合同违约责任详解

## 引言

合同签订后，一方不履行义务怎么办？民法典第577条为您提供了明确的法律依据。

## 一、法条原文

**《中华人民共和国民法典》第五百七十七条**

当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。

## 二、法律要点

### 1. 违约责任的构成要件

- **有效合同存在**：双方签订了合法有效的合同
- **违约行为发生**：一方不履行或不符合约定
- **造成实际损失**：给守约方造成损失

### 2. 承担责任的方式

- **继续履行**：要求对方继续履行义务
- **采取补救措施**：修理、更换、重做
- **赔偿损失**：赔偿实际损失

## 三、实务应用

### 常见违约情形

1. 逾期履行：要求支付逾期利息
2. 质量瑕疵：要求修理、更换或退货
3. 拒绝履行：解除合同并赔偿损失

### 如何主张违约责任

1. **收集证据**：合同原件、履约证据、损失证明
2. **发送通知**：书面通知对方，保留凭证
3. **协商解决**：尝试协商，保留记录
4. **法律途径**：协商不成可起诉

## 四、案例分析

张某与李某签订房屋买卖合同，约定李某于2025年12月31日前交付房屋。到期后，李某逾期1个月才交付，导致张某多支付房租5000元。

**结果**：李某赔偿张某5000元。

## 五、温馨提示

1. 保留证据至关重要
2. 及时维权
3. 合理约定合同条款
4. 选择适当的维权方式

## 结尾

合同是双方的法律承诺，违约就要承担责任。希望今天的分享对您有所帮助。

---

**北京能扬律师事务所**
专业法律服务
"""
            }
        }
    
    def get_tenant_access_token(self) -> Optional[str]:
        """获取租户访问令"""
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.feishu_app_id,
            "app_secret": self.feishu_app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                return result.get("tenant_access_token")
            else:
                print(f"❌ 获取租户令失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 获取租户令异常: {e}")
            return None
    
    def generate_article_content(
        self,
        template_key: str,
        custom_content: Optional[str] = None
    ) -> str:
        """生成文章内容"""
        
        # 如果有自定义内容，直接使用
        if custom_content:
            return custom_content
        
        # 否则使用预定义模板
        template = self.article_templates.get(template_key)
        if not template:
            return ""
        
        return template.get("content", "")
    
    def generate_card(
        self,
        title: str,
        summary: str,
        download_url: str,
        file_name: str,
        file_size: str
    ) -> Dict[str, Any]:
        """生成飞书机器人卡片"""
        
        card = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "title": f"📄 {title}",
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"{summary}\n\n"
                                       f"**文件名**: {file_name}\n"
                                       f"**文件大小**: {file_size}\n\n"
                                       f"👇 点击下方按钮下载文件"
                        }
                    },
                    {
                        "tag": "hr"
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "📥 下载Word文档"
                                },
                                "type": "primary",
                                "url": download_url
                            }
                        ]
                    }
                ]
            }
        }
        
        return card
    
    def generate_text_version(
        self,
        title: str,
        content: str
    ) -> str:
        """生成纯文本版本（备用）"""
        
        text = f"""📄 {title}

{content}

---
💡 温馨提示：
   - 您可以复制以上内容到Word
   - 如有需要，可以请求生成docx文件

---
📅 北京能扬律师事务所
专业法律服务
"""
        
        return text
    
    def send_card(self, card: Dict[str, Any]) -> Dict[str, Any]:
        """发送卡片到飞书（开发中）"""
        
        # TODO: 实现飞书机器人API调用
        # 这需要：
        # 1. 飞书机器人API配置
        # 2. 消息发送API调用
        # 3. 用户ID验证
        
        return {
            "success": False,
            "message": "飞书机器人API调用功能开发中",
            "card": card
        }
    
    def save_article(
        self,
        template_key: str,
        content: Optional[str] = None
    ) -> Dict[str, Any]:
        """保存文章到文件"""
        
        # 生成内容
        if content:
            article_content = content
            title = f"自定义文章_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        else:
            article_content = self.generate_article_content(template_key)
            template = self.article_templates.get(template_key, {})
            title = template.get("title", "未命名文章")
        
        # 保存文章
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        article_file = self.articles_dir / f"{title}_{timestamp}.md"
        
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        return {
            "success": True,
            "file_path": str(article_file),
            "file_name": article_file.name,
            "file_size": article_file.stat().st_size,
            "template_key": template_key
        }
