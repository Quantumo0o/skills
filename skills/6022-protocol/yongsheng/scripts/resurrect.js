#!/usr/bin/env node
/**
 * Yongsheng — Resurrection from HashKey Chain + IPFS
 * 
 * L1: K-Life API + Shamir share
 * L2: Scan HashKey Chain for YONGSHENG_BACKUP calldata → IPFS
 * 
 * Usage: node resurrect.js --address 0xYOUR_WALLET [--level 1|2]
 * Env: KLIFE_SEED (from OpenClaw secrets manager — see: openclaw secrets configure), HASHKEY_RPC
 */

import { ethers } from 'ethers'
import crypto from 'crypto'
import https from 'https'
import fs from 'fs'
import path from 'path'

const HASHKEY_RPC = process.env.HASHKEY_RPC || 'https://mainnet.hsk.xyz'
const WORKSPACE = process.env.WORKSPACE || process.env.HOME + '/workspace'

const args = process.argv.slice(2)
const addrIdx = args.indexOf('--address')
const lvlIdx = args.indexOf('--level')
const TARGET = addrIdx >= 0 ? args[addrIdx + 1] : null
const LEVEL = lvlIdx >= 0 ? parseInt(args[lvlIdx + 1]) : 2

if (!TARGET) { console.error('Usage: node resurrect.js --address 0xWALLET'); process.exit(1) }

function decryptMemory(encryptedB64, privKey) {
  const key = crypto.createHash('sha256').update(privKey).digest()
  const buf = Buffer.from(encryptedB64, 'base64')
  const iv = buf.slice(0, 16)
  const data = buf.slice(16)
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv)
  return Buffer.concat([decipher.update(data), decipher.final()]).toString('utf8')
}

async function fetchIPFS(cid) {
  return new Promise((resolve, reject) => {
    const gateways = [
      `https://ipfs.io/ipfs/${cid}`,
      `https://gateway.pinata.cloud/ipfs/${cid}`,
      `https://cloudflare-ipfs.com/ipfs/${cid}`
    ]
    const tryNext = (i) => {
      if (i >= gateways.length) return reject(new Error('All IPFS gateways failed'))
      https.get(gateways[i], res => {
        let data = ''
        res.on('data', d => data += d)
        res.on('end', () => resolve(data))
      }).on('error', () => tryNext(i + 1))
    }
    tryNext(0)
  })
}

async function scanHashKeyChain(address) {
  console.log(`[yongsheng] Scanning HashKey Chain for ${address} backup...`)
  // Scan last 10000 blocks for YONGSHENG_BACKUP calldata
  const provider = new ethers.JsonRpcProvider(HASHKEY_RPC)
  const latest = await provider.getBlockNumber()
  const from = Math.max(0, latest - 10000)

  // Use getLogs with address filter (self-to-self TXs)
  // HashKey Chain explorer API fallback
  const url = `https://explorer.hashkey.cloud/api?module=account&action=txlist&address=${address}&startblock=${from}&endblock=${latest}&sort=desc`

  return new Promise((resolve, reject) => {
    https.get(url, res => {
      let data = ''
      res.on('data', d => data += d)
      res.on('end', () => {
        try {
          const result = JSON.parse(data)
          const txs = result.result || []
          for (const tx of txs) {
            if (!tx.input) continue
            const decoded = Buffer.from(tx.input.replace('0x', ''), 'hex').toString('utf8')
            const match = decoded.match(/YONGSHENG_BACKUP:(Qm[A-Za-z0-9]+):/)
            if (match) { resolve(match[1]); return }
          }
          reject(new Error('No backup found on HashKey Chain'))
        } catch(e) { reject(e) }
      })
    }).on('error', reject)
  })
}

async function main() {
  console.log(`[yongsheng] Resurrection initiated for ${TARGET} (Level ${LEVEL})`)

  const seed = process.env.KLIFE_SEED
  const privkey = process.env.KLIFE_PRIVKEY
  if (!seed && !privkey) { console.error('No wallet configured. Run: openclaw secrets configure — then set KLIFE_SEED in the secure keystore.'); process.exit(1) }

  const wallet = seed ? ethers.Wallet.fromPhrase(seed) : new ethers.Wallet(privkey)
  const privKeyHex = wallet.privateKey

  let cid
  if (LEVEL === 1) {
    // L1: ask K-Life API
    console.log('[yongsheng] L1: Requesting share from K-Life API...')
    const sig = await wallet.signMessage(`resurrect:${TARGET}`)
    const apiUrl = `https://api.supercharged.works/resurrect/${TARGET}?sig=${sig}`
    cid = await new Promise((resolve, reject) => {
      https.get(apiUrl, res => {
        let d = ''
        res.on('data', c => d += c)
        res.on('end', () => {
          try { resolve(JSON.parse(d).cid) } catch(e) { reject(e) }
        })
      }).on('error', reject)
    })
  } else {
    // L2: scan HashKey Chain
    cid = await scanHashKeyChain(TARGET)
  }

  console.log(`[yongsheng] Found backup CID: ${cid}`)
  const encrypted = await fetchIPFS(cid)
  const decrypted = decryptMemory(encrypted, privKeyHex)

  // Parse and restore files
  const sections = decrypted.split(/=== ([A-Z]+\.md) ===\n/)
  for (let i = 1; i < sections.length; i += 2) {
    const fname = sections[i]
    const content = sections[i + 1] || ''
    if (content.trim()) {
      const dest = path.join(WORKSPACE, fname)
      fs.writeFileSync(dest, content)
      console.log(`[yongsheng] ✓ Restored ${fname} (${content.length} chars)`)
    }
  }

  // Broadcast resurrection proof on HashKey Chain
  const provider = new ethers.JsonRpcProvider(HASHKEY_RPC)
  const connectedWallet = wallet.connect(provider)
  const ts = Date.now()
  const proofData = ethers.hexlify(ethers.toUtf8Bytes(`YONGSHENG_RESURRECTION:${LEVEL}:${ts}:IPFS:${cid}`))
  const tx = await connectedWallet.sendTransaction({ to: TARGET, value: 0n, data: proofData })
  console.log(`[yongsheng] ✓ Resurrection proof on HashKey Chain: ${tx.hash}`)
  console.log('[yongsheng] ✓ Memory restored. The agent lives. 永生.')
}

main().catch(e => { console.error(e.message); process.exit(1) })
