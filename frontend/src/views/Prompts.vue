<template>
  <div class="prompt-page">
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <n-icon size="22" color="#5f7ce6">
            <DocumentTextOutline />
          </n-icon>
        </div>
        <div class="header-text">
          <div class="page-title">Prompt 管理</div>
          <div class="page-subtitle">管理你所有的Prompt</div>
        </div>
      </div>
    </div>

    <div class="prompt-body">
      <n-tabs v-model:value="activeTab" type="segment" size="small" class="prompt-tabs">
        <n-tab-pane name="preset" tab="预置模板" />
        <n-tab-pane name="custom" tab="自制模板" />
        <n-tab-pane name="favorite" tab="我的收藏" />
      </n-tabs>
      <div class="toolbar">
        <n-input v-model:value="searchQuery" round placeholder="输入模板名称、模板ID、内容检索">
          <template #prefix>
            <n-icon><SearchOutline /></n-icon>
          </template>
        </n-input>
        <div class="toolbar-actions">
          <n-dropdown :options="sortOptions" @select="handleSortSelect">
            <n-button quaternary size="small">
              {{ sortLabel }}
              <n-icon class="chevron-icon"><ChevronDownOutline /></n-icon>
            </n-button>
          </n-dropdown>
          <n-button type="primary" @click="handleCreate">
            <template #icon>
              <n-icon><AddOutline /></n-icon>
            </template>
            创建模板
          </n-button>
          <n-button quaternary circle @click="toggleView">
            <template #icon>
              <n-icon>
                <component :is="viewMode === 'grid' ? ListOutline : GridOutline" />
              </n-icon>
            </template>
          </n-button>
        </div>
      </div>

      <div v-if="viewMode === 'grid'" class="card-grid">
        <div v-for="item in pagedPrompts" :key="item.id" class="prompt-card">
          <div class="card-title">{{ item.title }}</div>
          <div class="card-desc">{{ item.content }}</div>
          <div class="card-tags">
            <n-tag size="small" :type="tagType(item.tag)">{{ item.tag }}</n-tag>
          </div>
          <div class="card-meta">
            <div class="meta-item">
              <n-icon size="14"><StarOutline /></n-icon>
              <span>{{ item.stars }}</span>
            </div>
            <div class="meta-item">
              <n-icon size="14"><EyeOutline /></n-icon>
              <span>{{ item.views }}</span>
            </div>
            <n-button text size="tiny">
              <template #icon>
                <n-icon><CopyOutline /></n-icon>
              </template>
              复制
            </n-button>
          </div>
        </div>
      </div>

      <div v-else class="table-wrapper">
        <table class="prompt-table">
          <thead>
            <tr>
              <th>模板名称</th>
              <th>模板标签</th>
              <th>浏览量</th>
              <th>模板内容</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in pagedPrompts" :key="item.id">
              <td class="title-cell">
                <span class="title-link">{{ item.title }}</span>
              </td>
              <td>
                <n-tag size="small" :type="tagType(item.tag)">{{ item.tag }}</n-tag>
              </td>
              <td>{{ item.views }}</td>
              <td class="content-cell">{{ item.content }}</td>
              <td>{{ item.createdAt }}</td>
              <td class="action-cell">
                <n-button text size="tiny">详情</n-button>
                <n-button text size="tiny">复制</n-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination">
        <div class="page-info">共 {{ totalCount }} 条</div>
        <n-pagination
          v-model:page="page"
          v-model:page-size="pageSize"
          :item-count="totalCount"
          :page-sizes="[12, 24, 36]"
          show-size-picker
          size="small"
        />
      </div>
     </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  DocumentTextOutline,
  SearchOutline,
  AddOutline,
  ChevronDownOutline,
  GridOutline,
  ListOutline,
  StarOutline,
  EyeOutline,
  CopyOutline
} from '@vicons/ionicons5'
import { prompts } from '../stores/promptStore'

const route = useRoute()
const router = useRouter()

const activeTab = ref<'preset' | 'custom' | 'favorite'>('preset')
const searchQuery = ref('')
const viewMode = ref<'grid' | 'list'>('grid')
const sortKey = ref<'default' | 'views' | 'stars'>('default')
const page = ref(1)
const pageSize = ref(12)

const sortOptions = [
  { label: '默认排序', key: 'default' },
  { label: '浏览量', key: 'views' },
  { label: '收藏数', key: 'stars' }
]

const setActiveTabFromQuery = (tab: unknown) => {
  if (tab === 'preset' || tab === 'custom' || tab === 'favorite') {
    activeTab.value = tab
  }
}

const filteredPrompts = computed(() => {
  const keyword = searchQuery.value.trim().toLowerCase()
  let list = prompts.value.filter((item) => item.type === activeTab.value)

  if (keyword) {
    list = list.filter(
      (item) =>
        item.title.toLowerCase().includes(keyword) || item.content.toLowerCase().includes(keyword)
    )
  }

  if (sortKey.value === 'views') {
    list = [...list].sort((a, b) => b.views - a.views)
  } else if (sortKey.value === 'stars') {
    list = [...list].sort((a, b) => b.stars - a.stars)
  }

  return list
})

const totalCount = computed(() => filteredPrompts.value.length)

const pagedPrompts = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return filteredPrompts.value.slice(start, start + pageSize.value)
})

const sortLabel = computed(() => {
  const selected = sortOptions.find((option) => option.key === sortKey.value)
  return selected ? selected.label : '默认排序'
})

const handleSortSelect = (key: 'default' | 'views' | 'stars') => {
  sortKey.value = key
}

const toggleView = () => {
  viewMode.value = viewMode.value === 'grid' ? 'list' : 'grid'
}

const handleCreate = () => {
  router.push({ name: 'prompts-create' })
}

const tagType = (tag: string) => {
  if (tag === '教育培训') return 'error'
  if (tag === '图像生成') return 'info'
  if (tag === '收藏') return 'success'
  return 'default'
}

watch(
  () => route.query.tab,
  (tab) => {
    setActiveTabFromQuery(tab)
  },
  { immediate: true }
)

watch([activeTab, searchQuery, sortKey, pageSize], () => {
  page.value = 1
})
</script>

<style scoped>
.prompt-page {
  height: 100%;
  background-color: #fff;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
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

.page-title {
  font-size: 18px;
  font-weight: 700;
  color: #2b2f38;
}

.page-subtitle {
  font-size: 12px;
  color: #8a93a6;
  margin-top: 4px;
}

.prompt-body {
  padding: 15px;
}

.prompt-tabs {
  margin-bottom: 16px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chevron-icon {
  margin-left: 6px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.prompt-card {
  border: 1px solid #eef0f5;
  border-radius: 12px;
  padding: 16px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 180px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #2e3445;
}

.card-desc {
  font-size: 12px;
  color: #8a93a6;
  line-height: 1.5;
  flex: 1;
}

.card-tags {
  display: flex;
  gap: 8px;
}

.card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: #7a8293;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.table-wrapper {
  border: 1px solid #eef0f5;
  border-radius: 12px;
  background-color: #fff;
  overflow: hidden;
}

.prompt-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.prompt-table th,
.prompt-table td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  text-align: left;
}

.prompt-table thead {
  background-color: #fafbff;
  color: #6b7280;
}

.prompt-table tbody tr:hover {
  background-color: #fafafa;
}

.title-cell {
  font-weight: 600;
  color: #2e3445;
}

.title-link {
  color: #4f46e5;
}

.content-cell {
  color: #8a93a6;
  max-width: 420px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-cell {
  display: flex;
  gap: 8px;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #6b7280;
  margin-top: 16px;
}

@media (max-width: 960px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-actions {
    justify-content: flex-end;
  }

  .content-cell {
    max-width: 240px;
  }
}
</style>
