"""
股票订单管理 Skill 主入口
"""

import os
import sys
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stock_order import StockOrderManager
from stock_info import StockInfoFetcher
from log_manager import LogManager
import argparse


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='股票订单管理工具')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 订单管理命令
    order_parser = subparsers.add_parser('order', help='订单管理')
    order_subparsers = order_parser.add_subparsers(dest='order_command', help='订单管理命令')

    # 股票信息获取命令
    stock_info_parser = subparsers.add_parser('stock', help='股票信息获取')
    stock_info_subparsers = stock_info_parser.add_subparsers(dest='stock_info_command', help='股票信息获取命令')

    # 日志管理命令
    log_parser = subparsers.add_parser('log', help='日志管理')
    log_subparsers = log_parser.add_subparsers(dest='log_command', help='日志管理命令')

    # 获取股票信息
    get_stock_info_parser = stock_info_subparsers.add_parser('get', help='获取股票信息')
    get_stock_info_parser.add_argument('--code', type=str, required=True, help='股票代码')

    # 日志管理命令
    log_list_parser = log_subparsers.add_parser('list', help='列出所有日志文件')
    log_list_parser.add_argument('--detail', action='store_true', help='显示详细信息')

    log_delete_parser = log_subparsers.add_parser('delete', help='删除日志文件')
    log_delete_parser.add_argument('--file', type=str, help='删除指定的日志文件')
    log_delete_parser.add_argument('--old', type=int, help='删除指定天数之前的旧日志')
    log_delete_parser.add_argument('--all', action='store_true', help='删除所有日志文件')

    log_size_parser = log_subparsers.add_parser('size', help='查看日志目录大小')

    # 添加订单
    add_order_parser = order_subparsers.add_parser('add', help='添加股票订单')
    add_order_parser.add_argument('--code', type=str, required=True, help='股票代码')
    add_order_parser.add_argument('--name', type=str, required=True, help='股票名称')
    add_order_parser.add_argument('--buy-time', type=str, required=True, help='买入时间（YYYY-MM-DD HH:MM:SS）')
    add_order_parser.add_argument('--buy-price', type=float, required=True, help='买入价格')
    add_order_parser.add_argument('--type', type=str, default='A股', help='股票类型（A股、美股、港股等）')
    add_order_parser.add_argument('--platform', type=str, help='股票交易平台（富途、平安等，可选）')
    add_order_parser.add_argument('--quantity', type=int, help='购买数量（股数，可选）')

    # 列出所有订单
    list_orders_parser = order_subparsers.add_parser('list', help='列出所有订单')
    list_orders_parser.add_argument('--status', type=str, help='按状态筛选')
    list_orders_parser.add_argument('--type', type=str, help='按股票类型筛选')
    list_orders_parser.add_argument('--platform', type=str, help='按交易平台筛选')

    # 获取订单详情
    get_order_parser = order_subparsers.add_parser('get', help='获取订单详情')
    get_order_parser.add_argument('--id', type=str, required=True, help='订单ID')

    # 更新订单状态
    update_order_parser = order_subparsers.add_parser('update', help='更新订单状态')
    update_order_parser.add_argument('--id', type=str, required=True, help='订单ID')
    update_order_parser.add_argument('--status', type=str, help='新状态（持有、已卖出、已止损等）')

    # 更新订单信息
    edit_order_parser = order_subparsers.add_parser('edit', help='更新订单信息')
    edit_order_parser.add_argument('--id', type=str, required=True, help='订单ID')
    edit_order_parser.add_argument('--name', type=str, help='股票名称')
    edit_order_parser.add_argument('--buy-time', type=str, help='买入时间（YYYY-MM-DD HH:MM:SS）')
    edit_order_parser.add_argument('--buy-price', type=float, help='买入价格')
    edit_order_parser.add_argument('--type', type=str, help='股票类型（A股、美股、港股等）')
    edit_order_parser.add_argument('--platform', type=str, help='股票交易平台（富途、平安等）')
    edit_order_parser.add_argument('--quantity', type=int, help='购买数量（股数）')
    edit_order_parser.add_argument('--status', type=str, help='订单状态（持有、已卖出、已止损等）')

    # 删除订单
    delete_order_parser = order_subparsers.add_parser('delete', help='删除订单')
    delete_order_parser.add_argument('--id', type=str, required=True, help='订单ID')

    # 订单备份管理
    backup_parser = order_subparsers.add_parser('backup', help='订单备份管理')
    backup_subparsers = backup_parser.add_subparsers(dest='backup_command', help='备份管理命令')

    # 查看备份
    list_backups_parser = backup_subparsers.add_parser('list', help='查看所有备份')

    # 清理旧备份
    cleanup_backups_parser = backup_subparsers.add_parser('cleanup', help='清理多余备份，只保留最近的10个')
    cleanup_backups_parser.add_argument('--max', type=int, default=10, help='保留的最大备份数量（默认10）')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 自动清理7天前的日志
    try:
        log_manager = LogManager()
        log_manager.delete_old_logs(days=7)
    except Exception as e:
        print(f"清理日志失败: {e}")

    try:
        if args.command == 'order':
            order_manager = StockOrderManager()

            if args.order_command == 'add':
                order_id = order_manager.add_order(
                    stock_code=args.code,
                    stock_name=args.name,
                    buy_time=args.buy_time,
                    buy_price=args.buy_price,
                    stock_type=args.type,
                    platform=args.platform,
                    quantity=args.quantity
                )
                print(f"\n成功添加订单，订单ID: {order_id}")
                print(f"股票: {args.name}({args.code})")
                print(f"买入时间: {args.buy_time}")
                print(f"买入价格: {args.buy_price}")
                print(f"股票类型: {args.type}")
                if args.platform:
                    print(f"交易平台: {args.platform}")
                if args.quantity:
                    print(f"购买数量: {args.quantity} 股")

            elif args.order_command == 'list':
                orders = order_manager.get_all_orders()

                # 按状态筛选
                if args.status:
                    orders = [order for order in orders if order['status'] == args.status]

                # 按股票类型筛选
                if args.type:
                    orders = [order for order in orders if order['stock_type'] == args.type]

                # 按交易平台筛选
                if args.platform:
                    orders = [order for order in orders if order.get('platform') == args.platform]

                print(f"\n共找到 {len(orders)} 个订单:")
                print("-" * 160)
                print(f"{'订单ID':<25} {'股票代码':<10} {'股票名称':<20} {'买入时间':<20} {'买入价格':<10} {'数量':<10} {'股票类型':<10} {'交易平台':<10} {'状态':<10}")
                print("-" * 160)
                for order in orders:
                    platform = order.get('platform', '-') or '-'
                    quantity = order.get('quantity', '-') or '-'
                    print(f"{order['order_id']:<25} {order['stock_code']:<10} {order['stock_name']:<20} "
                          f"{order['buy_time']:<20} {order['buy_price']:<10.2f} {quantity:<10} {order['stock_type']:<10} {platform:<10} {order['status']:<10}")
                print("-" * 160)

            elif args.order_command == 'get':
                order = order_manager.get_order_by_id(args.id)
                if order:
                    print(f"\n订单详情:")
                    print("-" * 50)
                    print(f"订单ID: {order['order_id']}")
                    print(f"股票代码: {order['stock_code']}")
                    print(f"股票名称: {order['stock_name']}")
                    print(f"买入时间: {order['buy_time']}")
                    print(f"买入价格: {order['buy_price']}")
                    if order.get('quantity'):
                        print(f"购买数量: {order['quantity']} 股")
                    print(f"股票类型: {order['stock_type']}")
                    if order.get('platform'):
                        print(f"交易平台: {order['platform']}")
                    print(f"状态: {order['status']}")
                    print(f"创建时间: {order['create_time']}")
                    if 'update_time' in order:
                        print(f"更新时间: {order['update_time']}")
                    print("-" * 50)
                else:
                    print(f"未找到订单: {args.id}")

            elif args.order_command == 'update':
                success = order_manager.update_order_status(args.id, args.status)
                if success:
                    print(f"成功更新订单状态: {args.id} -> {args.status}")
                else:
                    print(f"更新订单状态失败: {args.id}")

            elif args.order_command == 'edit':
                # 构建更新参数
                update_params = {}
                if args.name:
                    update_params['stock_name'] = args.name
                if args.buy_time:
                    update_params['buy_time'] = args.buy_time
                if args.buy_price:
                    update_params['buy_price'] = args.buy_price
                if args.type:
                    update_params['stock_type'] = args.type
                if args.platform:
                    update_params['platform'] = args.platform
                if args.status:
                    update_params['status'] = args.status
                
                if update_params:
                    success = order_manager.update_order(args.id, **update_params)
                    if success:
                        print(f"成功更新订单: {args.id}")
                        for key, value in update_params.items():
                            print(f"  {key}: {value}")
                    else:
                        print(f"更新订单失败: {args.id}")
                else:
                    print("未提供任何更新参数")

            elif args.order_command == 'delete':
                success = order_manager.delete_order(args.id)
                if success:
                    print(f"成功删除订单: {args.id}")
                else:
                    print(f"删除订单失败: {args.id}")

            elif args.order_command == 'backup':
                if args.backup_command == 'list':
                    backups = []
                    for filename in os.listdir(order_manager.order_dir):
                        if filename.startswith('orders.json_'):
                            filepath = os.path.join(order_manager.order_dir, filename)
                            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                            backups.append({
                                'filename': filename,
                                'filepath': filepath,
                                'mtime': file_mtime
                            })
                    
                    if backups:
                        backups.sort(key=lambda x: x['mtime'], reverse=True)
                        print(f"\n所有订单备份:")
                        print("-" * 80)
                        print(f"{'备份文件名':<30} {'备份时间':<20} {'文件大小':<15}")
                        print("-" * 80)
                        for backup in backups:
                            file_size = os.path.getsize(backup['filepath'])
                            size_str = f"{file_size / 1024:.2f} KB"
                            print(f"{backup['filename']:<30} {backup['mtime'].strftime('%Y-%m-%d %H:%M:%S'):<20} {size_str:<15}")
                        print("-" * 80)
                    else:
                        print("\n没有找到订单备份")

                elif args.backup_command == 'cleanup':
                    deleted_count = order_manager._cleanup_excess_backups(max_backups=args.max)
                    print(f"清理了 {deleted_count} 个多余备份（保留最近{args.max}个）")

                else:
                    backup_parser.print_help()

            else:
                order_parser.print_help()

        elif args.command == 'stock':
            stock_info_fetcher = StockInfoFetcher()

            if args.stock_info_command == 'get':
                stock_info = stock_info_fetcher.fetch_and_save_stock_info(args.code)
                if stock_info:
                    print(f"\n股票信息:")
                    print("-" * 50)
                    print(f"股票代码: {stock_info['code']}")
                    print(f"股票名称: {stock_info['name']}")
                    print(f"当前价格: {stock_info['current_price']}")
                    print(f"开盘价: {stock_info['open_price']}")
                    print(f"最高价: {stock_info['high_price']}")
                    print(f"最低价: {stock_info['low_price']}")
                    print(f"昨收价: {stock_info['previous_close']}")
                    print(f"涨跌额: {stock_info['price_change']}")
                    print(f"涨跌幅: {stock_info['price_change_percent']}%")
                    print(f"成交量: {stock_info['volume']}")
                    print(f"成交额: {stock_info['turnover']}")
                    print(f"市场: {stock_info['market']}")
                    print(f"数据来源: {stock_info.get('data_source', '未知')}")
                    print(f"数据日期: {stock_info['data_date']}")
                    print(f"获取时间: {stock_info['fetch_time']}")
                    print("-" * 50)
                else:
                    print(f"未找到股票 {args.code} 的信息")

            else:
                stock_info_parser.print_help()

        elif args.command == 'log':
            log_manager = LogManager()

            if args.log_command == 'list':
                log_files = log_manager.list_log_files()
                
                if not log_files:
                    print("\n没有找到日志文件")
                else:
                    print(f"\n共找到 {len(log_files)} 个日志文件:")
                    print("-" * 100)
                    if args.detail:
                        print(f"{'文件名':<40} {'大小':<15} {'修改时间':<25}")
                        print("-" * 100)
                        for log_file in log_files:
                            size_str = log_manager.format_size(log_file['size'])
                            mtime_str = log_file['mtime'].strftime('%Y-%m-%d %H:%M:%S')
                            print(f"{log_file['filename']:<40} {size_str:<15} {mtime_str:<25}")
                    else:
                        print(f"{'文件名':<40} {'大小':<15}")
                        print("-" * 100)
                        for log_file in log_files:
                            size_str = log_manager.format_size(log_file['size'])
                            print(f"{log_file['filename']:<40} {size_str:<15}")
                    print("-" * 100)

            elif args.log_command == 'delete':
                if args.all:
                    # 删除所有日志
                    confirm = input("确定要删除所有日志文件吗？(yes/no): ")
                    if confirm.lower() == 'yes':
                        deleted_count = log_manager.clear_all_logs()
                        print(f"\n成功删除 {deleted_count} 个日志文件")
                    else:
                        print("\n已取消删除操作")
                elif args.old:
                    # 删除旧日志
                    deleted_count = log_manager.delete_old_logs(args.old)
                    print(f"\n成功删除 {deleted_count} 个旧日志文件（{args.old}天前）")
                elif args.file:
                    # 删除指定文件
                    success = log_manager.delete_log_file(args.file)
                    if success:
                        print(f"\n成功删除日志文件: {args.file}")
                    else:
                        print(f"\n删除日志文件失败: {args.file}")
                else:
                    print("\n请指定要删除的日志文件或使用 --old 或 --all 参数")
                    log_delete_parser.print_help()

            elif args.log_command == 'size':
                total_size = log_manager.get_log_size()
                size_str = log_manager.format_size(total_size)
                print(f"\n日志目录总大小: {size_str}")

            else:
                log_parser.print_help()

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()