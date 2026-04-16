/**
 * Markdown Parser for Eisenhower Task Manager
 * Parses tasks.md, customer-projects.md, delegation.md, maybe.md
 */

const fs = require('fs');
const path = require('path');

// Tasks are located in workspace/tasks/ directory (3 levels up from dashboard)
const TASKS_DIR = path.join(__dirname, '../../..', 'tasks');

/**
 * Parse tasks.md - Four Quadrants Format
 */
function parseTasks(content) {
  const result = {
    q1: [],
    q2: [],
    q3: [],
    q4: [],
    stats: { q1: 0, q2: 0, q3: 0, q4: 0, total: 0 }
  };

  // Extract stats from header
  const statsMatch = content.match(/总任务数：(\d+) \(Q1: (\d+) \+ Q2: (\d+) \+ Q3: (\d+) \+ Q4: (\d+)\)/);
  if (statsMatch) {
    result.stats.total = parseInt(statsMatch[1]);
    result.stats.q1 = parseInt(statsMatch[2]);
    result.stats.q2 = parseInt(statsMatch[3]);
    result.stats.q3 = parseInt(statsMatch[4]);
    result.stats.q4 = parseInt(statsMatch[5]);
  }

  // Split by quadrants
  const q1Match = content.match(/## 🔥 Q1[\s\S]*?(?=## 💼 Q2|$)/);
  const q2Match = content.match(/## 💼 Q2[\s\S]*?(?=## ⚡ Q3|$)/);
  const q3Match = content.match(/## ⚡ Q3[\s\S]*?(?=## 🧘 Q4|$)/);
  const q4Match = content.match(/## 🧘 Q4[\s\S]*?(?=## 👑|$)/);

  if (q1Match) result.q1 = parseQuadrantTasks(q1Match[0], 'Q1');
  if (q2Match) result.q2 = parseQuadrantTasks(q2Match[0], 'Q2');
  if (q3Match) result.q3 = parseQuadrantTasks(q3Match[0], 'Q3');
  if (q4Match) result.q4 = parseQuadrantTasks(q4Match[0], 'Q4');

  return result;
}

function parseQuadrantTasks(content, quadrant) {
  const tasks = [];
  // Match task sections: ### X. Task Name [tags]
  const taskRegex = /### (\d+)\.\s*(.+?)(?:\s*\[([^\]]+)\])?\n([\s\S]*?)(?=### \d+\.|## |\n## |\n---|$)/g;

  let match;
  while ((match = taskRegex.exec(content)) !== null) {
    const taskContent = match[4];
    const task = {
      id: parseInt(match[1]),
      title: match[2].trim(),
      tags: match[3] ? match[3].split('/').map(t => t.trim()) : [],
      quadrant: quadrant,
      status: extractStatus(taskContent),
      priority: extractPriority(taskContent),
      description: extractDescription(taskContent),
      created: extractDate(taskContent, '创建'),
      updated: extractDate(taskContent, '更新'),
      blocked: taskContent.includes('🚫') || taskContent.includes('阻塞'),
      subtasks: extractSubtasks(taskContent),
      raw: match[0]
    };
    tasks.push(task);
  }

  return tasks;
}

function extractStatus(content) {
  const statusMatch = content.match(/\*\*状态\*\*：(.+)/);
  if (statusMatch) {
    const status = statusMatch[1].trim();
    if (status.includes('P0')) return 'P0';
    if (status.includes('P1')) return 'P1';
    if (status.includes('P2')) return 'P2';
    return status;
  }
  return '';
}

function extractPriority(content) {
  if (content.includes('P0')) return 'P0';
  if (content.includes('P1')) return 'P1';
  if (content.includes('P2')) return 'P2';
  return '';
}

function extractDescription(content) {
  const descMatch = content.match(/\*\*描述\*\*：(.+)/);
  return descMatch ? descMatch[1].trim() : '';
}

function extractDate(content, type) {
  const dateMatch = content.match(new RegExp(`\\*\\*${type}\\*\\*：(.+)`));
  return dateMatch ? dateMatch[1].trim() : '';
}

function extractSubtasks(content) {
  const subtasks = [];
  const subtaskRegex = /-\s*\*\*(.+?)\*\*\n([\s\S]*?)(?=\n\s*-\s*\*\*|\n### |\n## |$)/g;

  let match;
  while ((match = subtaskRegex.exec(content)) !== null) {
    subtasks.push({
      title: match[1].trim(),
      content: match[2].trim()
    });
  }

  return subtasks;
}

/**
 * Parse customer-projects.md - Customer Project List Format
 */
function parseCustomerProjects(content) {
  const result = {
    customers: [],
    stats: { active: 0, blocked: 0, pending: 0, total: 0 }
  };

  // Extract stats from overview table (support both Chinese and English)
  const activeMatch = content.match(/🟢 (?:Active|进行中)\s*\|\s*(\d+)/);
  const blockedMatch = content.match(/🟡 (?:Blocked|阻塞中)\s*\|\s*(\d+)/);
  const pendingMatch = content.match(/🔵 (?:Pending|待开始)\s*\|\s*(\d+)/);
  const totalMatch = content.match(/\*\*(?:Total|总计)\*\*\s*\|\s*\*\*(\d+)\*\*/);

  if (activeMatch) result.stats.active = parseInt(activeMatch[1]);
  if (blockedMatch) result.stats.blocked = parseInt(blockedMatch[1]);
  if (pendingMatch) result.stats.pending = parseInt(pendingMatch[1]);
  if (totalMatch) result.stats.total = parseInt(totalMatch[1]);

  // Parse customers and their projects
  // Support new format: ### 🔴 优先级1：Name
  // Note: Emoji is 2 UTF-16 code units (surrogate pair)
  // Use split parsing: first find customer headers, then extract sections manually
  const customerHeaders = Array.from(content.matchAll(/^###\s+(.{1,2})\s+优先级[\d一二三四五]+：(.+)$/gmu));

  for (let i = 0; i < customerHeaders.length; i++) {
    const headerMatch = customerHeaders[i];
    const startPos = headerMatch.index + headerMatch[0].length;
    const endPos = i < customerHeaders.length - 1 ? customerHeaders[i + 1].index : content.length;
    const section = content.substring(startPos, endPos);

    const customer = {
      name: headerMatch[2].trim(),
      priority: headerMatch[1].trim(),
      projects: []
    };

    // Parse projects within customer section
    // Match #### (project level)
    const projectRegex = /^#### (\d+)\.\s*(.+?)\n/gm;
    let projMatch;
    while ((projMatch = projectRegex.exec(section)) !== null) {
      const projStart = projMatch.index + projMatch[0].length;
      // Find where this project ends (next #### or end of section)
      const nextProjMatch = /^#### \d+\./m.exec(section.substring(projStart));
      const projEnd = nextProjMatch ? projStart + nextProjMatch.index : section.length;
      const projContent = section.substring(projStart, projEnd);

      const project = {
        id: parseInt(projMatch[1]),
        name: projMatch[2].trim(),
        status: extractField(projContent, '状态') || extractField(projContent, 'Status'),
        type: extractField(projContent, '类型') || extractField(projContent, 'Type'),
        priority: extractField(projContent, '优先级') || extractField(projContent, 'Priority'),
        created: extractField(projContent, '创建时间') || extractField(projContent, 'Created'),
        lastReview: extractField(projContent, '上次回顾') || extractField(projContent, 'Last Review'),
        nextReview: extractField(projContent, '下次检查') || extractField(projContent, 'Next Review'),
        notes: extractField(projContent, '备注') || extractField(projContent, 'Notes'),
        quadrantTask: extractField(projContent, '象限任务') || extractField(projContent, 'Quadrant Task'),
        blocked: projContent.includes('🟡') || projContent.includes('阻塞')
      };
      customer.projects.push(project);
    }

    result.customers.push(customer);
  }

  return result;
}

function extractField(content, fieldName) {
  // Escape special regex characters in fieldName
  const escapedFieldName = fieldName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // Support Chinese colon (：) - the document uses Chinese colons
  const regex = new RegExp(`- \\*\\*${escapedFieldName}\\*\\*：(.+)`, 'im');
  const match = content.match(regex);
  return match ? match[1].trim() : '';
}

/**
 * Parse delegation.md - Delegation List Format
 */
function parseDelegation(content) {
  const result = {
    tasks: [],
    stats: { total: 0, inProgress: 0, delegated: 0, overdue: 0 }
  };

  // Extract total count
  const totalMatch = content.match(/总任务数：(\d+) 个/);
  if (totalMatch) result.stats.total = parseInt(totalMatch[1]);

  // Parse delegation tasks
  const taskRegex = /#### (\d+)\.\s*(.+?)\n([\s\S]*?)(?=#### \d+\.|## |\n---|$)/g;

  let match;
  while ((match = taskRegex.exec(content)) !== null) {
    const taskContent = match[3];
    const task = {
      id: parseInt(match[1]),
      title: match[2].trim(),
      status: extractField(taskContent, '状态'),
      assignee: extractAssignee(taskContent),
      description: extractField(taskContent, '说明'),
      deadline: extractField(taskContent, 'Deadline'),
      created: extractField(taskContent, '创建时间'),
      lastReview: extractField(taskContent, 'Last Review'),
      nextReview: extractField(taskContent, 'Next Review'),
      overdue: taskContent.includes('⚠️') || taskContent.includes('已过期'),
      raw: match[0]
    };
    result.tasks.push(task);
  }

  // Calculate stats
  result.stats.inProgress = result.tasks.filter(t => t.status === '进行中').length;
  result.stats.delegated = result.tasks.filter(t => t.status === '待开始').length;
  result.stats.overdue = result.tasks.filter(t => t.overdue).length;

  return result;
}

function extractAssignee(content) {
  const match = content.match(/\*\*责任人\*\*：(.+)/);
  return match ? match[1].trim() : '';
}

/**
 * Parse maybe.md - Maybe List Format
 */
function parseMaybeList(content) {
  const result = {
    tasks: [],
    stats: { total: 0 }
  };

  // Extract total count
  const totalMatch = content.match(/总任务数：(\d+) 个/);
  if (totalMatch) result.stats.total = parseInt(totalMatch[1]);

  // Parse maybe tasks
  const taskRegex = /#### (\d+)\.\s*(.+?)\n([\s\S]*?)(?=#### \d+\.|## |\n---|$)/g;

  let match;
  while ((match = taskRegex.exec(content)) !== null) {
    const taskContent = match[3];
    const task = {
      id: parseInt(match[1]),
      title: match[2].trim(),
      status: extractField(taskContent, '状态'),
      description: extractField(taskContent, '说明'),
      created: extractField(taskContent, '创建时间'),
      category: extractCategory(taskContent),
      raw: match[0]
    };
    result.tasks.push(task);
  }

  return result;
}

function extractCategory(content) {
  const match = content.match(/【(.+?)】/);
  return match ? match[1] : '其他';
}

/**
 * Load and parse all task files
 */
function loadAllTasks() {
  const data = {
    timestamp: new Date().toISOString()
  };

  try {
    const tasksContent = fs.readFileSync(path.join(TASKS_DIR, 'tasks.md'), 'utf8');
    data.tasks = parseTasks(tasksContent);
  } catch (e) {
    data.tasks = { error: e.message, q1: [], q2: [], q3: [], q4: [], stats: {} };
  }

  try {
    const customerContent = fs.readFileSync(path.join(TASKS_DIR, 'customer-projects.md'), 'utf8');
    data.customerProjects = parseCustomerProjects(customerContent);
  } catch (e) {
    data.customerProjects = { error: e.message, customers: [], stats: {} };
  }

  try {
    const delegationContent = fs.readFileSync(path.join(TASKS_DIR, 'delegation.md'), 'utf8');
    data.delegation = parseDelegation(delegationContent);
  } catch (e) {
    data.delegation = { error: e.message, tasks: [], stats: {} };
  }

  try {
    const maybeContent = fs.readFileSync(path.join(TASKS_DIR, 'maybe.md'), 'utf8');
    data.maybe = parseMaybeList(maybeContent);
  } catch (e) {
    data.maybe = { error: e.message, tasks: [], stats: {} };
  }

  return data;
}

module.exports = {
  loadAllTasks,
  parseTasks,
  parseCustomerProjects,
  parseDelegation,
  parseMaybeList
};
