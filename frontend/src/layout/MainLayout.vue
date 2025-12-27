<template>
  <n-layout has-sider position="absolute">
    <Sidebar />
    <n-layout>
      <n-layout-content content-style="padding: 24px; background-color: #f5f7fa; min-height: 100vh;">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue'
</script>
