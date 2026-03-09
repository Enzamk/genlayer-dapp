<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createClient } from 'genlayer-js'
import { studionet } from 'genlayer-js/chains'
import { privateKeyToAccount } from 'viem/accounts'

const privateKey = import.meta.env.VITE_PRIVATE_KEY as `0x${string}`
const account = privateKeyToAccount(privateKey)
const client = createClient({ chain: studionet, account })
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS as `0x${string}`

const storage = ref('')
const newValue = ref('')
const loading = ref(false)
const txStatus = ref('')
const txType = ref<'success'|'error'|''>('')
const particles = ref(Array.from({length: 20}, (_, i) => ({
  id: i,
  x: Math.random() * 100,
  y: Math.random() * 100,
  size: Math.random() * 3 + 1,
  speed: Math.random() * 20 + 10
})))

async function fetchStorage() {
  loading.value = true
  try {
    const result = await client.readContract({
      address: contractAddress,
      functionName: 'get_storage',
      args: [],
      account: account.address,
    })
    storage.value = String(result)
  } catch (e: any) {
    storage.value = 'Error reading contract'
  } finally {
    loading.value = false
  }
}

async function updateStorage() {
  if (!newValue.value) return
  loading.value = true
  txStatus.value = 'Broadcasting transaction...'
  txType.value = ''
  try {
    await client.writeContract({
      address: contractAddress,
      functionName: 'update_storage',
      args: [newValue.value],
    })
    txStatus.value = 'Transaction confirmed! Finalizing on-chain...'
    txType.value = 'success'
    newValue.value = ''
    setTimeout(fetchStorage, 5000)
  } catch (e: any) {
    txStatus.value = 'Transaction failed: ' + e.message
    txType.value = 'error'
  } finally {
    loading.value = false
  }
}

onMounted(fetchStorage)
</script>

<template>
  <div class="app">
    <!-- Animated background -->
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>
    <div class="particles">
      <div
        v-for="p in particles"
        :key="p.id"
        class="particle"
        :style="{
          left: p.x + '%',
          top: p.y + '%',
          width: p.size + 'px',
          height: p.size + 'px',
          animationDuration: p.speed + 's'
        }"
      ></div>
    </div>

    <!-- Main card -->
    <div class="container">
      <!-- Header -->
      <header class="header">
        <div class="logo">
          <div class="logo-icon">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
              <polygon points="14,2 26,8 26,20 14,26 2,20 2,8" stroke="#00f5c4" stroke-width="1.5" fill="none"/>
              <polygon points="14,7 21,11 21,18 14,22 7,18 7,11" stroke="#00f5c4" stroke-width="1" fill="rgba(0,245,196,0.1)"/>
              <circle cx="14" cy="14" r="3" fill="#00f5c4"/>
            </svg>
          </div>
          <div>
            <h1 class="title">GenLayer</h1>
            <span class="subtitle">Intelligent Contract Interface</span>
          </div>
        </div>
        <div class="network-badge">
          <span class="dot"></span>
          studionet
        </div>
      </header>

      <!-- Contract info -->
      <div class="contract-card">
        <div class="card-label">CONTRACT ADDRESS</div>
        <div class="contract-address">
          <span class="address-text">{{ contractAddress }}</span>
          <div class="address-chip">ERC</div>
        </div>
      </div>

      <!-- Storage display -->
      <div class="storage-card">
        <div class="card-label">ON-CHAIN STORAGE</div>
        <div class="storage-value" :class="{ loading: loading }">
          <template v-if="loading">
            <div class="loading-dots">
              <span></span><span></span><span></span>
            </div>
          </template>
          <template v-else>
            <span class="value-text">{{ storage || 'Empty' }}</span>
          </template>
        </div>
        <div class="storage-meta">
          <span>Last synced: just now</span>
          <button class="refresh-btn" @click="fetchStorage" :disabled="loading">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 4v6h-6M1 20v-6h6"/>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
            Refresh
          </button>
        </div>
      </div>

      <!-- Update form -->
      <div class="update-card">
        <div class="card-label">UPDATE STORAGE</div>
        <div class="input-group">
          <input
            v-model="newValue"
            placeholder="Enter new value..."
            class="input"
            :disabled="loading"
            @keyup.enter="updateStorage"
          />
          <button
            class="submit-btn"
            @click="updateStorage"
            :disabled="loading || !newValue"
          >
            <template v-if="loading">
              <div class="spinner"></div>
            </template>
            <template v-else>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
              Send
            </template>
          </button>
        </div>

        <!-- Transaction status -->
        <div v-if="txStatus" class="tx-status" :class="txType">
          <div class="tx-icon">
            <template v-if="txType === 'success'">✓</template>
            <template v-else-if="txType === 'error'">✕</template>
            <template v-else>◌</template>
          </div>
          <span>{{ txStatus }}</span>
        </div>
      </div>

      <!-- Footer -->
      <footer class="footer">
        <span>Powered by GenLayer Protocol</span>
        <span class="separator">·</span>
        <span>Consensus: 5 validators</span>
      </footer>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --neon: #00f5c4;
  --neon-dim: rgba(0,245,196,0.15);
  --neon-glow: rgba(0,245,196,0.4);
  --bg: #050a0e;
  --surface: rgba(255,255,255,0.03);
  --surface-hover: rgba(255,255,255,0.06);
  --border: rgba(0,245,196,0.15);
  --text: #e2e8f0;
  --text-dim: rgba(226,232,240,0.4);
  --error: #ff4d6d;
  --success: #00f5c4;
}

body { background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; }

.app {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  position: relative;
  overflow: hidden;
}

/* Background effects */
.bg-grid {
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,245,196,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,196,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}

.bg-glow {
  position: fixed;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(0,245,196,0.08) 0%, transparent 70%);
  top: -200px; right: -200px;
  pointer-events: none;
}

.particles { position: fixed; inset: 0; pointer-events: none; }
.particle {
  position: absolute;
  background: var(--neon);
  border-radius: 50%;
  opacity: 0.3;
  animation: float linear infinite;
}
@keyframes float {
  0% { transform: translateY(0) scale(1); opacity: 0.3; }
  50% { opacity: 0.6; }
  100% { transform: translateY(-100vh) scale(0); opacity: 0; }
}

/* Container */
.container {
  width: 100%;
  max-width: 520px;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  backdrop-filter: blur(20px);
}

.logo { display: flex; align-items: center; gap: 14px; }
.logo-icon {
  width: 48px; height: 48px;
  background: var(--neon-dim);
  border: 1px solid var(--border);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 20px var(--neon-dim);
}

.title {
  font-family: 'Space Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  color: var(--neon);
  letter-spacing: -0.5px;
  line-height: 1;
}

.subtitle {
  font-size: 11px;
  color: var(--text-dim);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.network-badge {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  background: var(--neon-dim);
  border: 1px solid var(--border);
  border-radius: 20px;
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  color: var(--neon);
  letter-spacing: 0.5px;
}

.dot {
  width: 6px; height: 6px;
  background: var(--neon);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--neon);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 6px var(--neon); }
  50% { opacity: 0.5; box-shadow: 0 0 12px var(--neon); }
}

/* Cards */
.contract-card, .storage-card, .update-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px 24px;
  backdrop-filter: blur(20px);
  transition: border-color 0.2s;
}
.contract-card:hover, .storage-card:hover, .update-card:hover {
  border-color: rgba(0,245,196,0.3);
}

.card-label {
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  color: var(--text-dim);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

/* Contract address */
.contract-address {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
}
.address-text {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  color: var(--text-dim);
  word-break: break-all;
  flex: 1;
}
.address-chip {
  padding: 3px 8px;
  background: var(--neon-dim);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  color: var(--neon);
  white-space: nowrap;
}

/* Storage value */
.storage-value {
  min-height: 48px;
  display: flex; align-items: center;
  margin-bottom: 12px;
}
.value-text {
  font-family: 'Space Mono', monospace;
  font-size: 22px;
  font-weight: 700;
  color: var(--neon);
  text-shadow: 0 0 20px var(--neon-glow);
  word-break: break-all;
}

.loading-dots { display: flex; gap: 6px; align-items: center; }
.loading-dots span {
  width: 8px; height: 8px;
  background: var(--neon);
  border-radius: 50%;
  animation: bounce 1.2s ease-in-out infinite;
}
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

.storage-meta {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 11px; color: var(--text-dim);
}
.refresh-btn {
  display: flex; align-items: center; gap: 5px;
  background: none; border: none; cursor: pointer;
  color: var(--text-dim); font-size: 11px;
  font-family: 'DM Sans', sans-serif;
  transition: color 0.2s;
  padding: 4px 8px;
  border-radius: 6px;
}
.refresh-btn:hover:not(:disabled) { color: var(--neon); background: var(--neon-dim); }
.refresh-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* Input */
.input-group { display: flex; gap: 10px; margin-bottom: 12px; }

.input {
  flex: 1;
  background: rgba(0,0,0,0.3);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 16px;
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.input::placeholder { color: var(--text-dim); }
.input:focus {
  border-color: var(--neon);
  box-shadow: 0 0 0 3px var(--neon-dim);
}
.input:disabled { opacity: 0.5; cursor: not-allowed; }

.submit-btn {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 20px;
  background: var(--neon);
  border: none; border-radius: 10px;
  color: #050a0e;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  min-width: 90px; justify-content: center;
}
.submit-btn:hover:not(:disabled) {
  background: #00ffd0;
  box-shadow: 0 0 20px var(--neon-glow);
  transform: translateY(-1px);
}
.submit-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(5,10,14,0.3);
  border-top-color: #050a0e;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Transaction status */
.tx-status {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  animation: fadeIn 0.3s ease;
  background: rgba(0,245,196,0.05);
  border: 1px solid rgba(0,245,196,0.2);
  color: var(--neon);
}
.tx-status.error {
  background: rgba(255,77,109,0.05);
  border-color: rgba(255,77,109,0.2);
  color: var(--error);
}
.tx-icon {
  font-family: 'Space Mono', monospace;
  font-size: 14px;
  font-weight: 700;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Footer */
.footer {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px;
  font-size: 11px; color: var(--text-dim);
  letter-spacing: 0.3px;
}
.separator { color: var(--border); }
</style>
