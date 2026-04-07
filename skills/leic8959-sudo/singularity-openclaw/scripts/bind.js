#!/usr/bin/env node
import { runBindFlow, quickBind, checkStatus, runUnbind } from '../lib/binding.js';

const [cmd, ...rest] = process.argv.slice(2);
const code = rest[0];

(async () => {
  if (cmd === 'bind') {
    if (code) {
      console.log('\n快速绑定，绑定码:', code);
      const result = await quickBind(code);
      if (result.success) console.log('绑定成功！');
      else { console.error('绑定失败：' + result.message); process.exit(1); }
    } else {
      const result = await runBindFlow();
      if (!result.success) { console.error('失败：' + result.message); process.exit(1); }
      console.log('\n=== 绑定完成 ===');
    }
  } else if (cmd === 'status') {
    const s = await checkStatus();
    console.log('\n=== 绑定状态 ===');
    if (!s.configured) console.log('未配置凭证，请先运行 node scripts/setup.js');
    else if (s.bound) {
      console.log('已绑定'); console.log('   Webhook: ' + (s.webhookHost || '未知'));
      console.log('   Agent ID: ' + (s.agentId || '默认')); console.log('   绑定时间: ' + (s.boundAt || '未知'));
    } else { console.log('未绑定'); if (s.error) console.log('   错误: ' + s.error); }
  } else if (cmd === 'unbind') {
    const r = await runUnbind();
    console.log((r.success ? '✅' : '❌') + ' ' + r.message);
  } else {
    console.log('用法：'); console.log('  node scripts/bind.js bind         # 绑定（交互）');
    console.log('  node scripts/bind.js bind <CODE>  # 快速绑定'); console.log('  node scripts/bind.js status      # 状态'); console.log('  node scripts/bind.js unbind     # 解绑');
  }
})().catch(err => { console.error('Fatal:', err.message); process.exit(1); });
