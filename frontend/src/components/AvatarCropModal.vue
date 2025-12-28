<template>
  <n-modal
    :show="show"
    :mask-closable="false"
    :auto-focus="false"
    :z-index="modalZIndex"
    @update:show="emit('update:show', $event)"
  >
    <div class="avatar-modal">
      <div class="avatar-modal-header">
        <div class="avatar-modal-title">编辑头像</div>
        <n-button quaternary circle size="small" @click="handleCancel">
          <template #icon>
            <n-icon size="18"><CloseOutline /></n-icon>
          </template>
        </n-button>
      </div>
      <div class="avatar-modal-body">
        <div class="avatar-crop-panel">
          <canvas
            ref="cropCanvas"
            class="crop-canvas"
            width="280"
            height="280"
            @mousedown="handleCropStart"
            @mousemove="handleCropMove"
            @mouseup="handleCropEnd"
            @mouseleave="handleCropEnd"
            @wheel.prevent="handleWheelZoom"
          ></canvas>
          <div class="crop-tools">
            <n-upload
              accept="image/*"
              :show-file-list="false"
              :custom-request="uploadHandler"
            >
              <n-button size="small" secondary>
                <template #icon>
                  <n-icon size="16"><RefreshOutline /></n-icon>
                </template>
                重新选择
              </n-button>
            </n-upload>
          </div>
        </div>
        <div class="avatar-preview-panel">
          <canvas ref="previewCanvas" class="preview-canvas" width="120" height="120"></canvas>
          <div class="preview-label">预览</div>
        </div>
      </div>
      <div class="avatar-modal-footer">
        <n-button size="small" @click="handleCancel">取消</n-button>
        <n-button type="primary" size="small" @click="handleConfirm">确定</n-button>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, toRefs, watch } from 'vue'
import type { UploadCustomRequestOptions } from 'naive-ui'
import { CloseOutline, RefreshOutline } from '@vicons/ionicons5'

const props = defineProps<{
  show: boolean
  imageUrl: string
  uploadHandler: (options: UploadCustomRequestOptions) => void
  zIndex?: number
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'confirm', value: string): void
  (e: 'cancel'): void
}>()

const { show, uploadHandler } = toRefs(props)
const modalZIndex = computed(() => props.zIndex ?? 2100)

const cropCanvas = ref<HTMLCanvasElement | null>(null)
const previewCanvas = ref<HTMLCanvasElement | null>(null)
const cropZoom = ref(1)
const lastZoom = ref(1)
const cropOffset = ref({ x: 0, y: 0 })
const cropBaseScale = ref(1)
const cropImage = ref<HTMLImageElement | null>(null)
const isDragging = ref(false)
const dragPoint = ref({ x: 0, y: 0 })
const cropSize = 280
const lastImageUrl = ref('')

const drawCropCanvas = () => {
  if (!cropCanvas.value || !cropImage.value) {
    return
  }

  const ctx = cropCanvas.value.getContext('2d')
  if (!ctx) {
    return
  }

  const scale = cropBaseScale.value * cropZoom.value
  const scaledWidth = cropImage.value.width * scale
  const scaledHeight = cropImage.value.height * scale
  const minX = cropSize - scaledWidth
  const minY = cropSize - scaledHeight

  cropOffset.value = {
    x: Math.min(0, Math.max(minX, cropOffset.value.x)),
    y: Math.min(0, Math.max(minY, cropOffset.value.y))
  }

  ctx.clearRect(0, 0, cropSize, cropSize)
  ctx.drawImage(
    cropImage.value,
    cropOffset.value.x,
    cropOffset.value.y,
    scaledWidth,
    scaledHeight
  )

  if (previewCanvas.value) {
    const previewCtx = previewCanvas.value.getContext('2d')
    if (previewCtx) {
      const size = previewCanvas.value.width
      previewCtx.clearRect(0, 0, size, size)
      previewCtx.drawImage(cropCanvas.value, 0, 0, cropSize, cropSize, 0, 0, size, size)
    }
  }
}

const loadAvatarImage = async (url: string) => {
  const img = new Image()
  img.onload = async () => {
    cropImage.value = img
    cropBaseScale.value = Math.max(cropSize / img.width, cropSize / img.height)
    cropZoom.value = 1
    lastZoom.value = 1
    cropOffset.value = {
      x: (cropSize - img.width * cropBaseScale.value) / 2,
      y: (cropSize - img.height * cropBaseScale.value) / 2
    }
    await nextTick()
    drawCropCanvas()
  }
  img.src = url
}

const resetCropState = () => {
  cropImage.value = null
  cropZoom.value = 1
  lastZoom.value = 1
  cropOffset.value = { x: 0, y: 0 }
  cropBaseScale.value = 1
  lastImageUrl.value = ''
  if (cropCanvas.value) {
    const ctx = cropCanvas.value.getContext('2d')
    ctx?.clearRect(0, 0, cropSize, cropSize)
  }
  if (previewCanvas.value) {
    const ctx = previewCanvas.value.getContext('2d')
    ctx?.clearRect(0, 0, previewCanvas.value.width, previewCanvas.value.height)
  }
}

const handleCropStart = (event: MouseEvent) => {
  if (!cropImage.value) {
    return
  }
  isDragging.value = true
  dragPoint.value = { x: event.clientX, y: event.clientY }
}

const handleCropMove = (event: MouseEvent) => {
  if (!isDragging.value) {
    return
  }
  const deltaX = event.clientX - dragPoint.value.x
  const deltaY = event.clientY - dragPoint.value.y
  dragPoint.value = { x: event.clientX, y: event.clientY }
  cropOffset.value = {
    x: cropOffset.value.x + deltaX,
    y: cropOffset.value.y + deltaY
  }
  drawCropCanvas()
}

const handleCropEnd = () => {
  isDragging.value = false
}

const handleZoomChange = (value: number) => {
  if (!cropImage.value) {
    return
  }
  const previousScale = cropBaseScale.value * lastZoom.value
  const nextScale = cropBaseScale.value * value
  const centerX = (cropSize / 2 - cropOffset.value.x) / previousScale
  const centerY = (cropSize / 2 - cropOffset.value.y) / previousScale
  cropZoom.value = value
  lastZoom.value = value
  cropOffset.value = {
    x: cropSize / 2 - centerX * nextScale,
    y: cropSize / 2 - centerY * nextScale
  }
  drawCropCanvas()
}

const handleWheelZoom = (event: WheelEvent) => {
  if (!cropImage.value) {
    return
  }
  const direction = event.deltaY > 0 ? -1 : 1
  const nextZoom = Math.min(3, Math.max(1, cropZoom.value + direction * 0.06))
  handleZoomChange(nextZoom)
}

const handleCancel = () => {
  emit('cancel')
  emit('update:show', false)
}

const handleConfirm = () => {
  if (!cropCanvas.value) {
    return
  }
  emit('confirm', cropCanvas.value.toDataURL('image/png'))
  emit('update:show', false)
}

watch(
  () => [props.show, props.imageUrl],
  ([show, url]) => {
    if (!show) {
      resetCropState()
      return
    }
    if (url && url !== lastImageUrl.value) {
      lastImageUrl.value = url
      loadAvatarImage(url)
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.avatar-modal {
  width: 560px;
  background-color: #fff;
  border-radius: 16px;
  padding: 20px 20px 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.avatar-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.avatar-modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #2e3445;
}

.avatar-modal-body {
  display: flex;
  gap: 24px;
}

.avatar-crop-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.crop-canvas {
  width: 280px;
  height: 280px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background-color: #f6f7fb;
  cursor: grab;
}

.crop-canvas:active {
  cursor: grabbing;
}

.crop-tools {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.zoom-hint {
  font-size: 12px;
  color: #6b7280;
}

.avatar-preview-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.preview-canvas {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.preview-label {
  font-size: 12px;
  color: #8a93a6;
}

.avatar-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>
