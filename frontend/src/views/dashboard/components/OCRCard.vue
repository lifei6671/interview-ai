<template>
  <n-card class="ocr-card" :bordered="false">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <n-icon size="24" color="#5e7ce0" style="margin-right: 8px">
            <ScanOutline />
          </n-icon>
          <span class="header-title">OCR 文档解析</span>
        </div>
        <n-button size="small" secondary>
          <template #icon>
            <n-icon><SettingsOutline /></n-icon>
          </template>
          设置
        </n-button>
      </div>
    </template>

    <n-form label-placement="top">
      <n-form-item label="OCR 引擎">
        <n-select v-model:value="ocrEngine" :options="ocrOptions" />
      </n-form-item>
      
      <div class="engine-settings">
        <div class="setting-title">MinerU 翻译模式</div>
        <n-radio-group v-model:value="translationMode" name="translationMode">
          <n-space vertical>
            <n-radio value="standard">
              <div class="radio-content">
                <div class="radio-label">标准翻译模式</div>
                <div class="radio-desc">将 MinerU 输出的 Markdown 独立翻译</div>
              </div>
            </n-radio>
            <n-radio value="structured">
              <div class="radio-content">
                <div class="radio-label">结构化翻译模式</div>
                <div class="radio-desc">基于 JSON 进行翻译，支持 PDF 对照显示</div>
              </div>
            </n-radio>
          </n-space>
        </n-radio-group>
      </div>
    </n-form>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ScanOutline, SettingsOutline } from '@vicons/ionicons5'

const ocrEngine = ref('MinerU')
const translationMode = ref('standard')

const ocrOptions = [
  { label: 'MinerU', value: 'MinerU' },
  { label: 'Tesseract', value: 'Tesseract' }
]
</script>

<style scoped>
.ocr-card {
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
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

.engine-settings {
  background-color: #f9f9f9;
  padding: 16px;
  border-radius: 8px;
  margin-top: 12px;
}

.setting-title {
  font-weight: 500;
  margin-bottom: 12px;
  color: #666;
}

.radio-content {
  display: flex;
  flex-direction: column;
}

.radio-label {
  font-weight: 500;
}

.radio-desc {
  font-size: 12px;
  color: #999;
}
</style>
