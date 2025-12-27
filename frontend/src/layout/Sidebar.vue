<template>
  <n-layout-sider
    bordered
    width="320"
    content-style="padding: 24px;"
    collapse-mode="width"
    :native-scrollbar="false"
    style="height: 100vh"
  >
    <div class="logo">
      <n-icon size="32" color="#18a058">
        <LogoOctocat />
      </n-icon>
      <span class="logo-text">Interview AI</span>
    </div>
    
    <n-menu
      :options="menuOptions"
      :value="activeKey"
      @update:value="handleUpdateValue"
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
import type { MenuOption } from 'naive-ui'
import {
  DesktopOutline,
  TimeOutline,
  SettingsOutline,
  LogoGithub,
  LogoOctocat,
  StarOutline
} from '@vicons/ionicons5'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

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
</script>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding: 0 12px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
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
