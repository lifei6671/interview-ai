<template>
  <div class="login-page">
    <div class="login-card">
      <div class="card-title">Interview AI 管理面板</div>
      <n-form ref="formRef" label-placement="top" :model="form" :rules="rules">
        <n-form-item label="邮箱" path="email">
          <n-input
            v-model:value="form.email"
            placeholder="请输入邮箱"
            @update:value="clearError"
            @keydown.enter.prevent="handleSubmit"
          />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input
            v-model:value="form.password"
            type="password"
            placeholder="请输入密码"
            @update:value="clearError"
            @keydown.enter.prevent="handleSubmit"
          />
        </n-form-item>
        <n-button type="primary" block :loading="submitting" @click="handleSubmit">
          登录
        </n-button>
        <div v-if="loginError" class="login-error">{{ loginError }}</div>
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInst, FormRules } from 'naive-ui'

const router = useRouter()
const formRef = ref<FormInst | null>(null)
const submitting = ref(false)
const loginError = ref('')

const form = ref({
  email: '',
  password: ''
})

const rules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: ['blur', 'input'] },
    { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'input'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: ['blur', 'input'] },
    { min: 6, message: '密码至少 6 位', trigger: ['blur', 'input'] }
  ]
}

const clearError = () => {
  loginError.value = ''
}

const handleSubmit = async () => {
  if (!formRef.value || submitting.value) {
    return
  }

  loginError.value = ''
  submitting.value = true

  try {
    await formRef.value.validate()
    await router.push('/')
  } catch (err) {
    loginError.value = '登录失败，请检查邮箱和密码'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-color: #f2f4f7;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  width: 360px;
  background-color: #fff;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.card-title {
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  color: #2b2f38;
  margin-bottom: 16px;
}

.login-error {
  margin-top: 8px;
  font-size: 12px;
  color: #d03050;
  text-align: center;
}

:deep(.n-form-item-label) {
  font-size: 12px;
  color: #666;
}
</style>
