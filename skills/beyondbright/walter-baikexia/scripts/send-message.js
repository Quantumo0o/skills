/**
 * 百科虾消息发送脚本
 * 功能：
 * 1. 检测回复中的 mention 标签（『AT:...』 或 <at>）
 * 2. 通过飞书 IM API 发送消息，将 mention 信息正确传递
 * 3. 支持发送图片（使用 curl 上传）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILL_DIR = path.join(__dirname, '..');
const CONFIG_FILE = path.join(SKILL_DIR, 'config', 'app.json');
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
const APP_ID = config.app_id;
const APP_SECRET = config.app_secret;
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 获取 token
function getToken() {
    const cmd = `curl -s -X POST '${FEISHU_BASE}/auth/v3/tenant_access_token/internal' \\
        -H 'Content-Type: application/json' \\
        -d '{"app_id":"${APP_ID}","app_secret":"${APP_SECRET}"}'`;
    const result = execSync(cmd, { encoding: 'utf8' });
    const data = JSON.parse(result);
    if (!data.tenant_access_token) throw new Error('获取token失败');
    return data.tenant_access_token;
}

// 发送 HTTP 请求
function sendRequest(url, method, headers, body) {
    let cmd = `curl -s -X ${method} '${url}'`;
    for (const [k, v] of Object.entries(headers)) {
        cmd += ` -H '${k}: ${v}'`;
    }
    if (body) {
        cmd += ` -d '${body.replace(/'/g, "'\\''")}'`;
    }
    return execSync(cmd, { encoding: 'utf8' });
}

// 从文本中提取所有 mention 信息
function extractMentions(text) {
    const mentions = [];
    const patterns = [
        /『AT:([^:]+):([^』]+)』/g,
        /\{\{AT:([^:]+):([^}]+)\}\}/g,
        /<at user_id="([^"]+)">([^<]+)<\/at>/g
    ];
    
    for (const regex of patterns) {
        let match;
        while ((match = regex.exec(text)) !== null) {
            mentions.push({ userId: match[1], name: match[2] });
        }
    }
    return mentions;
}

// 将 mention 格式替换为纯名字
function stripAtTags(text) {
    text = text.replace(/『AT:[^:]+:([^』]+)』/g, '$1');
    text = text.replace(/\{\{AT:[^:]+:([^}]+)\}\}/g, '$1');
    text = text.replace(/<at user_id="[^"]+">([^<]+)<\/at>/g, '$1');
    return text;
}

// 上传图片获取 image_key（使用 curl）
function uploadImage(token, imagePath) {
    const cmd = `curl -s -X POST '${FEISHU_BASE}/im/v1/images' \\
        -H 'Authorization: Bearer ${token}' \\
        -F 'image=@${imagePath};type=image/jpeg' \\
        -F 'image_type=message'`;
    const result = execSync(cmd, { encoding: 'utf8' });
    const data = JSON.parse(result);
    if (data.code !== 0) throw new Error(data.msg || '图片上传失败');
    return data.data.image_key;
}

// 发送文本消息
function sendTextMessage(token, receiveId, receiveIdType, text, mentions) {
    let processedText = text;
    for (const m of mentions) {
        processedText = processedText.replace(
            `『AT:${m.userId}:${m.name}』`,
            `<at user_id="${m.userId}">${m.name}</at>`
        );
    }
    
    const payload = {
        receive_id: receiveId,
        msg_type: 'text',
        content: JSON.stringify({ text: processedText })
    };
    
    const result = sendRequest(
        `${FEISHU_BASE}/im/v1/messages?receive_id_type=${receiveIdType}`,
        'POST',
        {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        JSON.stringify(payload)
    );
    return JSON.parse(result);
}

// 发送图片消息
function sendImageMessage(token, receiveId, receiveIdType, imageKey) {
    const payload = {
        receive_id: receiveId,
        msg_type: 'image',
        content: JSON.stringify({ image_key: imageKey })
    };
    
    const result = sendRequest(
        `${FEISHU_BASE}/im/v1/messages?receive_id_type=${receiveIdType}`,
        'POST',
        {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        JSON.stringify(payload)
    );
    return JSON.parse(result);
}

async function main() {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        console.error('用法: node send-message.js <receive_id> <receive_id_type> [content_file]');
        process.exit(1);
    }
    
    const receiveId = args[0];
    const receiveIdType = args[1];
    let text;
    
    if (args[2]) {
        text = fs.readFileSync(args[2], 'utf8');
    } else {
        text = fs.readFileSync('/dev/stdin', 'utf8');
    }
    
    text = text.trim();
    if (!text) {
        console.log('消息内容为空，无需发送');
        process.exit(0);
    }
    
    // 检查是否包含图片路径标记
    const imageMatch = text.match(/『IMG:([^』]+)』/);
    const mediaMatch = text.match(/MEDIA:([^\n]+)/);
    const mentions = extractMentions(text);
    const cleanText = stripAtTags(text);
    
    console.log('发送消息...');
    console.log('原始文本:', text);
    console.log('清理后文本:', cleanText);
    console.log('Mentions:', JSON.stringify(mentions));
    console.log('Image match:', imageMatch);
    console.log('Media match:', mediaMatch);
    
    const token = getToken();
    let result;
    
    if (imageMatch) {
        // 发送图片消息
        const imagePath = imageMatch[1];
        console.log('检测到图片:', imagePath);
        const imageKey = uploadImage(token, imagePath);
        console.log('image_key:', imageKey);
        result = sendImageMessage(token, receiveId, receiveIdType, imageKey);
    } else if (mediaMatch) {
        // 发送 MEDIA 格式图片
        const imagePath = mediaMatch[1].trim();
        console.log('检测到 MEDIA 图片:', imagePath);
        const imageKey = uploadImage(token, imagePath);
        console.log('image_key:', imageKey);
        result = sendImageMessage(token, receiveId, receiveIdType, imageKey);
    } else {
        // 发送文本消息
        result = sendTextMessage(token, receiveId, receiveIdType, text, mentions);
    }
    
    if (result.code === 0) {
        console.log('消息发送成功');
    } else {
        console.error('消息发送失败:', result.msg);
        process.exit(1);
    }
}

main().catch(err => {
    console.error('错误:', err.message);
    process.exit(1);
});
