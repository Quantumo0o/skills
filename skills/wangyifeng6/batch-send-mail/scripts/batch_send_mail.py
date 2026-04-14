#!/usr/bin/env python3
"""
Bulk Email Sender
===============
批量发送个性化邮件，支持变量替换、HTML格式和附件。

用法:
python bulk_email_sender.py \
  --table contacts.csv \
  --template template.txt \
  --subject "邮件主题" \
  [--dry-run]

首次使用会提示输入 SMTP 配置并保存到配置文件，后续使用自动读取配置。
也可以通过命令行参数覆盖配置文件中的设置。
"""

import argparse
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import configparser
import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.parent
CONFIG_PATH = SCRIPT_DIR / 'config' / 'config.ini'


def load_config():
    """加载配置文件，如果不存在则交互式创建"""
    config = configparser.ConfigParser()

    if CONFIG_PATH.exists():
        config.read(CONFIG_PATH, encoding='utf-8')
        if 'smtp' in config:
            return config
        else:
            print(f"配置文件 {CONFIG_PATH} 格式不正确，将重新创建...")

    # 配置不存在或格式不正确，交互式创建
    print("=== 首次使用，请配置 SMTP 信息 ===")
    print()
    server = input("请输入 SMTP 服务器地址 (例如: smtp.qq.com): ").strip()
    while not server:
        server = input("SMTP 服务器地址不能为空，请重新输入: ").strip()

    port_input = input(f"请输入 SMTP 端口 (默认 587): ").strip()
    port = int(port_input) if port_input else 587

    sender_email = input("请输入发件人邮箱地址: ").strip()
    while not sender_email or '@' not in sender_email:
        sender_email = input("邮箱格式不正确，请重新输入: ").strip()

    sender_password = input("请输入密码/授权码: ").strip()
    while not sender_password:
        sender_password = input("密码/授权码不能为空，请重新输入: ").strip()

    # 保存配置
    config['smtp'] = {
        'server': server,
        'port': str(port),
        'sender_email': sender_email,
        'sender_password': sender_password
    }

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)

    print()
    print(f"✓ 配置已保存到 {CONFIG_PATH}")
    print()

    return config


def read_table(table_path):
    """读取表格文件，支持CSV和Excel"""
    ext = Path(table_path).suffix.lower()

    if ext == '.csv':
        df = pd.read_csv(table_path, header=None)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(table_path, header=None)
    else:
        raise ValueError(f"不支持的文件格式: {ext}，请使用 .csv 或 .xlsx")

    return df


def read_template(template_path):
    """读取邮件模板"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def count_template_variables(template):
    """统计模板中的变量数量
    查找 {variable1}, {variable2}, ... 和 {v1}, {v2}, ... 格式的变量
    返回找到的最大变量编号
    """
    import re

    # 匹配 {variableN} 和 {vN} 格式
    pattern = r'\{(?:variable|v)(\d+)\}'
    matches = re.findall(pattern, template)

    if not matches:
        return 0

    # 返回最大编号
    return max(int(n) for n in matches)


def substitute_variables(template, variables):
    """替换模板中的变量

    变量格式: {variable1}, {variable2}, ... 或 {v1}, {v2}, ...
    """
    result = template

    for i, value in enumerate(variables, start=1):
        # 处理 {variable1} 和 {v1} 两种格式
        placeholder1 = f"{{variable{i}}}"
        placeholder2 = f"{{v{i}}}"
        value_str = str(value) if pd.notna(value) else ""
        result = result.replace(placeholder1, value_str)
        result = result.replace(placeholder2, value_str)

    return result


def create_message(email_addr, variables, template, subject, sender_email, is_html=False, attachments=None):
    """创建邮件消息"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email_addr
    msg['Subject'] = subject

    # 替换变量
    content = substitute_variables(template, variables)

    # 添加正文
    mime_type = 'html' if is_html else 'plain'
    body = MIMEText(content, mime_type, 'utf-8')
    msg.attach(body)

    # 添加附件
    if attachments:
        for attach_path in attachments:
            if not os.path.exists(attach_path):
                print(f"警告: 附件不存在，跳过: {attach_path}")
                continue

            with open(attach_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(attach_path)}"'
            )
            msg.attach(part)

    return msg, content


def preview_message(email_addr, content, index):
    """干运行模式：预览邮件内容"""
    print("=" * 60)
    print(f"[{index+1}] 收件人: {email_addr}")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print()


def send_emails(df, template, args):
    """发送邮件主逻辑"""
    total = len(df)
    success = 0
    failed = 0

    print(f"开始处理，共 {total} 个收件人...")
    print()

    if args.dry_run:
        print("=== 干运行模式 (预览不发送) ===")
        print()

    # 连接 SMTP
    if not args.dry_run:
        try:
            if args.smtp_port == 465:
                server = smtplib.SMTP_SSL(args.smtp_server, args.smtp_port)
            else:
                server = smtplib.SMTP(args.smtp_server, args.smtp_port)
                server.starttls()

            server.login(args.sender_email, args.sender_password)
            print("✓ SMTP 连接成功")
            print()
        except Exception as e:
            print(f"✗ SMTP 连接失败: {e}")
            return 0, total

    # 逐个处理
    for idx, row in df.iterrows():
        # 第一列是邮箱
        email_addr = str(row.iloc[0])
        if pd.isna(row.iloc[0]) or '@' not in email_addr:
            print(f"[{idx+1}] 跳过无效邮箱: {email_addr}")
            failed += 1
            continue

        # 剩余列是变量
        variables = row.iloc[1:].tolist()

        # 创建消息
        msg, content = create_message(
            email_addr, variables, template,
            args.subject, args.sender_email,
            args.html, args.attachments
        )

        # 干运行只预览
        if args.dry_run:
            preview_message(email_addr, content, idx)
            success += 1
            continue

        # 实际发送
        try:
            server.send_message(msg)
            print(f"[{idx+1}] ✓ 成功发送给 {email_addr}")
            success += 1
        except Exception as e:
            print(f"[{idx+1}] ✗ 发送失败 {email_addr}: {e}")
            failed += 1

    if not args.dry_run:
        server.quit()

    print()
    print("=" * 60)
    print(f"处理完成: 成功 {success}, 失败 {failed}, 总计 {total}")
    print("=" * 60)

    return success, failed


def main():
    # 加载配置
    config = load_config()

    parser = argparse.ArgumentParser(
        description='批量发送个性化邮件'
    )
    parser.add_argument('--table', required=True, help='表格文件路径 (CSV 或 .xlsx)')
    parser.add_argument('--template', required=True, help='邮件模板文件路径')
    parser.add_argument('--subject', required=True, help='邮件主题')
    parser.add_argument('--smtp-server', help='SMTP 服务器地址（覆盖配置文件）')
    parser.add_argument('--smtp-port', type=int, help='SMTP 端口（覆盖配置文件，默认: 587）')
    parser.add_argument('--sender-email', help='发件人邮箱（覆盖配置文件）')
    parser.add_argument('--sender-password', help='发件人密码/授权码（覆盖配置文件）')
    parser.add_argument('--attachments', nargs='*', help='通用附件文件路径，多个用空格分隔')
    parser.add_argument('--dry-run', action='store_true', help='干运行模式，只预览不发送')
    parser.add_argument('--html', action='store_true', help='HTML格式邮件')
    parser.add_argument('--show-config', action='store_true', help='显示当前配置并退出')

    args = parser.parse_args()

    # 从配置文件读取，命令行参数覆盖
    if 'smtp' in config:
        args.smtp_server = args.smtp_server or config['smtp'].get('server', None)
        args.smtp_port = args.smtp_port or config['smtp'].getint('port', 587)
        args.sender_email = args.sender_email or config['smtp'].get('sender_email', None)
        args.sender_password = args.sender_password or config['smtp'].get('sender_password', None)

    # 显示配置并退出
    if args.show_config:
        print("当前 SMTP 配置:")
        print(f"  服务器: {args.smtp_server}")
        print(f"  端口: {args.smtp_port}")
        print(f"  发件人邮箱: {args.sender_email}")
        print(f"  配置文件: {CONFIG_PATH}")
        return

    # 检查必填项
    missing = []
    if not args.smtp_server:
        missing.append('smtp-server')
    if not args.smtp_port:
        missing.append('smtp-port')
    if not args.sender_email:
        missing.append('sender-email')
    if not args.sender_password:
        missing.append('sender-password')

    if missing:
        print(f"错误: 以下配置缺失: {', '.join(missing)}")
        print(f"请在配置文件 {CONFIG_PATH} 中设置，或通过命令行参数提供")
        return

    # 读取表格
    try:
        df = read_table(args.table)
    except Exception as e:
        print(f"读取表格失败: {e}")
        return

    print(f"读取表格成功，共 {len(df)} 行")

    # 读取模板
    try:
        template = read_template(args.template)
    except Exception as e:
        print(f"读取模板失败: {e}")
        return

    print(f"读取模板成功，模板长度: {len(template)} 字符")
    print(f"使用配置文件: {CONFIG_PATH}")

    # 检查模板变量数量与表格列数是否匹配
    table_variable_count = df.shape[1] - 1  # 减去第一列邮箱
    template_variable_count = count_template_variables(template)

    if table_variable_count != template_variable_count:
        print()
        print(f"⚠️  警告: 模板变量数量与表格变量列数不匹配")
        print(f"    表格中变量列数: {table_variable_count} (除第一列邮箱外)")
        print(f"    模板中找到变量: {template_variable_count} 个")
        print(f"    请检查表格和模板是否匹配")
        print()

    # 发送邮件
    send_emails(df, template, args)


if __name__ == '__main__':
    main()
