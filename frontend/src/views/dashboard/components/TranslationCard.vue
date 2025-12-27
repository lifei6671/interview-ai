<template>
  <n-card class="translation-card" :bordered="false">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <n-icon size="24" color="#8a5ee0" style="margin-right: 8px">
            <LanguageOutline />
          </n-icon>
          <span class="header-title">翻译与分析</span>
        </div>
      </div>
    </template>

    <n-form label-placement="top">
      <n-grid :cols="2" :x-gap="24">
        <n-form-item-gi label="翻译和分析模型">
          <n-select v-model:value="model" :options="modelOptions" />
        </n-form-item-gi>
        <n-form-item-gi label="目标语言">
          <n-select v-model:value="targetLang" :options="langOptions" />
        </n-form-item-gi>
      </n-grid>

      <div class="model-settings">
        <div class="setting-header">
          <span>Gemini 默认模型</span>
          <div class="setting-actions">
            <span class="tag">无可用 Key</span>
            <span class="tag primary">检测可用模型</span>
          </div>
        </div>
        <n-select placeholder="（未设置，点击检测获取列表）" disabled />
        <div class="setting-tip">若列表为空，请先点击上方“检测可用模型”。</div>
      </div>

      <div class="term-management">
        <div class="term-header">
          <div class="term-title">
            <span>翻译术语库管理</span>
            <n-tag size="small" type="info" bordered>暂无术语库</n-tag>
          </div>
          <n-checkbox v-model:checked="enableTerm">启用翻译术语库</n-checkbox>
        </div>
        <div class="term-desc">
          支持维护多套术语库，会话时自动注入提示词，辅助保持术语一致性。可按项目导入导出，灵活协同。
        </div>
        <n-space>
          <n-button dashed>
            <template #icon><n-icon><AddOutline /></n-icon></template>
            新增术语库
          </n-button>
          <n-button dashed>
            导入术语库
          </n-button>
          <n-button dashed>
            <template #icon><n-icon><CloudUploadOutline /></n-icon></template>
            导出全部术语库
          </n-button>
        </n-space>
        
        <div class="empty-state">
          <n-icon size="48" color="#ddd"><LibraryOutline /></n-icon>
          <div class="empty-text">正在加载术语库...</div>
        </div>
      </div>
    </n-form>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  LanguageOutline, 
  AddOutline, 
  CloudUploadOutline,
  LibraryOutline
} from '@vicons/ionicons5'

const model = ref('gemini')
const targetLang = ref('zh')
const enableTerm = ref(false)

const modelOptions = [
  { label: 'gemini', value: 'gemini' },
  { label: 'gpt-4', value: 'gpt-4' }
]

const langOptions = [
  { label: '中文', value: 'zh' },
  { label: 'English', value: 'en' }
]
</script>

<style scoped>
.translation-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
}

.card-header {
  display: flex;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
}

.model-settings {
  background-color: #f9f9f9;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.setting-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.setting-actions {
  display: flex;
  gap: 8px;
}

.tag {
  font-size: 12px;
  color: #999;
  cursor: pointer;
}

.tag.primary {
  color: #18a058;
}

.setting-tip {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.term-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.term-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  font-size: 16px;
}

.term-desc {
  font-size: 12px;
  color: #666;
  margin-bottom: 16px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #ccc;
}

.empty-text {
  margin-top: 12px;
  font-size: 14px;
}
</style>
