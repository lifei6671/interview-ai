<template>
  <n-card class="translation-card" :bordered="false">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <n-icon size="24" color="#8a5ee0" style="margin-right: 8px">
            <GridSharp />
          </n-icon>
          <span class="header-title">任务与配置</span>
        </div>
      </div>
    </template>

    <n-form label-placement="top">
      <n-grid :cols="2" :x-gap="24">
        <n-form-item-gi label="分析模型">
          <n-select v-model:value="model" :options="modelOptions" />
        </n-form-item-gi>
        <n-form-item-gi label="提问策略">
          <n-select
          multiple 
            v-model:value="targetStrategy"
            :options="strategyOptions"
            :render-label="renderStrategyLabel"
          />
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
import { ref, h } from 'vue'
import type { SelectOption } from 'naive-ui'
import { 
  GridSharp, 
  AddOutline, 
  CloudUploadOutline,
  LibraryOutline
} from '@vicons/ionicons5'

const model = ref('gemini')
const targetStrategy = ref('counterfactual')
const enableTerm = ref(false)

const modelOptions = [
  { label: 'gemini', value: 'gemini' },
  { label: 'gpt-4', value: 'gpt-4' }
]

const strategyOptions = [
  { label: '反常识问题', value: 'counterfactual', desc:"为什么 TCP 握手不是两次、四次，而是三次？"},
  { label: '反向工程', value: 'reverse-engineering',desc:"你如何从现象反推 Redis 出现阻塞的根因？" },
  { label: '机制替代', value: 'mechanism-replacement',desc:"为什么 Go 要采用 CSP，而不是 Actor Model？" },
  { label: '边界与极限', value: 'boundary-case',desc:"在极端网络抖动环境下，TCP 的 TIME_WAIT 会发生什么变化？" },
  { label: '对比策略', value:'comparative-reason',desc:"在相同负载下，为什么 Kafka 的吞吐可以比 RabbitMQ 高？" },
  { label: '系统化问题', value: 'system-level-thinking',desc:"如果服务间依赖链增长，你的链路追踪方案如何保持可观测性？" },
  { label: '假设故障', value: 'failure-injection',desc:"如果 Redis 的热点 key 访问量突然增长 100 倍，你如何定位瓶颈？" },
  { label: '隐含代价', value: 'hidden-cost',desc:"为什么过度使用 goroutine 反而会降低性能？" },
  { label: '设计权衡', value: 'design-tradeoff',desc:"在分布式系统中，你如何在一致性和可用性间做权衡？" },
  { label: '架构演进', value: 'architecture-evolution',desc:"当单体应用无法满足需求时，你如何设计微服务架构？" },
  { label: '性能优化', value: 'performance-optimization',desc:"在高并发场景下，你如何优化数据库的读写性能？" },
  { label: '安全防护', value: 'security-hardening',desc:"你如何防范 SQL 注入攻击？" }
]

const renderStrategyLabel = (option: SelectOption) => {
  const desc = (option as SelectOption & { desc?: string }).desc
  return h('div', { class: 'strategy-option' }, [
    h('span', { class: 'strategy-option-label' }, String(option.label ?? '')),
    desc ? h('span', { class: 'strategy-option-desc' }, desc) : null
  ])
}
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

:global(.strategy-option) {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  width: 100%;
}

:global(.strategy-option-label) {
  font-size: 14px;
  color: #2e3445;
  flex-shrink: 0;
}

:global(.strategy-option-desc) {
  font-size: 11px;
  color: #9aa0a6;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
