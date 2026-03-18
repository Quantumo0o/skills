// 请替换为实际项目包名
package com.yourcompany.huifu.dto;

import com.yourcompany.huifu.enums.ResponseEnum;
import lombok.Data;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.MDC;
import com.yourcompany.huifu.constant.Constants;

@Data
public class Result<T> {

    private String respCode;
    private String respDesc;
    private String uniqueId;
    private T data;

    public static <T> Result<T> ok() {
        return new Result<T>().respCode(ResponseEnum.SUCCESS.getRespCode()).respDesc(ResponseEnum.SUCCESS.getRespDesc());
    }

    public static <T> Result<T> ok(T payload) {
        return new Result<T>().respCode(ResponseEnum.SUCCESS.getRespCode()).respDesc(ResponseEnum.SUCCESS.getRespDesc()).payload(payload);
    }

    public static <T> Result<T> fail(ResponseEnum responseEnum) {
        return new Result<T>().respCode(responseEnum.getRespCode()).respDesc(responseEnum.getRespDesc());
    }

    public static <T> Result<T> fail(String code, String message) {
        return new Result<T>().respCode(code).respDesc(message);
    }

    private Result<T> respCode(String respCode) {
        this.respCode = respCode;
        return this;
    }

    private Result<T> respDesc(String respDesc) {
        this.respDesc = respDesc;
        return this;
    }

    private Result<T> uniqueId(String uniqueId) {
        this.uniqueId = uniqueId;
        return this;
    }

    private Result<T> payload(T payload) {
        this.data = payload;
        return this;
    }

    public String getUniqueId() {
        if (StringUtils.isBlank(uniqueId)) {
            uniqueId = MDC.get(Constants.TRACE_ID);
        }
        return uniqueId;
    }
}
