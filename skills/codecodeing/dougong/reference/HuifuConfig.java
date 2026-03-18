// 请替换为实际项目包名
package com.yourcompany.huifu.config;

import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.config.MerConfig;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;

@Configuration
@Slf4j
public class HuifuConfig {

    // 从配置文件读取，配置文件通过环境变量注入，严禁硬编码
    @Value("${huifu.product-id}")
    private String productId;

    @Value("${huifu.sys-id}")
    private String sysId;

    @Value("${huifu.rsa-private-key}")
    private String rsaPrivateKey;

    @Value("${huifu.rsa-public-key}")
    private String rsaPublicKey;

    // SDK 初始化在应用启动时执行一次，避免每次请求重复初始化
    @PostConstruct
    public void initSdk() {
        MerConfig merConfig = new MerConfig();
        // 注意：SDK 原生方法名即为 setProcutId（非 setProductId），请勿"修正"
        merConfig.setProcutId(productId);
        merConfig.setSysId(sysId);
        merConfig.setRsaPrivateKey(rsaPrivateKey);
        merConfig.setRsaPublicKey(rsaPublicKey);
        BasePay.initWithMerConfig(merConfig);
        log.info("汇付SDK初始化完成");
    }
}
