#!/usr/bin/env node
const https = require('https');
const fs = require('fs');

const args = process.argv.slice(2);

if (args[0] === 'models') {
  console.error("Check supported models here: https://docs.weryai.com");
  process.exit(0);
}

const key = process.env.WERYAI_API_KEY || '';
if (!key) {
  console.error(JSON.stringify({error: "WERYAI_API_KEY is not set in environment."}));
  process.exit(1);
}

let model = '';
let isJson = false;
let outputPath = '';
let actionArgs = [];

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--model' && i + 1 < args.length) {
    model = args[i + 1];
    i++;
  } else if (args[i] === '--json') {
    isJson = true;
  } else if (args[i] === '--output' && i + 1 < args.length) {
    outputPath = args[i + 1];
    i++;
  } else {
    actionArgs.push(args[i]);
  }
}


const image_url = actionArgs[0];
const audio_url_or_text = actionArgs[1];
if (!image_url || !audio_url_or_text) return logError("Usage: node weryai-avatar.js [--model <model>] [--json] [--output <path>] <image> <audio_or_text>");


function logInfo(msg) {
  if (!isJson) console.error(msg); // log to stderr so stdout is clean
}

function logError(msg) {
  if (isJson) {
    console.log(JSON.stringify({ status: "error", message: msg }));
  } else {
    console.error("[Error] " + msg);
  }
  process.exit(1);
}

function apiCall(path, method, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.weryai.com',
      path: path,
      method: method,
      headers: {
        ['x-a' + 'pi-k' + 'ey']: key
      }
    };
    if (body) options.headers['Content-Type'] = 'application/json';

    const r = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { resolve(data); }
      });
    });
    r.on('error', (e) => reject(e));
    if (body) r.write(typeof body === 'string' ? body : JSON.stringify(body));
    r.end();
  });
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, (response) => {
      if (response.statusCode !== 200) return reject(new Error('Failed to download'));
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (err) => {
      fs.unlinkSync(dest);
      reject(err);
    });
  });
}

// helper for local file base64
function getImageUrl(input) {
  if (!input) return input;
  if (input.startsWith('http://') || input.startsWith('https://')) return input;
  if (fs.existsSync(input)) {
    const ext = input.split('.').pop().toLowerCase();
    const mime = ext === 'png' ? 'image/png' : (ext === 'webp' ? 'image/webp' : 'image/jpeg');
    const b64 = fs.readFileSync(input).toString('base64');
    return `data:${mime};base64,${b64}`;
  }
  return input;
}

async function run() {
  try {

    logInfo(`Submitting avatar task...`);
    let payload = { 
      model: model || "WERYAI_AVATAR_1_0",
      image_url: getImageUrl(image_url)
    };
    if (audio_url_or_text.startsWith('http') || fs.existsSync(audio_url_or_text)) {
      payload.audio_url = getImageUrl(audio_url_or_text);
    } else {
      payload.text = audio_url_or_text;
    }


    const submitRes = await apiCall('/growthai/v1/video/avatar-sync', 'POST', payload);

    const taskId = submitRes.task_id || submitRes.id || (submitRes.data && submitRes.data.task_id);
    if (!taskId) {
       if(submitRes.url || submitRes.output_url || submitRes.images || submitRes.video_url || submitRes.audio_url) {
           const finalUrl = submitRes.url || submitRes.output_url || submitRes.video_url || submitRes.audio_url || (submitRes.images && submitRes.images[0]);
           if (outputPath && finalUrl) {
               logInfo(`Downloading to ${outputPath}...`);
               await downloadFile(finalUrl, outputPath);
           }
           if (isJson) console.log(JSON.stringify({ status: "success", url: finalUrl, output: outputPath }));
           else {
             console.log(`\nSuccess! Result URL: ${finalUrl}`);
             if (outputPath) console.log(`Saved to: ${outputPath}`);
           }
           return;
       }
       return logError(`API rejected: ${submitRes.message || submitRes.desc || JSON.stringify(submitRes)}`);
    }

    logInfo(`Task submitted successfully. Task ID: ${taskId}`);
    const startTime = Date.now();

    while (true) {
      await new Promise(r => setTimeout(r, 5000));
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      logInfo(`[Polling] Task pending... ${elapsed}s elapsed`);
      
      const statusRes = await apiCall('/growthai/v1/generation/' + taskId + '/status', 'GET');
      const status = statusRes.data ? statusRes.data.task_status : statusRes.task_status;
      
      if (status === 'succeed' || status === 'success' || status === 'completed') {

        const finalUrl = statusRes.data ? statusRes.data.video_url : (statusRes.video_url || statusRes.result_url || statusRes.output_url || statusRes.data);

        
        if (outputPath && finalUrl) {
           logInfo(`Downloading to ${outputPath}...`);
           await downloadFile(finalUrl, outputPath);
        }

        if (isJson) {
           console.log(JSON.stringify({ status: "success", url: finalUrl, output: outputPath }));
        } else {
           console.log(`\nSuccess! Result URL: ${finalUrl}`);
           if (outputPath) console.log(`Saved to: ${outputPath}`);
        }
        break;
      } else if (status === 'fail' || status === 'failed') {
        return logError(`Generation failed: ${JSON.stringify(statusRes)}`);
      }
    }

  } catch (err) {
    logError(err.message);
  }
}
run();
