<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createClient } from 'genlayer-js'
import { localnet } from 'genlayer-js/chains'
import { privateKeyToAccount } from 'viem/accounts'

const privateKey = '0x422ddc857dfe9163119ff671b6240c0dc580bd02520225a2931a7cdfee33a707' as `0x${string}`
const account = privateKeyToAccount(privateKey)

const client = createClient({ chain: localnet, account })
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS as `0x${string}`

const storage = ref('')
const newValue = ref('')
const loading = ref(false)
const txStatus = ref('')

async function fetchStorage() {
  loading.value = true
  try {
    const result = await client.readContract({
      address: contractAddress,
      functionName: 'get_storage',
      args: [],
      account: account.address,
    })
    storage.value = JSON.stringify(result)
  } catch (e: any) {
    storage.value = 'Error: ' + e.message
  } finally {
    loading.value = false
  }
}

async function updateStorage() {
  if (!newValue.value) return
  loading.value = true
  txStatus.value = 'Sending...'
  try {
    await client.writeContract({
      address: contractAddress,
      functionName: 'update_storage',
      args: [newValue.value],
    })
    txStatus.value = 'Sent! Waiting for finalization...'
    newValue.value = ''
    setTimeout(fetchStorage, 5000)
  } catch (e: any) {
    txStatus.value = 'Failed: ' + e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchStorage)
</script>

<template>
  <div style="max-width:600px;margin:60px auto;font-family:sans-serif;padding:0 20px;">
    <h1>GenLayer dApp 🚀</h1>
    <p><strong>Contract:</strong> {{ contractAddress }}</p>
    <hr/>
    <h2>Current Storage</h2>
    <p>{{ loading ? 'Loading...' : storage }}</p>
    <h2>Update Storage</h2>
    <input v-model="newValue" placeholder="Enter new value"
      style="padding:8px;width:300px;margin-right:8px;" />
    <button @click="updateStorage" :disabled="loading"
      style="padding:8px 16px;cursor:pointer;">
      {{ loading ? 'Wait...' : 'Update' }}
    </button>
    <p v-if="txStatus" style="color:green;">{{ txStatus }}</p>
  </div>
</template>
