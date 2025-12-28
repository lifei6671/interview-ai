<template>
  <n-layout-sider
    bordered
    width="320"
    content-style="padding: 24px;"
    collapse-mode="width"
    :native-scrollbar="false"
    style="height: 100vh"
  >
    <div class="logo-row">
      <div class="logo">
        <n-icon size="32" color="#18a058">
          <LogoOctocat />
        </n-icon>
        <span class="logo-text">Interview AI</span>
      </div>
      <div class="logo-actions">
        <n-popover
          v-model:show="showUserPopover"
          trigger="click"
          placement="bottom"
          :show-arrow="false"
          :content-style="{ padding: '0' }"
        >
          <template #trigger>
            <div class="avatar-trigger">
              <n-avatar round size="small" class="user-avatar" :src="avatarPreview || undefined">
                <n-icon v-if="!avatarPreview" size="20"><PersonCircleOutline /></n-icon>
              </n-avatar>
            </div>
          </template>
          <div class="user-panel">
            <div class="user-panel-header">
              <div class="user-panel-main">
                <n-avatar round size="medium" class="user-avatar" :src="avatarPreview || undefined">
                  <n-icon v-if="!avatarPreview" size="26"><PersonCircleOutline /></n-icon>
                </n-avatar>
                <div class="user-meta">
                  <div class="user-name">
                    倔强的贝吉塔
                    <span class="user-level">1</span>
                  </div>
                  <div class="user-desc">
                    AI 面试助手，使用手册点击
                    <span class="user-link">教程</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="user-panel-divider"></div>
            <div class="user-panel-list">
              <div class="panel-item" @click="handleOpenProfileModal">
                <n-icon size="18"><SettingsOutline /></n-icon>
                <span>个人设置</span>
              </div>
            </div>
            <div class="user-panel-divider"></div>
            <div class="panel-item logout">
              <n-icon size="18"><LogOutOutline /></n-icon>
              <span>退出登录</span>
            </div>
          </div>
        </n-popover>
      </div>
    </div>
    
    <n-menu
      :options="menuOptions"
      :value="activeKey"
      @update:value="handleUpdateValue"
    />

    <ProfileSettingsModal
      v-model:show="showProfileModal"
      :avatar-url="avatarPreview"
      :form="profileForm"
      :upload-handler="handleAvatarUpload"
      :z-index="2000"
      @save="handleProfileSave"
      @cancel="handleProfileCancel"
    />

    <AvatarCropModal
      v-model:show="showAvatarModal"
      :image-url="avatarEditingUrl"
      :upload-handler="handleAvatarUpload"
      :z-index="2100"
      @confirm="handleAvatarConfirm"
      @cancel="handleAvatarCancel"
    />

    <div class="footer-info">
      <div class="github-card">
        <div class="icon-box">
          <n-icon size="24"><LogoGithub /></n-icon>
        </div>
        <div class="card-content">
          <div class="star-badge">
            <n-icon size="12"><StarOutline /></n-icon>
            <span>1.3k stars</span>
          </div>
          <div class="card-desc">支持自部署，欢迎星标</div>
        </div>
      </div>
      <div class="about">
        <span>Paper Burner X | 关于</span>
      </div>
    </div>
  </n-layout-sider>
</template>

<script setup lang="ts">
import { h, ref, watch } from 'vue'
import { NIcon } from 'naive-ui'
import type { MenuOption, UploadCustomRequestOptions } from 'naive-ui'
import {
  DesktopOutline,
  TimeOutline,
  SettingsOutline,
  PersonCircleOutline,
  LogOutOutline,
  LogoGithub,
  LogoOctocat,
  StarOutline
} from '@vicons/ionicons5'
import { useRouter, useRoute } from 'vue-router'
import AvatarCropModal from '../components/AvatarCropModal.vue'
import ProfileSettingsModal from '../components/ProfileSettingsModal.vue'

const router = useRouter()
const route = useRoute()
const showUserPopover = ref(false)
const showProfileModal = ref(false)
const avatarPreview = ref('')
const avatarEditingUrl = ref('')
const showAvatarModal = ref(false)
const profileForm = ref({
  nickname: '倔强的贝吉塔',
  email: 'vegeta@example.com',
  oldPassword: '',
  newPassword: ''
})

const resolveMenuKey = (name: unknown) => {
  if (name === 'prompts-create') {
    return 'prompts'
  }
  return typeof name === 'string' ? name : 'dashboard'
}

const activeKey = ref<string>(resolveMenuKey(route.name))

watch(
  () => route.name,
  (name) => {
    activeKey.value = resolveMenuKey(name)
  }
)

watch(showProfileModal, (value) => {
  if (value) {
    showUserPopover.value = false
  }
})

function renderIcon(icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  {
    label: '工作台',
    key: 'dashboard',
    icon: renderIcon(DesktopOutline)
  },
  {
    label: '历史记录',
    key: 'history',
    icon: renderIcon(TimeOutline)
  },
  {
    label: '模型配置',
    key: 'settings',
    icon: renderIcon(SettingsOutline)
  },
  {
    label: 'Prompt 管理',
    key: 'prompts',
    icon: renderIcon(StarOutline)
  }
]

function handleUpdateValue(key: string) {
  activeKey.value = key
  if (key === 'dashboard' || key === 'history' || key === 'settings' || key === 'prompts') {
    router.push({ name: key })
  } else {
    // For demo purposes
    console.log('Navigate to', key)
  }
}

const handleOpenProfileModal = () => {
  showProfileModal.value = true
  showUserPopover.value = false
}

const handleAvatarUpload = (options: UploadCustomRequestOptions) => {
  const rawFile = options.file.file
  if (rawFile) {
    if (avatarEditingUrl.value) {
      URL.revokeObjectURL(avatarEditingUrl.value)
    }
    avatarEditingUrl.value = URL.createObjectURL(rawFile)
    showAvatarModal.value = true
  }
  options.onFinish()
}
const cleanupAvatarEditing = () => {
  if (avatarEditingUrl.value) {
    URL.revokeObjectURL(avatarEditingUrl.value)
    avatarEditingUrl.value = ''
  }
}

const handleProfileCancel = () => {
  showProfileModal.value = false
}

const handleProfileSave = () => {
  showProfileModal.value = false
}

const handleAvatarCancel = () => {
  showAvatarModal.value = false
  cleanupAvatarEditing()
}

const handleAvatarConfirm = (dataUrl: string) => {
  if (dataUrl) {
    avatarPreview.value = dataUrl
  }
  showAvatarModal.value = false
  cleanupAvatarEditing()
}
</script>

<style scoped>
.logo-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 24px;
  padding: 0 12px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
}

.logo-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-button {
  width: 32px;
  height: 32px;
  background-color: #f6f7fb;
  border-radius: 50%;
}

.avatar-trigger {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background-color: #f6f7fb;
  border: 1px solid #eef0f5;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #2e3445;
  display: flex;
  align-items: center;
  gap: 6px;
}

.user-level {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 8px;
  background-color: #f7c948;
  color: #fff;
  font-size: 10px;
  font-weight: 600;
}

.user-desc {
  font-size: 12px;
  color: #8a93a6;
}

.user-link {
  margin-left: 6px;
  color: #3b82f6;
  cursor: pointer;
}

.user-panel-divider {
  height: 1px;
  background-color: #eef0f5;
  margin: 12px 0;
}

.user-panel-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.panel-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 10px;
  color: #2e3445;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.panel-item:hover {
  background-color: #f6f7fb;
}

.panel-item.active {
  background-color: #f1f3f5;
  font-weight: 600;
}

.panel-item.logout {
  color: #4b5563;
}

.user-panel {
  width: 260px;
  padding: 5px;
  background-color: #fff;
}

.user-panel-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}

.user-panel-main {
  display: flex;
  gap: 12px;
  align-items: center;
}

.footer-info {
  position: absolute;
  bottom: 24px;
  left: 0;
  width: 100%;
  padding: 0 24px;
  font-size: 12px;
  color: #666;
}

.github-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: #f8f9fb;
  padding: 12px;
  border-radius: 12px;
  margin-bottom: 16px;
  border: 1px solid #f0f0f0;
}

.icon-box {
  width: 40px;
  height: 40px;
  background-color: #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.star-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background-color: #eef2f6;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #333;
  font-weight: 500;
  width: fit-content;
}

.card-desc {
  font-size: 12px;
  color: #666;
}

.about {
  text-align: center;
  color: #999;
}
</style>
