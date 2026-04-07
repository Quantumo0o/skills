const https = require('node:https');
const { Readable } = require('stream');
const { listTextFiles } = require('C:/npm-global/node_modules/clawhub/dist/skills.js');

const ROOT = 'C:/Users/Administrator/Desktop/singularity';
const TOKEN = 'clh_zx-WHXE8PlycqfNv5Z3eW47S5MkO5AeREn74ISAZgjs';
const SLUG = 'singularity-openclaw';
const VERSION = '2.5.0';
const DISPLAY_NAME = 'Singularity (OpenClaw)';
const CHANGELOG = 'v2.5.0: 整合服务器文档 v2.2.0，新增快速开始/evolver/心跳自动化';

async function postMultipart(files) {
  const boundary = '----FormBoundary' + Math.random().toString(36).slice(2);
  
  // Build multipart manually
  const parts = [];
  
  // Payload
  const payload = JSON.stringify({ slug: SLUG, displayName: DISPLAY_NAME, version: VERSION, changelog: CHANGELOG, tags: [] });
  parts.push(Buffer.from(
    `--${boundary}\r\n` +
    `Content-Disposition: form-data; name="payload"\r\n` +
    `Content-Type: application/json\r\n\r\n` +
    payload + '\r\n'
  ));
  
  // Files
  for (const file of files) {
    const header = 
      `--${boundary}\r\n` +
      `Content-Disposition: form-data; name="files"; filename="${file.relPath}"\r\n` +
      `Content-Type: ${file.contentType || 'text/plain'}\r\n\r\n`;
    const buf = Buffer.isBuffer(file.bytes) ? file.bytes : Buffer.from(file.bytes);
    parts.push(Buffer.concat([Buffer.from(header), buf, Buffer.from('\r\n')]));
  }
  
  parts.push(Buffer.from(`--${boundary}--\r\n`));
  
  const body = Buffer.concat(parts);
  
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'clawhub.ai',
      port: 443,
      path: '/api/v1/skills',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
      }
    };
    
    console.log(`POSTing ${body.length} bytes to /api/v1/skills...`);
    const req = https.request(options, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        console.log('HTTP Status:', res.statusCode);
        try {
          const parsed = JSON.parse(d);
          console.log('Response:', JSON.stringify(parsed).slice(0, 500));
          resolve(parsed);
        } catch(e) {
          console.log('Raw response:', d.slice(0, 300));
          resolve(d);
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

(async () => {
  console.log('Reading files...');
  const files = await listTextFiles(ROOT);
  console.log(`Found ${files.length} files`);
  
  const result = await postMultipart(files);
  
  if (result && (result.ok || result.skillId)) {
    console.log('✅ PUBLISHED SUCCESSFULLY!');
    console.log('Version ID:', result.versionId || result.id);
  } else {
    console.log('❌ FAILED');
  }
})().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
