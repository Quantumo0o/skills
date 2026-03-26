#!/usr/bin/env node
import { readFileSync } from 'fs';
import { join } from 'path';

const args = process.argv.slice(2);
const command = args[0];

function loadConfig() {
  const toolsPath = join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace', 'TOOLS.md');
  const content = readFileSync(toolsPath, 'utf-8');
  const section = content.match(/## 禅道 API \(ZenTao API\)([\s\S]*?)(?=##|$)/)?.[1];
  if (!section) throw new Error('未找到禅道 API 配置');
  
  const apiUrl = section.match(/API 地址[:：]\s*(.+)/)?.[1]?.trim();
  const username = section.match(/用户名[:：]\s*(.+)/)?.[1]?.trim();
  const password = section.match(/密码[:：]\s*(.+)/)?.[1]?.trim();
  
  if (!apiUrl || !username || !password) throw new Error('禅道 API 配置不完整');
  
  return { apiUrl: apiUrl.replace(/\/$/, ''), username, password };
}

async function getToken(config) {
  const res = await fetch(`${config.apiUrl}/api.php/v1/tokens`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ account: config.username, password: config.password })
  });
  if (!res.ok) throw new Error(`登录失败: ${res.status}`);
  const data = await res.json();
  if (!data.token) throw new Error('未获取到 token');
  return data.token;
}

async function login() {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    console.log(JSON.stringify({ success: true, token, message: '登录成功' }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

async function listExecutions(keyword = '') {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    const executions = [];
    let page = 1;
    
    while (page <= 10) {
      const res = await fetch(`${config.apiUrl}/api.php/v1/executions?page=${page}&limit=100`, {
        headers: { 'Content-Type': 'application/json', 'token': token }
      });
      if (!res.ok) throw new Error(`获取失败: ${res.status}`);
      const data = await res.json();
      if (!data.executions?.length) break;
      
      if (keyword) {
        executions.push(...data.executions.filter(e => e.name?.includes(keyword) || e.project?.includes(keyword)));
      } else {
        executions.push(...data.executions);
      }
      page++;
    }
    
    console.log(JSON.stringify({ success: true, count: executions.length, executions: executions.map(e => ({ id: e.id, name: e.name, project: e.project, status: e.status, begin: e.begin, end: e.end })) }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

async function createTask(executionId, name, assignedTo, options = {}) {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    
    const tomorrow = new Date(); tomorrow.setDate(tomorrow.getDate() + 1);
    const dayAfter = new Date(); dayAfter.setDate(dayAfter.getDate() + 2);
    const fmt = d => d.toISOString().split('T')[0];
    
    const taskData = {
      name, assignedTo,
      pri: options.pri || 3,
      estimate: options.estimate || 6,
      type: options.type || 'test',
      estStarted: options.estStarted || fmt(tomorrow),
      deadline: options.deadline || fmt(dayAfter),
      desc: options.desc || ''
    };
    
    const res = await fetch(`${config.apiUrl}/api.php/v1/executions/${executionId}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'token': token },
      body: JSON.stringify(taskData)
    });
    
    if (!res.ok) throw new Error(`创建失败: ${await res.text()}`);
    const result = await res.json();
    console.log(JSON.stringify({ success: true, taskId: result.id, name: result.name, assignedTo: result.assignedTo, message: `任务创建成功！ID: ${result.id}` }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

async function listTasks(executionId, status = '') {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    let url = `${config.apiUrl}/api.php/v1/executions/${executionId}/tasks`;
    if (status) url += `?status=${status}`;
    
    const res = await fetch(url, { headers: { 'Content-Type': 'application/json', 'token': token } });
    if (!res.ok) throw new Error(`获取失败: ${res.status}`);
    const data = await res.json();
    const tasks = data.tasks || [];
    
    console.log(JSON.stringify({ success: true, count: tasks.length, tasks: tasks.map(t => ({ id: t.id, name: t.name, assignedTo: t.assignedTo, status: t.status, pri: t.pri, estimate: t.estimate, consumed: t.consumed, left: t.left })) }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

// CLI 路由
switch (command) {
  case 'login':
    await login();
    break;
  case 'list-executions':
    await listExecutions(args[1] || '');
    break;
  case 'create-task':
    if (args.length < 4) {
      console.error('用法: cym-zentao create-task <executionId> <name> <assignedTo> [options]');
      process.exit(1);
    }
    const options = args[4] ? JSON.parse(args[4]) : {};
    await createTask(parseInt(args[1]), args[2], args[3], options);
    break;
  case 'list-tasks':
    if (args.length < 2) {
      console.error('用法: cym-zentao list-tasks <executionId> [status]');
      process.exit(1);
    }
    await listTasks(parseInt(args[1]), args[2] || '');
    break;
  default:
    console.log(`
禅道项目管理 CLI

用法:
  cym-zentao login                          测试登录
  cym-zentao list-executions [keyword]      列出执行
  cym-zentao create-task <executionId> <name> <assignedTo> [options]  创建任务
  cym-zentao list-tasks <executionId> [status]  列出任务

示例:
  cym-zentao list-executions "日常任务"
  cym-zentao create-task 6159 "测试功能" "陈跃美"
  cym-zentao create-task 6159 "测试功能" "陈跃美" '{"pri":2,"estimate":8}'
`);
    process.exit(1);
}
