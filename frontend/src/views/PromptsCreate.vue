<template>
  <div class="prompt-create">
    <div class="create-header">
      <n-button text class="back-button" @click="handleBack">
        <template #icon>
          <n-icon><ArrowBackOutline /></n-icon>
        </template>
        返回
      </n-button>
      <div class="create-title">创建Prompt模板</div>
    </div>

    <div class="create-body">
      <div class="form-row">
        <div class="form-label"><span class="required">*</span> 模板名称</div>
        <div class="form-control">
          <n-input
            v-model:value="form.name"
            placeholder="请输入模板名称"
            maxlength="64"
            show-count
          />
          <div class="form-hint">支持中英文、数字、中划线(-)、下划线(_)，2-64字符</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-label">模板标签</div>
        <div class="form-control">
          <n-select
            v-model:value="form.tag"
            :options="tagOptions"
            placeholder="请选择模板标签"
          />
          <div class="form-hint">单个模板最多可选 3 个标签</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-label">场景类型</div>
        <div class="form-control">
          <div class="scene-options">
            <button
              v-for="option in sceneOptions"
              :key="option.value"
              class="scene-card"
              :class="{ active: form.sceneType === option.value }"
              type="button"
              @click="form.sceneType = option.value"
            >
              <div class="scene-title">{{ option.label }}</div>
              <div class="scene-desc">{{ option.desc }}</div>
            </button>
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-label">变量标识符</div>
        <div class="form-control">
          <n-select
            v-model:value="form.variableStyle"
            :options="variableOptions"
            placeholder="双大括号{{}}"
          />
          <div class="form-hint">
            模板内容中使用变量时会自动识别，例如：&#123;&#123;name&#125;&#125;。
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-label"><span class="required">*</span> 正向Prompt</div>
        <div class="form-control">
          <n-input
            v-model:value="form.positivePrompt"
            type="textarea"
            placeholder="输入正向Prompt"
            maxlength="10000"
            show-count
            :autosize="{ minRows: 6, maxRows: 10 }"
          />
          <div class="form-hint">建议详细描述目标与结构，便于模型输出一致内容。</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-label">负向Prompt</div>
        <div class="form-control">
          <n-input
            v-model:value="form.negativePrompt"
            type="textarea"
            placeholder="输入负向Prompt（可选）"
            maxlength="10000"
            show-count
            :autosize="{ minRows: 4, maxRows: 8 }"
          />
          <div class="form-hint">用于排除不希望的输出内容，可留空。</div>
        </div>
      </div>
    </div>

    <div class="action-bar">
      <n-button type="primary" @click="handleSubmit">确定</n-button>
      <n-button @click="handleBack">取消</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { ArrowBackOutline } from '@vicons/ionicons5'
import { addPrompt, type PromptItem } from '../stores/promptStore'

const router = useRouter()
const message = useMessage()

const form = ref({
  name: '',
  tag: '',
  sceneType: 'text',
  variableStyle: 'double',
  positivePrompt: '',
  negativePrompt: ''
})

const tagOptions = [
  { label: '教育培训', value: '教育培训' },
  { label: '图像生成', value: '图像生成' },
  { label: '生活助手', value: '生活助手' },
  { label: '自定义', value: '自定义' }
]

const sceneOptions = [
  { label: '文生文', value: 'text', desc: '适用于文字任务与对话' },
  { label: '文生图', value: 'image', desc: '适用于图像生成与创意' }
]

const variableOptions = [
  { label: '双大括号 {{}}', value: 'double' },
  { label: '美元符号 ${}', value: 'dollar' }
]

const formatDate = (date: Date) => {
  const pad = (num: number) => String(num).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(
    date.getHours()
  )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

const handleBack = () => {
  router.push({ name: 'prompts' })
}

const handleSubmit = () => {
  if (!form.value.name.trim()) {
    message.warning('请输入模板名称')
    return
  }

  if (!form.value.positivePrompt.trim()) {
    message.warning('请输入正向Prompt')
    return
  }

  const now = new Date()
  const newPrompt: PromptItem = {
    id: `custom-${now.getTime()}`,
    title: form.value.name.trim(),
    content: form.value.positivePrompt.trim(),
    tag: form.value.tag || '自定义',
    views: 0,
    stars: 0,
    createdAt: formatDate(now),
    type: 'custom'
  }

  addPrompt(newPrompt)
  router.push({ name: 'prompts', query: { tab: 'custom' } })
}
</script>

<style scoped>
.prompt-create {
  background-color: #fff;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.create-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.create-title {
  font-size: 16px;
  font-weight: 600;
  color: #2b2f38;
}

.create-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 16px;
  align-items: start;
}

.form-label {
  font-size: 13px;
  color: #5a6275;
  padding-top: 8px;
}

.required {
  color: #e05858;
  margin-right: 4px;
}

.form-control {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-hint {
  font-size: 12px;
  color: #8a93a6;
}

.scene-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
}

.scene-card {
  border: 1px solid #e7eaf1;
  border-radius: 12px;
  padding: 16px;
  background-color: #f9fafc;
  text-align: left;
  cursor: pointer;
}

.scene-card.active {
  border-color: #6b79f5;
  background-color: #eef2ff;
}

.scene-title {
  font-size: 14px;
  font-weight: 600;
  color: #2e3445;
}

.scene-desc {
  font-size: 12px;
  color: #8a93a6;
  margin-top: 6px;
}

.action-bar {
  margin-top: auto;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 12px;
}

@media (max-width: 960px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
