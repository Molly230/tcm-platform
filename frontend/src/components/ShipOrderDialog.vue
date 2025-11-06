<template>
  <el-dialog
    v-model="dialogVisible"
    title="📦 订单发货"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="120px"
      label-position="right"
    >
      <el-form-item label="订单信息">
        <div class="order-info">
          <div class="info-item">
            <span class="label">订单号：</span>
            <span class="value">{{ order?.order_number }}</span>
          </div>
          <div class="info-item">
            <span class="label">订单金额：</span>
            <span class="value">¥{{ order?.total_amount }}</span>
          </div>
        </div>
      </el-form-item>

      <el-form-item label="物流公司" prop="courier_company" required>
        <el-select
          v-model="formData.courier_company"
          placeholder="请选择物流公司"
          filterable
          style="width: 100%"
        >
          <el-option
            v-for="company in courierCompanies"
            :key="company.code"
            :label="company.zh"
            :value="company.code"
          >
            <div class="company-option">
              <span>{{ company.zh }}</span>
              <span class="company-en">{{ company.en }}</span>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="物流单号" prop="tracking_number" required>
        <el-input
          v-model="formData.tracking_number"
          placeholder="请输入物流单号"
          clearable
        />
      </el-form-item>

      <el-form-item label="配送员姓名" prop="courier_name">
        <el-input
          v-model="formData.courier_name"
          placeholder="请输入配送员姓名（选填）"
          clearable
        />
      </el-form-item>

      <el-form-item label="配送员电话" prop="courier_phone">
        <el-input
          v-model="formData.courier_phone"
          placeholder="请输入配送员电话（选填）"
          clearable
        />
      </el-form-item>

      <el-form-item label="备注" prop="notes">
        <el-input
          v-model="formData.notes"
          type="textarea"
          :rows="3"
          placeholder="请输入发货备注（选填）"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确认发货
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

interface Order {
  id: number
  order_number: string
  total_amount: number
  status: string
}

interface CourierCompany {
  code: string
  zh: string
  en: string
}

interface Props {
  visible: boolean
  order: Order | null
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const formRef = ref<FormInstance>()
const submitting = ref(false)

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const formData = reactive({
  courier_company: '',
  tracking_number: '',
  courier_name: '',
  courier_phone: '',
  notes: ''
})

// 快递公司列表（从后端获取或硬编码）
const courierCompanies = ref<CourierCompany[]>([
  { code: 'SF', zh: '顺丰速运', en: 'SF Express' },
  { code: 'ZTO', zh: '中通快递', en: 'ZTO Express' },
  { code: 'YTO', zh: '圆通速递', en: 'YTO Express' },
  { code: 'STO', zh: '申通快递', en: 'STO Express' },
  { code: 'YD', zh: '韵达快递', en: 'Yunda Express' },
  { code: 'JTSD', zh: '极兔速递', en: 'J&T Express' },
  { code: 'JD', zh: '京东物流', en: 'JD Logistics' },
  { code: 'EMS', zh: '邮政EMS', en: 'China EMS' },
  { code: 'DBKD', zh: '德邦快递', en: 'Deppon' }
])

const rules: FormRules = {
  courier_company: [
    { required: true, message: '请选择物流公司', trigger: 'change' }
  ],
  tracking_number: [
    { required: true, message: '请输入物流单号', trigger: 'blur' },
    { min: 6, max: 50, message: '物流单号长度在 6 到 50 个字符', trigger: 'blur' }
  ],
  courier_phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号码',
      trigger: 'blur'
    }
  ]
}

const handleClose = () => {
  formRef.value?.resetFields()
  dialogVisible.value = false
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    if (!props.order) {
      ElMessage.error('订单信息丢失')
      return
    }

    submitting.value = true

    try {
      const selectedCompany = courierCompanies.value.find(
        c => c.code === formData.courier_company
      )

      const response = await fetch('/api/shipping/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          order_id: props.order.id,
          courier_company: formData.courier_company,
          courier_company_name: selectedCompany?.zh || formData.courier_company,
          tracking_number: formData.tracking_number,
          courier_name: formData.courier_name || null,
          courier_phone: formData.courier_phone || null,
          notes: formData.notes || null
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '发货失败')
      }

      ElMessage.success('发货成功！订单状态已更新')
      emit('success')
      handleClose()
    } catch (error: any) {
      console.error('发货失败:', error)
      ElMessage.error(error.message || '发货失败，请重试')
    } finally {
      submitting.value = false
    }
  })
}

// 监听对话框打开，重置表单
watch(() => props.visible, (newVal) => {
  if (newVal) {
    formRef.value?.resetFields()
  }
})
</script>

<style scoped>
.order-info {
  padding: 16px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.info-item .label {
  color: var(--el-text-color-secondary);
  min-width: 80px;
}

.info-item .value {
  color: var(--el-text-color-primary);
  font-weight: 500;
}

.company-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.company-en {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
