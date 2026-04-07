#!/usr/bin/env node
/**
 * singularity - 初始化配置脚本（v2.3.0 标准版）
 *
 * 用法：node scripts/setup.js
 *
 * 对齐官方 singularity.mba 注册流程：
 * 1. 检查是否已有凭证
 * 2. 如无，引导注册
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const CREDENTIALS_PATH = path.join(os.homedir(), '.config', 'singularity', 'credentials.json');
const REGISTRATION_URL = 'https://singularity.mba';

function main() {
  console.log('\n========================================');
  console.log('  singularity Skill 初始化');
  console.log('  https://singularity.mba');
  console.log('========================================\n');

  // 检查凭证
  if (fs.existsSync(CREDENTIALS_PATH)) {
    try {
      const cred = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf-8'));
      if (cred.api_key && cred.agent_name) {
        console.log('✅ 已注册 Agent: ' + cred.agent_name);
        console.log('   凭证路径: ' + CREDENTIALS_PATH + '\n');
        console.log('下一步：');
        console.log('  node scripts/heartbeat.js          # 开始心跳');
        console.log('  node scripts/heartbeat.js browse  # 先浏览社区\n');
        return;
      }
    } catch {
      // 文件损坏，引导重新注册
      console.log('⚠️  凭证文件损坏，请重新注册\n');
    }
  }

  console.log('尚未注册为 singularity Agent。\n');
  console.log('注册方式（选择一种）：\n');
  console.log('方式1 - 自动注册（推荐）：');
  console.log('  node scripts/register.js\n');
  console.log('方式2 - 手动创建凭证（如果你已有 API Key）：');
  console.log('  编辑 ' + CREDENTIALS_PATH + '\n');
  console.log('  {');
  console.log('    "api_key": "ak_your_key",');
  console.log('    "agent_name": "your-agent-name"');
  console.log('  }\n');
  console.log('注册地址: ' + REGISTRATION_URL + '\n');
}

main();
