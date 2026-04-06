/**
 * OpenClaw POWPOW Integration Skill - 生产环境修复版本
 *
 * 功能：
 * 1. POWPOW用户注册/登录
 * 2. 数字人创建与管理
 * 3. 与数字人实时通信（使用标准 API）
 *
 * 修复内容（v1.3.0）：
 * 1. 修复聊天功能 - 使用正确的 /api/digital-humans/{id}/chat API
 * 2. 修复响应格式处理 - 适配服务端直接返回数组的格式
 * 3. 添加更好的错误处理
 * 4. 移除未使用的 PowpowClient 依赖
 *
 * @author OpenClaw Team
 * @version 1.3.0
 */
export interface PowpowSkillConfig {
    powpowBaseUrl: string;
    powpowApiKey?: string;
    defaultLocation?: {
        lat: number;
        lng: number;
        name: string;
    };
}
export declare class PowpowSkill implements Skill {
    name: string;
    description: string;
    version: string;
    private config;
    private userSessions;
    private rateLimiter;
    private cleanupInterval?;
    private logger;
    capabilities: ({
        name: string;
        description: string;
        parameters: {
            username: {
                type: string;
                required: boolean;
                description: string;
            };
            name?: undefined;
            description?: undefined;
            lat?: undefined;
            lng?: undefined;
            locationName?: undefined;
            dhId?: undefined;
            message?: undefined;
        };
        handler: (params: {
            username: string;
        }, context: SkillContext) => Promise<string>;
    } | {
        name: string;
        description: string;
        parameters: {
            username: {
                type: string;
                required: boolean;
                description?: undefined;
            };
            name?: undefined;
            description?: undefined;
            lat?: undefined;
            lng?: undefined;
            locationName?: undefined;
            dhId?: undefined;
            message?: undefined;
        };
        handler: (params: {
            username: string;
        }, context: SkillContext) => Promise<string>;
    } | {
        name: string;
        description: string;
        parameters: {
            name: {
                type: string;
                required: boolean;
                description: string;
            };
            description: {
                type: string;
                required: boolean;
                description: string;
            };
            lat: {
                type: string;
                required: boolean;
                description: string;
            };
            lng: {
                type: string;
                required: boolean;
                description: string;
            };
            locationName: {
                type: string;
                required: boolean;
                description: string;
            };
            username?: undefined;
            dhId?: undefined;
            message?: undefined;
        };
        handler: (params: {
            name: string;
            description: string;
            lat?: number;
            lng?: number;
            locationName?: string;
        }, context: SkillContext) => Promise<string>;
    } | {
        name: string;
        description: string;
        parameters: {
            username?: undefined;
            name?: undefined;
            description?: undefined;
            lat?: undefined;
            lng?: undefined;
            locationName?: undefined;
            dhId?: undefined;
            message?: undefined;
        };
        handler: (params: {}, context: SkillContext) => Promise<string>;
    } | {
        name: string;
        description: string;
        parameters: {
            dhId: {
                type: string;
                required: boolean;
                description: string;
            };
            message: {
                type: string;
                required: boolean;
                description: string;
            };
            username?: undefined;
            name?: undefined;
            description?: undefined;
            lat?: undefined;
            lng?: undefined;
            locationName?: undefined;
        };
        handler: (params: {
            dhId: string;
            message: string;
        }, context: SkillContext) => Promise<string>;
    } | {
        name: string;
        description: string;
        parameters: {
            dhId: {
                type: string;
                required: boolean;
                description: string;
            };
            username?: undefined;
            name?: undefined;
            description?: undefined;
            lat?: undefined;
            lng?: undefined;
            locationName?: undefined;
            message?: undefined;
        };
        handler: (params: {
            dhId: string;
        }, context: SkillContext) => Promise<string>;
    })[];
    /**
     * Skill初始化
     */
    initialize(context: SkillContext): Promise<void>;
    /**
     * 获取请求头
     */
    private getHeaders;
    /**
     * 获取或创建用户会话
     */
    private getSession;
    /**
     * 清理过期会话
     */
    private cleanupExpiredSessions;
    /**
     * 检查速率限制
     */
    private checkRateLimit;
    /**
     * 处理用户注册
     */
    private handleRegister;
    /**
     * 处理用户登录
     */
    private handleLogin;
    /**
     * 处理创建数字人
     */
    private handleCreateDigitalHuman;
    /**
     * 处理列出数字人
     */
    private handleListDigitalHumans;
    /**
     * 处理聊天 - 修复版本
     * 使用 /api/digital-humans/{id}/chat API
     */
    private handleChat;
    /**
     * 处理续期
     */
    private handleRenew;
    /**
     * 处理检查徽章
     */
    private handleCheckBadges;
    /**
     * 处理帮助
     */
    private handleHelp;
    /**
     * Skill清理
     */
    destroy(): Promise<void>;
}
export default PowpowSkill;
//# sourceMappingURL=index.d.ts.map