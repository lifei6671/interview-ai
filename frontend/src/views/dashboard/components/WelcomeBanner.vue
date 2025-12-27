<template>
  <div class="welcome-banner">
    <div class="content">
      <h1 class="title">开始新的任务</h1>
      <p class="description">开始一个新任务，选择不同模型和 Prompt 生成面试题。</p>
    </div>
    <div class="illustration">
      <!-- Placeholder for illustration -->
      <n-icon size="120" color="rgba(255,255,255,0.2)">
        <DocumentTextOutline />
      </n-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DocumentTextOutline } from '@vicons/ionicons5'
</script>

<style scoped>
.welcome-banner {
  background: linear-gradient(135deg, #eef1f5 0%, #e6e9f0 100%);
  border-radius: 16px;
  padding: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}

.content {
  z-index: 1;
}

.title {
  font-size: 32px;
  font-weight: bold;
  margin: 0 0 16px 0;
  color: #333;
}

.description {
  font-size: 16px;
  color: #666;
  max-width: 600px;
  line-height: 1.6;
  margin: 0;
}

.illustration {
  position: absolute;
  right: 40px;
  bottom: -20px;
  transform: rotate(-15deg);
}
</style>
