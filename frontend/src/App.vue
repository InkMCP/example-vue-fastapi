<template>
  <div class="body">
    <div class="container">
      <h1>Vue + FastAPI</h1>
      <p class="subtitle">A full-stack app with Vue frontend and Python backend</p>

      <form @submit.prevent="addItem" class="form">
        <input
          v-model="newName"
          type="text"
          placeholder="Add a new item..."
          class="input"
        />
        <button type="submit" class="btn">Add</button>
      </form>

      <p v-if="loading" class="empty">Loading...</p>
      <p v-else-if="items.length === 0" class="empty">No items yet. Add one above!</p>
      <div v-else>
        <div v-for="item in items" :key="item.id" class="item">
          <span class="item-name">{{ item.name }}</span>
          <button @click="deleteItem(item.id)" class="delete-btn">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const items = ref([]);
const newName = ref('');
const loading = ref(true);

async function fetchItems() {
  const res = await fetch('/api/items');
  items.value = await res.json();
  loading.value = false;
}

async function addItem() {
  if (!newName.value.trim()) return;
  await fetch('/api/items', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: newName.value.trim() })
  });
  newName.value = '';
  fetchItems();
}

async function deleteItem(id) {
  await fetch(`/api/items/${id}`, { method: 'DELETE' });
  fetchItems();
}

onMounted(fetchItems);
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
.body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0a0a0a;
  color: #ededed;
  min-height: 100vh;
  padding: 4rem 1.5rem;
}
.container { max-width: 640px; margin: 0 auto; }
h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
.subtitle { color: #888; margin-bottom: 2rem; }
.form { display: flex; gap: 0.5rem; margin-bottom: 2rem; }
.input {
  flex: 1; padding: 0.625rem 0.875rem; background: #1a1a1a;
  border: 1px solid #333; border-radius: 0.5rem; color: #ededed;
  font-size: 0.9375rem; outline: none;
}
.input:focus { border-color: #555; }
.input::placeholder { color: #555; }
.btn {
  padding: 0.625rem 1.25rem; background: #ededed; color: #0a0a0a;
  border: none; border-radius: 0.5rem; font-size: 0.9375rem;
  font-weight: 500; cursor: pointer;
}
.btn:hover { background: #d4d4d4; }
.item {
  padding: 0.875rem; border-bottom: 1px solid #1a1a1a;
  display: flex; justify-content: space-between; align-items: center;
}
.item-name { font-weight: 500; }
.delete-btn {
  background: transparent; color: #555; border: 1px solid #333;
  border-radius: 0.375rem; padding: 0.25rem 0.625rem;
  cursor: pointer; font-size: 0.8125rem;
}
.empty { text-align: center; color: #555; padding: 3rem 0; }
</style>
