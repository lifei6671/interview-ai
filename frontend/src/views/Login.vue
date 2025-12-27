<template>
  <div class="login-container">
    <n-card title="Login" style="max-width: 400px; width: 100%">
      <n-form
        ref="formRef"
        :model="model"
        :rules="rules"
        label-placement="left"
        label-width="auto"
      >
        <n-form-item label="Username" path="username">
          <n-input v-model:value="model.username" placeholder="Enter username" />
        </n-form-item>
        <n-form-item label="Password" path="password">
          <n-input
            v-model:value="model.password"
            type="password"
            show-password-on="click"
            placeholder="Enter password"
          />
        </n-form-item>
        <div style="display: flex; justify-content: flex-end">
          <n-button type="primary" @click="handleValidateButtonClick">
            Login
          </n-button>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, FormInst, FormItemRule } from 'naive-ui'

const router = useRouter()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const model = ref({
  username: '',
  password: ''
})

const rules = {
  username: {
    required: true,
    message: 'Please input your username',
    trigger: ['input', 'blur']
  },
  password: {
    required: true,
    message: 'Please input your password',
    trigger: ['input', 'blur']
  }
}

const handleValidateButtonClick = (e: MouseEvent) => {
  e.preventDefault()
  formRef.value?.validate((errors) => {
    if (!errors) {
      message.success('Login success')
      // Simulate login success
      setTimeout(() => {
        router.push('/')
      }, 500)
    } else {
      console.log(errors)
      message.error('Invalid inputs')
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
</style>
