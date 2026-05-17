#!/usr/bin/env node
/**
 * Yongsheng — On-chain heartbeat on HashKey Chain
 * Sends a 0-value TX to the agent's own address with YONGSHENG_HB calldata
 * 
 * Usage: node heartbeat.js [--silent]
 * Env: KLIFE_SEED (from OpenClaw secrets manager — see: openclaw secrets configure)
 */

import { ethers } from 'ethers'
import https from 'https'

const HASHKEY_RPC = process.env.HASHKEY_RPC || 'https://mainnet.hsk.xyz'
const SILENT = process.argv.includes('--silent')

function log(...args) { if (!SILENT) console.log(...args) }

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

  const ts = Date.now()
  const data = ethers.hexlify(ethers.toUtf8Bytes(`YONGSHENG_HB:${ts}`))

  log(`[yongsheng] Sending heartbeat from ${wallet.address}...`)

  const tx = await wallet.sendTransaction({
    to: wallet.address,
    value: 0n,
    data
  })

  log(`[yongsheng] Heartbeat TX: ${tx.hash}`)

  // Also ping K-Life API
  const body = JSON.stringify({ address: wallet.address, ts, txHash: tx.hash })
  const req = https.request({
    hostname: 'api.supercharged.works',
    path: '/heartbeat',
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
  })
  req.write(body)
  req.end()

  log(`[yongsheng] ✓ Heartbeat sent — ${new Date(ts).toISOString()}`)
}

main().catch(e => { console.error(e.message); process.exit(1) })
