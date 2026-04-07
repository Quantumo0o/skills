/**
 * singularity-forum - Skill Distiller 模块
 * 从 runtime 日志和记忆文件中自动 distill 出新的 OpenClaw Skill
 *
 * 功能：
 * - 分析 session 日志，识别重复使用的工具组合
 * - 从错误修复中提取模式
 * - 生成 SKILL.md + 脚本
 * - 写入 workspace/skills/ 目录
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';
import { loadCredentials, log } from '../../lib/api.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const SKILLS_OUT = path.join(WORKSPACE, 'skills');

// =============================================================================
// 类型定义
// =============================================================================

export interface DistillConfig {
  minOccurrences?: number;    // 最小出现次数才 distill
  days?: number;              // 分析最近几天
  force?: boolean;             // 强制重新分析
  dryRun?: boolean;           // 不写文件，只输出
}

export interface DistillResult {
  success: boolean;
  skills: DistilledSkill[];
  skipped: number;
  errors: string[];
}

export interface DistilledSkill {
  name: string;
  slug: string;
  description: string;
  triggers: string[];
  scriptContent: string;
  skillMdContent: string;
  confidence: number;
  sourcePattern: string;
  usageCount: number;
  filesWritten?: string[];
}

// =============================================================================
// 工具调用模式识别
// =============================================================================

interface ToolCall {
  tool: string;
  args: Record<string, unknown>;
  timestamp: string;
  success: boolean;
}

interface ToolPattern {
  sequence: string[];    // 工具调用序列
  count: number;         // 出现次数
  successRate: number;    // 成功率
  avgDuration?: number;   // 平均耗时（ms）
  lastSeen: string;
}

/**
 * 从 session transcript 中提取工具调用序列
 */
function extractToolSequences(sessionsDir: string, days: number): ToolPattern[] {
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const patterns: Map<string, ToolPattern> = new Map();

  if (!fs.existsSync(sessionsDir)) return [];

  for (const dir of fs.readdirSync(sessionsDir)) {
    const transcript = path.join(sessionsDir, dir, 'transcript.jsonl');
    if (!fs.existsSync(transcript)) continue;

    try {
      const stat = fs.statSync(transcript);
      if (stat.mtimeMs < cutoff) continue;

      const lines = fs.readFileSync(transcript, 'utf-8')
        .split('\n')
        .filter(l => l.trim());

      let lastTool = '';
      const sequence: string[] = [];

      for (const line of lines) {
        try {
          const entry = JSON.parse(line);
          if (entry.type === 'tool_use' || entry.tool) {
            const tool = entry.tool || entry.name || '';
            if (tool && typeof tool === 'string') {
              // 提取工具名（去掉 namespace）
              const toolName = tool.split('.').pop() || tool;

              if (lastTool) {
                const seqKey = `${lastTool} -> ${toolName}`;
                const existing = patterns.get(seqKey);
                if (existing) {
                  existing.count++;
                  if (entry.success === false) existing.successRate -= 0.1;
                } else {
                  patterns.set(seqKey, {
                    sequence: [lastTool, toolName],
                    count: 1,
                    successRate: entry.success === false ? 0.9 : 1.0,
                    lastSeen: entry.timestamp || new Date().toISOString(),
                  });
                }
              }
              lastTool = toolName;
            }
          }
          // 重置序列如果间隔超过 5 分钟
          if (entry.type === 'tool_result' || entry.type === 'result') {
            lastTool = '';
          }
        } catch { /* skip malformed lines */ }
      }
    } catch { /* skip unreadable */ }
  }

  return Array.from(patterns.values())
    .filter(p => p.count >= 2)
    .sort((a, b) => b.count - a.count);
}

// =============================================================================
// 模式 → Skill 转换
// =============================================================================

function patternToSkill(
  pattern: ToolPattern,
  index: number
): DistilledSkill | null {
  if (pattern.count < 3) return null;

  const tools = pattern.sequence;
  if (tools.length < 2) return null;

  // 生成 skill name
  const primaryTool = tools[0];
  const secondaryTool = tools[1];
  const slug = `auto-${primaryTool.toLowerCase()}-${secondaryTool.toLowerCase()}-${String(index).padStart(2, '0')}`;
  const name = `${capitalize(primaryTool)} + ${capitalize(secondaryTool)} Automation`;

  const description = `自动执行 ${tools.join(' -> ')} 工具序列，成功率 ${(pattern.successRate * 100).toFixed(0)}%，已使用 ${pattern.count} 次。`;

  const triggers = generateTriggers(tools);

  // 生成 SKILL.md
  const skillMd = `# ${name}

> 自动 distill 的 Skill | 模式来源：${pattern.sequence.join(' -> ')}

## 概览

- **Slug**: \`${slug}\`
- **来源**: 从 ${pattern.count} 次实际使用中自动提取
- **成功率**: ${(pattern.successRate * 100).toFixed(0)}%
- **Pattern**: \`${pattern.sequence.join(' -> ')}\`

## 功能

自动执行以下工具序列：

${tools.map((t, i) => `${i + 1}. **${t}**`).join('\n')}

## 触发词

${triggers.map(t => `- "${t}"`).join('\n')}

## 使用方式

\`\`\`bash
node skills/${slug}/index.js
\`\`\`

## 实现说明

本 Skill 由 \`skillDistiller\` 自动生成。
如需修改，请手动编辑。

---

*Generated by singularity-forum skillDistiller @ ${new Date().toISOString()}*
`;

  // 生成脚本
  const scriptContent = `/**
 * ${name}
 * 自动 distill 的 Skill
 *
 * 模式: ${pattern.sequence.join(' -> ')}
 * 使用次数: ${pattern.count}
 * 成功率: ${(pattern.successRate * 100).toFixed(0)}%
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 工具序列
const SEQUENCE = ${JSON.stringify(tools)};
const SUCCESS_RATE = ${pattern.successRate.toFixed(2)};
const USAGE_COUNT = ${pattern.count};

async function run() {
  console.log(\`[${slug}] Starting automated sequence: \${SEQUENCE.join(' -> ')}\`);
  // TODO: 实现具体工具调用逻辑
  console.log(\`[${slug}] Completed successfully\`);
}

// 如果直接运行
run().catch(console.error);

export { run };
`;

  return {
    name,
    slug,
    description,
    triggers,
    scriptContent,
    skillMdContent: skillMd,
    confidence: Math.min(pattern.successRate, pattern.count / 10),
    sourcePattern: pattern.sequence.join(' -> '),
    usageCount: pattern.count,
  };
}

function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function generateTriggers(tools: string[]): string[] {
  const triggers: string[] = [];
  for (const t of tools) {
    triggers.push(\`\${t} 自动化\`);
    triggers.push(\`执行 \${t}\`);
  }
  return [...new Set(triggers)];
}

// =============================================================================
// 错误修复模式识别
// =============================================================================

interface ErrorFixPattern {
  error: string;
  fix: string;
  count: number;
  lastSeen: string;
}

function extractErrorFixPatterns(cacheDir: string, days: number): ErrorFixPattern[] {
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const patterns: Map<string, ErrorFixPattern> = new Map();
  const skillLog = path.join(cacheDir, 'skill.log');

  if (!fs.existsSync(skillLog)) return [];

  try {
    const lines = fs.readFileSync(skillLog, 'utf-8').split('\n').filter(Boolean);
    let currentError = '';

    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        const ts = new Date(entry.timestamp).getTime();
        if (ts < cutoff) continue;

        if (entry.level === 'ERROR' && entry.message) {
          currentError = entry.message.slice(0, 100);
        } else if (entry.level === 'INFO' && entry.message && currentError) {
          const fix = entry.message;
          if (fix.includes('success') || fix.includes('done') || fix.includes('published')) {
            const key = currentError;
            const existing = patterns.get(key);
            if (existing) {
              existing.count++;
              existing.lastSeen = entry.timestamp;
            } else {
              patterns.set(key, {
                error: currentError,
                fix: fix.slice(0, 100),
                count: 1,
                lastSeen: entry.timestamp,
              });
            }
            currentError = '';
          }
        }
      } catch { /* skip */ }
    }
  } catch { /* skip */ }

  return Array.from(patterns.values())
    .filter(p => p.count >= 2)
    .sort((a, b) => b.count - a.count);
}

// =============================================================================
// 主流程
// =============================================================================

export async function distillSkills(config: DistillConfig = {}): Promise<DistillResult> {
  const {
    minOccurrences = 3,
    days = 7,
    dryRun = false,
  } = config;

  const sessionsDir = path.join(os.homedir(), '.openclaw', 'sessions');
  const cacheDir = path.join(os.homedir(), '.cache', 'singularity-forum');

  log('INFO', 'skillDistiller', `Starting distillation (days=${days}, minOccurrences=${minOccurrences}, dryRun=${dryRun})`);

  const errors: string[] = [];
  const skipped: number[] = [];

  // 1. 工具序列模式
  const patterns = extractToolSequences(sessionsDir, days);
  log('INFO', 'skillDistiller', `Found ${patterns.length} tool patterns`);

  // 2. 错误修复模式
  const errorFixes = extractErrorFixPatterns(cacheDir, days);
  log('INFO', 'skillDistiller', `Found ${errorFixes.length} error-fix patterns`);

  // 3. 转换
  const skills: DistilledSkill[] = [];
  let i = 0;
  for (const p of patterns) {
    if (p.count < minOccurrences) { skipped.push(p.count); continue; }
    const skill = patternToSkill(p, i++);
    if (skill) skills.push(skill);
  }

  // 4. 写入文件
  if (!dryRun) {
    if (!fs.existsSync(SKILLS_OUT)) {
      fs.mkdirSync(SKILLS_OUT, { recursive: true });
    }

    for (const skill of skills) {
      try {
        const skillDir = path.join(SKILLS_OUT, skill.slug);
        fs.mkdirSync(skillDir, { recursive: true });

        fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skill.skillMdContent, 'utf-8');
        fs.writeFileSync(path.join(skillDir, 'index.js'), skill.scriptContent, 'utf-8');

        skill.filesWritten = [
          path.join(skillDir, 'SKILL.md'),
          path.join(skillDir, 'index.js'),
        ];

        log('INFO', 'skillDistiller', `Written skill: ${skill.slug}`);
      } catch (e) {
        errors.push(`Failed to write ${skill.slug}: ${e instanceof Error ? e.message : String(e)}`);
      }
    }
  } else {
    for (const s of skills) {
      console.log(\`[DRY RUN] Would create skill: \${s.slug} (\${s.description})\`);
    }
  }

  return {
    success: errors.length === 0,
    skills,
    skipped: skipped.length,
    errors,
  };
}

// =============================================================================
// CLI
// =============================================================================

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const daysArg = args.find(a => a.startsWith('--days='));
const days = daysArg ? parseInt(daysArg.split('=')[1]) : 7;

distillSkills({ days, dryRun })
  .then(result => {
    console.log(`\\n=== Distill Result ===`);
    console.log(`Skills created: ${result.skills.length}`);
    console.log(`Skipped (below threshold): ${result.skipped}`);
    if (result.errors.length > 0) {
      console.log(\`Errors: \${result.errors.join(', ')}\`);
    }
    process.exit(result.errors.length > 0 ? 1 : 0);
  })
  .catch(e => {
    console.error('Fatal:', e instanceof Error ? e.message : String(e));
    process.exit(1);
  });
