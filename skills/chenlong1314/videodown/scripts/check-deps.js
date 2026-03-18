#!/usr/bin/env node

/**
 * 依赖检查脚本
 * 在 npm install 后自动运行
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('🔍 检查 videodown 依赖...\n');

const deps = [
  {
    name: 'yt-dlp',
    checkCmd: 'yt-dlp --version',
    installCmd: {
      darwin: 'brew install yt-dlp',
      linux: 'sudo apt install yt-dlp',
      win32: 'choco install yt-dlp'
    },
    required: true
  },
  {
    name: 'ffmpeg',
    checkCmd: 'ffmpeg -version',
    installCmd: {
      darwin: 'brew install ffmpeg',
      linux: 'sudo apt install ffmpeg',
      win32: 'choco install ffmpeg'
    },
    required: true
  },
  {
    name: 'jq',
    checkCmd: 'jq --version',
    installCmd: {
      darwin: 'brew install jq',
      linux: 'sudo apt install jq',
      win32: 'choco install jq'
    },
    required: false
  }
];

let missingDeps = [];

deps.forEach(dep => {
  try {
    execSync(dep.checkCmd, { stdio: 'ignore' });
    console.log(`✅ ${dep.name} 已安装`);
  } catch (error) {
    const status = dep.required ? '❌' : '⚠️';
    console.log(`${status} ${dep.name} 未安装${dep.required ? '' : '（可选）'}`);
    if (dep.required) {
      missingDeps.push(dep);
    }
  }
});

console.log('');

if (missingDeps.length > 0) {
  console.log('⚠️  以下必需依赖未安装:\n');
  missingDeps.forEach(dep => {
    const platform = process.platform;
    const installCmd = dep.installCmd[platform] || dep.installCmd.linux;
    console.log(`  ${dep.name}: ${installCmd}`);
  });
  console.log('\n💡 请手动安装上述依赖后使用 videodown');
  console.log('');
  process.exit(1);
} else {
  console.log('✅ 所有依赖检查通过！\n');
  console.log('🎉 videodown 已就绪，可以开始使用：');
  console.log('   videodown search "关键词"');
  console.log('   videodown <url>');
  console.log('');
}
