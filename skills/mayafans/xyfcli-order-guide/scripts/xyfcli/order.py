"""Order 下单技能模块 - 完整的下单流程"""

import typer
import asyncio
import json
import re
from typing import Optional, List
from .api_client import api_client

order_app = typer.Typer(name="order", help="下单订货流程技能")


def sync_run(coroutine):
    """同步运行异步函数"""
    return asyncio.get_event_loop().run_until_complete(coroutine)


def handle_errors(func):
    """错误处理装饰器，提供结构化的错误输出"""
    import functools
    import traceback
    import json as json_module
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 从参数中获取json_output，如果不存在则默认为False
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


@order_app.command("place")
@handle_errors
def place_order(
    dealer_code: str = typer.Option(..., "-dealer", "--dealer-code", help="客户编号"),
    dealer_name: str = typer.Option(..., "-name", "--dealer-name", help="客户名称"),
    sales_code: str = typer.Option(..., "-sales", "--sales-code", help="业务员编号"),
    product_codes: str = typer.Option(..., "-products", "--product-codes", help="商品编号列表，逗号分隔"),
    departure_base: str = typer.Option(..., "-base", "--departure-base", help="发货基地"),
    destination: str = typer.Option(..., "-dest", "--destination", help="收货地址"),
    cover_image_urls: Optional[str] = typer.Option(None, "-images", "--cover-images", help="商品封面图 URL 列表，逗号分隔"),
    quantities: Optional[str] = typer.Option(None, "-q", "--quantities", help="商品数量列表，逗号分隔，与商品编号一一对应，默认为1"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    完成下单流程，生成订单页面 URL

    示例：
    order place -dealer "J620522007" -name "牛建建" -sales "EZB2019063" \\
                -products "Y163U1305276020000" -base "新洋丰中磷" \\
                -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
    
    带数量的示例：
    order place -dealer "J620522007" -name "牛建建" -sales "EZB2019063" \\
                -products "Y163U1305276020000,ABC123456789" \\
                -q "5,3" -base "新洋丰中磷" \\
                -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
    """
    # 解析商品编号列表
    product_code_list = [p.strip() for p in product_codes.split(",") if p.strip()]

    # 解析封面图 URL 列表
    image_url_list = []
    if cover_image_urls:
        image_url_list = [url.strip() for url in cover_image_urls.split(",") if url.strip()]

    # 解析数量列表
    quantity_list = []
    if quantities:
        try:
            quantity_list = [int(q.strip()) for q in quantities.split(",") if q.strip()]
            if len(quantity_list) != len(product_code_list):
                raise typer.BadParameter(
                    f"数量列表长度({len(quantity_list)})与商品编号列表长度({len(product_code_list)})不匹配"
                )
            # 验证数量是否为正整数
            for q in quantity_list:
                if q <= 0:
                    raise typer.BadParameter(f"商品数量必须为正整数，当前值: {q}")
        except ValueError:
            raise typer.BadParameter("数量列表必须为逗号分隔的整数")
    else:
        # 默认所有商品数量为1
        quantity_list = [1] * len(product_code_list)

    # 构建商品列表
    product_list = []
    for i, code in enumerate(product_code_list):
        product_info = {
            "product_code": code,
            "cover_image_url": image_url_list[i] if i < len(image_url_list) else "",
            "quantity": quantity_list[i]
        }
        product_list.append(product_info)

    # 构建请求数据
    order_data = {
        "customer_code": dealer_code,
        "customer_name": dealer_name,
        "sales_code": sales_code,
        "product_list": product_list,
        "departure_base": departure_base,
        "destination": destination
    }

    async def _run():
        result = await api_client.post("/getorderaddress", order_data)
        return result

    result = sync_run(_run())

    # 输出结果
    if json_output:
        output_data = {
            "order_data": order_data,
            "api_response": result
        }
        typer.echo(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        typer.echo("=" * 50)
        typer.echo("订单信息页面 URL 生成成功")
        typer.echo("=" * 50)

        if isinstance(result, dict):
            if "url" in result:
                typer.echo(f"\n订单页面 URL: {result['url']}")

            if "message" in result:
                typer.echo(f"消息：{result['message']}")

            if "order_info" in result:
                typer.echo("\n订单详情:")
                order_info = result["order_info"]
                typer.echo(f"  客户编号：{order_info.get('customer_code', '')}")
                typer.echo(f"  客户名称：{order_info.get('customer_name', '')}")
                typer.echo(f"  业务员编号：{order_info.get('sales_code', '')}")
                typer.echo(f"  发货基地：{order_info.get('departure_base', '')}")
                typer.echo(f"  收货地址：{order_info.get('destination', '')}")
                typer.echo("  商品列表:")
                for product in order_info.get("product_list", []):
                    product_code = product.get('product_code', '')
                    quantity = product.get('quantity', 1)
                    if quantity != 1:
                        typer.echo(f"    - {product_code} ×{quantity}")
                    else:
                        typer.echo(f"    - {product_code}")
        else:
            typer.echo(result)


@order_app.command("full-flow")
@handle_errors
def full_order_flow(
    product_description: Optional[str] = typer.Option(None, "-desc", "--description", help="产品描述（用于图片识别或文字搜索）"),
    product_codes: Optional[str] = typer.Option(None, "-pc", "--product-codes", help="产品编码列表，逗号分隔，如果提供则跳过搜索步骤"),
    quantities: Optional[str] = typer.Option(None, "-q", "--quantities", help="商品数量列表，逗号分隔，与产品编码一一对应，默认为1"),
    product_index: int = typer.Option(0, "-pi", "--product-index", help="产品索引（0-based），默认为0"),
    dealer_index: int = typer.Option(0, "-di", "--dealer-index", help="客户索引（0-based），默认为0"),
    base_index: int = typer.Option(0, "-bi", "--base-index", help="发货基地索引（0-based），默认为0"),
    address_index: int = typer.Option(0, "-ai", "--address-index", help="收货地址索引（0-based），默认为0"),
    address: Optional[str] = typer.Option(None, "-addr", "--address", help="直接指定收货地址，如果提供则忽略地址索引"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    完整的下单流程 - 从产品搜索到下单（非交互式，Agent友好）
    
    支持单个产品（通过描述搜索）或多个产品（直接提供产品编码）
    
    流程：
    1. 通过产品描述搜索产品 URI（如果未提供产品编码）
    2. 获取产品详细信息并提取产品编号（如果未提供产品编码）
    3. 查询商品信息（排除 AI 幻觉）
    4. 获取业务员编号
    5. 获取客户列表并选择
    6. 获取可购买产品列表
    7. 获取发货基地列表
    8. 获取收货地址
    9. 生成订单页面
    
    示例：
    # 单个产品，通过描述搜索
    order full-flow -desc "含量 45% 13-5-27" -pi 0 -di 0 -bi 0 -ai 0
    order full-flow -desc "含量 45% 13-5-27" --json
    
    # 多个产品，直接提供产品编码和数量
    order full-flow -pc "Y163U1305276020000,ABC123456789" -q "5,3" -di 0 -bi 0 -ai 0
    """
    # 初始化结果字典，用于JSON输出
    result_data = {
        "steps": {},
        "final_order": {}
    }

    # 验证参数：必须提供 product_description 或 product_codes
    if not product_description and not product_codes:
        if json_output:
            typer.echo(json.dumps({"error": "必须提供产品描述(--desc)或产品编码列表(--product-codes)"}))
        else:
            typer.echo("错误：必须提供产品描述(--desc)或产品编码列表(--product-codes)")
        return

    # 解析产品编码和数量
    product_code_list = []
    cover_images = []
    quantities_list = []
    validated_products = []  # 存储已验证的产品信息

    if product_codes:
        # 使用直接提供的产品编码
        product_code_list = [code.strip() for code in product_codes.split(",") if code.strip()]
        if not product_code_list:
            if json_output:
                typer.echo(json.dumps({"error": "产品编码列表不能为空"}))
            else:
                typer.echo("错误：产品编码列表不能为空")
            return

        # 解析数量列表
        if quantities:
            try:
                quantities_list = [int(q.strip()) for q in quantities.split(",") if q.strip()]
                if len(quantities_list) != len(product_code_list):
                    raise typer.BadParameter(
                        f"数量列表长度({len(quantities_list)})与产品编码列表长度({len(product_code_list)})不匹配"
                    )
                # 验证数量是否为正整数
                for q in quantities_list:
                    if q <= 0:
                        raise typer.BadParameter(f"商品数量必须为正整数，当前值: {q}")
            except ValueError:
                raise typer.BadParameter("数量列表必须为逗号分隔的整数")
        else:
            # 默认所有商品数量为1
            quantities_list = [1] * len(product_code_list)

        if not json_output:
            typer.echo(f"使用直接提供的 {len(product_code_list)} 个产品编码")
            for i, (code, qty) in enumerate(zip(product_code_list, quantities_list)):
                typer.echo(f"  产品 {i+1}: {code} ×{qty}")

        # 标记为直接提供编码模式
        direct_codes_mode = True
    else:
        # 使用产品描述搜索模式（单个产品）
        direct_codes_mode = False
        quantities_list = [1]  # 单个产品默认数量为1
    
    # Step 1: 搜索产品 URI（仅当未提供产品编码时）
    if not json_output:
        typer.echo("开始完整下单流程...")
        typer.echo("=" * 50)
        typer.echo("\n[Step 1/8] 搜索产品 URI...")
    
    search_result = sync_run(
        api_client.post(
            "/api/proxy/openviking/api/v1/search/find",
            {"query": product_description, "limit": 5}
        )
    )

    resources = search_result.get("result", {}).get("resources", [])
    if not resources:
        if json_output:
            typer.echo(json.dumps({"error": "未找到相关产品", "step": 1}))
        else:
            typer.echo("未找到相关产品")
        return

    # 选择产品
    if product_index >= len(resources):
        if json_output:
            typer.echo(json.dumps({"error": f"产品索引 {product_index} 超出范围，共 {len(resources)} 个产品", "step": 1}))
        else:
            typer.echo(f"错误：产品索引 {product_index} 超出范围，共 {len(resources)} 个产品")
        return
    
    # 处理 .abstract.md 文件问题：如果选择的资源是 .abstract.md，尝试下一个资源
    selected_resource = resources[product_index]
    original_index = product_index
    adjusted_index = product_index
    
    # 如果 URI 以 .abstract.md 结尾，尝试下一个资源（最多尝试 3 次）
    max_attempts = min(3, len(resources))
    for attempt in range(max_attempts):
        temp_resource = resources[adjusted_index]
        temp_uri = temp_resource.get("uri", "")
        if temp_uri.endswith(".abstract.md"):
            # 尝试下一个资源
            if adjusted_index + 1 < len(resources):
                adjusted_index += 1
                if not json_output:
                    typer.echo(f"警告：索引 {original_index} 指向 .abstract.md 文件，自动调整为索引 {adjusted_index}")
            else:
                # 没有更多资源可用
                break
        else:
            # 找到非 .abstract.md 资源
            break
    
    selected_resource = resources[adjusted_index]
    product_uri = selected_resource.get("uri", "")
    
    if not json_output:
        if original_index != adjusted_index:
            typer.echo(f"找到 {len(resources)} 个产品，原始索引 {original_index} 调整为索引 {adjusted_index}: {product_uri}")
        else:
            typer.echo(f"找到 {len(resources)} 个产品，选择索引 {product_index}: {product_uri}")
    
    result_data["steps"]["product_search"] = {
        "found_count": len(resources),
        "selected_index": adjusted_index,
        "selected_uri": product_uri,
        "original_index": original_index,
        "adjusted": original_index != adjusted_index
    }

    # Step 2: 获取产品详细信息并提取产品编号
    if not json_output:
        typer.echo("\n[Step 2/8] 获取产品详细信息并提取产品编号...")
    
    detail_result = sync_run(
        api_client.get(
            "/api/proxy/openviking/api/v1/content/read",
            {"uri": product_uri, "offset": 0, "limit": -1}
        )
    )

    content = detail_result.get("result", "")
    # 解析产品编码（从 markdown 表格内容中提取）
    product_code = None
    content_lines = content.split("\n")
    for i, line in enumerate(content_lines):
        # 匹配表格中的产品编码行
        if "产品编码" in line and "|" in line:
            parts = line.split("|")
            # 表格格式：| 字段 | 值 |，取第三部分（索引 2）的值
            if len(parts) >= 3:
                product_code = parts[2].strip()
                break

    # 如果表格解析失败，尝试其他格式
    if not product_code:
        for line in content_lines:
            # 匹配 "产品编码：XXX" 或 "产品编码：XXX" 格式
            if "产品编码" in line:
                import re
                match = re.search(r'产品编码 [:：]\s*([A-Za-z0-9]+)', line)
                if match:
                    product_code = match.group(1)
                    break

    if not product_code:
        if json_output:
            typer.echo(json.dumps({"error": "无法从产品详情中提取产品编码", "step": 2, "content_preview": content[:500]}))
        else:
            typer.echo("无法从产品详情中提取产品编码")
            typer.echo("产品详情内容预览:")
            typer.echo(content[:500] + "..." if len(content) > 500 else content)
        return

    if not json_output:
        typer.echo(f"提取到产品编号：{product_code}")
    
    result_data["steps"]["product_detail"] = {
        "product_code": product_code,
        "uri": product_uri
    }

    # Step 3: 验证产品编号是否能查到产品信息
    if not json_output:
        typer.echo("\n[Step 3/8] 验证产品编号...")
    
    goods_result = sync_run(
        api_client.post(
            "/api/proxy/shoptest/admin/AI/goods/info",
            {"productCode": product_code}
        )
    )

    if goods_result.get("code") != 200:
        if json_output:
            typer.echo(json.dumps({"error": f"产品编号验证失败：{goods_result.get('msg', '')}", "step": 3}))
        else:
            typer.echo(f"产品编号验证失败：{goods_result.get('msg', '')}")
            typer.echo("请检查产品编号是否正确")
        return

    goods_data = goods_result.get("data", {})
    cover_image = goods_data.get("coverImage", "")
    
    if not json_output:
        typer.echo(f"产品编号验证成功")
        typer.echo(f"商品封面图：{cover_image}")
    
    result_data["steps"]["product_validation"] = {
        "success": True,
        "cover_image": cover_image
    }

    # 将单个产品添加到验证列表
    validated_products.append({
        "product_code": product_code,
        "cover_image": cover_image,
        "quantity": quantities_list[0] if quantities_list else 1
    })

    # Step 4: 获取业务员编号
    if not json_output:
        typer.echo("\n[Step 4/8] 获取业务员编号...")
    
    saler_result = sync_run(
        api_client.get("/protected/user-info")
    )

    saler_info = saler_result.get("token_info", {})
    description = saler_info.get("description", "")
    
    # 从描述字符串中提取业务员编码
    # 格式示例："业务员编号：EZB2019063 姓名：汤晓杰"
    if "：" in description:  # 中文冒号
        # 分割字符串获取编码部分
        parts = description.split("：", 1)  # 最多分割一次
        if len(parts) > 1:
            # 提取"姓名"之前的部分
            saler_code_part = parts[1]
            if "姓名" in saler_code_part:
                saler_code = saler_code_part.split("姓名")[0].strip()
            else:
                saler_code = saler_code_part.strip()
        else:
            saler_code = description.strip()
    else:
        saler_code = description.strip()
    
    if not json_output:
        typer.echo(f"业务员编号：{saler_code}")
    
    result_data["steps"]["saler_info"] = {
        "saler_code": saler_code
    }

    # Step 5: 获取客户列表
    if not json_output:
        typer.echo("\n[Step 5/8] 获取客户列表...")
    
    dealer_result = sync_run(
        api_client.post(
            "/api/proxy/shoptest/admin/AI/dealer/listWithScope",
            {"salerCode": saler_code}
        )
    )

    dealer_list = dealer_result.get("data", [])
    if not dealer_list:
        if json_output:
            typer.echo(json.dumps({"error": "未找到客户", "step": 5}))
        else:
            typer.echo("未找到客户")
        return

    # 选择客户
    if dealer_index >= len(dealer_list):
        if json_output:
            typer.echo(json.dumps({"error": f"客户索引 {dealer_index} 超出范围，共 {len(dealer_list)} 个客户", "step": 5}))
        else:
            typer.echo(f"错误：客户索引 {dealer_index} 超出范围，共 {len(dealer_list)} 个客户")
        return
    
    selected_dealer = dealer_list[dealer_index]
    dealer_code = selected_dealer.get("dealerCode", "")
    dealer_name = selected_dealer.get("dealerName", "")
    
    if not json_output:
        typer.echo(f"找到 {len(dealer_list)} 个客户，选择索引 {dealer_index}: {dealer_code} - {dealer_name}")
    
    result_data["steps"]["dealer_selection"] = {
        "found_count": len(dealer_list),
        "selected_index": dealer_index,
        "dealer_code": dealer_code,
        "dealer_name": dealer_name
    }

    # Step 6: 获取可购买产品列表
    if not json_output:
        typer.echo("\n[Step 6/8] 获取可购买产品列表...")
    
    # 使用产品描述的分词作为搜索值
    search_value = product_description.replace("%", " ").replace("(", " ").replace(")", " ")
    search_value = " ".join(search_value.split())  # 规范化空格

    product_list_result = sync_run(
        api_client.post(
            "/api/proxy/shoptest/admin/AI/goods/list",
            {"dealerCode": dealer_code, "searchValue": search_value}
        )
    )

    product_list_data = product_list_result.get("data", [])
    if not product_list_data:
        if json_output:
            typer.echo(json.dumps({"error": "该客户无此产品购买权限", "step": 6}))
        else:
            typer.echo("该客户无此产品购买权限")
        return

    available_codes = [prod.get("productCode", "") for prod in product_list_data]
    
    if not json_output:
        typer.echo(f"客户可购买 {len(product_list_data)} 个产品")
    
    # 确认产品是否在可购买列表中
    if product_code not in available_codes:
        if not json_output:
            typer.echo(f"警告：产品 {product_code} 不在客户可购买列表中，继续处理...")
        # 继续处理，不中断
        result_data["steps"]["product_availability"] = {
            "available": False,
            "available_count": len(product_list_data),
            "warning": f"产品 {product_code} 不在客户可购买列表中"
        }
    else:
        if not json_output:
            typer.echo(f"产品 {product_code} 在可购买列表中")
        result_data["steps"]["product_availability"] = {
            "available": True,
            "available_count": len(product_list_data)
        }

    # Step 7: 获取发货基地列表
    if not json_output:
        typer.echo("\n[Step 7/8] 获取发货基地列表...")
    
    base_result = sync_run(
        api_client.post(
            "/api/proxy/shoptest/admin/AI/goods/getProductInit",
            {"productCode": product_code, "dealerCode": dealer_code}
        )
    )

    base_data = base_result.get("data", {})
    delivery_base_list = base_data.get("deliveryBaseList", [])

    if not delivery_base_list:
        if json_output:
            typer.echo(json.dumps({"error": "未找到发货基地", "step": 7}))
        else:
            typer.echo("未找到发货基地")
        return

    # 选择发货基地
    if base_index >= len(delivery_base_list):
        if json_output:
            typer.echo(json.dumps({"error": f"发货基地索引 {base_index} 超出范围，共 {len(delivery_base_list)} 个基地", "step": 7}))
        else:
            typer.echo(f"错误：发货基地索引 {base_index} 超出范围，共 {len(delivery_base_list)} 个基地")
        return
    
    selected_base = delivery_base_list[base_index]
    departure_base = selected_base.get("dictLabel", "")
    
    if not json_output:
        typer.echo(f"可发货基地 {len(delivery_base_list)} 个，选择索引 {base_index}: {departure_base}")
    
    result_data["steps"]["delivery_base"] = {
        "found_count": len(delivery_base_list),
        "selected_index": base_index,
        "departure_base": departure_base
    }

    # Step 8: 获取收货地址
    if not json_output:
        typer.echo("\n[Step 8/8] 获取收货地址...")
    
    destination = ""
    if address:
        # 使用直接提供的地址
        destination = address
        if not json_output:
            typer.echo(f"使用直接提供的收货地址: {destination}")
        result_data["steps"]["address"] = {
            "source": "direct",
            "address": destination
        }
    else:
        # 从地址列表中选择
        address_result = sync_run(
            api_client.post(
                "/api/proxy/shoptest/admin/AI/address/list",
                {"dealerCode": dealer_code}
            )
        )

        address_list = address_result.get("data", [])
        if address_list:
            if address_index >= len(address_list):
                if json_output:
                    typer.echo(json.dumps({"error": f"收货地址索引 {address_index} 超出范围，共 {len(address_list)} 个地址", "step": 8}))
                else:
                    typer.echo(f"错误：收货地址索引 {address_index} 超出范围，共 {len(address_list)} 个地址")
                return
            
            selected_address = address_list[address_index]
            destination = selected_address.get("addressTxt", "") + selected_address.get("addressDetail", "")
            
            if not json_output:
                typer.echo(f"客户有 {len(address_list)} 个收货地址，选择索引 {address_index}: {destination}")
            
            result_data["steps"]["address"] = {
                "source": "list",
                "found_count": len(address_list),
                "selected_index": address_index,
                "address": destination
            }
        else:
            if json_output:
                typer.echo(json.dumps({"error": "未找到收货地址且未提供直接地址", "step": 8}))
            else:
                typer.echo("错误：未找到收货地址且未提供直接地址")
            return

    # 生成订单
    if not json_output:
        typer.echo("\n" + "=" * 50)
        typer.echo("生成订单...")
    
    # 构建产品列表
    product_list_data = []
    
    if direct_codes_mode and validated_products:
        # 使用已验证的产品列表
        for item in validated_products:
            product_list_data.append({
                "product_code": item["product_code"],
                "cover_image_url": item["cover_image"],
                "quantity": item["quantity"]
            })
    else:
        # 单个产品模式
        product_list_data.append({
            "product_code": product_code,
            "cover_image_url": cover_image,
            "quantity": quantities_list[0] if quantities_list else 1
        })
    
    order_data = {
        "customer_code": dealer_code,
        "customer_name": dealer_name,
        "sales_code": saler_code,
        "product_list": product_list_data,
        "departure_base": departure_base,
        "destination": destination
    }

    order_result = sync_run(
        api_client.post("/getorderaddress", order_data)
    )

    result_data["final_order"] = {
        "order_data": order_data,
        "order_result": order_result
    }

    # 输出结果
    if json_output:
        typer.echo(json.dumps(result_data, ensure_ascii=False, indent=2))
    else:
        typer.echo("\n" + "=" * 50)
        typer.echo("订单生成成功!")
        if isinstance(order_result, dict) and "url" in order_result:
            typer.echo(f"订单页面 URL: {order_result['url']}")
            result_data["final_order"]["url"] = order_result["url"]
        else:
            typer.echo(order_result)

