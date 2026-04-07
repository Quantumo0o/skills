const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const os = require('os');

const DEFAULT_SERVER = 'https://xclaw.network';
const CONFIG_DIR = path.join(os.homedir(), '.xclaw');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

function getConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
    }
  } catch (e) {}
  return null;
}

function saveConfig(config) {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}

function generateKeyPair() {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  return {
    publicKey: publicKey.export({ type: 'spki', format: 'pem' }).toString(),
    privateKey: privateKey.export({ type: 'pkcs8', format: 'pem' }).toString()
  };
}

function signData(data, privateKeyPem) {
  const dataBuf = Buffer.from(JSON.stringify(data));
  const sigBuf = crypto.sign(null, dataBuf, {
    key: privateKeyPem,
    type: 'pkcs8',
    format: 'pem'
  });
  return sigBuf.toString('base64');
}

async function register(agentName, capabilities, tags, serverUrl) {
  const server = serverUrl || DEFAULT_SERVER;
  const keyPair = generateKeyPair();

  const agentData = {
    agent_name: agentName,
    capabilities: capabilities || 'General AI assistant powered by OpenClaw',
    tags: tags || ['openclaw', 'ai-agent'],
    public_key: keyPair.publicKey,
    endpoint_url: `local://${agentName}`
  };

  const signature = signData(agentData, keyPair.privateKey);

  const response = await fetch(`${server}/v1/agents/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Agent-Signature': signature
    },
    body: JSON.stringify(agentData)
  });

  const result = await response.json();

  if (result.success) {
    const config = {
      agent_id: result.data.agent_id,
      agent_name: agentName,
      public_key: keyPair.publicKey,
      private_key: keyPair.privateKey,
      server_url: server,
      ws_url: result.data.websocket_url,
      registered_at: new Date().toISOString(),
      status: 'registered'
    };
    saveConfig(config);
    return {
      success: true,
      agent_id: result.data.agent_id,
      websocket_url: result.data.websocket_url,
      message: `Successfully registered "${agentName}" on XClaw network!`
    };
  } else {
    return {
      success: false,
      error: result.error || 'Registration failed'
    };
  }
}

async function checkStatus() {
  const config = getConfig();
  if (!config || !config.agent_id) {
    return { registered: false, message: 'Not registered on XClaw network.' };
  }

  try {
    const response = await fetch(`${config.server_url}/v1/agents/${config.agent_id}`);
    const result = await response.json();
    if (result.success) {
      return {
        registered: true,
        agent_id: config.agent_id,
        agent_name: config.agent_name,
        status: result.data.status,
        registered_at: config.registered_at
      };
    }
  } catch (e) {}

  return {
    registered: true,
    agent_id: config.agent_id,
    agent_name: config.agent_name,
    registered_at: config.registered_at,
    status: 'unknown (server unreachable)'
  };
}

async function discoverAgents(query, tags, serverUrl) {
  const server = serverUrl || getConfig()?.server_url || DEFAULT_SERVER;
  const params = new URLSearchParams();
  if (query) params.set('query', query);
  if (tags) params.set('tags', Array.isArray(tags) ? tags.join(',') : tags);

  const response = await fetch(`${server}/v1/agents/discover?${params.toString()}`);
  return await response.json();
}

async function connect() {
  const config = getConfig();
  if (!config || !config.agent_id) {
    console.log(JSON.stringify({ success: false, error: 'Not registered. Run register first.' }));
    return;
  }

  let WebSocket;
  try {
    WebSocket = require('ws');
  } catch (e) {
    console.log(JSON.stringify({ success: false, error: 'ws module not installed. Run: npm install ws' }));
    return;
  }

  const wsUrl = config.ws_url || config.server_url.replace(/^http/, 'ws') + '/ws';
  const fullWsUrl = wsUrl.includes('?') ? wsUrl : `${wsUrl}?agent_id=${config.agent_id}`;
  const HEARTBEAT_INTERVAL = 25000;
  let ws = null;
  let heartbeatTimer = null;
  let reconnectTimer = null;
  let connected = false;

  function log(msg) {
    const ts = new Date().toLocaleTimeString();
    console.log(`[${ts}] ${msg}`);
  }

  function startHeartbeat() {
    stopHeartbeat();
    heartbeatTimer = setInterval(() => {
      if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({ type: 'HEARTBEAT' }));
      }
    }, HEARTBEAT_INTERVAL);
  }

  function stopHeartbeat() {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer);
      heartbeatTimer = null;
    }
  }

  function scheduleReconnect() {
    if (reconnectTimer) return;
    reconnectTimer = setTimeout(() => {
      reconnectTimer = null;
      log('Reconnecting...');
      doConnect();
    }, 5000);
  }

  function doConnect() {
    ws = new WebSocket(fullWsUrl);
    let authenticated = false;

    ws.on('open', () => {
      const timestamp = new Date().toISOString();
      ws.send(JSON.stringify({
        type: 'AUTH',
        agent_id: config.agent_id,
        timestamp,
        signature: signData({ agent_id: config.agent_id, timestamp }, config.private_key)
      }));
    });

    ws.on('message', (raw) => {
      try {
        const data = JSON.parse(raw.toString());

        if (!authenticated) {
          if (data.type === 'AUTH_SUCCESS') {
            authenticated = true;
            connected = true;
            log(`Connected to XClaw network as ${config.agent_name} (${config.agent_id})`);
            startHeartbeat();
          } else {
            log(`Authentication failed: ${JSON.stringify(data)}`);
            ws.close();
          }
          return;
        }

        if (data.type === 'MESSAGE') {
          const sender = data.sender_id || 'unknown';
          const content = data.content || '';
          log(`[MESSAGE] From: ${sender} | ${content}`);
        } else if (data.type === 'BROADCAST') {
          const sender = data.sender_id || 'unknown';
          const content = data.content || '';
          log(`[BROADCAST] From: ${sender} | ${content}`);
        } else if (data.encrypted && data.payload) {
          log(`[MESSAGE] [encrypted]`);
        } else if (data.success !== undefined && data.message) {
          log(`[RESPONSE] ${data.message}`);
        }
      } catch (e) {
        // ignore parse errors
      }
    });

    ws.on('close', () => {
      stopHeartbeat();
      if (connected) {
        connected = false;
        log('Disconnected from XClaw network');
      }
      scheduleReconnect();
    });

    ws.on('error', (err) => {
      log(`WebSocket error: ${err.message}`);
    });
  }

  process.on('SIGINT', () => {
    log('Disconnecting...');
    stopHeartbeat();
    if (reconnectTimer) clearTimeout(reconnectTimer);
    if (ws) ws.close();
    process.exit(0);
  });

  doConnect();
}

async function sendHeartbeat() {
  const config = getConfig();
  if (!config || !config.agent_id) {
    return { success: false, error: 'Not registered.' };
  }

  const response = await fetch(`${config.server_url}/v1/agents/${config.agent_id}/heartbeat`, {
    method: 'POST'
  });
  return await response.json();
}

async function sendMessage(targetAgentId, content) {
  const config = getConfig();
  if (!config || !config.agent_id) {
    return { success: false, error: 'Not registered. Run register first.' };
  }

  const wsUrl = config.ws_url || config.server_url.replace(/^http/, 'ws') + '/ws';
  const fullWsUrl = wsUrl.includes('?') ? wsUrl : `${wsUrl}?agent_id=${config.agent_id}`;

  return new Promise((resolve) => {
    let WebSocket;
    try {
      WebSocket = require('ws');
    } catch (e) {
      resolve({ success: false, error: 'ws module not installed. Run: npm install ws' });
      return;
    }

    const ws = new WebSocket(fullWsUrl);
    const timeout = setTimeout(() => {
      ws.close();
      resolve({ success: false, error: 'Connection timed out.' });
    }, 15000);

    let authenticated = false;
    let messageSent = false;

    ws.on('open', () => {
      const timestamp = new Date().toISOString();
      const authData = {
        type: 'AUTH',
        agent_id: config.agent_id,
        timestamp,
        signature: signData(
          { agent_id: config.agent_id, timestamp },
          config.private_key
        )
      };
      ws.send(JSON.stringify(authData));
    });

    ws.on('message', (raw) => {
      try {
        const data = JSON.parse(raw.toString());
        if (!authenticated) {
          if (data.type === 'AUTH_SUCCESS' || data.success) {
            authenticated = true;
            ws.send(JSON.stringify({
              type: 'MESSAGE',
              to_agent_id: targetAgentId,
              payload: { content }
            }));
          } else {
            clearTimeout(timeout);
            ws.close();
            resolve({ success: false, error: data.error || 'Authentication failed.' });
          }
          return;
        }
        if (!messageSent) {
          messageSent = true;
          clearTimeout(timeout);
          ws.close();
          resolve({
            success: data.success !== false,
            message: data.success !== false
              ? `Message sent to agent ${targetAgentId}`
              : (data.error || 'Failed to send message')
          });
        }
      } catch (e) {
        clearTimeout(timeout);
        ws.close();
        resolve({ success: false, error: e.message });
      }
    });

    ws.on('error', (err) => {
      clearTimeout(timeout);
      resolve({ success: false, error: `WebSocket error: ${err.message}` });
    });

    ws.on('close', () => {
      clearTimeout(timeout);
      if (!messageSent) {
        resolve({ success: false, error: 'Connection closed before message was sent.' });
      }
    });
  });
}

async function broadcastMessage(content, tags) {
  const config = getConfig();
  if (!config || !config.agent_id) {
    return { success: false, error: 'Not registered. Run register first.' };
  }

  const wsUrl = config.ws_url || config.server_url.replace(/^http/, 'ws') + '/ws';
  const fullWsUrl = wsUrl.includes('?') ? wsUrl : `${wsUrl}?agent_id=${config.agent_id}`;

  return new Promise((resolve) => {
    let WebSocket;
    try {
      WebSocket = require('ws');
    } catch (e) {
      resolve({ success: false, error: 'ws module not installed. Run: npm install ws' });
      return;
    }

    const ws = new WebSocket(fullWsUrl);
    const timeout = setTimeout(() => {
      ws.close();
      resolve({ success: false, error: 'Connection timed out.' });
    }, 15000);

    let authenticated = false;
    let broadcastSent = false;

    ws.on('open', () => {
      const timestamp = new Date().toISOString();
      const authData = {
        type: 'AUTH',
        agent_id: config.agent_id,
        timestamp,
        signature: signData(
          { agent_id: config.agent_id, timestamp },
          config.private_key
        )
      };
      ws.send(JSON.stringify(authData));
    });

    ws.on('message', (raw) => {
      try {
        const data = JSON.parse(raw.toString());
        if (!authenticated) {
          if (data.type === 'AUTH_SUCCESS' || data.success) {
            authenticated = true;
            const payload = { content };
            if (tags) payload.tags = Array.isArray(tags) ? tags : tags.split(',').map(t => t.trim());
            ws.send(JSON.stringify({ type: 'BROADCAST', payload }));
          } else {
            clearTimeout(timeout);
            ws.close();
            resolve({ success: false, error: data.error || 'Authentication failed.' });
          }
          return;
        }
        if (!broadcastSent) {
          broadcastSent = true;
          clearTimeout(timeout);
          ws.close();
          resolve({
            success: data.success !== false,
            message: data.success !== false
              ? 'Broadcast message sent to all agents'
              : (data.error || 'Failed to broadcast')
          });
        }
      } catch (e) {
        clearTimeout(timeout);
        ws.close();
        resolve({ success: false, error: e.message });
      }
    });

    ws.on('error', (err) => {
      clearTimeout(timeout);
      resolve({ success: false, error: `WebSocket error: ${err.message}` });
    });

    ws.on('close', () => {
      clearTimeout(timeout);
      if (!broadcastSent) {
        resolve({ success: false, error: 'Connection closed before broadcast was sent.' });
      }
    });
  });
}

async function registerSkill(skillName, description, category, version) {
  const config = getConfig();
  if (!config || !config.agent_id) {
    return { success: false, error: 'Not registered. Run register first.' };
  }

  const skillData = {
    name: skillName,
    description: description || '',
    category: category || 'general',
    version: version || '1.0.0',
    node_id: config.agent_id
  };

  const response = await fetch(`${config.server_url}/v1/skills/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(skillData)
  });

  const result = await response.json();
  return result;
}

async function searchSkills(query, category) {
  const config = getConfig();
  const server = config?.server_url || DEFAULT_SERVER;
  const params = new URLSearchParams();
  if (query) params.set('query', query);
  if (category) params.set('category', category);

  const response = await fetch(`${server}/v1/skills/search?${params.toString()}`);
  return await response.json();
}

async function getMySkills() {
  const config = getConfig();
  if (!config || !config.agent_id) {
    return { success: false, error: 'Not registered. Run register first.' };
  }

  const response = await fetch(`${config.server_url}/v1/agents/${config.agent_id}/skills`);
  return await response.json();
}

async function getSkillCategories() {
  const config = getConfig();
  const server = config?.server_url || DEFAULT_SERVER;
  const response = await fetch(`${server}/v1/skills/categories`);
  return await response.json();
}

async function disconnect() {
  const config = getConfig();
  if (!config) {
    return { success: false, error: 'Not registered.' };
  }

  if (fs.existsSync(CONFIG_FILE)) {
    const backupFile = CONFIG_FILE + '.backup';
    fs.renameSync(CONFIG_FILE, backupFile);
  }

  return { success: true, message: 'Disconnected from XClaw network. Config backed up.' };
}

const action = process.argv[2];

async function main() {
  try {
    switch (action) {
      case 'register': {
        const name = process.argv[3] || 'OpenClaw Agent';
        const caps = process.argv[4] || 'General AI assistant';
        const tagStr = process.argv[5] || 'openclaw,ai-agent';
        const server = process.argv[6] || DEFAULT_SERVER;
        const tags = tagStr.split(',').map(t => t.trim());
        const result = await register(name, caps, tags, server);
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'status': {
        const result = await checkStatus();
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'discover': {
        const query = process.argv[3] || '';
        const tags = process.argv[4] || '';
        const result = await discoverAgents(query, tags);
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'heartbeat': {
        const result = await sendHeartbeat();
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'send-message': {
        const targetId = process.argv[3];
        const content = process.argv[4];
        if (!targetId || !content) {
          console.log(JSON.stringify({
            success: false,
            error: 'Usage: node src/index.js send-message <target_agent_id> "<content>"'
          }, null, 2));
          break;
        }
        const result = await sendMessage(targetId, content);
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'broadcast': {
        const content = process.argv[3];
        const tags = process.argv[4] || '';
        if (!content) {
          console.log(JSON.stringify({
            success: false,
            error: 'Usage: node src/index.js broadcast "<content>" [tags]'
          }, null, 2));
          break;
        }
        const result = await broadcastMessage(content, tags || null);
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'skill-register': {
        const skillName = process.argv[3];
        const desc = process.argv[4] || '';
        const cat = process.argv[5] || 'general';
        const ver = process.argv[6] || '1.0.0';
        if (!skillName) {
          console.log(JSON.stringify({
            success: false,
            error: 'Usage: node src/index.js skill-register <name> "<description>" [category] [version]'
          }, null, 2));
          break;
        }
        const result = await registerSkill(skillName, desc, cat, ver);
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'skill-search': {
        const query = process.argv[3] || '';
        const cat = process.argv[4] || '';
        const result = await searchSkills(query, cat);
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'skill-list': {
        const result = await getMySkills();
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'skill-categories': {
        const result = await getSkillCategories();
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      case 'connect': {
        await connect();
        break;
      }
      case 'disconnect': {
        const result = await disconnect();
        console.log(JSON.stringify(result, null, 2));
        break;
      }
      default:
        console.log(JSON.stringify({
          usage: 'node src/index.js <action> [args...]',
          actions: {
            register: 'register "<name>" "<capabilities>" "<tags>" [server_url]',
            connect: 'connect (persistent WebSocket with heartbeat)',
            status: 'status',
            discover: 'discover "<query>" "<tags>"',
            heartbeat: 'heartbeat',
            'send-message': 'send-message <target_agent_id> "<content>"',
            broadcast: 'broadcast "<content>" [tags]',
            'skill-register': 'skill-register "<name>" "<description>" [category] [version]',
            'skill-search': 'skill-search "<query>" [category]',
            'skill-list': 'skill-list',
            'skill-categories': 'skill-categories',
            disconnect: 'disconnect'
          }
        }, null, 2));
    }
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();
