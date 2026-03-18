// 请替换为实际项目包名
package com.yourcompany.huifu.dto;

import com.yourcompany.huifu.dto.BaseRequest;
import lombok.Data;
import lombok.EqualsAndHashCode;

import javax.validation.constraints.NotBlank;

@Data
@EqualsAndHashCode(callSuper = false)
public class HostingPayPreOrderReq extends BaseRequest {

    @NotBlank(message = "商户号不能为空")
    private String huifuId;

    @NotBlank(message = "交易金额不能为空")
    private String transAmt;

    @NotBlank(message = "商品描述不能为空")
    private String goodsDesc;

    // 预下单类型：1=H5/PC；2=支付宝小程序；3=微信小程序，默认 "1"
    private String preOrderType;

    // 支付结果异步通知地址，选填，未传则使用配置文件中的默认值
    private String notifyUrl;
}
