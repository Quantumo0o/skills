#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { TradfriClient, AccessoryTypes } = require('node-tradfri-client');

const configPath = path.join(__dirname, '..', 'config.json');
const fileConfig = fs.existsSync(configPath)
  ? JSON.parse(fs.readFileSync(configPath, 'utf8'))
  : {};

const host = process.env.TRADFRI_HOST || fileConfig.host;
const identity = process.env.TRADFRI_IDENTITY || fileConfig.identity;
const psk = process.env.TRADFRI_PSK || fileConfig.psk;

const cmd = process.argv[2];
const targetName = process.argv[3];
const value = process.argv[4];
const EXCLUDED_GROUPS = new Set(['SuperGroup', 'Instellen']);

function die(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

if (!host || !identity || !psk) {
  die('Missing TRADFRI config. Set config.json or TRADFRI_HOST/TRADFRI_IDENTITY/TRADFRI_PSK.');
}

function normalizeName(name) {
  return String(name || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim()
    .toLowerCase();
}

function lightState(device) {
  return device.lightList && device.lightList[0] ? device.lightList[0] : null;
}

function summarizeDevice(device) {
  const light = lightState(device);
  return {
    instanceId: device.instanceId,
    name: device.name,
    type: device.type,
    alive: device.alive,
    onOff: light ? light.onOff : undefined,
    dimmer: light ? light.dimmer : undefined,
  };
}

function summarizeGroup(group) {
  return {
    instanceId: group.instanceId,
    name: group.name,
    onOff: group.onOff,
    dimmer: group.dimmer,
  };
}

async function collect(tradfri) {
  const devices = new Map();
  const groups = new Map();

  tradfri
    .on('device updated', (device) => devices.set(device.instanceId, device))
    .on('group updated', (group) => groups.set(group.instanceId, group));

  await tradfri.connect(identity, psk);
  await tradfri.observeDevices();
  await tradfri.observeGroupsAndScenes();
  await new Promise((resolve) => setTimeout(resolve, 3000));
  return { devices, groups };
}

function scoreMatch(itemName, rawName) {
  const item = normalizeName(itemName);
  const needle = normalizeName(rawName);
  if (!needle) return 0;
  if (item === needle) return 100;
  if (item.startsWith(needle)) return 80;
  if (item.includes(needle)) return 60;
  const words = item.split(/\s+/);
  if (words.some((w) => w.startsWith(needle))) return 40;
  return 0;
}

function resolveByName(items, rawName) {
  const arr = [...items.values()]
    .map((item) => ({ item, score: scoreMatch(item.name, rawName) }))
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score || normalizeName(a.item.name).localeCompare(normalizeName(b.item.name)));

  if (arr.length === 0) return { match: null, candidates: [] };
  if (arr.length === 1) return { match: arr[0].item, candidates: [] };
  if (arr[0].score >= 80 && arr[1].score < arr[0].score) return { match: arr[0].item, candidates: [] };
  return { match: null, candidates: arr.slice(0, 10).map((x) => x.item) };
}

function allLightDevices(devices) {
  return [...devices.values()].filter((d) => d.type === AccessoryTypes.lightbulb);
}

function realGroups(groups) {
  return [...groups.values()].filter((g) => !EXCLUDED_GROUPS.has(g.name));
}

(async () => {
  const tradfri = new TradfriClient(host);
  try {
    const { devices, groups } = await collect(tradfri);
    const lights = allLightDevices(devices);
    const usableGroups = realGroups(groups);

    if (cmd === 'status') {
      console.log(JSON.stringify({
        ok: true,
        host,
        counts: { devices: devices.size, lights: lights.length, groups: usableGroups.length },
      }, null, 2));
      return;
    }

    if (cmd === 'list-devices') {
      console.log(JSON.stringify({ ok: true, host, devices: lights.map(summarizeDevice) }, null, 2));
      return;
    }

    if (cmd === 'list-groups') {
      console.log(JSON.stringify({ ok: true, host, groups: usableGroups.map(summarizeGroup) }, null, 2));
      return;
    }

    if (cmd === 'whats-on') {
      const onLights = lights.filter((d) => {
        const light = lightState(d);
        return d.alive && light && light.onOff;
      });
      console.log(JSON.stringify({ ok: true, host, lights: onLights.map(summarizeDevice) }, null, 2));
      return;
    }

    if (cmd === 'offline') {
      const offline = lights.filter((d) => !d.alive);
      console.log(JSON.stringify({ ok: true, host, lights: offline.map(summarizeDevice) }, null, 2));
      return;
    }

    if (cmd === 'all-on' || cmd === 'all-off') {
      const brightness = value != null ? Number(value) : (cmd === 'all-on' ? 100 : 0);
      if (!Number.isFinite(brightness) || brightness < 0 || brightness > 100) die('Brightness must be 0-100');
      const results = [];
      for (const group of usableGroups) {
        const result = await tradfri.operateGroup(group, { onOff: cmd === 'all-on', dimmer: brightness }, true);
        results.push({ name: group.name, instanceId: group.instanceId, result });
      }
      console.log(JSON.stringify({ ok: true, host, command: cmd, brightness, count: results.length, results }, null, 2));
      return;
    }

    if (!targetName && !['whats-on', 'offline', 'status', 'list-devices', 'list-groups'].includes(cmd)) {
      die('Target name required');
    }

    if (cmd === 'light-on' || cmd === 'light-off' || cmd === 'brightness') {
      const lightMap = new Map(lights.map((d) => [d.instanceId, d]));
      const { match: target, candidates } = resolveByName(lightMap, targetName);
      if (!target) {
        die(`Light not found or ambiguous: ${targetName}\nCandidates: ${candidates.map((c) => c.name).join(', ') || '-'}`);
      }
      if (!target.alive) die(`Light is offline: ${target.name}`);

      let result;
      if (cmd === 'light-on') result = await tradfri.operateLight(target, { onOff: true }, true);
      if (cmd === 'light-off') result = await tradfri.operateLight(target, { onOff: false }, true);
      if (cmd === 'brightness') {
        const num = Number(value);
        if (!Number.isFinite(num) || num < 0 || num > 100) die('Brightness must be 0-100');
        result = await tradfri.operateLight(target, { dimmer: num, onOff: num > 0 }, true);
      }

      console.log(JSON.stringify({ ok: true, host, command: cmd, target: summarizeDevice(target), result }, null, 2));
      return;
    }

    if (cmd === 'group-on' || cmd === 'group-off') {
      const groupMap = new Map(usableGroups.map((g) => [g.instanceId, g]));
      const { match: target, candidates } = resolveByName(groupMap, targetName);
      if (!target) {
        die(`Group not found or ambiguous: ${targetName}\nCandidates: ${candidates.map((c) => c.name).join(', ') || '-'}`);
      }
      const result = await tradfri.operateGroup(target, { onOff: cmd === 'group-on' }, true);
      console.log(JSON.stringify({ ok: true, host, command: cmd, target: summarizeGroup(target), result }, null, 2));
      return;
    }

    die(`Unknown command: ${cmd}`);
  } catch (e) {
    console.error(e && e.stack ? e.stack : e);
    process.exit(1);
  } finally {
    try { tradfri.destroy(); } catch {}
  }
})();
