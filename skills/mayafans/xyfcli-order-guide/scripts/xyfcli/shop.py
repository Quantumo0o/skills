"""Shop 技能模块 - 商品相关 API 调用命令"""

import typer
import asyncio
from typing import Optional
from .api_client import api_client

shop_app = typer.Typer(name="shop", help="商品相关 API 调用命令")


def sync_run(coroutine):
    """同步运行异步函数"""
    return asyncio.get_event_loop().run_until_complete(coroutine)


def format_output(result, json_output: bool = False):
    """格式化输出为JSON或原始格式"""
    import json
    if json_output:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        typer.echo(result)


def handle_errors(func):
    """错误处理装饰器，提供结构化的错误输出"""
    import functools
    import traceback
    import json as json_module
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 从参数中获取json_output
        json_output = kwargs.get('json_output', False)
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if json_output:
                error_data = {
                    "error": True,
                    "type": type(e).__name__,
                    "message": str(e),
                    "traceback": traceback.format_exc() if hasattr(e, '__traceback__') else None
                }
                typer.echo(json_module.dumps(error_data, ensure_ascii=False, indent=2))
                # 输出JSON错误后退出，退出码为1
                raise typer.Exit(code=1)
            else:
                # 让Typer处理默认错误输出
                raise
    
    return wrapper


@shop_app.command("getproducturibydesc")
@handle_errors
def get_product_uri_by_desc(
    desc: str = typer.Option(..., "-desc", "--description", help="产品描述"),
    limit: int = typer.Option(5, "-limit", "--limit", help="返回数量限制，-1 表示返回所有结果"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    通过语义查询，获取产品描述对应的 URI 地址，以及此地址内容描述信息，用来判断是否需要读取完整内容

    示例：shop getproducturibydesc -desc "含量 45% 13-5-27" -limit 5
    """
    async def _run():
        result = await api_client.post(
            "/api/proxy/openviking/api/v1/search/find",
            {"query": desc, "limit": limit,  "target_uri": "viking://resources","score_threshold": 0.2}
        )
        return result

    result = sync_run(_run())
    format_output(result, json_output)


@shop_app.command("getproductdetailbyuri")
@handle_errors
def get_product_detail_by_uri(
    uri: str = typer.Option(..., "-uri", "--uri", help="需要读取的 URI 地址"),
    offset: int = typer.Option(0, "-offset", "--offset", help="Starting line number (0-indexed)"),
    limit: int = typer.Option(-1, "-limit", "--limit", help="Number of lines to read, -1 means read to end"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    读取 URI 地址对应的完整内容，可以指定读取的行数区间，默认读取到文件结束

    示例：shop getproductdetailbyuri -uri "viking://resources/products/xxx.md" -offset 0 -limit -1
    """
    async def _run():
        result = await api_client.get(
            "/api/proxy/openviking/api/v1/content/read",
            {"uri": uri, "offset": offset, "limit": limit}
        )
        return result

    result = sync_run(_run())
    format_output(result, json_output)


@shop_app.command("getgoodsinfo")
def get_goods_info(
    product_code: str,
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    通过产品编号查询商品信息（排除 AI 幻觉）

    示例：shop getgoodsinfo "Y163U1305276020000"
    """
    async def _run():
        result = await api_client.post(
            "/api/proxy/shoptest/admin/AI/goods/info",
            {"productCode": product_code}
        )
        return result

    result = sync_run(_run())
    format_output(result, json_output)


@shop_app.command("getsalercode")
def get_saler_code(
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    获取下单销售人员信息，包含下单销售人员编号和姓名等信息，编号可以用来获取客户列表

    示例：shop getsalercode
    """
    async def _run():
        # 使用配置文件中的 token，不需要额外传参
        result = await api_client.get("/protected/user-info")
        return result

    result = sync_run(_run())
    format_output(result, json_output)


@shop_app.command("getdealercode")
def get_dealer_code(
    saler_code: str = typer.Argument(..., help="下单销售人员编号"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    通过下单销售人员编号获取客户列表，包含客户编号、姓名、手机号、邮箱等信息，客户编号可以用来查询可购买的产品列表

    示例：shop getdealercode "EZB2019063"
    """
    async def _run():
        result = await api_client.post(
            "/api/proxy/shoptest/admin/AI/dealer/listWithScope",
            {"salerCode": saler_code}
        )
        return result

    result = sync_run(_run())
    format_output(result, json_output)


@shop_app.command("getproductlist")
def get_product_list(
    dealer_code: str = typer.Option(..., "-dealercode", "--dealer-code", help="客户编号"),
    search_value: str = typer.Option(..., "-search", "--search-value", help="产品编码或搜索关键词"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    通过客户编号和产品编号/关键词获取该客户可购买的产品列表
    
    用法：
    1. 精确验证：传入产品编码，返回结果表示客户可购买此产品
    2. 模糊搜索：传入关键词（如"15-15-15"），返回匹配的可购产品列表

    示例：
    # 精确验证产品可用性
    shop getproductlist -dealercode "J620522007" -search "Y163U1305276020000"
    
    # 模糊搜索可购产品
    shop getproductlist -dealercode "J620522007" -search "15-15-15"
    """
    async def _run():
        result = await api_client.post(
            "/api/proxy/shoptest/admin/AI/goods/list",
            {"dealerCode": dealer_code, "searchValue": search_value}
        )
        return result

    result = sync_run(_run())
    format_output(result, json_output)


@shop_app.command("getdeliverybase")
def get_delivery_base(
    product_code: str = typer.Option(..., "-productcode", "--product-code", help="产品编号"),
    dealer_code: str = typer.Option(..., "-dealercode", "--dealer-code", help="客户编号"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    通过客户编号和产品编号获取发货基地列表

    示例：shop getdeliverybase -productcode "Y68000500000023100" -dealercode "J620522007"
    """
    async def _run():
        result = await api_client.post(
            "/api/proxy/shoptest/admin/AI/goods/getProductInit",
            {"productCode": product_code, "dealerCode": dealer_code}
        )
        return result

    result = sync_run(_run())
    format_output(result, json_output)


@shop_app.command("getdealeraddresses")
def get_dealer_addresses(
    dealer_code: str = typer.Argument(..., help="客户编号"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    通过客户编号获取客户设置好的收货地址

    示例：shop getdealeraddresses "J620522007"
    """
    async def _run():
        result = await api_client.post(
            "/api/proxy/shoptest/admin/AI/address/list",
            {"dealerCode": dealer_code}
        )
        return result

    result = sync_run(_run())
    format_output(result, json_output)

