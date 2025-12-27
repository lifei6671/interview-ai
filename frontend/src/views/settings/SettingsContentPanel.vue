<template>
  <component :is="activeComponent" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SettingsVolcano from './SettingsVolcano.vue'
import SettingsCustom from './SettingsCustom.vue'
import SettingsDeepseek from './SettingsDeepseek.vue'
import SettingsGemini from './SettingsGemini.vue'
import SettingsOpenai from './SettingsOpenai.vue'
import SettingsTongyi from './SettingsTongyi.vue'

const props = defineProps<{ activeKey: string }>()

const componentMap = {
  volcano: SettingsVolcano,
  custom: SettingsCustom,
  deepseek: SettingsDeepseek,
  gemini: SettingsGemini,
  openai: SettingsOpenai,
  tongyi: SettingsTongyi
} as const

const activeComponent = computed(() => componentMap[props.activeKey] ?? SettingsVolcano)
</script>
