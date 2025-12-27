<template>
  <div class="settings-page">
    <div class="settings-header">
      <div class="header-left">
        <div class="header-icon">
          <n-icon size="22" color="#5f7ce6">
            <SettingsOutline />
          </n-icon>
        </div>
        <div class="header-text">
          <div class="title">模型与密钥配置</div>
          <div class="subtitle">集中管理所有 AI 服务的连接信息</div>
        </div>
      </div>

    </div>

    <div class="settings-body">
      <div class="side-panel">
        <div class="panel-card">
          <div class="panel-actions">
            <n-button size="small" secondary>
              <template #icon>
                <n-icon><DownloadOutline /></n-icon>
              </template>
              导出全部
            </n-button>
            <n-button size="small" secondary>
              <template #icon>
                <n-icon><CloudUploadOutline /></n-icon>
              </template>
              导入全部
            </n-button>
          </div>
          <div class="panel-note">配置文件为 Interview AI 专用配置。</div>
        </div>

        <div class="group-title">模型配置</div>
        <div class="side-list">
          <button
            v-for="item in translateItems"
            :key="item.key"
            class="side-item"
            :class="{ active: activeKey === item.key }"
            @click="activeKey = item.key"
            type="button"
          >
            {{ item.label }}
          </button>
        </div>
      </div>

      <SettingsContentPanel :active-key="activeKey" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { SettingsOutline, DownloadOutline, CloudUploadOutline } from '@vicons/ionicons5'
import SettingsContentPanel from './settings/SettingsContentPanel.vue'

const activeKey = ref('volcano')

const translateItems = [
  { key: 'deepseek', label: 'DeepSeek 配置' },
  { key: 'gemini', label: 'Gemini 配置' },
  { key: 'openai', label: 'OpenAPI 配置' },
  { key: 'tongyi', label: '通义千问' },
  { key: 'volcano', label: '火山引擎' },
  { key: 'custom', label: '自定义模型' }
]
</script>

<style scoped>
.settings-page {
  height: 100%;
  background-color: #fff;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.settings-header {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left {
  display: flex;
  gap: 12px;
  align-items: center;
}

.header-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background-color: #eef2ff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-text .title {
  font-size: 18px;
  font-weight: bold;
  color: #2b2f38;
}

.header-text .subtitle {
  font-size: 12px;
  color: #8a93a6;
  margin-top: 4px;
}

.settings-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.side-panel {
  width: 280px;
  border-right: 1px solid #f0f0f0;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: #fbfbfd;
}

.panel-card {
  background-color: #fff;
  border: 1px solid #eef0f5;
  border-radius: 10px;
  padding: 12px;
}

.panel-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.panel-note {
  margin-top: 8px;
  font-size: 12px;
  color: #8b93a7;
}

.side-alert {
  font-size: 12px;
}

.group-title {
  font-size: 12px;
  color: #707991;
  font-weight: 600;
  margin-top: 4px;
}

.side-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.side-item {
  width: 100%;
  text-align: left;
  padding: 8px 12px;
  border-radius: 8px;
  border: none;
  background-color: transparent;
  color: #3b4457;
  cursor: pointer;
  font-size: 14px;
}

.side-item:hover {
  background-color: #f1f4ff;
}

.side-item.active {
  background-color: #dfe9ff;
  color: #2f5fd2;
  font-weight: 600;
}

@media (max-width: 960px) {
  .settings-body {
    flex-direction: column;
  }

  .side-panel {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #f0f0f0;
  }
}
</style>
