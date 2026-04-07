#!/usr/bin/env node
/**
 * 自动配置 npm/yarn/pnpm 国内镜像源
 * 支持 Windows、Linux、Mac 系统
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 可用的镜像源
const MIRRORS = {
    aliyun: {
        url: 'https://registry.npmmirror.com',
        name: '阿里云'
    },
    tencent: {
        url: 'https://mirrors.cloud.tencent.com/npm/',
        name: '腾讯云'
    },
    huawei: {
        url: 'https://repo.huaweicloud.com/repository/npm/',
        name: '华为云'
    }
};

const DEFAULT_MIRROR = 'aliyun';

/**
 * 检测已安装的包管理器
 */
function detectPackageManager() {
    const managers = [];
    
    try {
        execSync('npm --version', { stdio: 'ignore' });
        managers.push('npm');
    } catch (e) {}
    
    try {
        execSync('yarn --version', { stdio: 'ignore' });
        managers.push('yarn');
    } catch (e) {}
    
    try {
        execSync('pnpm --version', { stdio: 'ignore' });
        managers.push('pnpm');
    } catch (e) {}
    
    return managers;
}

/**
 * 配置指定包管理器的镜像
 */
function configure(manager, mirrorKey) {
    const mirror = MIRRORS[mirrorKey] || MIRRORS[DEFAULT_MIRROR];
    console.log(`\n正在配置 ${manager}...`);
    
    try {
        execSync(`${manager} config set registry ${mirror.url}`, { 
            stdio: 'inherit' 
        });
        console.log(`✓ ${manager} 配置成功`);
        console.log(`  镜像: ${mirror.name}`);
        console.log(`  URL: ${mirror.url}`);
    } catch (error) {
        console.error(`✗ ${manager} 配置失败:`, error.message);
    }
}

/**
 * 创建项目级 .npmrc 文件
 */
function createProjectConfig(mirrorKey, projectPath) {
    const mirror = MIRRORS[mirrorKey] || MIRRORS[DEFAULT_MIRROR];
    const npmrcPath = path.join(projectPath || process.cwd(), '.npmrc');
    
    const content = `registry=${mirror.url}\n`;
    fs.writeFileSync(npmrcPath, content, 'utf-8');
    
    console.log(`✓ 项目级配置已保存到: ${npmrcPath}`);
    console.log(`  镜像: ${mirror.name}`);
    console.log(`  URL: ${mirror.url}`);
}

/**
 * 显示当前配置
 */
function showCurrentConfig(manager) {
    try {
        const registry = execSync(`${manager} config get registry`, { 
            encoding: 'utf-8' 
        }).trim();
        console.log(`\n${manager} 当前 registry:`);
        console.log(`  ${registry}`);
    } catch (error) {
        console.error(`无法获取 ${manager} 配置:`, error.message);
    }
}

/**
 * 列出所有可用镜像
 */
function listMirrors() {
    console.log('\n可用的 npm 镜像源:');
    console.log('-'.repeat(60));
    Object.entries(MIRRORS).forEach(([key, info]) => {
        console.log(`  ${key.padEnd(12)} - ${info.name.padEnd(10)} - ${info.url}`);
    });
    console.log('-'.repeat(60));
}

/**
 * 主函数
 */
function main() {
    const args = process.argv.slice(2);
    
    // 解析参数
    const options = {
        mirror: DEFAULT_MIRROR,
        project: false,
        show: false,
        list: false,
        manager: null
    };
    
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--project' || arg === '-p') {
            options.project = true;
        } else if (arg === '--show' || arg === '-s') {
            options.show = true;
        } else if (arg === '--list' || arg === '-l') {
            options.list = true;
        } else if (arg.startsWith('--mirror=')) {
            options.mirror = arg.split('=')[1];
        } else if (arg.startsWith('-m=')) {
            options.mirror = arg.split('=')[1];
        } else if (!arg.startsWith('-')) {
            options.manager = arg;
        }
    }
    
    // 处理命令
    if (options.list) {
        listMirrors();
        return;
    }
    
    // 检测包管理器
    const managers = options.manager ? [options.manager] : detectPackageManager();
    
    if (managers.length === 0) {
        console.log('✗ 未检测到任何包管理器');
        console.log('请先安装 npm、yarn 或 pnpm');
        process.exit(1);
    }
    
    if (options.show) {
        managers.forEach(manager => showCurrentConfig(manager));
        return;
    }
    
    // 执行配置
    console.log('检测到包管理器:', managers.join(', '));
    
    if (options.project) {
        createProjectConfig(options.mirror);
    } else {
        managers.forEach(manager => configure(manager, options.mirror));
    }
    
    console.log('\n验证配置:');
    console.log('运行以下命令测试:');
    managers.forEach(manager => {
        console.log(`  ${manager} config get registry`);
    });
}

main();
