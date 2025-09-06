<template>
  <div class="test-upload">
    <h2>文件上传测试</h2>
    
    <div class="upload-section">
      <h3>图片上传测试</h3>
      <el-upload
        class="upload-demo"
        :action="uploadUrl"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        name="file"
      >
        <el-button type="primary">点击上传图片</el-button>
        <template #tip>
          <div class="el-upload__tip">
            只能上传jpg/png文件，且不超过2MB
          </div>
        </template>
      </el-upload>
      
      <div v-if="uploadedImageUrl" class="uploaded-result">
        <p>上传成功！</p>
        <img :src="uploadedImageUrl" alt="上传的图片" style="max-width: 200px; max-height: 200px;" />
        <p>图片URL: {{ uploadedImageUrl }}</p>
      </div>
    </div>

    <div class="upload-section">
      <h3>手动测试上传API</h3>
      <input type="file" ref="fileInput" accept="image/*" @change="handleFileSelect" />
      <el-button @click="testManualUpload" :loading="uploading">手动上传测试</el-button>
      
      <div v-if="manualResult" class="manual-result">
        <h4>上传结果:</h4>
        <pre>{{ JSON.stringify(manualResult, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const uploadUrl = 'http://localhost:8000/api/upload/image'
const uploadedImageUrl = ref('')
const fileInput = ref()
const selectedFile = ref(null)
const uploading = ref(false)
const manualResult = ref(null)

const handleUploadSuccess = (response: any) => {
  console.log('Upload success:', response)
  if (response.success && response.file_url) {
    uploadedImageUrl.value = `http://localhost:8000${response.file_url}`
    ElMessage.success('图片上传成功!')
  } else {
    ElMessage.error('上传失败：' + (response.message || '未知错误'))
  }
}

const handleUploadError = (error: any) => {
  console.error('Upload error:', error)
  ElMessage.error('上传失败，请检查网络连接和API服务')
}

const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('上传文件大小不能超过 2MB!')
    return false
  }
  return true
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
  }
}

const testManualUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.error('请先选择一个文件')
    return
  }

  uploading.value = true
  manualResult.value = null

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    console.log('开始上传文件:', selectedFile.value.name)

    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData
    })

    console.log('响应状态:', response.status)
    console.log('响应头:', Object.fromEntries(response.headers.entries()))

    if (!response.ok) {
      const errorText = await response.text()
      console.error('HTTP错误:', errorText)
      throw new Error(`HTTP ${response.status}: ${errorText}`)
    }

    const result = await response.json()
    console.log('上传结果:', result)

    manualResult.value = result

    if (result.success) {
      ElMessage.success('手动上传成功!')
      if (result.file_url) {
        uploadedImageUrl.value = `http://localhost:8000${result.file_url}`
      }
    } else {
      ElMessage.error('上传失败：' + (result.message || '未知错误'))
    }
  } catch (error) {
    console.error('上传过程出错:', error)
    manualResult.value = { error: error.message }
    ElMessage.error('上传失败: ' + error.message)
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.test-upload {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.upload-section {
  margin-bottom: 40px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
}

.uploaded-result, .manual-result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

pre {
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

input[type="file"] {
  margin-bottom: 10px;
}
</style>