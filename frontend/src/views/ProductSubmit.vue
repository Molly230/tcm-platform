<template>
  <div class="product-submit">
    <PageContainer>
      <div class="submit-header">
        <h2>产品提交</h2>
        <p class="header-desc">请填写完整的产品信息，提交后将进入审核流程</p>
      </div>

      <el-card class="submit-card" shadow="never">
        <el-form
          ref="submitForm"
          :model="productForm"
          :rules="formRules"
          label-width="120px"
          @submit.prevent
        >
          <!-- 基本信息 -->
          <div class="form-section">
            <h3 class="section-title">基本信息</h3>
            
            <el-form-item label="产品名称" prop="name" required>
              <el-input
                v-model="productForm.name"
                placeholder="请输入产品名称"
                maxlength="100"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="产品描述" prop="description">
              <el-input
                v-model="productForm.description"
                type="textarea"
                :rows="4"
                placeholder="请详细描述产品的特点、功效等"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="产品价格" prop="price" required>
              <el-input-number
                v-model="productForm.price"
                :precision="2"
                :step="0.01"
                :min="0.01"
                :max="99999.99"
                placeholder="0.00"
                style="width: 200px"
              />
              <span style="margin-left: 10px; color: #909399;">元</span>
            </el-form-item>

            <el-form-item label="原价">
              <el-input-number
                v-model="productForm.original_price"
                :precision="2"
                :step="0.01"
                :min="0.01"
                :max="99999.99"
                placeholder="0.00"
                style="width: 200px"
              />
              <span style="margin-left: 10px; color: #909399;">元（选填，用于显示折扣）</span>
            </el-form-item>

            <el-form-item label="库存数量" prop="stock_quantity" required>
              <el-input-number
                v-model="productForm.stock_quantity"
                :min="0"
                :max="99999"
                placeholder="0"
                style="width: 200px"
              />
              <span style="margin-left: 10px; color: #909399;">件</span>
            </el-form-item>
          </div>

          <!-- 产品详情 -->
          <div class="form-section">
            <h3 class="section-title">产品详情</h3>

            <el-form-item label="产品图片">
              <div class="image-upload-section">
                <el-upload
                  ref="imageUpload"
                  v-model:file-list="imageList"
                  :auto-upload="false"
                  :limit="5"
                  :on-change="handleImageChange"
                  :on-remove="handleImageRemove"
                  list-type="picture-card"
                  accept="image/*"
                >
                  <el-icon><Plus /></el-icon>
                </el-upload>
                <div class="upload-tip">
                  <p>• 最多上传5张图片</p>
                  <p>• 支持 JPG、PNG 格式</p>
                  <p>• 单张图片不超过5MB</p>
                  <p>• 建议尺寸：800x800像素</p>
                </div>
              </div>
            </el-form-item>

            <el-form-item label="功效特点">
              <div class="features-input">
                <el-tag
                  v-for="feature in productForm.features"
                  :key="feature"
                  closable
                  @close="removeFeature(feature)"
                  class="feature-tag"
                >
                  {{ feature }}
                </el-tag>
                <el-input
                  v-if="inputVisible"
                  ref="featureInput"
                  v-model="inputValue"
                  class="feature-input"
                  size="small"
                  @keyup.enter="addFeature"
                  @blur="addFeature"
                />
                <el-button v-else class="feature-add-btn" size="small" @click="showInput">
                  <el-icon><Plus /></el-icon>
                  添加功效
                </el-button>
              </div>
              <div class="form-tip">例如：补气、养血、增强免疫力等</div>
            </el-form-item>

            <el-form-item label="使用方法">
              <el-input
                v-model="productForm.usage_instructions"
                type="textarea"
                :rows="3"
                placeholder="请详细说明产品的使用方法、用量、注意事项等"
                maxlength="300"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="产品规格">
              <div class="specifications-section">
                <el-row :gutter="16">
                  <el-col :span="12">
                    <el-input
                      v-model="specKey"
                      placeholder="规格名称"
                      @keyup.enter="addSpecification"
                    />
                  </el-col>
                  <el-col :span="12">
                    <div style="display: flex; gap: 10px;">
                      <el-input
                        v-model="specValue"
                        placeholder="规格值"
                        @keyup.enter="addSpecification"
                      />
                      <el-button type="primary" @click="addSpecification">添加</el-button>
                    </div>
                  </el-col>
                </el-row>
                
                <div v-if="Object.keys(productForm.specifications).length > 0" class="spec-list">
                  <div
                    v-for="[key, value] in Object.entries(productForm.specifications)"
                    :key="key"
                    class="spec-item"
                  >
                    <span>{{ key }}: {{ value }}</span>
                    <el-button
                      type="danger"
                      link
                      size="small"
                      @click="removeSpecification(key)"
                    >
                      删除
                    </el-button>
                  </div>
                </div>
              </div>
            </el-form-item>
          </div>

          <!-- 提交信息 -->
          <div class="form-section">
            <h3 class="section-title">提交信息</h3>
            
            <el-form-item label="提交人" prop="submitted_by" required>
              <el-input
                v-model="productForm.submitted_by"
                placeholder="请输入您的姓名或团队名称"
                maxlength="50"
              />
            </el-form-item>

            <el-form-item label="联系方式">
              <el-input
                v-model="contactInfo"
                placeholder="请输入邮箱或电话，便于审核沟通"
                maxlength="100"
              />
            </el-form-item>

            <el-form-item label="备注说明">
              <el-input
                v-model="productForm.audit_notes"
                type="textarea"
                :rows="3"
                placeholder="其他需要说明的信息（选填）"
                maxlength="200"
                show-word-limit
              />
            </el-form-item>
          </div>

          <!-- 提交按钮 -->
          <div class="submit-actions">
            <el-button size="large" @click="resetForm">重置</el-button>
            <el-button
              type="primary"
              size="large"
              :loading="submitting"
              @click="submitProduct"
            >
              提交审核
            </el-button>
          </div>
        </el-form>
      </el-card>

      <!-- 提交历史 -->
      <el-card v-if="submittedProducts.length > 0" class="history-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>提交历史</span>
            <el-button text @click="loadSubmittedProducts">刷新</el-button>
          </div>
        </template>

        <el-table :data="submittedProducts" stripe>
          <el-table-column prop="name" label="产品名称" min-width="150" />
          <el-table-column prop="price" label="价格" width="100">
            <template #default="{ row }">¥{{ row.price }}</template>
          </el-table-column>
          <el-table-column prop="submitted_at" label="提交时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.submitted_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="audit_status" label="审核状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.audit_status)">
                {{ getStatusText(row.audit_status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="reviewed_at" label="审核时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.reviewed_at) }}
            </template>
          </el-table-column>
          <el-table-column label="审核备注" min-width="200">
            <template #default="{ row }">
              {{ row.audit_notes || '-' }}
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import PageContainer from '../components/PageContainer.vue'

// 响应式数据
const submitting = ref(false)
const imageList = ref<any[]>([])
const submittedProducts = ref<any[]>([])

// 功效标签相关
const inputVisible = ref(false)
const inputValue = ref('')
const featureInput = ref()

// 规格相关
const specKey = ref('')
const specValue = ref('')
const contactInfo = ref('')

// 表单数据
const productForm = reactive({
  name: '',
  description: '',
  price: null as number | null,
  original_price: null as number | null,
  stock_quantity: null as number | null,
  images: [] as string[],
  features: [] as string[],
  usage_instructions: '',
  specifications: {} as Record<string, string>,
  submitted_by: '',
  audit_notes: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' },
    { min: 2, max: 100, message: '产品名称长度应为2-100个字符', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入产品价格', trigger: 'blur' }
  ],
  stock_quantity: [
    { required: true, message: '请输入库存数量', trigger: 'blur' }
  ],
  submitted_by: [
    { required: true, message: '请输入提交人信息', trigger: 'blur' },
    { min: 2, max: 50, message: '提交人信息长度应为2-50个字符', trigger: 'blur' }
  ]
}

// 方法
const handleImageChange = (file: any) => {
  // 模拟图片上传，实际应用中需要上传到服务器
  const reader = new FileReader()
  reader.onload = (e) => {
    productForm.images.push(e.target?.result as string)
  }
  reader.readAsDataURL(file.raw)
}

const handleImageRemove = (file: any) => {
  const index = imageList.value.findIndex(item => item.uid === file.uid)
  if (index > -1) {
    productForm.images.splice(index, 1)
  }
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    featureInput.value?.focus()
  })
}

const addFeature = () => {
  if (inputValue.value && !productForm.features.includes(inputValue.value)) {
    productForm.features.push(inputValue.value)
    inputValue.value = ''
  }
  inputVisible.value = false
}

const removeFeature = (feature: string) => {
  const index = productForm.features.indexOf(feature)
  if (index > -1) {
    productForm.features.splice(index, 1)
  }
}

const addSpecification = () => {
  if (specKey.value && specValue.value) {
    productForm.specifications[specKey.value] = specValue.value
    specKey.value = ''
    specValue.value = ''
  }
}

const removeSpecification = (key: string) => {
  delete productForm.specifications[key]
}

const submitProduct = async () => {
  const submitForm = ref()
  if (!submitForm.value) return

  try {
    await submitForm.value.validate()
  } catch (error) {
    ElMessage.error('请完善表单信息')
    return
  }

  submitting.value = true
  try {
    const response = await fetch('/api/products/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...productForm,
        category: 'PRODUCT'
      })
    })

    if (response.ok) {
      ElMessage.success('产品提交成功，请等待审核')
      resetForm()
      loadSubmittedProducts()
    } else {
      const error = await response.json()
      ElMessage.error(error.detail || '提交失败，请重试')
    }
  } catch (error) {
    console.error('提交产品失败:', error)
    ElMessage.error('提交失败，请检查网络连接')
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  Object.assign(productForm, {
    name: '',
    description: '',
    price: null,
    original_price: null,
    stock_quantity: null,
    images: [],
    features: [],
    usage_instructions: '',
    specifications: {},
    submitted_by: '',
    audit_notes: ''
  })
  imageList.value = []
  contactInfo.value = ''
}

const loadSubmittedProducts = async () => {
  try {
    // 实际应用中需要根据提交人过滤
    const response = await fetch('/api/products/pending')
    if (response.ok) {
      submittedProducts.value = await response.json()
    }
  } catch (error) {
    console.error('加载提交历史失败:', error)
  }
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    revision: 'info'
  }
  return map[status] || ''
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    revision: '需修改'
  }
  return map[status] || status
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadSubmittedProducts()
})
</script>

<style scoped>
.product-submit {
  padding: 20px;
}

.submit-header {
  margin-bottom: 24px;
}

.submit-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.header-desc {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.submit-card, .history-card {
  margin-bottom: 24px;
}

.form-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #ebeef5;
}

.form-section:last-child {
  border-bottom: none;
}

.section-title {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.image-upload-section {
  display: flex;
  gap: 16px;
}

.upload-tip {
  color: #909399;
  font-size: 12px;
  line-height: 1.5;
}

.upload-tip p {
  margin: 0;
}

.features-input {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.feature-tag {
  margin: 0;
}

.feature-input {
  width: 120px;
}

.feature-add-btn {
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-tip {
  margin-top: 4px;
  color: #909399;
  font-size: 12px;
}

.specifications-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.spec-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.spec-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.submit-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-card :deep(.el-card__body) {
  padding: 0;
}
</style>