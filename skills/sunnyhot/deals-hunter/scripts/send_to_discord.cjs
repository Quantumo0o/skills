#!/usr/bin/env node
/**
 * 将羊毛报告分段发送到 Discord
 */

const fs = require('fs');

// 读取报告
const report = fs.readFileSync('/tmp/deals_report.md', 'utf-8');

// Discord 字符限制
const MAX_LENGTH = 1900;

// 分段
function splitMessage(text, maxLength) {
  const lines = text.split('\n');
  const chunks = [];
  let currentChunk = '';
  
  for (const line of lines) {
    if (currentChunk.length + line.length + 1 > maxLength) {
      chunks.push(currentChunk.trim());
      currentChunk = line + '\n';
    } else {
      currentChunk += line + '\n';
    }
  }
  
  if (currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }
  
  return chunks;
}

const chunks = splitMessage(report, MAX_LENGTH);

// 输出到 stdout（供 cron 读取）
console.log('---DISCORD_CHUNKS_START---');
chunks.forEach((chunk, i) => {
  console.log(`---CHUNK_${i + 1}---`);
  console.log(chunk);
});
console.log('---DISCORD_CHUNKS_END---');
