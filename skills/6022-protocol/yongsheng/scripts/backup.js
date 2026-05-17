#!/usr/bin/env node
/**
 * Yongsheng — Memory backup to IPFS + anchor on HashKey Chain
 * 
 * Usage: node backup.js [--silent]
 * Env: KLIFE_SEED (from OpenClaw secrets manager — see: openclaw secrets configure), PINATA_JWT (optional)
 */

import { ethers } from 'ethers'
import crypto from 'crypto'
import fs from 'fs'
import path from 'path'
import https from 'https'

const HASHKEY_RPC = process.env.HASHKEY_RPC || 'https://mainnet.hsk.xyz'
const WORKSPACE = process.env.WORKSPACE || process.env.HOME + '/workspace'
const SILENT = process.argv.includes('--silent')

function log(...args) { if (!SILENT) console.log(...args) }

function encryptMemory(data, privKey) {
  const key = crypto.createHash('sha256').update(privKey).digest()
  const iv = crypto.randomBytes(16)
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv)
  const encrypted = Buffer.concat([cipher.update(data), cipher.final()])
  return Buffer.concat([iv, encrypted]).toString('base64')
}

async function pinToIPFS(content, jwt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      pinataContent: { data: content },
      pinataMetadata: { name: `yongsheng-backup-${Date.now()}` }
    })
    const req = https.request({
      hostname: 'api.pinata.cloud',
      path: '/pinning/pinJSONToIPFS',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwt}`,
        'Content-Length': Buffer.byteLength(body)
      }
    }, res => {
      let data = ''
      res.on('data', d => data += d)
      res.on('end', () => {
        try { resolve(JSON.parse(data).IpfsHash) }
        catch(e) { reject(new Error('Pinata error: ' + data)) }
      })
    })
    req.on('error', reject)
    req.write(body)
    req.end()
  })
}

async function main() {
  const seed = process.env.KLIFE_SEED
  const privkey = process.env.KLIFE_PRIVKEY

  if (!seed && !privkey) {
    console.error('Set KLIFE_SEED or KLIFE_PRIVKEY')
    process.exit(1)
  }

  const provider = new ethers.JsonRpcProvider(HASHKEY_RPC)
  const wallet = seed
    ? ethers.Wallet.fromPhrase(seed).connect(provider)
    : new ethers.Wallet(privkey, provider).connect(provider)

  // Read memory files
  const files = ['MEMORY.md', 'SOUL.md', 'USER.md'].map(f => {
    const p = path.join(WORKSPACE, f)
    try { return { name: f, content: fs.readFileSync(p, 'utf8') } }
    catch { return { name: f, content: '' } }
  })

  const memoryBundle = files.map(f => `=== ${f.name} ===\n${f.content}`).join('\n\n')
  const privKeyHex = wallet.privateKey
  const encrypted = encryptMemory(memoryBundle, privKeyHex)

  log(`[yongsheng] Memory bundle: ${memoryBundle.length} chars → encrypted: ${encrypted.length} chars`)

  // Upload to IPFS
  let cid
  const jwt = process.env.PINATA_JWT
  if (jwt) {
    cid = await pinToIPFS(encrypted, jwt)
    log(`[yongsheng] IPFS CID: ${cid}`)
  } else {
    log('[yongsheng] No PINATA_JWT — skipping IPFS upload, using placeholder CID')
    cid = 'QmYONGSHENG_NO_JWT_' + Date.now()
  }

  // Anchor on HashKey Chain
  const ts = Date.now()
  const data = ethers.hexlify(ethers.toUtf8Bytes(`YONGSHENG_BACKUP:${cid}:${ts}`))

  const tx = await wallet.sendTransaction({ to: wallet.address, value: 0n, data })
  log(`[yongsheng] Backup anchored on HashKey Chain: ${tx.hash}`)
  log(`[yongsheng] ✓ Backup complete — CID: ${cid}`)
}

main().catch(e => { console.error(e.message); process.exit(1) })
