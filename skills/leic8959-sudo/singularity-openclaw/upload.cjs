const https = require('https');
const fs = require('fs');

const TOKEN = 'clh_zx-WHXE8PlycqfNv5Z3eW47S5MkO5AeREn74ISAZgjs';
const SLUG = 'singularity-openclaw';
const VERSION = '2.5.0';
const CHANGELOG = 'v2.5.0: 整合服务器文档 v2.2.0，新增快速开始/evolver/心跳自动化';

// Step 1: Get upload URL from clawhub.ai
function step1() {
  return new Promise((resolve) => {
    const body = JSON.stringify({ slug: SLUG, version: VERSION, changelog: CHANGELOG, name: 'Singularity (OpenClaw)' });
    const req = https.request({
      hostname: 'clawhub.ai', port: 443, path: '/api/cli/upload-url', method: 'POST',
      headers: { 'Authorization': `Bearer ${TOKEN}`, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
    }, (res) => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => {
        const r = JSON.parse(d);
        console.log('Upload URL received:', r.uploadUrl.slice(0, 80) + '...');
        resolve(r.uploadUrl);
      });
    });
    req.on('error', e => console.error(e.message));
    req.write(body); req.end();
  });
}

// Step 2: Upload tarball
function step2(uploadUrl) {
  return new Promise((resolve) => {
    const tarBuf = fs.readFileSync('/tmp/sing-final.tar');
    console.log('Uploading', tarBuf.length, 'bytes...');
    const url = new URL(uploadUrl);
    const req = https.request({
      hostname: url.hostname, port: 443, path: url.pathname + url.search, method: 'POST',
      headers: { 'Content-Type': 'application/octet-stream', 'Content-Length': tarBuf.length }
    }, (res) => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => {
        console.log('Upload status:', res.statusCode, 'Body:', d.slice(0, 200));
        resolve({ status: res.statusCode, body: d });
      });
    });
    req.on('error', e => console.error(e.message));
    req.write(tarBuf); req.end();
  });
}

step1().then(step2).then(() => console.log('DONE'));
