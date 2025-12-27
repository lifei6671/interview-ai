<template>
  <div class="home-container">
    <n-layout>
      <n-layout-header bordered style="padding: 24px">
        <div style="display: flex; justify-content: space-between; align-items: center">
          <n-h2 style="margin: 0">Interview AI</n-h2>
          <n-button @click="handleLogout">Logout</n-button>
        </div>
      </n-layout-header>
      <n-layout-content content-style="padding: 24px">
        <n-card title="Welcome">
          <p>Welcome to the Interview AI Dashboard!</p>
          <p>You can start managing your interviews here.</p>
        </n-card>
      </n-layout-content>
    </n-layout>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleLogout = () => {
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  height: 100vh;
}
</style>
