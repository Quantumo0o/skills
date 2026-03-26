/**
 * Clarity Ollama - 本地模型精准转换核心 V3
 * 规则引擎 + Ollama混合
 */

const http = require('http');

const OLLAMA_HOST = 'localhost';
const OLLAMA_PORT = 11434;
const MODEL = 'qwen:0.5b';

// ============================================
// 规则库
// ============================================

const INTENT_PATTERNS = {
  performance: ['慢', '性能', '优化', '快', '效率', '卡顿', '延迟', '耗时', '为什么慢', '运行慢'],
  debug: ['debug', '调试', 'bug', '错误', '报错', '出问题', '有问题', '不对', '失败', '异常', '有什么问题', '找出问题'],
  create: ['写代码', '创建', '做一个', '写一个', '帮我写', '生成', '写段', '写个'],
  explain: ['解释', '讲讲', '什么是', '是什么', '原理', '科普'],
  modify: ['修改', '改成', '改一下', '重构', '重写'],
  analyze: ['分析', '检查', '评估', '看看', '审查'],
  teach: ['教我', '学习', '教一下', '入门'],
};

const LANGUAGE_PATTERNS = {
  javascript: ['javascript', 'js', 'node'],
  typescript: ['typescript', 'ts'],
  python: ['python', 'py'],
  java: ['java'],
  cpp: ['c++', 'cpp'],
  csharp: ['c#', 'csharp'],
  go: ['golang', 'go语言'],
  rust: ['rust'],
  php: ['php'],
  ruby: ['ruby'],
  swift: ['swift', 'ios'],
  kotlin: ['kotlin'],
  sql: ['sql', 'mysql', '数据库'],
  html: ['html', '前端'],
  css: ['css', '样式'],
  react: ['react', 'jsx'],
  vue: ['vue'],
  nextjs: ['nextjs'],
};

const FOCUS_PATTERNS = {
  loop: ['循环', 'for', 'while', '迭代'],
  function: ['函数', 'function', '方法'],
  async: ['异步', 'async', 'await', 'promise'],
  array: ['数组', 'array', '列表'],
  object: ['对象', 'object', '字典'],
  string: ['字符串', 'string'],
  error: ['错误', 'exception', '报错'],
  memory: ['内存', 'memory'],
  api: ['api', '接口', 'http'],
  database: ['数据库', 'db'],
  security: ['安全', 'security'],
  algorithm: ['算法', '排序', '搜索'],
  ui: ['界面', 'ui', '样式'],
  test: ['测试', 'test'],
  deploy: ['部署', 'deploy'],
};

const INTENT_LABELS = {
  performance: '性能优化',
  debug: '代码调试',
  create: '代码创建',
  explain: '概念解释',
  modify: '代码修改',
  analyze: '分析检查',
  teach: '学习指导',
};

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function ruleBasedTransform(input) {
  let cleaned = input.trim().toLowerCase();
  
  // 去除废话
  const fillers = ['你好', '您好', '请问', '请教', '谢谢', '感谢', '那个', '这个', '就是', '关于', '能不能', '啊', '呀', '呢', '吧', '哦', '非常', '特别', '很'];
  for (let f of fillers) {
    cleaned = cleaned.replace(new RegExp(escapeRegex(f), 'gi'), ' ');
  }
  cleaned = cleaned.replace(/\s+/g, ' ').trim();
  
  // 识别意图 - 按优先级
  let intent = 'general';
  const intentPriority = ['performance', 'debug', 'create', 'explain', 'modify', 'analyze', 'teach'];
  for (let key of intentPriority) {
    const words = INTENT_PATTERNS[key];
    for (let w of words) {
      if (cleaned.includes(w)) {
        intent = key;
        break;
      }
    }
    if (intent !== 'general') break;
  }
  
  // 识别语言
  let languages = [];
  for (let [lang, words] of Object.entries(LANGUAGE_PATTERNS)) {
    for (let w of words) {
      if (cleaned.includes(w)) {
        languages.push(lang.charAt(0).toUpperCase() + lang.slice(1));
        break;
      }
    }
  }
  
  // 识别关注点
  let focus = [];
  for (let [key, words] of Object.entries(FOCUS_PATTERNS)) {
    for (let w of words) {
      if (cleaned.includes(w)) {
        focus.push(key.charAt(0).toUpperCase() + key.slice(1));
        break;
      }
    }
  }
  
  // 生成目标
  let goal = cleaned;
  for (let words of Object.values(INTENT_PATTERNS)) {
    for (let w of words) {
      goal = goal.replace(new RegExp(escapeRegex(w), 'gi'), ' ');
    }
  }
  for (let words of Object.values(LANGUAGE_PATTERNS)) {
    for (let w of words) {
      goal = goal.replace(new RegExp(escapeRegex(w), 'gi'), ' ');
    }
  }
  
  // 清理
  goal = goal.replace(/[,，。!！?？]+/g, ' ').replace(/\s+/g, ' ').trim();
  goal = goal.replace(/^[\s]+/, '').replace(/[\s]+$/, '');
  
  if (goal.length < 2) {
    goal = INTENT_LABELS[intent] || '完成请求';
  }
  
  return {
    intent: INTENT_LABELS[intent] || '一般请求',
    language: languages[0] || '',
    focus: focus.join(', '),
    goal,
    missing: [],
    source: 'rule',
  };
}

// ============================================
// Ollama API
// ============================================

function callOllama(prompt) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: MODEL,
      prompt: prompt,
      stream: false,
      options: { temperature: 0.1, num_predict: 60 }
    });

    const options = {
      hostname: OLLAMA_HOST,
      port: OLLAMA_PORT,
      path: '/api/generate',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          resolve(parsed.response || '');
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// ============================================
// 主函数
// ============================================

async function transform(input) {
  const original = input.trim();
  const ruleResult = ruleBasedTransform(original);
  
  let enhanced = false;
  try {
    await callOllama(original);
    enhanced = true;
  } catch (e) { }
  
  return { success: true, data: ruleResult, enhanced, original };
}

function formatOutput(data, original, enhanced) {
  const lines = [];
  lines.push('## 🎯 精准化指令');
  lines.push(enhanced ? '*(规则引擎 + Ollama)*' : '*(规则引擎)*');
  lines.push('');
  if (data.intent) lines.push(`**📌 意图：** ${data.intent}`);
  if (data.language) lines.push(`**💻 语言：** ${data.language}`);
  if (data.focus) lines.push(`**🎯 关注点：** ${data.focus}`);
  if (data.goal) lines.push(`**🎯 目标：** ${data.goal}`);
  lines.push('');
  lines.push('---');
  lines.push(`**📝 原始消息：** ${original}`);
  return lines.join('\n');
}

// ============================================
// CLI
// ============================================

async function main() {
  const input = process.argv.slice(2).join(' ');
  
  if (!input) {
    console.log('用法: node precision-ollama.js <消息>');
    process.exit(0);
  }
  
  if (input === '--test') {
    const tests = [
      'Python的for循环为什么运行慢',
      '帮我看看代码有什么问题',
      'React的useEffect是什么',
      '帮我写一个登录功能',
      '这个Java代码性能很差帮我优化',
    ];
    
    for (let test of tests) {
      const r = await transform(test);
      console.log(`📝 ${test}\n${formatOutput(r.data, r.original, r.enhanced)}\n`);
    }
    process.exit(0);
  }
  
  const r = await transform(input);
  console.log(formatOutput(r.data, r.original, r.enhanced));
}

module.exports = { transform, formatOutput };

if (require.main === module) {
  main();
}
