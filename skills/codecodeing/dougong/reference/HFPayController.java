// 请替换为实际项目包名
package com.yourcompany.huifu.controller;

import com.yourcompany.huifu.dto.Result;
import com.yourcompany.huifu.dto.HostingPayHtRefundReq;
import com.yourcompany.huifu.dto.HostingPayPreOrderReq;
import com.yourcompany.huifu.dto.HostingPayQueryOrderReq;
import com.yourcompany.huifu.service.HostingPayService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/hfpay")
@Slf4j
public class HFPayController {

    private final HostingPayService hostingPayService;

    public HFPayController(HostingPayService hostingPayService) {
        this.hostingPayService = hostingPayService;
    }

    @PostMapping(value = "/preOrder", produces = "application/json", consumes = "application/json")
    public Result<Map<String, Object>> preOrder(@Validated @RequestBody HostingPayPreOrderReq req) {
        return Result.ok(hostingPayService.preOrder(req));
    }

    @PostMapping(value = "/queryorderinfo", produces = "application/json", consumes = "application/json")
    public Result<Map<String, Object>> queryOrderInfo(@Validated @RequestBody HostingPayQueryOrderReq req) {
        return Result.ok(hostingPayService.queryOrderInfo(req));
    }

    @PostMapping(value = "/htRefund", produces = "application/json", consumes = "application/json")
    public Result<Map<String, Object>> htRefund(@Validated @RequestBody HostingPayHtRefundReq req) {
        return Result.ok(hostingPayService.htRefund(req));
    }
}
