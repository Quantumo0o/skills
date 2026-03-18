// 请替换为实际项目包名
package com.yourcompany.huifu.dto;

import com.yourcompany.huifu.dto.BaseRequest;
import lombok.Data;
import lombok.EqualsAndHashCode;

import javax.validation.constraints.NotBlank;

@Data
@EqualsAndHashCode(callSuper = false)
public class HostingPayQueryOrderReq extends BaseRequest {

    @NotBlank(message = "商户号不能为空")
    private String huifuId;

    @NotBlank(message = "原交易请求日期不能为空")
    private String orgReqDate;

    @NotBlank(message = "原交易请求流水号不能为空")
    private String orgReqSeqId;
}
