<template>
  <n-modal
    :show="show"
    :mask-closable="true"
    :auto-focus="false"
    :z-index="zIndex"
    @update:show="emit('update:show', $event)"
  >
    <div class="profile-modal">
      <div class="profile-modal-header">
        <div class="profile-modal-title">个人设置</div>
        <n-button quaternary circle size="small" @click="handleCancel">
          <template #icon>
            <n-icon size="16"><CloseOutline /></n-icon>
          </template>
        </n-button>
      </div>
      <n-form ref="formRef" :model="form" :rules="rules" label-placement="top" size="small">
        <n-form-item label="头像">
          <n-upload accept="image/*" :show-file-list="false" :custom-request="uploadHandler">
            <div class="avatar-upload">
              <n-avatar round size="large" class="user-avatar" :src="avatarUrl || undefined">
                <n-icon v-if="!avatarUrl" size="24">
                  <PersonCircleOutline />
                </n-icon>
              </n-avatar>
              <span class="avatar-upload-text">点击上传头像</span>
            </div>
          </n-upload>
        </n-form-item>
        <n-form-item label="昵称" path="nickname">
          <n-input v-model:value="form.nickname" placeholder="请输入昵称" />
        </n-form-item>
        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="form.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="原密码" path="oldPassword">
          <n-input v-model:value="form.oldPassword" type="password" placeholder="请输入原密码" />
        </n-form-item>
        <n-form-item label="新密码" path="newPassword">
          <n-input v-model:value="form.newPassword" type="password" placeholder="请输入新密码" />
        </n-form-item>
        <div class="profile-actions">
          <n-button size="small" @click="handleCancel">取消</n-button>
          <n-button type="primary" size="small" @click="handleSave">保存</n-button>
        </div>
      </n-form>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { computed, ref, toRefs } from 'vue'
import type { FormInst, FormRules, UploadCustomRequestOptions } from 'naive-ui'
import { CloseOutline, PersonCircleOutline } from '@vicons/ionicons5'

const props = defineProps<{
  show: boolean
  avatarUrl: string
  form: {
    nickname: string
    email: string
    oldPassword: string
    newPassword: string
  }
  uploadHandler: (options: UploadCustomRequestOptions) => void
  zIndex?: number
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'save', value: {
    nickname: string
    email: string
    oldPassword: string
    newPassword: string
  }): void
  (e: 'cancel'): void
}>()

const { form, show } = toRefs(props)
const zIndex = computed(() => props.zIndex ?? 2000)
const formRef = ref<FormInst | null>(null)

const rules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: ['blur', 'input'] },
    { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'input'] }
  ],
  oldPassword: [{ required: true, message: '请输入原密码', trigger: ['blur', 'input'] }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: ['blur', 'input'] },
    { min: 6, message: '密码至少 6 位', trigger: ['blur', 'input'] }
  ]
}

const handleCancel = () => {
  emit('cancel')
  emit('update:show', false)
}

const handleSave = async () => {
  if (!formRef.value) {
    return
  }
  try {
    await formRef.value.validate()
    emit('save', { ...form.value })
    emit('update:show', false)
  } catch {
    // Validation handled by form
  }
}
</script>

<style scoped>
.profile-modal {
  width: 360px;
  background-color: #fff;
  border-radius: 16px;
  padding: 20px 20px 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.profile-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.profile-modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #2e3445;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.avatar-upload-text {
  font-size: 12px;
  color: #6b7280;
}

.profile-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
</style>
