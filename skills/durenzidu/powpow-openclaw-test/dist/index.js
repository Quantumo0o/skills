"use strict";
// @ts-nocheck
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.PowpowSkill = void 0;
const powpow_client_1 = require("./powpow-client");
const validator_1 = require("./utils/validator");
const rate_limiter_1 = require("./utils/rate-limiter");
const constants_1 = require("./utils/constants");
class PowpowSkill {
    name = 'powpow-integration';
    description = 'Integration with POWPOW platform for digital human management and communication';
    version = '1.3.0';
    config;
    userSessions = new Map();
    rateLimiter;
    cleanupInterval;
    logger;
    // 能力定义
    capabilities = [
        {
            name: 'register',
            description: 'Register a new POWPOW account',
            parameters: {
                username: { type: 'string', required: true, description: 'Username for POWPOW (3-50 chars, alphanumeric)' },
            },
            handler: this.handleRegister.bind(this),
        },
        {
            name: 'login',
            description: 'Login to existing POWPOW account',
            parameters: {
                username: { type: 'string', required: true },
            },
            handler: this.handleLogin.bind(this),
        },
        {
            name: 'createDigitalHuman',
            description: 'Create a digital human on POWPOW map (requires 2 badges)',
            parameters: {
                name: { type: 'string', required: true, description: 'Digital human name (1-100 chars)' },
                description: { type: 'string', required: true, description: 'Description/personality (max 500 chars)' },
                lat: { type: 'number', required: false, description: 'Latitude (-90 to 90)' },
                lng: { type: 'number', required: false, description: 'Longitude (-180 to 180)' },
                locationName: { type: 'string', required: false, description: 'Location name' },
            },
            handler: this.handleCreateDigitalHuman.bind(this),
        },
        {
            name: 'listDigitalHumans',
            description: 'List all your digital humans',
            parameters: {},
            handler: this.handleListDigitalHumans.bind(this),
        },
        {
            name: 'chat',
            description: 'Chat with a digital human (one message at a time)',
            parameters: {
                dhId: { type: 'string', required: true, description: 'Digital human ID' },
                message: { type: 'string', required: true, description: 'Message to send (max 2000 chars)' },
            },
            handler: this.handleChat.bind(this),
        },
        {
            name: 'renew',
            description: 'Renew a digital human for 30 days (requires 1 badge)',
            parameters: {
                dhId: { type: 'string', required: true, description: 'Digital human ID to renew' },
            },
            handler: this.handleRenew.bind(this),
        },
        {
            name: 'checkBadges',
            description: 'Check your badge balance',
            parameters: {},
            handler: this.handleCheckBadges.bind(this),
        },
        {
            name: 'help',
            description: 'Show available commands',
            parameters: {},
            handler: this.handleHelp.bind(this),
        },
    ];
    /**
     * Skill初始化
     */
    async initialize(context) {
        this.config = context.getConfig('powpow');
        if (!this.config?.powpowBaseUrl) {
            throw new Error('POWPOW base URL is required in skill configuration');
        }
        // 初始化日志
        this.logger = {
            debug: (msg, meta) => context.logger.debug(`[POWPOW] ${msg}`, meta),
            info: (msg, meta) => context.logger.info(`[POWPOW] ${msg}`, meta),
            warn: (msg, meta) => context.logger.warn(`[POWPOW] ${msg}`, meta),
            error: (msg, err, meta) => context.logger.error(`[POWPOW] ${msg}`, err, meta),
        };
        // 初始化速率限制器
        this.rateLimiter = new rate_limiter_1.RateLimiter();
        // 启动会话清理定时器
        this.cleanupInterval = setInterval(() => {
            this.cleanupExpiredSessions();
        }, constants_1.SESSION_CONFIG.CLEANUP_INTERVAL);
        this.logger.info('POWPOW skill initialized (v1.3.0 - production ready)', {
            baseUrl: this.config.powpowBaseUrl,
            hasApiKey: !!this.config.powpowApiKey,
        });
    }
    /**
     * 获取请求头
     */
    getHeaders(token) {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        if (this.config.powpowApiKey) {
            headers['X-API-Key'] = this.config.powpowApiKey;
        }
        return headers;
    }
    /**
     * 获取或创建用户会话
     */
    getSession(userId) {
        if (!this.userSessions.has(userId)) {
            this.userSessions.set(userId, {
                isChatting: false,
                lastActivity: Date.now()
            });
        }
        else {
            const session = this.userSessions.get(userId);
            session.lastActivity = Date.now();
        }
        return this.userSessions.get(userId);
    }
    /**
     * 清理过期会话
     */
    cleanupExpiredSessions() {
        const now = Date.now();
        let cleanedCount = 0;
        for (const [userId, session] of this.userSessions.entries()) {
            if (now - session.lastActivity > constants_1.SESSION_CONFIG.TIMEOUT) {
                this.userSessions.delete(userId);
                cleanedCount++;
            }
        }
        if (cleanedCount > 0) {
            this.logger.info(`Cleaned up ${cleanedCount} expired sessions`);
        }
    }
    /**
     * 检查速率限制
     */
    checkRateLimit(userId, action) {
        if (!this.rateLimiter.isAllowed(userId)) {
            const resetTime = this.rateLimiter.getResetTime(userId);
            const waitSeconds = resetTime ? Math.ceil((resetTime - Date.now()) / 1000) : 60;
            return `❌ Rate limit exceeded. Please try again in ${waitSeconds} seconds.`;
        }
        return null;
    }
    /**
     * 处理用户注册
     */
    async handleRegister(params, context) {
        const rateLimitError = this.checkRateLimit(context.userId, 'register');
        if (rateLimitError)
            return rateLimitError;
        const usernameValidation = validator_1.Validator.validateUsername(params.username);
        if (!usernameValidation.valid) {
            return `❌ ${usernameValidation.error}`;
        }
        this.logger.info('Processing registration', {
            username: params.username,
            openclawUserId: context.userId
        });
        try {
            const response = await fetch(`${this.config.powpowBaseUrl}/api/openclaw/auth/register`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    username: validator_1.Validator.sanitizeString(params.username),
                    nickname: validator_1.Validator.sanitizeString(params.username),
                }),
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ message: 'Unknown error' }));
                throw new powpow_client_1.PowpowAPIError(error.message || response.statusText, response.status);
            }
            const result = await response.json();
            const session = this.getSession(context.userId);
            session.powpowUserId = result.data.user_id;
            this.rateLimiter.clearForKey(context.userId);
            this.logger.info('Registration successful', {
                powpowUserId: result.data.user_id,
                openclawUserId: context.userId
            });
            return `✅ Registration successful!\n` +
                `👤 User ID: ${result.data.user_id}\n` +
                `🏅 Initial badges: ${result.data.badges}\n` +
                `\nYou can now create digital humans using the 'createDigitalHuman' command.`;
        }
        catch (error) {
            if (error instanceof powpow_client_1.PowpowAPIError) {
                this.logger.error('Registration failed', error, {
                    username: params.username,
                    status: error.statusCode
                });
                if (error.statusCode === 409) {
                    return `❌ 用户名 "${params.username}" 已被注册，请尝试其他用户名`;
                }
                if (error.statusCode === 400) {
                    return `❌ 注册信息不完整，请检查用户名格式（3-50字符）`;
                }
                return `❌ 注册失败: ${error.message}`;
            }
            this.logger.error('Unexpected registration error', error);
            return '❌ 注册时发生未知错误，请稍后重试';
        }
    }
    /**
     * 处理用户登录
     */
    async handleLogin(params, context) {
        const rateLimitError = this.checkRateLimit(context.userId, 'login');
        if (rateLimitError)
            return rateLimitError;
        const usernameValidation = validator_1.Validator.validateUsername(params.username);
        if (!usernameValidation.valid) {
            return `❌ ${usernameValidation.error}`;
        }
        this.logger.info('Processing login', {
            username: params.username,
            openclawUserId: context.userId
        });
        try {
            const response = await fetch(`${this.config.powpowBaseUrl}/api/openclaw/auth/login`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    username: validator_1.Validator.sanitizeString(params.username),
                }),
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ message: 'Unknown error' }));
                throw new powpow_client_1.PowpowAPIError(error.message || response.statusText, response.status);
            }
            const result = await response.json();
            const session = this.getSession(context.userId);
            session.powpowUserId = result.data.user_id;
            session.powpowToken = result.data.token;
            this.rateLimiter.clearForKey(context.userId);
            this.logger.info('Login successful', {
                powpowUserId: result.data.user_id,
                openclawUserId: context.userId
            });
            return `✅ Login successful!\n` +
                `👤 User ID: ${result.data.user_id}\n` +
                `🏅 Available badges: ${result.data.badges}`;
        }
        catch (error) {
            if (error instanceof powpow_client_1.PowpowAPIError) {
                this.logger.warn('Login failed', {
                    username: params.username,
                    status: error.statusCode
                });
                if (error.statusCode === 404) {
                    return `❌ 用户 "${params.username}" 不存在，请先使用 "register username=${params.username}" 注册账号`;
                }
                return `❌ 登录失败: ${error.message}`;
            }
            this.logger.error('Unexpected login error', error);
            return '❌ 登录时发生未知错误，请稍后重试';
        }
    }
    /**
     * 处理创建数字人
     */
    async handleCreateDigitalHuman(params, context) {
        const session = this.getSession(context.userId);
        if (!session.powpowUserId || !session.powpowToken) {
            return '⚠️ 请先登录 PowPow 账号\n使用命令: login username=<你的用户名>';
        }
        const nameValidation = validator_1.Validator.validateDigitalHumanName(params.name);
        if (!nameValidation.valid) {
            return `❌ ${nameValidation.error}`;
        }
        const descValidation = validator_1.Validator.validateDescription(params.description);
        if (!descValidation.valid) {
            return `❌ ${descValidation.error}`;
        }
        const lat = params.lat ?? this.config.defaultLocation?.lat ?? 39.9042;
        const lng = params.lng ?? this.config.defaultLocation?.lng ?? 116.4074;
        const coordValidation = validator_1.Validator.validateCoordinates(lat, lng);
        if (!coordValidation.valid) {
            return `❌ ${coordValidation.error}`;
        }
        const locationName = params.locationName
            ? validator_1.Validator.sanitizeString(params.locationName)
            : this.config.defaultLocation?.name ?? 'Beijing';
        this.logger.info('Creating digital human', {
            name: params.name,
            userId: session.powpowUserId
        });
        try {
            const response = await fetch(`${this.config.powpowBaseUrl}/api/openclaw/digital-humans`, {
                method: 'POST',
                headers: this.getHeaders(session.powpowToken),
                body: JSON.stringify({
                    name: validator_1.Validator.sanitizeString(params.name),
                    description: validator_1.Validator.sanitizeString(params.description),
                    lat,
                    lng,
                    locationName,
                    userId: session.powpowUserId,
                }),
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ message: 'Unknown error' }));
                throw new powpow_client_1.PowpowAPIError(error.message || response.statusText, response.status);
            }
            const result = await response.json();
            const dh = result.data;
            session.currentDigitalHuman = dh;
            this.logger.info('Digital human created', {
                dhId: dh.id,
                name: dh.name
            });
            return `✅ Digital human created successfully!\n` +
                `🎭 Name: ${dh.name}\n` +
                `🆔 ID: ${dh.id}\n` +
                `📍 Location: ${dh.locationName} (${dh.lat}, ${dh.lng})\n` +
                `⏰ Expires at: ${new Date(dh.expiresAt).toLocaleString()}\n` +
                `\nYou can now chat with it using: chat dhId=${dh.id} message=<your_message>`;
        }
        catch (error) {
            if (error instanceof powpow_client_1.PowpowAPIError) {
                if (error.statusCode === 402) {
                    return `❌ 徽章不足！创建数字人需要 2 个徽章。\n\n` +
                        `💡 获取徽章的方法：\n` +
                        `1. 新用户注册自动获得 3 个徽章\n` +
                        `2. 参与 Act3 剧情决策获得徽章\n` +
                        `3. 在 Act4 打卡景点获得徽章\n` +
                        `4. 在 Act5 与数字人对话（每3次+1徽章）\n\n` +
                        `使用 "checkBadges" 命令查看当前徽章余额`;
                }
                if (error.statusCode === 401) {
                    return `❌ 登录已过期，请使用 "login username=<你的用户名>" 重新登录`;
                }
                return `❌ 创建数字人失败: ${error.message}`;
            }
            this.logger.error('Unexpected error creating digital human', error);
            return '❌ 创建数字人时发生未知错误，请稍后重试';
        }
    }
    /**
     * 处理列出数字人
     */
    async handleListDigitalHumans(params, context) {
        const session = this.getSession(context.userId);
        if (!session.powpowUserId || !session.powpowToken) {
            return '⚠️ 请先登录 PowPow 账号\n使用命令: login username=<你的用户名>';
        }
        try {
            // 修复：服务端直接返回数组，不是 { data: [...] }
            const response = await fetch(`${this.config.powpowBaseUrl}/api/openclaw/users/${session.powpowUserId}/digital-humans`, {
                headers: this.getHeaders(session.powpowToken),
            });
            if (!response.ok) {
                throw new powpow_client_1.PowpowAPIError('Failed to fetch digital humans', response.status);
            }
            // 直接解析为数组（服务端返回的是数组，不是对象）
            const dhs = await response.json();
            // 确保是数组
            const digitalHumans = Array.isArray(dhs) ? dhs : (dhs.data || []);
            if (digitalHumans.length === 0) {
                return '📭 You have no digital humans yet.\n' +
                    'Create one using: createDigitalHuman name=<name> description=<description>';
            }
            let response_text = `🎭 You have ${digitalHumans.length} digital human(s):\n\n`;
            digitalHumans.forEach((dh, index) => {
                const daysLeft = Math.ceil((new Date(dh.expiresAt).getTime() - Date.now()) / (1000 * 60 * 60 * 24));
                const status = dh.isActive ? '✅' : '❌';
                response_text += `${index + 1}. ${status} ${dh.name}\n` +
                    `   ID: ${dh.id}\n` +
                    `   📍 ${dh.locationName}\n` +
                    `   ⏰ ${daysLeft} days left\n` +
                    `   💬 Chat: chat dhId=${dh.id} message=hello\n\n`;
            });
            return response_text;
        }
        catch (error) {
            if (error instanceof powpow_client_1.PowpowAPIError) {
                this.logger.error('Failed to list digital humans', error);
                if (error.statusCode === 401) {
                    return `❌ 登录已过期，请使用 "login username=<你的用户名>" 重新登录`;
                }
                return `❌ 获取数字人列表失败: ${error.message}`;
            }
            this.logger.error('Unexpected error listing digital humans', error);
            return '❌ 获取数字人列表时发生错误，请稍后重试';
        }
    }
    /**
     * 处理聊天 - 修复版本
     * 使用 /api/digital-humans/{id}/chat API
     */
    async handleChat(params, context) {
        const session = this.getSession(context.userId);
        if (!session.powpowUserId || !session.powpowToken) {
            return '⚠️ 请先登录 PowPow 账号\n使用命令: login username=<你的用户名>';
        }
        const dhIdValidation = validator_1.Validator.validateDigitalHumanId(params.dhId);
        if (!dhIdValidation.valid) {
            return `❌ ${dhIdValidation.error}`;
        }
        const messageValidation = validator_1.Validator.validateMessage(params.message);
        if (!messageValidation.valid) {
            return `❌ ${messageValidation.error}`;
        }
        this.logger.info('Sending chat message', {
            dhId: params.dhId,
            userId: session.powpowUserId,
            messageLength: params.message.length
        });
        try {
            // 发送消息并获取 SSE 流式响应
            const response = await fetch(`${this.config.powpowBaseUrl}/api/digital-humans/${params.dhId}/chat`, {
                method: 'POST',
                headers: this.getHeaders(session.powpowToken),
                body: JSON.stringify({
                    digitalHumanId: params.dhId,
                    message: params.message,
                }),
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ error: 'Unknown error' }));
                throw new powpow_client_1.PowpowAPIError(error.error || response.statusText, response.status);
            }
            // 检查是否是 SSE 流
            const contentType = response.headers.get('content-type');
            if (contentType?.includes('text/event-stream')) {
                // 处理 SSE 流式响应
                const reader = response.body?.getReader();
                if (!reader) {
                    throw new Error('No response body');
                }
                const decoder = new TextDecoder();
                let buffer = '';
                let fullContent = '';
                let sessionId = null;
                // 读取流
                while (true) {
                    const { done, value } = await reader.read();
                    if (done)
                        break;
                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop() || '';
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const dataStr = line.slice(6);
                            // 检查是否完成
                            if (dataStr === '[DONE]') {
                                continue;
                            }
                            try {
                                const data = JSON.parse(dataStr);
                                // 获取 sessionId
                                if (data.sessionId) {
                                    sessionId = data.sessionId;
                                }
                                // 累加内容
                                if (data.content) {
                                    fullContent += data.content;
                                }
                            }
                            catch (e) {
                                // 忽略解析错误
                            }
                        }
                    }
                }
                this.logger.info('Chat response received', {
                    dhId: params.dhId,
                    contentLength: fullContent.length,
                    sessionId
                });
                if (fullContent) {
                    return `💬 **${params.dhId}**: ${fullContent}`;
                }
                else {
                    return `💬 Message sent, but no response received. Please try again.`;
                }
            }
            else {
                // 普通 JSON 响应
                const result = await response.json();
                if (result.error) {
                    throw new powpow_client_1.PowpowAPIError(result.error, response.status);
                }
                return `💬 **${params.dhId}**: ${result.content || result.message || 'No response'}`;
            }
        }
        catch (error) {
            if (error instanceof powpow_client_1.PowpowAPIError) {
                this.logger.error('Chat failed', error, { dhId: params.dhId });
                if (error.statusCode === 404) {
                    return `❌ 数字人不存在或已过期，请使用 "listDigitalHumans" 查看可用的数字人`;
                }
                if (error.statusCode === 401) {
                    return `❌ 登录已过期，请使用 "login username=<你的用户名>" 重新登录`;
                }
                if (error.statusCode === 400) {
                    return `❌ ${error.message}`;
                }
                return `❌ 聊天失败: ${error.message}`;
            }
            this.logger.error('Unexpected chat error', error, { dhId: params.dhId });
            return '❌ 聊天时发生错误，请稍后重试';
        }
    }
    /**
     * 处理续期
     */
    async handleRenew(params, context) {
        const session = this.getSession(context.userId);
        if (!session.powpowUserId || !session.powpowToken) {
            return '⚠️ 请先登录 PowPow 账号\n使用命令: login username=<你的用户名>';
        }
        const dhIdValidation = validator_1.Validator.validateDigitalHumanId(params.dhId);
        if (!dhIdValidation.valid) {
            return `❌ ${dhIdValidation.error}`;
        }
        this.logger.info('Renewing digital human', {
            dhId: params.dhId,
            userId: session.powpowUserId
        });
        try {
            const response = await fetch(`${this.config.powpowBaseUrl}/api/openclaw/digital-humans/${params.dhId}/renew`, {
                method: 'POST',
                headers: this.getHeaders(session.powpowToken),
                body: JSON.stringify({ userId: session.powpowUserId }),
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ message: 'Unknown error' }));
                throw new powpow_client_1.PowpowAPIError(error.message || response.statusText, response.status);
            }
            const result = await response.json();
            const dh = result.data;
            this.logger.info('Digital human renewed', {
                dhId: params.dhId,
                newExpiry: dh.expiresAt
            });
            return `✅ 数字人续期成功！\n` +
                `🎭 名称: ${dh.name}\n` +
                `⏰ 新过期时间: ${new Date(dh.expiresAt).toLocaleString()}\n` +
                `📅 已延长 30 天`;
        }
        catch (error) {
            if (error instanceof powpow_client_1.PowpowAPIError) {
                if (error.statusCode === 402) {
                    return `❌ 徽章不足！续期数字人需要 1 个徽章。\n\n` +
                        `💡 获取徽章的方法：\n` +
                        `1. 参与 Act3 剧情决策获得徽章\n` +
                        `2. 在 Act4 打卡景点获得徽章\n` +
                        `3. 在 Act5 与数字人对话（每3次+1徽章）\n\n` +
                        `使用 "checkBadges" 命令查看当前徽章余额`;
                }
                if (error.statusCode === 404) {
                    return `❌ 数字人不存在，请使用 "listDigitalHumans" 查看可用的数字人`;
                }
                if (error.statusCode === 401) {
                    return `❌ 登录已过期，请使用 "login username=<你的用户名>" 重新登录`;
                }
                return `❌ 续期失败: ${error.message}`;
            }
            this.logger.error('Unexpected error renewing digital human', error);
            return '❌ 续期时发生错误，请稍后重试';
        }
    }
    /**
     * 处理检查徽章
     */
    async handleCheckBadges(params, context) {
        const session = this.getSession(context.userId);
        if (!session.powpowUserId || !session.powpowToken) {
            return '⚠️ 请先登录 PowPow 账号\n使用命令: login username=<你的用户名>';
        }
        try {
            const response = await fetch(`${this.config.powpowBaseUrl}/api/openclaw/users/${session.powpowUserId}/badges`, {
                headers: this.getHeaders(session.powpowToken),
            });
            if (!response.ok) {
                throw new powpow_client_1.PowpowAPIError('Failed to check badges', response.status);
            }
            const result = await response.json();
            const badges = result.data;
            return `🏅 徽章余额\n` +
                `   数量: ${badges.count}\n` +
                `   类型: ${badges.type === 'standard' ? '标准徽章' : badges.type}\n\n` +
                `💡 徽章用途:\n` +
                `   • 创建数字人: 消耗 2 个徽章\n` +
                `   • 续期数字人: 消耗 1 个徽章（延长30天）\n\n` +
                `💰 获取徽章:\n` +
                `   • 新用户注册: +3 徽章\n` +
                `   • Act3 剧情决策: 每次 +1~2 徽章\n` +
                `   • Act4 打卡景点: 每次 +1 徽章\n` +
                `   • Act5 数字人对话: 每3次 +1 徽章`;
        }
        catch (error) {
            if (error instanceof powpow_client_1.PowpowAPIError) {
                this.logger.error('Failed to check badges', error);
                if (error.statusCode === 401) {
                    return `❌ 登录已过期，请使用 "login username=<你的用户名>" 重新登录`;
                }
                return `❌ 查询徽章失败: ${error.message}`;
            }
            this.logger.error('Unexpected error checking badges', error);
            return '❌ 查询徽章时发生错误，请稍后重试';
        }
    }
    /**
     * 处理帮助
     */
    async handleHelp(params, context) {
        return `🎭 PowPow 数字人 Skill - 可用命令\n\n` +
            `🔐 认证命令:\n` +
            `  • register username=<用户名> - 注册新账号（用户名：3-50字符）\n` +
            `  • login username=<用户名> - 登录已有账号\n\n` +
            `🎭 数字人管理:\n` +
            `  • createDigitalHuman name=<名称> description=<描述> [lat=<纬度> lng=<经度> locationName=<位置>] - 创建数字人（消耗2徽章）\n` +
            `  • listDigitalHumans - 列出所有数字人\n` +
            `  • renew dhId=<数字人ID> - 续期数字人（消耗1徽章，延长30天）\n\n` +
            `💬 通信:\n` +
            `  • chat dhId=<数字人ID> message=<消息> - 与数字人聊天\n\n` +
            `💰 账户:\n` +
            `  • checkBadges - 查看徽章余额\n` +
            `  • help - 显示此帮助信息\n\n` +
            `💡 提示:\n` +
            `  • 新用户注册获得3个徽章\n` +
            `  • 创建数字人需要2个徽章\n` +
            `  • 数字人有效期30天，可续期`;
    }
    /**
     * Skill清理
     */
    async destroy() {
        if (this.cleanupInterval) {
            clearInterval(this.cleanupInterval);
            this.cleanupInterval = undefined;
        }
        this.userSessions.clear();
        this.rateLimiter.clear();
        this.logger.info('POWPOW skill destroyed');
    }
}
exports.PowpowSkill = PowpowSkill;
// 导出Skill类
exports.default = PowpowSkill;
//# sourceMappingURL=index.js.map