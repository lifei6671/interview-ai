<template>
  <div class="content-panel">
    <div class="section-title">火山引擎 - 配置</div>
    <div class="section-divider"></div>

    <div class="section-actions">
      <div class="left-actions">
        <n-button size="small" secondary>
          <template #icon>
            <n-icon><DownloadOutline /></n-icon>
          </template>
          导出配置
        </n-button>
        <n-button size="small" secondary>
          <template #icon>
            <n-icon><CloudUploadOutline /></n-icon>
          </template>
          导入配置
        </n-button>
      </div>
      <n-button type="success" size="small" ghost @click="showAddForm = true">
        <template #icon>
          <n-icon><AddOutline /></n-icon>
        </template>
        添加新 Key
      </n-button>
    </div>

    <n-alert type="info" bordered class="info-alert">
      导入/导出的配置文件采用 Paper Burner X 固定格式 JSON，请勿修改字段结构。
    </n-alert>

    <div v-if="apiKeys.length" class="key-list">
      <div v-for="(item, index) in apiKeys" :key="item.id" class="key-card">
        <div class="key-card-header">
          <div class="key-title">{{ item.label }}</div>
          <n-tag size="small" round>未测试</n-tag>
        </div>
        <n-input v-model:value="item.value" placeholder="请输入 API Key" />
        <div class="key-actions">
          <n-button
            quaternary
            circle
            size="tiny"
            :disabled="index === 0"
            @click="moveKey(index, -1)"
          >
            <template #icon>
              <n-icon><ArrowUpOutline /></n-icon>
            </template>
          </n-button>
          <n-button
            quaternary
            circle
            size="tiny"
            :disabled="index === apiKeys.length - 1"
            @click="moveKey(index, 1)"
          >
            <template #icon>
              <n-icon><ArrowDownOutline /></n-icon>
            </template>
          </n-button>
          <n-button quaternary circle size="tiny" @click="handleTest(item)">
            <template #icon>
              <n-icon><PlayCircleOutline /></n-icon>
            </template>
          </n-button>
          <n-button quaternary circle size="tiny" @click="handleDelete(item.id)">
            <template #icon>
              <n-icon><TrashOutline /></n-icon>
            </template>
          </n-button>
        </div>
      </div>
    </div>

    <div v-else class="empty-tip">volcano 当前没有已保存的 API Key。</div>

    <div v-if="showAddForm" class="form-card">
      <div class="card-title">为 volcano 添加新的 API Key</div>
      <n-input
        v-model:value="apiKeyValue"
        type="textarea"
        placeholder="API Key 值（可每行输入一个实现批量添加）"
        :autosize="{ minRows: 4, maxRows: 6 }"
      />
      <n-input v-model:value="apiKeyNote" placeholder="备注（可选，应用于本批次所有 Key）" />
      <div class="form-actions">
        <n-button @click="showAddForm = false">取消</n-button>
        <n-button type="success" class="add-button" @click="handleAddKeys">
          <template #icon>
            <n-icon><AddOutline /></n-icon>
          </template>
          添加 Key(s)
        </n-button>
      </div>
    </div>

    <div class="form-card muted">
      <div class="card-title">火山 可用模型检测</div>
      <div class="inline-input">
        <n-input v-model:value="modelId" placeholder="例如：doubao-1-5-pro-32k-250115" />
        <n-button type="info">设为默认</n-button>
      </div>
      <div class="card-hint">不提供在线检测，请手动输入模型ID。</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import {
  DownloadOutline,
  CloudUploadOutline,
  AddOutline,
  ArrowUpOutline,
  ArrowDownOutline,
  PlayCircleOutline,
  TrashOutline
} from '@vicons/ionicons5'

const message = useMessage()
const apiKeyValue = ref('')
const apiKeyNote = ref('')
const modelId = ref('')
const showAddForm = ref(false)
const apiKeys = ref<Array<{ id: string; label: string; value: string }>>([])

const handleAddKeys = () => {
  const lines = apiKeyValue.value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)

  if (!lines.length) {
    message.warning('请输入 API Key')
    return
  }

  const note = apiKeyNote.value.trim()
  const newItems = lines.map((value, index) => ({
    id: `${Date.now()}-${index}`,
    label: note ? `${note} key` : '测试 key',
    value
  }))

  apiKeys.value = [...newItems, ...apiKeys.value]
  apiKeyValue.value = ''
  apiKeyNote.value = ''
  showAddForm.value = false
}

const moveKey = (index: number, direction: number) => {
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= apiKeys.value.length) {
    return
  }

  const next = [...apiKeys.value]
  const [item] = next.splice(index, 1)
  next.splice(targetIndex, 0, item)
  apiKeys.value = next
}

const handleTest = (item: { label: string }) => {
  message.info(`开始测试 ${item.label}`)
}

const handleDelete = (id: string) => {
  apiKeys.value = apiKeys.value.filter((item) => item.id !== id)
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

.section-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.left-actions {
  display: flex;
  gap: 8px;
}

.info-alert {
  font-size: 12px;
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

.form-card.muted {
  background-color: #f3f7ff;
  border-color: #d9e4ff;
}

.key-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.key-card {
  border: 1px solid #eef0f5;
  border-radius: 12px;
  padding: 12px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.key-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.key-title {
  font-size: 14px;
  font-weight: 600;
  color: #2e3445;
}

.key-actions {
  display: flex;
  gap: 6px;
  padding-top: 4px;
  border-top: 1px solid #edf0f4;
}

.form-actions {
  display: flex;
  gap: 12px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #2e3445;
}

.add-button {
  width: 140px;
}

.empty-tip {
  color: #8a93a6;
  font-size: 13px;
}

.inline-input {
  display: flex;
  gap: 12px;
}

.card-hint {
  color: #8a93a6;
  font-size: 12px;
}

@media (max-width: 960px) {
  .section-actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .inline-input {
    flex-direction: column;
  }
}
</style>
