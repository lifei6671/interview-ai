<template>
  <div class="content-panel">
    <div class="section-title">自定义源站管理</div>
    <div class="section-divider"></div>
    <div class="custom-toolbar">
      <n-button type="success" @click="showCustomForm = true">
        <template #icon>
          <n-icon><AddOutline /></n-icon>
        </template>
        添加新源站
      </n-button>
    </div>
    <div v-if="!customSources.length" class="empty-tip">
      还没有自定义源站。请点击上方按钮添加一个。
    </div>

    <div v-if="showCustomForm" class="form-card">
      <div class="card-title">添加新源站</div>
      <div class="form-field">
        <div class="field-label">显示名称 *</div>
        <n-input v-model:value="customForm.name" placeholder="例如：我的备用 OpenAI" />
      </div>
      <div class="form-field">
        <div class="field-label">API Base URL *</div>
        <n-input v-model:value="customForm.baseUrl" placeholder="例如：https://api.openai.com" />
      </div>
      <div class="form-field">
        <div class="field-label">端点补全方式</div>
        <n-select
          v-model:value="customForm.endpointMode"
          :options="endpointOptions"
          placeholder="自动补全（必要时追加 /v1/...）"
        />
        <div class="field-hint">
          若第三方已提供完整的 /chat/completions 或 /messages 地址，请选择“已是完整端点”。
        </div>
      </div>
      <div class="form-field">
        <div class="field-label">默认模型 ID *</div>
        <div class="inline-input">
          <n-input v-model:value="customForm.modelId" placeholder="例如：gpt-4-turbo" />
          <n-button type="info">检测</n-button>
        </div>
      </div>
      <div class="form-field">
        <div class="field-label">API Key（检测时使用，可留空）</div>
        <n-input v-model:value="customForm.testKey" placeholder="如需临时检测可填写 Key" />
        <div class="field-hint">如已在下方 API Key 列表中添加 Key，可留空自动使用。</div>
      </div>
      <div class="form-field">
        <div class="field-label">请求格式</div>
        <n-select
          v-model:value="customForm.protocol"
          :options="protocolOptions"
          placeholder="OpenAI 格式"
        />
      </div>
      <div class="form-field">
        <div class="field-label">温度 (0-2)</div>
        <n-input-number v-model:value="customForm.temperature" :min="0" :max="2" />
      </div>
      <div class="form-field">
        <div class="field-label">最大 Tokens</div>
        <n-input-number v-model:value="customForm.maxTokens" :min="1" />
      </div>
      <div class="form-actions">
        <n-button @click="showCustomForm = false">取消</n-button>
        <n-button type="success" @click="handleSaveSource">保存</n-button>
      </div>
    </div>

    <div v-if="customSources.length" class="source-list">
      <div v-for="item in customSources" :key="item.id" class="source-card">
        <div class="source-title">{{ item.name }}</div>
        <div class="source-meta">{{ item.baseUrl }}</div>
        <div class="source-meta">默认模型：{{ item.modelId }}</div>
      </div>
    </div>

    <div class="section-divider"></div>
    <div class="empty-tip">请选择一个源站以管理其 API Keys。</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import { AddOutline } from '@vicons/ionicons5'

const message = useMessage()
const showCustomForm = ref(false)
const customSources = ref<Array<{
  id: string
  name: string
  baseUrl: string
  modelId: string
  endpointMode: string
  protocol: string
  temperature: number | null
  maxTokens: number | null
}>>([])
const customForm = ref({
  name: '',
  baseUrl: '',
  endpointMode: 'auto',
  modelId: '',
  testKey: '',
  protocol: 'openai',
  temperature: 0.5,
  maxTokens: 8000
})
const endpointOptions = [
  { label: '自动补全（必要时追加 /v1/...）', value: 'auto' },
  { label: '已是完整端点', value: 'full' }
]
const protocolOptions = [
  { label: 'OpenAI 格式', value: 'openai' },
  { label: 'Claude 格式', value: 'claude' },
  { label: 'Gemini 格式', value: 'gemini' }
]

const handleSaveSource = () => {
  if (!customForm.value.name.trim() || !customForm.value.baseUrl.trim() || !customForm.value.modelId.trim()) {
    message.warning('请完整填写必填项')
    return
  }

  customSources.value = [
    {
      id: `${Date.now()}`,
      name: customForm.value.name.trim(),
      baseUrl: customForm.value.baseUrl.trim(),
      modelId: customForm.value.modelId.trim(),
      endpointMode: customForm.value.endpointMode,
      protocol: customForm.value.protocol,
      temperature: customForm.value.temperature,
      maxTokens: customForm.value.maxTokens
    },
    ...customSources.value
  ]

  customForm.value = {
    name: '',
    baseUrl: '',
    endpointMode: 'auto',
    modelId: '',
    testKey: '',
    protocol: 'openai',
    temperature: 0.5,
    maxTokens: 8000
  }
  showCustomForm.value = false
}
</script>

<style scoped>
.content-panel {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #2b2f38;
}

.section-divider {
  height: 1px;
  background-color: #edf0f4;
  width: 100%;
}

.form-card {
  border: 1px solid #eef0f5;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: #fff;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #2e3445;
}

.custom-toolbar {
  margin: 8px 0 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  font-size: 13px;
  font-weight: 600;
  color: #5a6275;
}

.field-hint {
  font-size: 12px;
  color: #8a93a6;
}

.form-actions {
  display: flex;
  gap: 12px;
}

.source-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.source-card {
  border: 1px solid #eef0f5;
  border-radius: 12px;
  padding: 14px 16px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.source-title {
  font-size: 15px;
  font-weight: 600;
  color: #2e3445;
}

.source-meta {
  font-size: 12px;
  color: #8a93a6;
}

.empty-tip {
  color: #8a93a6;
  font-size: 13px;
}

.inline-input {
  display: flex;
  gap: 12px;
}

@media (max-width: 960px) {
  .inline-input {
    flex-direction: column;
  }
}
</style>
