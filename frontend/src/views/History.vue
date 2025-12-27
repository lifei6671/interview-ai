<template>
  <div class="history-container">
    <div class="history-header">
      <div class="header-left">
        <n-icon size="24" color="#8a5ee0" class="header-icon">
          <TimeOutline />
        </n-icon>
        <div class="header-text">
          <div class="title">历史记录</div>
          <div class="subtitle">查看和管理您处理过的文档</div>
        </div>
      </div>
    </div>

    <div class="history-content">
      <div class="sidebar">
        <div class="sidebar-header">
          <span>文件夹</span>
          <n-button text class="add-btn" @click="showAddModal = true">
            <template #icon>
              <n-icon><AddOutline /></n-icon>
            </template>
          </n-button>
        </div>

        <div class="folder-list">
          <!-- Fixed Folders -->
          <div
            v-for="folder in fixedFolders"
            :key="folder.id"
            class="folder-item"
            :class="{ active: currentFolderId === folder.id }"
            @click="currentFolderId = folder.id"
          >
            <span class="folder-name">{{ folder.name }}</span>
            <span class="folder-count">{{ folder.count }}</span>
          </div>

          <!-- Custom Folders -->
          <div
            v-for="folder in customFolders"
            :key="folder.id"
            class="folder-item custom-folder"
            :class="{ active: currentFolderId === folder.id }"
            @click="currentFolderId = folder.id"
          >
            <div class="folder-info">
              <span class="folder-name">{{ folder.name }}</span>
              <span class="folder-count">{{ folder.count }}</span>
            </div>
            <div class="folder-actions">
              <n-button text size="tiny" @click.stop="handleEdit(folder)">
                <template #icon><n-icon><PencilOutline /></n-icon></template>
              </n-button>
              <n-button text size="tiny" @click.stop="handleDelete(folder)">
                <template #icon><n-icon><TrashOutline /></n-icon></template>
              </n-button>
            </div>
          </div>
        </div>
      </div>

      <div class="main-area">
        <div class="search-bar">
          <n-input placeholder="搜索文档标题、内容或 OCR 结果..." round>
            <template #prefix>
              <n-icon><SearchOutline /></n-icon>
            </template>
          </n-input>
        </div>

        <div class="empty-state">
          <div class="empty-text">暂无历史记录</div>
        </div>

        <div class="footer-action">
          <n-button text type="error" @click="handleClearAll">
            <template #icon><n-icon><TrashOutline /></n-icon></template>
            清空所有历史记录
          </n-button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Folder Modal -->
    <n-modal
      v-model:show="showModal"
      preset="dialog"
      :title="modalMode === 'add' ? '新建文件夹' : '重命名文件夹'"
      :positive-text="modalMode === 'add' ? '创建' : '保存'"
      negative-text="取消"
      @positive-click="handleModalSubmit"
      @negative-click="showModal = false"
    >
      <n-input
        v-model:value="folderNameInput"
        placeholder="请输入文件夹名称"
        @keyup.enter="handleModalSubmit"
      />
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  TimeOutline,
  AddOutline,
  PencilOutline,
  TrashOutline,
  SearchOutline
} from '@vicons/ionicons5'
import { useMessage, useDialog } from 'naive-ui'

interface Folder {
  id: string
  name: string
  count: number
  isCustom: boolean
}

const router = useRouter()
const message = useMessage()
const dialog = useDialog()

// State
const currentFolderId = ref('all')
const showModal = ref(false)
const modalMode = ref<'add' | 'edit'>('add')
const folderNameInput = ref('')
const editingFolderId = ref<string | null>(null)

// Data
const fixedFolders = ref<Folder[]>([
  { id: 'all', name: '全部记录', count: 0, isCustom: false },
  { id: 'uncategorized', name: '未分组', count: 0, isCustom: false }
])

const customFolders = ref<Folder[]>([
  { id: '1', name: 'orcl', count: 0, isCustom: true }
])

// Computed for modal visibility control
const showAddModal = computed({
  get: () => showModal.value && modalMode.value === 'add',
  set: (val) => {
    if (val) {
      modalMode.value = 'add'
      folderNameInput.value = ''
      showModal.value = true
    } else {
      showModal.value = false
    }
  }
})


const handleEdit = (folder: Folder) => {
  modalMode.value = 'edit'
  editingFolderId.value = folder.id
  folderNameInput.value = folder.name
  showModal.value = true
}

const handleDelete = (folder: Folder) => {
  dialog.warning({
    title: '删除文件夹',
    content: `确定要删除文件夹 "${folder.name}" 吗？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: () => {
      customFolders.value = customFolders.value.filter(f => f.id !== folder.id)
      if (currentFolderId.value === folder.id) {
        currentFolderId.value = 'all'
      }
      message.success('删除成功')
    }
  })
}

const handleModalSubmit = () => {
  if (!folderNameInput.value.trim()) {
    message.warning('请输入文件夹名称')
    return false
  }

  if (modalMode.value === 'add') {
    const newFolder: Folder = {
      id: Date.now().toString(),
      name: folderNameInput.value,
      count: 0,
      isCustom: true
    }
    customFolders.value.push(newFolder)
    message.success('创建成功')
  } else {
    const folder = customFolders.value.find(f => f.id === editingFolderId.value)
    if (folder) {
      folder.name = folderNameInput.value
      message.success('修改成功')
    }
  }
  showModal.value = false
  return true
}

const handleClearAll = () => {
  dialog.error({
    title: '清空历史记录',
    content: '确定要清空所有历史记录吗？此操作不可恢复。',
    positiveText: '确定清空',
    negativeText: '取消',
    onPositiveClick: () => {
      message.success('已清空所有记录')
    }
  })
}
</script>

<style scoped>
.history-container {
  height: 100%;
  background-color: #fff;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.history-header {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left {
  display: flex;
  gap: 12px;
}

.header-icon {
  margin-top: 4px;
  background-color: #f3f0ff;
  padding: 8px;
  border-radius: 8px;
  box-sizing: content-box;
}

.header-text .title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.header-text .subtitle {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.history-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.sidebar {
  width: 240px;
  border-right: 1px solid #f0f0f0;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-weight: bold;
  color: #666;
  padding: 0 8px;
}

.folder-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.folder-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
}

.folder-item:hover {
  background-color: #f5f7fa;
}

.folder-item.active {
  background-color: #eef2ff;
  color: #5e7ce0;
}

.folder-count {
  background-color: #f0f0f0;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  color: #999;
}

.custom-folder {
  position: relative;
}

.custom-folder .folder-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
}

.custom-folder .folder-actions {
  display: none;
  position: absolute;
  right: 8px;
  background-color: inherit;
}

.custom-folder:hover .folder-actions {
  display: flex;
  gap: 4px;
}

.custom-folder:hover .folder-info .folder-count {
  display: none;
}

.main-area {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
  background-color: #fff;
}

.search-bar {
  margin-bottom: 40px;
}

.empty-state {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ccc;
  font-size: 16px;
}

.footer-action {
  display: flex;
  justify-content: center;
  padding-top: 20px;
}

.footer-action :deep(.n-button) {
  background-color: #fff0f0;
  width: 100%;
  height: 48px;
  border-radius: 8px;
}

.footer-action :deep(.n-button:hover) {
  background-color: #ffdede;
}
</style>
