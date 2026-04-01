#!/usr/bin/env node

const fs = require("fs");
const net = require("net");
const os = require("os");
const path = require("path");
const { execFileSync, spawn } = require("child_process");

const DEFAULT_PROTOCOL_VERSION = "2024-11-05";
const DEFAULT_TIMEOUT_MS = 10000;
const DEFAULT_PIPE_NAME = "pixcake-mcp";
const DEFAULT_BRIDGE_BASENAME = "pixcake-mcp-bridge";
const BRIDGE_CANDIDATES_BY_PLATFORM = {
  darwin: [
    DEFAULT_BRIDGE_BASENAME,
  ],
  win32: [
    `${DEFAULT_BRIDGE_BASENAME}.exe`,
    DEFAULT_BRIDGE_BASENAME,
  ],
  linux: [
    DEFAULT_BRIDGE_BASENAME,
  ],
};

let cachedLocalConfig = null;

function uniqueNonEmpty(values) {
  const results = [];
  const seen = new Set();

  for (const value of values) {
    if (typeof value !== "string") continue;
    const normalized = value.trim();
    if (!normalized || seen.has(normalized)) continue;
    seen.add(normalized);
    results.push(normalized);
  }

  return results;
}

function getLocalConfigCandidatePaths() {
  return uniqueNonEmpty([
    process.env.PIXCAKE_SKILLS_CONFIG,
    path.join(os.homedir(), ".openclaw", "skills", "pixcake-skills", "config.local.json"),
    path.join(__dirname, "..", "config.local.json"),
  ]);
}

function loadLocalConfig() {
  if (cachedLocalConfig) return cachedLocalConfig;

  for (const candidatePath of getLocalConfigCandidatePaths()) {
    try {
      if (!fs.existsSync(candidatePath)) continue;
      const raw = fs.readFileSync(candidatePath, "utf8");
      const parsed = JSON.parse(raw);
      cachedLocalConfig = {
        path: candidatePath,
        bridgePath: parsed.bridgePath || parsed.bridge_path || null,
        socketPath: parsed.socketPath || parsed.socket_path || null,
        bridgeCandidates: Array.isArray(parsed.bridgeCandidates)
          ? parsed.bridgeCandidates
          : Array.isArray(parsed.bridge_candidates)
            ? parsed.bridge_candidates
            : [],
      };
      return cachedLocalConfig;
    } catch {
      // Ignore invalid local config and continue with auto discovery.
    }
  }

  cachedLocalConfig = {
    path: null,
    bridgePath: null,
    socketPath: null,
    bridgeCandidates: [],
  };
  return cachedLocalConfig;
}

function jsonDump(value) {
  return JSON.stringify(value, null, 2);
}

function hasPathSeparators(value) {
  return value.includes("/") || value.includes("\\");
}

function getWindowsExecutableExtensions() {
  const raw = process.env.PATHEXT || ".EXE;.CMD;.BAT;.COM";
  return raw.split(";").map((item) => item.trim().toLowerCase()).filter(Boolean);
}

function resolvePathLikeExecutable(command) {
  const candidates = [command];

  if (process.platform === "win32" && path.extname(command) === "") {
    for (const extension of getWindowsExecutableExtensions()) {
      candidates.push(`${command}${extension}`);
    }
  }

  for (const candidate of candidates) {
    if (candidate && fs.existsSync(candidate)) return candidate;
  }

  return null;
}

function resolveCommandOnPath(command) {
  const lookupCommand = process.platform === "win32" ? "where" : "which";

  try {
    const output = execFileSync(lookupCommand, [command], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    return output.split(/\r?\n/).map((line) => line.trim()).find(Boolean) || null;
  } catch {
    return null;
  }
}

function resolveExecutable(command) {
  if (!command) return null;
  if (path.isAbsolute(command) || hasPathSeparators(command)) {
    return resolvePathLikeExecutable(command);
  }
  return resolveCommandOnPath(command);
}

function getSiblingBridgeCandidate(executablePath) {
  if (!executablePath) return null;
  const extension = process.platform === "win32" ? ".exe" : "";
  return path.join(path.dirname(executablePath), `${DEFAULT_BRIDGE_BASENAME}${extension}`);
}

function getDarwinProcessExecutablePaths() {
  try {
    const output = execFileSync("ps", ["-axo", "command="], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });

    const results = [];
    for (const line of output.split(/\r?\n/)) {
      if (!line || !line.toLowerCase().includes("pixcake")) continue;
      const match = line.match(/(\/.*?\.app\/Contents\/MacOS\/[^\s]+)/);
      if (match && match[1]) {
        results.push(match[1].trim());
      }
    }
    return uniqueNonEmpty(results);
  } catch {
    return [];
  }
}

function listMacBridgeCandidates() {
  const appRoots = uniqueNonEmpty([
    "/Applications",
    path.join(os.homedir(), "Applications"),
  ]);
  const results = [];

  for (const appRoot of appRoots) {
    try {
      const entries = fs.readdirSync(appRoot, { withFileTypes: true });
      for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        if (!entry.name.toLowerCase().endsWith(".app")) continue;
        if (!entry.name.toLowerCase().includes("pixcake")) continue;
        results.push(path.join(appRoot, entry.name, "Contents", "MacOS", DEFAULT_BRIDGE_BASENAME));
      }
    } catch {
      // Ignore unreadable application roots.
    }
  }

  return results.sort((left, right) => {
    const leftIsTest = /test/i.test(left);
    const rightIsTest = /test/i.test(right);
    if (leftIsTest === rightIsTest) return left.localeCompare(right);
    return leftIsTest ? 1 : -1;
  });
}

function parseJsonFromCommand(command, args) {
  try {
    const output = execFileSync(command, args, {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();

    if (!output) return [];
    const parsed = JSON.parse(output);
    if (Array.isArray(parsed)) return parsed;
    if (parsed == null) return [];
    return [parsed];
  } catch {
    return [];
  }
}

function getWindowsProcessDetails() {
  const script = [
    "$items = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |",
    "  Where-Object {",
    "    ($_.Name -match 'pixcake') -or ($_.ExecutablePath -match 'pixcake')",
    "  } |",
    "  Select-Object ProcessId, Name, ExecutablePath",
    "$items | ConvertTo-Json -Compress",
  ].join(" ");

  return parseJsonFromCommand("powershell.exe", [
    "-NoProfile",
    "-NonInteractive",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    script,
  ]).filter((item) => item && typeof item === "object");
}

function getWindowsRegistryInstallCandidates() {
  const script = [
    "$roots = @(",
    "  'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',",
    "  'HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',",
    "  'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'",
    ")",
    "$items = foreach ($root in $roots) {",
    "  Get-ItemProperty $root -ErrorAction SilentlyContinue |",
    "    Where-Object {",
    "      ($_.DisplayName -match 'pixcake') -or",
    "      ($_.InstallLocation -match 'pixcake') -or",
    "      ($_.DisplayIcon -match 'pixcake')",
    "    } |",
    "    Select-Object DisplayName, InstallLocation, DisplayIcon",
    "}",
    "$items | ConvertTo-Json -Compress",
  ].join(" ");

  const items = parseJsonFromCommand("powershell.exe", [
    "-NoProfile",
    "-NonInteractive",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    script,
  ]);

  const results = [];
  for (const item of items) {
    if (!item || typeof item !== "object") continue;

    if (typeof item.InstallLocation === "string" && item.InstallLocation.trim()) {
      results.push(path.join(item.InstallLocation.trim(), `${DEFAULT_BRIDGE_BASENAME}.exe`));
    }

    if (typeof item.DisplayIcon === "string" && item.DisplayIcon.trim()) {
      const cleaned = item.DisplayIcon.split(",")[0].trim().replace(/^"|"$/g, "");
      if (cleaned) {
        results.push(path.join(path.dirname(cleaned), `${DEFAULT_BRIDGE_BASENAME}.exe`));
      }
    }
  }

  return results;
}

function getAutoDiscoveredBridgeCandidates() {
  const localConfig = loadLocalConfig();
  const candidates = [];

  if (localConfig.bridgePath) candidates.push(localConfig.bridgePath);
  if (Array.isArray(localConfig.bridgeCandidates)) {
    candidates.push(...localConfig.bridgeCandidates);
  }

  if (process.platform === "darwin") {
    for (const executablePath of getDarwinProcessExecutablePaths()) {
      candidates.push(getSiblingBridgeCandidate(executablePath));
    }
    candidates.push(...listMacBridgeCandidates());
  }

  if (process.platform === "win32") {
    const processDetails = getWindowsProcessDetails();
    for (const detail of processDetails) {
      if (detail && typeof detail.ExecutablePath === "string" && detail.ExecutablePath.trim()) {
        candidates.push(getSiblingBridgeCandidate(detail.ExecutablePath.trim()));
      }
    }
    candidates.push(...getWindowsRegistryInstallCandidates());
  }

  candidates.push(...(BRIDGE_CANDIDATES_BY_PLATFORM[process.platform] || []));

  return uniqueNonEmpty(candidates);
}

function detectBridgePath(explicitPath) {
  if (explicitPath) return explicitPath;
  if (process.env.PIXCAKE_BRIDGE_CMD) return process.env.PIXCAKE_BRIDGE_CMD;
  for (const candidate of getAutoDiscoveredBridgeCandidates()) {
    if (resolveExecutable(candidate)) return candidate;
  }
  return null;
}

function detectSocketPath(explicitPath) {
  if (explicitPath) return explicitPath;
  if (process.env.PIXCAKE_SOCKET_PATH) return process.env.PIXCAKE_SOCKET_PATH;
  const localConfig = loadLocalConfig();
  if (localConfig.socketPath) return localConfig.socketPath;
  if (process.platform === "win32") return `\\\\.\\pipe\\${DEFAULT_PIPE_NAME}`;
  return path.join(os.tmpdir(), "pixcake-mcp");
}

function detectPixcakeProcesses() {
  if (process.platform === "win32") {
    return getWindowsProcessDetails().map((item) => {
      const name = item.Name || "pixcake";
      const pid = item.ProcessId != null ? `pid=${item.ProcessId}` : "pid=?";
      const executablePath = item.ExecutablePath || "";
      return executablePath ? `${pid} ${name} ${executablePath}` : `${pid} ${name}`;
    });
  }

  try {
    const output = execFileSync("pgrep", ["-fl", "pixcake"], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    return output.split("\n").map((line) => line.trim()).filter(Boolean);
  } catch {
    return [];
  }
}

function testSocketConnection(socketPath) {
  return new Promise((resolve) => {
    const client = net.createConnection({ path: socketPath });
    let finished = false;

    const done = (result) => {
      if (finished) return;
      finished = true;
      client.destroy();
      resolve(result);
    };

    client.setTimeout(1500);
    client.once("connect", () => done({ ok: true, error: null }));
    client.once("timeout", () => done({ ok: false, error: "socket connect timeout" }));
    client.once("error", (error) => done({ ok: false, error: error.message }));
  });
}

function isNamedPipePath(socketPath) {
  return typeof socketPath === "string" && socketPath.startsWith("\\\\.\\pipe\\");
}

function formatSocketLabel(socketPath) {
  return isNamedPipePath(socketPath) ? "pipe" : "socket";
}

async function doctor(bridgePath, explicitSocketPath) {
  const socketPath = detectSocketPath(explicitSocketPath);
  const bridgeResolvedPath = resolveExecutable(bridgePath);
  const bridgeExists = !!bridgePath && !!bridgeResolvedPath;
  const socketExists = isNamedPipePath(socketPath) ? null : fs.existsSync(socketPath);
  const pixcakeProcesses = detectPixcakeProcesses();
  let socketConnectable = false;
  let socketError = null;

  if (socketExists !== false) {
    const result = await testSocketConnection(socketPath);
    socketConnectable = result.ok;
    socketError = result.error;
  }

  const issues = [];
  const socketLabel = formatSocketLabel(socketPath);
  if (!bridgeExists) issues.push("pixcake-mcp-bridge not found");
  if (pixcakeProcesses.length === 0) issues.push("PixCake client process is not running");
  if (socketExists === false) {
    issues.push(`PixCake ${socketLabel} not found at ${socketPath}`);
  } else if (isNamedPipePath(socketPath) && socketError && /ENOENT|not found/i.test(socketError)) {
    issues.push(`PixCake ${socketLabel} not found at ${socketPath}`);
  } else if (!socketConnectable) {
    issues.push(`PixCake ${socketLabel} is not accepting connections: ${socketError}`);
  }

  return {
    platform: process.platform,
    ready: bridgeExists && socketConnectable,
    bridge_path: bridgePath,
    bridge_resolved_path: bridgeResolvedPath,
    bridge_exists: bridgeExists,
    node: process.execPath,
    socket_path: socketPath,
    socket_exists: socketExists,
    socket_connectable: socketConnectable,
    socket_error: socketError,
    pixcake_processes: pixcakeProcesses,
    issues: issues,
  };
}

class MCPBridgeClient {
  constructor(bridgePath, timeoutMs) {
    this.bridgePath = bridgePath;
    this.spawnCommand = resolveExecutable(bridgePath) || bridgePath;
    this.timeoutMs = timeoutMs;
    this.nextId = 1;
    this.stdoutBuffer = Buffer.alloc(0);
    this.stderrBuffer = "";
    this.pending = new Map();
    this.proc = null;
  }

  async start() {
    this.proc = spawn(this.spawnCommand, [], {
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true,
    });

    this.proc.stdout.on("data", (chunk) => {
      this.stdoutBuffer = Buffer.concat([this.stdoutBuffer, chunk]);
      this._drainStdout();
    });

    this.proc.stderr.on("data", (chunk) => {
      this.stderrBuffer += chunk.toString("utf8");
      if (this.stderrBuffer.length > 4000) {
        this.stderrBuffer = this.stderrBuffer.slice(-4000);
      }
    });

    this.proc.on("exit", (code, signal) => {
      const message = `bridge exited before response (code=${code}, signal=${signal})`;
      for (const { reject, timer } of this.pending.values()) {
        clearTimeout(timer);
        reject(new Error(`${message}; stderr=${this.stderrBuffer.trim()}`));
      }
      this.pending.clear();
    });

    await this.request("initialize", {
      protocolVersion: DEFAULT_PROTOCOL_VERSION,
      capabilities: {},
      clientInfo: {
        name: "pixcake-skills-bridge-runner",
        version: "0.1.0",
      },
    });

    this.notify("notifications/initialized", {});
  }

  stop() {
    if (!this.proc) return;
    this.proc.kill("SIGTERM");
  }

  request(method, params) {
    const id = this.nextId++;
    const payload = {
      jsonrpc: "2.0",
      id,
      method,
      params,
    };

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Timed out while waiting for ${method}. stderr=${this.stderrBuffer.trim()}`));
      }, this.timeoutMs);

      this.pending.set(id, { resolve, reject, timer });
      this._send(payload);
    });
  }

  notify(method, params) {
    this._send({
      jsonrpc: "2.0",
      method,
      params,
    });
  }

  listTools() {
    return this.request("tools/list", {});
  }

  callTool(name, args) {
    return this.request("tools/call", {
      name,
      arguments: args,
    });
  }

  _send(payload) {
    const body = Buffer.from(JSON.stringify(payload), "utf8");
    const header = Buffer.from(`Content-Length: ${body.length}\r\n\r\n`, "ascii");
    this.proc.stdin.write(Buffer.concat([header, body]));
  }

  _drainStdout() {
    while (true) {
      const marker = this.stdoutBuffer.indexOf("\r\n\r\n");
      if (marker === -1) return;

      const headerBlob = this.stdoutBuffer.slice(0, marker).toString("utf8");
      const match = headerBlob.match(/Content-Length:\s*(\d+)/i);
      if (!match) {
        throw new Error("bridge returned message without Content-Length");
      }

      const contentLength = Number(match[1]);
      const bodyStart = marker + 4;
      const bodyEnd = bodyStart + contentLength;
      if (this.stdoutBuffer.length < bodyEnd) return;

      const body = this.stdoutBuffer.slice(bodyStart, bodyEnd).toString("utf8");
      this.stdoutBuffer = this.stdoutBuffer.slice(bodyEnd);

      let payload;
      try {
        payload = JSON.parse(body);
      } catch (error) {
        throw new Error(`failed to parse bridge response: ${error.message}`);
      }

      const pending = this.pending.get(payload.id);
      if (!pending) continue;

      clearTimeout(pending.timer);
      this.pending.delete(payload.id);

      if (payload.error) {
        pending.reject(new Error(jsonDump(payload.error)));
      } else {
        pending.resolve(payload.result);
      }
    }
  }
}

function normalizeToolResult(result) {
  if (!result || typeof result !== "object" || !Array.isArray(result.content)) {
    return result;
  }

  const normalizedItems = result.content.map((item) => {
    if (!item || typeof item !== "object" || item.type !== "text" || typeof item.text !== "string") {
      return item;
    }
    try {
      return JSON.parse(item.text);
    } catch {
      return item.text;
    }
  });

  return {
    isError: Boolean(result.isError),
    data: normalizedItems.length === 1 ? normalizedItems[0] : normalizedItems,
  };
}

function parseArgs(argv) {
  const state = {
    bridge: null,
    socket: null,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    json: false,
    command: null,
    toolName: null,
    argsJson: "{}",
  };

  const args = [...argv];
  while (args.length > 0) {
    const current = args.shift();
    if (current === "--bridge") {
      state.bridge = args.shift() || null;
    } else if (current === "--socket") {
      state.socket = args.shift() || null;
    } else if (current === "--timeout") {
      state.timeoutMs = Number(args.shift() || DEFAULT_TIMEOUT_MS);
    } else if (current === "--json") {
      state.json = true;
    } else if (!state.command) {
      state.command = current;
      if (current === "call") {
        state.toolName = args.shift() || null;
      }
    } else if (current === "--args") {
      state.argsJson = args.shift() || "{}";
    }
  }

  return state;
}

async function run() {
  const cli = parseArgs(process.argv.slice(2));
  const bridgePath = detectBridgePath(cli.bridge);

  if (!cli.command || !["doctor", "list", "call"].includes(cli.command)) {
    console.error("Usage: node pixcake_bridge.js [--bridge PATH] [--socket PATH] [--timeout MS] <doctor|list|call> [tool_name] [--args JSON] [--json]");
    process.exit(2);
  }

  if (cli.command === "doctor") {
    const result = await doctor(bridgePath, cli.socket);
    console.log(jsonDump(result));
    process.exit(result.ready ? 0 : 1);
  }

  const resolvedBridgePath = resolveExecutable(bridgePath);

  if (!bridgePath || !resolvedBridgePath) {
    console.log(jsonDump({
      ok: false,
      error: "pixcake-mcp-bridge not found",
      bridge_path: bridgePath,
      bridge_resolved_path: resolvedBridgePath,
    }));
    process.exit(1);
  }

  const client = new MCPBridgeClient(bridgePath, cli.timeoutMs);
  try {
    await client.start();

    if (cli.command === "list") {
      const result = await client.listTools();
      console.log(jsonDump(result));
      process.exit(0);
    }

    let parsedArgs = {};
    try {
      parsedArgs = JSON.parse(cli.argsJson || "{}");
    } catch (error) {
      console.log(jsonDump({
        ok: false,
        error: `invalid --args JSON: ${error.message}`,
      }));
      process.exit(1);
    }

    if (!cli.toolName) {
      console.log(jsonDump({
        ok: false,
        error: "tool name is required for call",
      }));
      process.exit(1);
    }

    const result = await client.callTool(cli.toolName, parsedArgs);
    console.log(jsonDump(normalizeToolResult(result)));
    process.exit(0);
  } catch (error) {
    console.log(jsonDump({
      ok: false,
      error: error.message,
      bridge_path: bridgePath,
    }));
    process.exit(1);
  } finally {
    client.stop();
  }
}

run();
