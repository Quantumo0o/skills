import fs from 'node:fs';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import {
  CHROME_CANDIDATES_FULL,
  CdpConnection,
  copyImageToClipboard,
  findExistingChromeDebugPort,
  getDefaultProfileDir,
  gracefulKillChrome,
  launchChrome,
  openPageSession,
  pasteFromClipboard,
  sleep,
  waitForXSessionPersistence,
  waitForChromeDebugPort,
} from './x-utils.js';

const X_COMPOSE_URL = 'https://x.com/compose/post';

async function waitForUserPostOrClose(
  cdp: CdpConnection,
  sessionId: string,
  maxWaitMs: number,
): Promise<'posted' | 'browser_closed' | 'timeout'> {
  const t0 = Date.now();
  while (Date.now() - t0 < maxWaitMs) {
    await sleep(3000);
    try {
      const state = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(function() {
          const url = location.href;
          if (!url.includes('x.com')) return 'navigated';
          // Compose dialog gone = post was sent
          const editor = document.querySelector('[data-testid="tweetTextarea_0"]');
          const composeDialog = document.querySelector('[data-testid="tweetButton"]');
          if (!editor && !composeDialog) return 'posted';
          // Toast/success indicator
          const toasts = document.querySelectorAll('[data-testid="toast"], [role="alert"]');
          for (const t of toasts) {
            const txt = t.textContent || '';
            if (txt.includes('post') || txt.includes('sent') || txt.includes('Your post')) return 'posted';
          }
          return 'editing';
        })()`,
        returnByValue: true,
      }, { sessionId });
      const val = state.result.value;
      if (val === 'posted' || val === 'navigated') return 'posted';
    } catch {
      return 'browser_closed';
    }
  }
  return 'timeout';
}

interface XBrowserOptions {
  text?: string;
  images?: string[];
  submit?: boolean;
  timeoutMs?: number;
  profileDir?: string;
  chromePath?: string;
}

export async function postToX(options: XBrowserOptions): Promise<void> {
  const { text, images = [], submit = false, timeoutMs = 120_000, profileDir = getDefaultProfileDir() } = options;

  await mkdir(profileDir, { recursive: true });

  const existingPort = await findExistingChromeDebugPort(profileDir);
  const reusing = existingPort !== null;
  let port = existingPort ?? 0;
  let chrome: Awaited<ReturnType<typeof launchChrome>>['chrome'] | null = null;
  if (!reusing) {
    const launched = await launchChrome(X_COMPOSE_URL, profileDir, CHROME_CANDIDATES_FULL, options.chromePath);
    port = launched.port;
    chrome = launched.chrome;
  }

  if (reusing) console.log(`[x-browser] Reusing existing Chrome on port ${port}`);
  else console.log(`[x-browser] Launching Chrome (profile: ${profileDir})`);

  let cdp: CdpConnection | null = null;
  let sessionId: string | null = null;
  let loggedInDuringRun = false;

  try {
    const wsUrl = await waitForChromeDebugPort(port, 30_000, { includeLastError: true });
    cdp = await CdpConnection.connect(wsUrl, 30_000, { defaultTimeoutMs: 15_000 });

    const page = await openPageSession({
      cdp,
      reusing,
      url: X_COMPOSE_URL,
      matchTarget: (target) => target.type === 'page' && target.url.includes('x.com'),
      enablePage: true,
      enableRuntime: true,
      enableNetwork: true,
    });
    const activeSessionId = page.sessionId;
    sessionId = activeSessionId;
    await cdp.send('Input.setIgnoreInputEvents', { ignore: false }, { sessionId: activeSessionId });

    console.log('[x-browser] Waiting for X editor...');
    await sleep(3000);

    const waitForEditor = async (): Promise<boolean> => {
      const start = Date.now();
      while (Date.now() - start < timeoutMs) {
        const result = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
          expression: `!!document.querySelector('[data-testid="tweetTextarea_0"]')`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (result.result.value) return true;
        await sleep(1000);
      }
      return false;
    };

    const editorFound = await waitForEditor();
    if (!editorFound) {
      console.log('[x-browser] Editor not found. Please log in to X in the browser window.');
      console.log('[x-browser] Waiting for login...');
      const loggedIn = await waitForEditor();
      if (!loggedIn) throw new Error('Timed out waiting for X editor. Please log in first.');
      loggedInDuringRun = true;
    }

    // ── PHASE 1: Upload images FIRST (before typing text) ──
    // DOM.setFileInputFiles can leak file paths into the editor as text on some X/React versions.
    // By uploading images first and clearing leaked paths, we ensure clean text input later.
    for (const imagePath of images) {
      if (!fs.existsSync(imagePath)) {
        console.warn(`[x-browser] Image not found: ${imagePath}`);
        continue;
      }

      const absPath = path.isAbsolute(imagePath) ? imagePath : path.resolve(process.cwd(), imagePath);
      console.log(`[x-browser] Uploading image: ${absPath}`);

      const imgCountBefore = await cdp.send<{ result: { value: number } }>('Runtime.evaluate', {
        expression: `document.querySelectorAll('img[src^="blob:"]').length`,
        returnByValue: true,
      }, { sessionId: activeSessionId });
      const expectedImgCount = imgCountBefore.result.value + 1;
      let imgUploadOk = false;

      // Strategy 1 (preferred): DOM.setFileInputFiles — no clipboard, no anti-automation risk
      console.log('[x-browser] Trying DOM.setFileInputFiles (preferred)...');
      try {
        const fileInputResult = await cdp!.send<{ result: { objectId?: string; subtype?: string } }>('Runtime.evaluate', {
          expression: `document.querySelector('input[type="file"][data-testid="fileInput"], input[type="file"][accept*="image"], input[type="file"]')`,
          returnByValue: false,
        }, { sessionId: activeSessionId });

        if (fileInputResult.result.objectId) {
          await cdp!.send('DOM.setFileInputFiles', {
            files: [absPath],
            objectId: fileInputResult.result.objectId,
          }, { sessionId: activeSessionId });
          console.log('[x-browser] Files set via DOM.setFileInputFiles');

          const domWaitStart = Date.now();
          while (Date.now() - domWaitStart < 20_000) {
            const r = await cdp!.send<{ result: { value: number } }>('Runtime.evaluate', {
              expression: `document.querySelectorAll('img[src^="blob:"]').length`,
              returnByValue: true,
            }, { sessionId: activeSessionId });
            if (r.result.value >= expectedImgCount) {
              imgUploadOk = true;
              console.log('[x-browser] Image upload verified (DOM.setFileInputFiles)');
              break;
            }
            await sleep(1000);
          }
        } else {
          console.warn('[x-browser] No file input element found');
        }
      } catch (domErr) {
        console.warn(`[x-browser] DOM.setFileInputFiles failed: ${domErr instanceof Error ? domErr.message : String(domErr)}`);
      }

      // Strategy 2 (fallback): Clipboard paste
      if (!imgUploadOk) {
        console.log('[x-browser] Falling back to clipboard paste...');
        if (copyImageToClipboard(absPath)) {
          await sleep(500);
          await cdp!.send('Runtime.evaluate', {
            expression: `document.querySelector('[data-testid="tweetTextarea_0"]')?.focus()`,
          }, { sessionId: activeSessionId });
          await sleep(200);

          const pasteSuccess = pasteFromClipboard('Google Chrome', 5, 500);
          if (!pasteSuccess) {
            const modifiers = process.platform === 'darwin' ? 4 : 2;
            await cdp!.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'v', code: 'KeyV', modifiers, windowsVirtualKeyCode: 86 }, { sessionId: activeSessionId });
            await cdp!.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'v', code: 'KeyV', modifiers, windowsVirtualKeyCode: 86 }, { sessionId: activeSessionId });
          }

          const pasteWaitStart = Date.now();
          while (Date.now() - pasteWaitStart < 15_000) {
            const r = await cdp!.send<{ result: { value: number } }>('Runtime.evaluate', {
              expression: `document.querySelectorAll('img[src^="blob:"]').length`,
              returnByValue: true,
            }, { sessionId: activeSessionId });
            if (r.result.value >= expectedImgCount) {
              imgUploadOk = true;
              console.log('[x-browser] Image upload verified (clipboard paste)');
              break;
            }
            await sleep(1000);
          }
        } else {
          console.warn(`[x-browser] Failed to copy image to clipboard: ${absPath}`);
        }
      }

      if (!imgUploadOk) {
        console.warn('[x-browser] ⚠️ Image upload not detected after all strategies');
        continue;
      }

      // ── Clean up leaked file paths from editor ──
      // DOM.setFileInputFiles on X's React app can leak the file path as text into the editor.
      // Detect and remove it before typing the actual tweet text.
      console.log('[x-browser] Checking for leaked file path in editor...');
      const editorText = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '')`,
        returnByValue: true,
      }, { sessionId: activeSessionId });
      const leaked = editorText.result.value;
      if (leaked && (leaked.includes(absPath) || leaked.includes(path.basename(absPath)) || leaked.match(/\.(png|jpg|jpeg|gif|webp)$/i))) {
        console.log(`[x-browser] Leaked path detected: "${leaked.substring(0, 80)}...". Clearing editor.`);
        await cdp!.send('Runtime.evaluate', {
          expression: `(function() {
            var el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (!el) return;
            el.focus();
            document.execCommand('selectAll');
            document.execCommand('delete');
          })()`,
        }, { sessionId: activeSessionId });
        await sleep(300);
      }

      // ── Wait for X to finish processing the image ──
      console.log('[x-browser] Waiting for X to process image...');
      const processingStart = Date.now();
      let imageReady = false;
      while (Date.now() - processingStart < 30_000) {
        const status = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
          expression: `(function() {
            var btn = document.querySelector('[data-testid="tweetButton"]');
            if (!btn) return 'no_btn';
            if (btn.getAttribute('aria-disabled') === 'true' || btn.disabled) return 'disabled';
            var progress = document.querySelector('[role="progressbar"]');
            if (progress) return 'processing';
            return 'ready';
          })()`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (status.result.value === 'ready') {
          imageReady = true;
          console.log('[x-browser] Image processing complete, Post button ready');
          break;
        }
        if (status.result.value === 'no_btn') {
          console.warn('[x-browser] Post button not found');
          break;
        }
        await sleep(1000);
      }
      if (!imageReady) {
        console.warn('[x-browser] ⚠️ Image processing did not complete within 30s');
      }
    }

    // ── PHASE 2: Type text AFTER all images are uploaded and editor is clean ──
    if (text) {
      // Final cleanup: ensure editor is empty before typing (in case any residual content)
      if (images.length > 0) {
        const residual = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
          expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '')`,
          returnByValue: true,
        }, { sessionId: activeSessionId });
        if (residual.result.value.trim()) {
          console.log(`[x-browser] Clearing residual editor text: "${residual.result.value.substring(0, 60)}..."`);
          await cdp!.send('Runtime.evaluate', {
            expression: `(function() {
              var el = document.querySelector('[data-testid="tweetTextarea_0"]');
              if (!el) return;
              el.focus();
              document.execCommand('selectAll');
              document.execCommand('delete');
            })()`,
          }, { sessionId: activeSessionId });
          await sleep(300);
        }
      }

      console.log('[x-browser] Typing text...');
      await cdp.send('Runtime.evaluate', {
        expression: `
          const editor = document.querySelector('[data-testid="tweetTextarea_0"]');
          if (editor) {
            editor.focus();
            document.execCommand('insertText', false, ${JSON.stringify(text)});
          }
        `,
      }, { sessionId: activeSessionId });
      await sleep(500);

      // Verify text was typed correctly (not containing file paths)
      const typedText = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(document.querySelector('[data-testid="tweetTextarea_0"]')?.textContent || '')`,
        returnByValue: true,
      }, { sessionId: activeSessionId });
      const typed = typedText.result.value;
      if (typed.includes('.png') || typed.includes('.jpg') || typed.includes('.jpeg') || typed.includes('/media/') || typed.includes('\\media\\')) {
        console.warn(`[x-browser] ⚠️ Editor text may contain file paths: "${typed.substring(0, 100)}..."`);
      } else {
        console.log(`[x-browser] Text verified (${typed.length} chars)`);
      }
    }

    if (submit) {
      // Verify Post button is clickable before clicking
      const btnCheck = await cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
        expression: `(function() {
          var btn = document.querySelector('[data-testid="tweetButton"]');
          if (!btn) return 'not_found';
          if (btn.getAttribute('aria-disabled') === 'true' || btn.disabled) return 'disabled';
          return 'ok';
        })()`,
        returnByValue: true,
      }, { sessionId: activeSessionId });

      if (btnCheck.result.value === 'disabled') {
        console.warn('[x-browser] ⚠️ Post button is disabled (image may still be processing). Waiting up to 15s...');
        const disabledWait = Date.now();
        while (Date.now() - disabledWait < 15_000) {
          await sleep(1000);
          const r = await cdp!.send<{ result: { value: boolean } }>('Runtime.evaluate', {
            expression: `!(document.querySelector('[data-testid="tweetButton"]')?.getAttribute('aria-disabled') === 'true')`,
            returnByValue: true,
          }, { sessionId: activeSessionId });
          if (r.result.value) break;
        }
      }

      console.log('[x-browser] Clicking Post button...');
      await cdp.send('Runtime.evaluate', {
        expression: `document.querySelector('[data-testid="tweetButton"]')?.click()`,
      }, { sessionId: activeSessionId });

      // Verify the compose dialog disappears (= post was actually sent)
      console.log('[x-browser] Verifying post was published...');
      let postVerified = false;
      const verifyStart = Date.now();
      while (Date.now() - verifyStart < 15_000) {
        await sleep(1500);
        try {
          const state = await cdp!.send<{ result: { value: string } }>('Runtime.evaluate', {
            expression: `(function() {
              var editor = document.querySelector('[data-testid="tweetTextarea_0"]');
              var btn = document.querySelector('[data-testid="tweetButton"]');
              if (!editor && !btn) return 'posted';
              var toasts = document.querySelectorAll('[data-testid="toast"], [role="alert"]');
              for (var i = 0; i < toasts.length; i++) {
                var txt = toasts[i].textContent || '';
                if (txt.includes('post') || txt.includes('sent') || txt.includes('Your post')) return 'posted';
              }
              return 'still_editing';
            })()`,
            returnByValue: true,
          }, { sessionId: activeSessionId });
          if (state.result.value === 'posted') {
            postVerified = true;
            break;
          }
        } catch {
          // CDP disconnected = browser closed or navigated away
          postVerified = true;
          break;
        }
      }

      if (postVerified) {
        console.log('[x-browser] ✅ Post published successfully!');
      } else {
        console.warn('[x-browser] ⚠️ Post button was clicked but compose dialog is still open.');
        console.warn('[x-browser] The post may have been blocked by X (captcha, rate limit, or anti-automation).');
        console.warn('[x-browser] Please check the browser window for any prompts.');
      }
    } else {
      console.log('[x-browser] ✅ Post composed. Browser stays open for your review.');
      console.log('[x-browser] 👀 Waiting for you to review and click the post button...');
      console.log('[x-browser] (Script will auto-detect when you post or close the browser)');

      const waitResult = await waitForUserPostOrClose(cdp, activeSessionId, timeoutMs);
      switch (waitResult) {
        case 'posted':
          console.log('[x-browser] ✅ Post published successfully!');
          break;
        case 'browser_closed':
          console.log('[x-browser] 🔒 Browser was closed. Post was NOT published.');
          break;
        case 'timeout':
          console.log(`[x-browser] ⏰ Wait timeout (${Math.round(timeoutMs / 1000)}s). Browser left open — post manually if needed.`);
          break;
      }
    }
  } finally {
    let leaveChromeOpen = !submit;
    if (chrome && submit && loggedInDuringRun && cdp && sessionId) {
      console.log('[x-browser] Waiting for X session cookies to persist...');
      const sessionReady = await waitForXSessionPersistence({ cdp, sessionId });
      if (!sessionReady) {
        console.warn('[x-browser] X session cookies not observed yet. Leaving Chrome open so login can finish persisting.');
        leaveChromeOpen = true;
      }
    }

    if (cdp) {
      cdp.close();
    }
    if (chrome) {
      if (leaveChromeOpen) {
        chrome.unref();
      } else {
        await gracefulKillChrome(chrome, port);
      }
    }
  }
}

function printUsage(): never {
  console.log(`Post to X (Twitter) using real Chrome browser

Usage:
  npx -y bun x-browser.ts [options] [text]

Options:
  --image <path>   Add image (can be repeated, max 4)
  --submit         Actually post (default: preview only)
  --profile <dir>  Chrome profile directory
  --help           Show this help

Examples:
  npx -y bun x-browser.ts "Hello from CLI!"
  npx -y bun x-browser.ts "Check this out" --image ./screenshot.png
  npx -y bun x-browser.ts "Post it!" --image a.png --image b.png --submit
`);
  process.exit(0);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) printUsage();

  const images: string[] = [];
  let submit = false;
  let profileDir: string | undefined;
  const textParts: string[] = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!;
    if (arg === '--image' && args[i + 1]) {
      images.push(args[++i]!);
    } else if (arg === '--submit') {
      submit = true;
    } else if (arg === '--profile' && args[i + 1]) {
      profileDir = args[++i];
    } else if (!arg.startsWith('-')) {
      textParts.push(arg);
    }
  }

  const text = textParts.join(' ').trim() || undefined;

  if (!text && images.length === 0) {
    console.error('Error: Provide text or at least one image.');
    process.exit(1);
  }

  await postToX({ text, images, submit, profileDir });
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
