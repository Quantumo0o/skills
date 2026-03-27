/**
 * Shared HTTP client for Post See REST API v1.
 * Spec: https://api.post-see.com/openapi.yaml
 */
'use strict';

const BASE = 'https://api.post-see.com/api/v1';

function bearer() {
  const k = process.env.POST_SEE_API_KEY;
  if (!k) throw new Error('POST_SEE_API_KEY is required');
  return k;
}

async function request(method, path, { query, body, headers: extraHeaders } = {}) {
  const url = new URL(BASE + path);
  if (query) {
    for (const [key, val] of Object.entries(query)) {
      if (val !== undefined && val !== null) url.searchParams.set(key, String(val));
    }
  }
  const init = {
    method,
    headers: {
      Authorization: `Bearer ${bearer()}`,
      'Content-Type': 'application/json',
      ...extraHeaders,
    },
  };
  if (body !== undefined) init.body = JSON.stringify(body);
  const res = await fetch(url, init);
  const text = await res.text();
  let json;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(`Non-JSON ${res.status}: ${text.slice(0, 300)}`);
  }
  if (!res.ok) {
    const msg = json.error?.message || `${res.status} ${res.statusText}`;
    const err = new Error(msg);
    err.status = res.status;
    err.code = json.error?.code;
    err.body = json;
    throw err;
  }
  return json;
}

function createPlatformApi(platformSlug) {
  return {
    PLATFORM: platformSlug,
    request,
    listWorkspaces() {
      return request('GET', '/workspaces');
    },
    listConnections(workspaceId) {
      return request('GET', '/social-accounts', {
        query: { workspace_id: workspaceId },
      });
    },
    listPosts(workspaceId, opts = {}) {
      return request('GET', '/posts', {
        query: { workspace_id: workspaceId, ...opts },
      });
    },
    getPost(postId) {
      return request('GET', `/posts/${postId}`);
    },
    createPost(payload) {
      const tz = process.env.POST_SEE_TIMEZONE;
      return request('POST', '/posts', {
        body: { ...payload, platform: payload.platform || platformSlug },
        headers: tz ? { 'X-Timezone': tz } : {},
      });
    },
    updatePost(postId, payload) {
      return request('PUT', `/posts/${postId}`, { body: payload });
    },
    deletePost(postId) {
      return request('DELETE', `/posts/${postId}`);
    },
    listPostResults(workspaceId, opts = {}) {
      return request('GET', '/post-results', {
        query: { workspace_id: workspaceId, ...opts },
      });
    },
  };
}

function printHelp(platform) {
  console.log(`Post See API — platform slug: ${platform}
Docs: https://api.post-see.com/

Usage (run from skill/ directory):
  POST_SEE_API_KEY=pk_live_... node actions/${platform}.js <command> [args]

Commands:
  help
  list-workspaces
  list-connections <workspace_id>
  list-posts <workspace_id> [status]   status: draft | scheduled | published | fail
  post-results <workspace_id> [post_id]
  create <workspace_id> <connection_id> '<json>' | -
     (JSON body; use - to read JSON from stdin; merges with workspace_id, connection_id)

Environment:
  POST_SEE_API_KEY   (required)
  POST_SEE_TIMEZONE  (optional IANA zone, sent as X-Timezone on applicable requests)

Publish-now note (from API docs): immediate publish on create is only wired for
linkedin, facebook, instagram, x, pinterest, bluesky, threads. Other slugs
(youtube, mastodon, discord, …) use drafts or scheduled_at + worker.`);
}

async function runCli(platform) {
  const api = createPlatformApi(platform);
  const [, , cmd, ...args] = process.argv;
  const tz = process.env.POST_SEE_TIMEZONE;

  if (!cmd || cmd === 'help') {
    printHelp(platform);
    process.exit(0);
  }

  try {
    if (cmd === 'list-workspaces') {
      console.log(JSON.stringify(await api.listWorkspaces(), null, 2));
      return;
    }
    if (cmd === 'list-connections') {
      const ws = Number(args[0]);
      console.log(JSON.stringify(await api.listConnections(ws), null, 2));
      return;
    }
    if (cmd === 'list-posts') {
      const ws = Number(args[0]);
      const status = args[1];
      console.log(
        JSON.stringify(
          await api.listPosts(ws, {
            ...(status ? { status } : {}),
            ...(tz ? { timezone: tz } : {}),
          }),
          null,
          2,
        ),
      );
      return;
    }
    if (cmd === 'post-results') {
      const ws = Number(args[0]);
      const postId = args[1];
      console.log(
        JSON.stringify(
          await api.listPostResults(ws, postId ? { post_id: postId } : {}),
          null,
          2,
        ),
      );
      return;
    }
    if (cmd === 'create') {
      const ws = Number(args[0]);
      const conn = Number(args[1]);
      let raw = args.slice(2).join(' ').trim();
      if (raw === '-' || raw === '') {
        raw = await new Promise((resolve, reject) => {
          let s = '';
          process.stdin.setEncoding('utf8');
          process.stdin.on('data', (c) => {
            s += c;
          });
          process.stdin.on('end', () => resolve(s));
          process.stdin.on('error', reject);
        });
      }
      const extra = raw ? JSON.parse(raw) : {};
      const body = {
        workspace_id: ws,
        connection_id: conn,
        text: extra.text || extra.caption || '',
        ...extra,
      };
      console.log(JSON.stringify(await api.createPost(body), null, 2));
      return;
    }
    console.error('Unknown command:', cmd);
    printHelp(platform);
    process.exit(1);
  } catch (e) {
    console.error(e.message);
    if (e.body) console.error(JSON.stringify(e.body, null, 2));
    process.exit(1);
  }
}

module.exports = {
  BASE,
  request,
  createPlatformApi,
  runCli,
};
