#!/usr/bin/env node
/**
 * h-ear CLI — OpenClaw-friendly command-line interface for H-ear audio classification.
 *
 * Usage:
 *   h-ear health                          Check API status
 *   h-ear sounds [search]                 List sound classes
 *   h-ear usage                           Show API usage
 *   h-ear classify <file-or-url>          Classify audio (sync, polls for results)
 *   h-ear capture [--duration 15]         Capture audio from RTSP camera and classify
 *   h-ear jobs [--limit 5]               List recent jobs
 *
 * Environment:
 *   HEAR_API_KEY    API key (required)
 *   HEAR_ENV        Environment: dev, staging, prod (default: prod)
 *   LISTEN_RTSP_URL RTSP source URL (for capture command)
 */

import { readFileSync, unlinkSync, existsSync, mkdirSync } from 'fs';
import { spawnSync } from 'child_process';
import { join } from 'path';
import { tmpdir } from 'os';
import { createSkill } from './index.js';
import { healthCommand } from './commands/health.js';
import { soundsCommand } from './commands/sounds.js';
import { usageCommand } from './commands/usage.js';
import { classifySyncCommand } from './commands/classify.js';
import { jobsCommand } from './commands/jobs.js';
import { formatClassifyResult } from './formatter.js';

// --- Arg parsing -------------------------------------------------------------

const args = process.argv.slice(2);
const command = args[0] ?? 'help';

function getFlag(flag: string): string | null {
    const idx = args.indexOf(flag);
    return idx >= 0 && args[idx + 1] ? args[idx + 1] : null;
}

function hasFlag(flag: string): boolean {
    return args.includes(flag);
}

// --- Capture -----------------------------------------------------------------

function captureAudio(sourceUrl: string, durationSec: number): { buffer: Buffer; fileName: string } {
    const tmpDir = join(tmpdir(), 'h-ear-listen');
    if (!existsSync(tmpDir)) mkdirSync(tmpDir, { recursive: true });

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').replace('T', '_').slice(0, 19);
    const outFile = join(tmpDir, `capture_${timestamp}_${durationSec}s.wav`);

    const ffmpegArgs: string[] = ['-y'];
    if (sourceUrl.startsWith('rtsp://')) ffmpegArgs.push('-rtsp_transport', 'tcp');
    ffmpegArgs.push(
        '-i', sourceUrl,
        '-vn', '-ac', '1', '-ar', '16000', '-acodec', 'pcm_s16le',
        '-t', String(durationSec), '-f', 'wav', outFile,
    );

    const result = spawnSync('ffmpeg', ffmpegArgs, {
        stdio: ['pipe', 'pipe', 'pipe'],
        encoding: 'utf-8',
        timeout: (durationSec + 30) * 1000,
    });

    if (result.status !== 0 || !existsSync(outFile)) {
        const stderr = (result.stderr || '').trim().split('\n').slice(-3).join('\n');
        throw new Error(`ffmpeg capture failed (exit ${result.status}): ${stderr}`);
    }

    const buffer = readFileSync(outFile);
    try { unlinkSync(outFile); } catch (err) { console.error(`  Cleanup warning: failed to remove temp file ${outFile}`, err); }
    return { buffer: Buffer.from(buffer), fileName: `capture_${timestamp}_${durationSec}s.wav` };
}

// --- Main --------------------------------------------------------------------

async function main(): Promise<void> {
    if (command === 'help' || command === '--help' || command === '-h') {
        console.log(`h-ear — Sound Intelligence CLI

Usage:
  h-ear health                          Check API status
  h-ear sounds [search]                 List sound classes (521+)
  h-ear usage                           Show API usage stats
  h-ear classify <file-or-url>          Classify audio (waits for results)
  h-ear capture [--duration 15]         Capture from RTSP camera and classify
  h-ear jobs [--limit 5]                List recent jobs

Environment:
  HEAR_API_KEY      H-ear API key (required)
  HEAR_ENV          dev | staging | prod (default: prod)
  LISTEN_RTSP_URL   RTSP camera URL (for capture command)`);
        return;
    }

    const { client } = createSkill();

    switch (command) {
        case 'health': {
            console.log(await healthCommand(client));
            break;
        }
        case 'sounds': {
            const search = args[1] && !args[1].startsWith('-') ? args[1] : undefined;
            const limit = parseInt(getFlag('--limit') ?? '20', 10);
            console.log(await soundsCommand(client, search, { limit }));
            break;
        }
        case 'usage': {
            console.log(await usageCommand(client));
            break;
        }
        case 'classify': {
            const target = args[1];
            if (!target) { console.error('Error: h-ear classify <file-or-url>'); process.exit(1); }

            if (target.startsWith('http://') || target.startsWith('https://')) {
                // URL mode — use existing sync command
                console.log(await classifySyncCommand(client, target, undefined, (msg) => console.error(`  ${msg}`)));
            } else {
                // File mode — read and upload
                if (!existsSync(target)) { console.error(`Error: file not found: ${target}`); process.exit(1); }
                const buffer = readFileSync(target);
                const fileName = target.split(/[/\\]/).pop() ?? 'audio.wav';
                console.error(`  Uploading ${fileName} (${(buffer.length / 1024).toFixed(0)} KB)...`);
                const accepted = await client.submitClassifyFile(buffer, fileName, { threshold: 0.3 });
                console.error(`  Job ${accepted.requestId} queued, polling...`);
                const result = await client.pollJob(accepted.requestId, (msg) => console.error(`  ${msg}`));
                console.log(formatClassifyResult(result));
            }
            break;
        }
        case 'listen':
        case 'capture': {
            const rtspUrl = getFlag('--rtsp') ?? process.env.LISTEN_RTSP_URL;
            if (!rtspUrl) {
                console.error('Error: RTSP URL required. Pass --rtsp <url> or set LISTEN_RTSP_URL');
                process.exit(1);
            }
            const duration = parseInt(getFlag('--duration') ?? '15', 10);
            const classifyAfter = !hasFlag('--no-classify');

            console.error(`  Capturing ${duration}s audio from ${rtspUrl}...`);
            const { buffer, fileName } = captureAudio(rtspUrl, duration);
            console.error(`  Captured ${(buffer.length / 1024).toFixed(0)} KB`);

            if (classifyAfter) {
                console.error(`  Uploading ${fileName}...`);
                const accepted = await client.submitClassifyFile(buffer, fileName, { threshold: 0.3 });
                console.error(`  Job ${accepted.requestId} queued, polling...`);
                const result = await client.pollJob(accepted.requestId, (msg) => console.error(`  ${msg}`));
                console.log(formatClassifyResult(result));
            } else {
                console.log(`Captured: ${fileName} (${(buffer.length / 1024).toFixed(0)} KB)`);
            }
            break;
        }
        case 'jobs': {
            const limit = parseInt(getFlag('--limit') ?? '5', 10);
            console.log(await jobsCommand(client, { limit }));
            break;
        }
        default: {
            console.error(`Unknown command: ${command}. Run 'h-ear help' for usage.`);
            process.exit(1);
        }
    }
}

main().catch((err: Error) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
});
