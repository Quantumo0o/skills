// 请替换为实际项目包名
package com.yourcompany.huifu.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.exception.BasePayException;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentHtrefundRequest;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentPreorderH5Request;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentQueryorderinfoRequest;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;
import com.yourcompany.huifu.dto.HostingPayHtRefundReq;
import com.yourcompany.huifu.dto.HostingPayPreOrderReq;
import com.yourcompany.huifu.dto.HostingPayQueryOrderReq;
import com.yourcompany.huifu.enums.ResponseEnum;
import com.yourcompany.huifu.exception.BizException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
public class HostingPayService {

    // 从配置文件读取，严禁硬编码
    @Value("${huifu.notify-url}")
    private String defaultNotifyUrl;

    @Value("${huifu.refund-notify-url}")
    private String refundNotifyUrl;

    @Value("${huifu.hosting.project-id}")
    private String projectId;

    @Value("${huifu.hosting.project-title}")
    private String projectTitle;

    @Value("${huifu.hosting.callback-url}")
    private String callbackUrl;

    private final ObjectMapper objectMapper;

    public HostingPayService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    // ==================== 预下单 ====================

    public Map<String, Object> preOrder(HostingPayPreOrderReq req) {
        V2TradeHostingPaymentPreorderH5Request request = buildPreOrderRequest(req);
        try {
            Map<String, Object> response = BasePayClient.request(request, false);
            log.info("汇付预下单响应: huifuId={}, resp_code={}", req.getHuifuId(), response.get("resp_code"));
            return response;
        } catch (BasePayException | IllegalAccessException e) {
            log.error("汇付SDK调用异常(预下单), huifuId={}", req.getHuifuId(), e);
            throw new BizException(ResponseEnum.SYSTEM_ERROR);
        }
    }

    private V2TradeHostingPaymentPreorderH5Request buildPreOrderRequest(HostingPayPreOrderReq req) {
        V2TradeHostingPaymentPreorderH5Request request = new V2TradeHostingPaymentPreorderH5Request();
        request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
        request.setReqSeqId(SequenceTools.getReqSeqId32());
        request.setHuifuId(req.getHuifuId());
        request.setTransAmt(req.getTransAmt());
        request.setGoodsDesc(req.getGoodsDesc());

        // 预下单类型：默认 H5/PC
        String preOrderType = StringUtils.hasText(req.getPreOrderType()) ? req.getPreOrderType() : "1";
        request.setPreOrderType(preOrderType);

        request.setHostingData(buildHostingData());

        Map<String, Object> extendInfoMap = new HashMap<>(4);
        extendInfoMap.put("delay_acct_flag", "N");
        // 通知地址优先使用请求传入的，其次使用配置文件默认值
        String notifyUrl = StringUtils.hasText(req.getNotifyUrl()) ? req.getNotifyUrl() : defaultNotifyUrl;
        extendInfoMap.put("notify_url", notifyUrl);
        request.setExtendInfo(extendInfoMap);
        return request;
    }

    private String buildHostingData() {
        ObjectNode dto = objectMapper.createObjectNode();
        dto.put("project_title", projectTitle);
        dto.put("project_id", projectId);
        dto.put("callback_url", callbackUrl);
        return dto.toString();
    }

    // ==================== 订单查询 ====================

    public Map<String, Object> queryOrderInfo(HostingPayQueryOrderReq req) {
        V2TradeHostingPaymentQueryorderinfoRequest request = buildQueryOrderInfoRequest(req);
        try {
            Map<String, Object> response = BasePayClient.request(request, false);
            log.info("汇付订单查询响应: huifuId={}, resp_code={}, trans_stat={}",
                    req.getHuifuId(), response.get("resp_code"), response.get("trans_stat"));
            return response;
        } catch (BasePayException | IllegalAccessException e) {
            log.error("汇付SDK调用异常(订单查询), huifuId={}, orgReqSeqId={}", req.getHuifuId(), req.getOrgReqSeqId(), e);
            throw new BizException(ResponseEnum.SYSTEM_ERROR);
        }
    }

    private V2TradeHostingPaymentQueryorderinfoRequest buildQueryOrderInfoRequest(HostingPayQueryOrderReq req) {
        V2TradeHostingPaymentQueryorderinfoRequest request = new V2TradeHostingPaymentQueryorderinfoRequest();
        // reqDate 为本次查询请求的日期，由系统自动生成
        request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
        request.setReqSeqId(SequenceTools.getReqSeqId32());
        request.setHuifuId(req.getHuifuId());
        // orgReqDate 为原交易的请求日期，由调用方传入
        request.setOrgReqDate(req.getOrgReqDate());
        request.setOrgReqSeqId(req.getOrgReqSeqId());
        return request;
    }

    // ==================== 退款 ====================

    public Map<String, Object> htRefund(HostingPayHtRefundReq req) {
        V2TradeHostingPaymentHtrefundRequest request = buildHtRefundRequest(req);
        try {
            Map<String, Object> response = BasePayClient.request(request, false);
            log.info("汇付退款响应: huifuId={}, orgReqSeqId={}, resp_code={}",
                    req.getHuifuId(), req.getOrgReqSeqId(), response.get("resp_code"));
            return response;
        } catch (BasePayException | IllegalAccessException e) {
            log.error("汇付SDK调用异常(退款), huifuId={}, orgReqSeqId={}", req.getHuifuId(), req.getOrgReqSeqId(), e);
            throw new BizException(ResponseEnum.SYSTEM_ERROR);
        }
    }

    private V2TradeHostingPaymentHtrefundRequest buildHtRefundRequest(HostingPayHtRefundReq req) {
        V2TradeHostingPaymentHtrefundRequest request = new V2TradeHostingPaymentHtrefundRequest();
        request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
        request.setReqSeqId(SequenceTools.getReqSeqId32());
        request.setHuifuId(req.getHuifuId());
        request.setOrdAmt(req.getOrdAmt());
        request.setOrgReqDate(req.getOrgReqDate());

        Map<String, Object> extendInfoMap = new HashMap<>(8);
        extendInfoMap.put("org_req_seq_id", req.getOrgReqSeqId());
        // device_type 枚举：1=SDK，2=手机浏览器，3=PC浏览器，4=公众号/小程序
        extendInfoMap.put("terminal_device_data", "{\"device_type\":\"4\"}");
        // 退款回调地址从配置文件读取
        extendInfoMap.put("notify_url", refundNotifyUrl);
        request.setExtendInfo(extendInfoMap);
        return request;
    }
}
