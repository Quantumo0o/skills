#!/usr/bin/env node

/**
 * videodown - YouTube/Bilibili 视频下载工具
 * 
 * 可执行入口文件
 */

const { main } = require('../src/index');

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
