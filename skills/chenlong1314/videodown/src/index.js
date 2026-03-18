/**
 * videodown - 主入口
 */

const { program } = require('commander');
const { download, showHistory, DEFAULT_OUTPUT } = require('./download');
const { search } = require('./search');
const { parseQuickCommand, showHelp } = require('./interaction');

const pkg = require('../package.json');

/**
 * 主函数
 */
async function main() {
  program
    .name('videodown')
    .description(pkg.description)
    .version(pkg.version);

  // 快捷命令支持（交互式）
  program
    .command('interactive')
    .alias('i')
    .description('进入交互模式（支持快捷命令）')
    .action(async () => {
      console.log('🎬 videodown 交互模式');
      console.log('输入 /help 查看可用命令，输入 q 退出\n');
      
      const readline = require('readline');
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });

      const prompt = () => {
        rl.question('videodown> ', async (input) => {
          const trimmed = input.trim();
          
          if (trimmed.toLowerCase() === 'q' || trimmed.toLowerCase() === 'quit') {
            console.log('👋 再见！');
            rl.close();
            return;
          }

          // 尝试解析快捷命令
          const handled = await parseQuickCommand(trimmed, {
            options: {},
            onCancel: () => {}
          });

          if (!handled && trimmed) {
            // 不是快捷命令，尝试自然语言处理
            console.log('💡 提示：使用 /search、/download 等命令，或输入 q 退出');
          }

          prompt();
        });
      };

      prompt();
    });

  // 下载命令
  program
    .command('download [url]')
    .alias('dl')
    .description('下载视频')
    .option('-q, --quality <quality>', '视频质量 (360p|720p|1080p|best)', 'best')
    .option('-o, --output <path>', '输出目录', DEFAULT_OUTPUT)
    .option('-f, --format <format>', '输出格式 (mp4|webm|mp3)', 'mp4')
    .option('--audio-only', '仅下载音频', false)
    .option('--convert', '转码为 H.264 兼容格式 (QuickTime 可用)', false)
    .option('--skip-confirm', '跳过确认', false)
    .action(async (url, options) => {
      if (!url) {
        console.error('❌ 请提供视频 URL');
        console.log('用法：videodown download <url>');
        process.exit(1);
      }
      await download(url, options);
    });

  // 搜索命令
  program
    .command('search <query>')
    .description('搜索视频')
    .option('-p, --platform <platform>', '平台 (youtube|bilibili|all)', 'all')
    .option('-l, --limit <number>', '结果数量', '10')
    .option('-d, --duration <duration>', '时长过滤 (short|medium|long)')
    .option('-s, --select <number>', '直接下载第 N 个结果')
    .action(async (query, options) => {
      await search(query, options);
    });

  // 查看历史命令
  program
    .command('history')
    .alias('h')
    .description('查看下载历史')
    .option('-l, --limit <number>', '显示数量', '10')
    .action((options) => {
      showHistory(parseInt(options.limit));
    });

  // 快捷命令别名
  program
    .command('/search <query>')
    .description('快捷命令：搜索视频')
    .action(async (query) => {
      await search(query, {});
    });

  program
    .command('/download <url>')
    .description('快捷命令：下载视频')
    .action(async (url) => {
      await download(url, {});
    });

  program
    .command('/audio <url>')
    .description('快捷命令：提取音频')
    .action(async (url) => {
      await download(url, { audioOnly: true });
    });

  program
    .command('/history [limit]')
    .description('快捷命令：查看历史')
    .action((limit) => {
      showHistory(parseInt(limit) || 10);
    });

  program
    .command('/cancel')
    .description('快捷命令：取消当前任务')
    .action(() => {
      console.log('🚫 已取消当前任务');
    });

  program
    .command('/help')
    .description('快捷命令：帮助信息')
    .action(() => {
      showHelp();
    });

  // 默认命令（直接提供 URL 时）
  program
    .argument('[url]', '视频 URL')
    .option('-q, --quality <quality>', '视频质量', 'best')
    .option('-o, --output <path>', '输出目录', DEFAULT_OUTPUT)
    .action(async (url, options) => {
      if (!url) {
        program.help();
      }
      await download(url, options);
    });

  program.parse();
}

module.exports = { main };
