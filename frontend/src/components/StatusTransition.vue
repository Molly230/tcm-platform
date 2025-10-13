<template>
  <div class="status-transition">
    <!-- 当前状态显示 -->
    <div class="current-status">
      <el-tag 
        :type="getStatusTagType(currentStatus)"
        :color="getStatusColor(currentStatus)"
        size="small"
        effect="light"
      >
        <div class="status-tag-content">
          <div class="status-indicator" :style="{ backgroundColor: getStatusColor(currentStatus) }"></div>
          <span>{{ getStatusLabel(currentStatus) }}</span>
        </div>
      </el-tag>
    </div>

    <!-- 状态转换按钮 -->
    <div v-if="availableTransitions.length > 0" class="status-actions">
      <el-divider direction="vertical" />
      
      <div class="transition-buttons">
        <el-button-group v-if="showAsGroup">
          <el-button
            v-for="transition in availableTransitions"
            :key="transition.code"
            :type="getButtonType(transition.code)"
            size="small"
            :loading="isTransitioning && targetStatus === transition.code"
            :disabled="!canTransitionTo(transition) || disabled"
            @click="handleTransition(transition)"
          >
            <div class="button-content">
              <div 
                class="status-indicator small"
                :style="{ backgroundColor: transition.color }"
              ></div>
              <span>{{ transition.zh }}</span>
            </div>
          </el-button>
        </el-button-group>

        <template v-else>
          <el-button
            v-for="transition in availableTransitions"
            :key="transition.code"
            :type="getButtonType(transition.code)"
            size="small"
            :loading="isTransitioning && targetStatus === transition.code"
            :disabled="!canTransitionTo(transition) || disabled"
            @click="handleTransition(transition)"
            class="transition-button"
          >
            <div class="button-content">
              <div 
                class="status-indicator small"
                :style="{ backgroundColor: transition.color }"
              ></div>
              <span>{{ transition.zh }}</span>
            </div>
          </el-button>
        </template>
      </div>
    </div>

    <!-- 批量操作模式 -->
    <div v-if="showBatchActions && selectedCount > 0" class="batch-actions">
      <el-divider direction="vertical" />
      <span class="batch-info">已选择 {{ selectedCount }} 项</span>
      <el-button
        v-for="transition in commonTransitions"
        :key="`batch-${transition.code}`"
        :type="getButtonType(transition.code)"
        size="small"
        :loading="isBatchTransitioning && batchTargetStatus === transition.code"
        @click="handleBatchTransition(transition)"
      >
        批量{{ transition.zh }}
      </el-button>
    </div>

    <!-- 状态转换确认对话框 -->
    <el-dialog
      v-model="showConfirmDialog"
      :title="`确认${actionLabel}`"
      width="400px"
      :before-close="handleDialogClose"
    >
      <div class="confirm-content">
        <el-alert
          :title="`即将将状态从「${getStatusLabel(currentStatus)}」变更为「${pendingTransition?.zh}」`"
          type="warning"
          show-icon
          :closable="false"
        />
        
        <el-form v-if="needReason" class="reason-form" label-position="top">
          <el-form-item label="变更原因" :rules="reasonRules">
            <el-input
              v-model="transitionReason"
              type="textarea"
              :rows="3"
              placeholder="请输入状态变更的原因..."
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
        </el-form>

        <div v-if="pendingTransition?.description" class="transition-description">
          <el-text type="info" size="small">{{ pendingTransition.description }}</el-text>
        </div>
      </div>

      <template #footer>
        <el-button @click="showConfirmDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          :loading="isTransitioning"
          @click="confirmTransition"
          :disabled="needReason && !transitionReason.trim()"
        >
          确认{{ actionLabel }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import EnumService, { type EnumItem, type EnumType } from '@/services/EnumService'
import { useUserStore } from '@/stores/user'

interface Props {
  currentStatus: string
  entityType: 'product' | 'order' | 'expert' | 'course' | 'consultation'
  entityId?: number
  entityIds?: number[]  // 批量操作
  disabled?: boolean
  showAsGroup?: boolean
  showBatchActions?: boolean
  selectedCount?: number
  needConfirm?: boolean
  needReason?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  showAsGroup: false,
  showBatchActions: false,
  selectedCount: 0,
  needConfirm: true,
  needReason: false
})

const emit = defineEmits<{
  (e: 'statusChanged', data: { 
    oldStatus: string
    newStatus: string
    entityId?: number
    entityIds?: number[]
    reason?: string 
  }): void
  (e: 'batchStatusChanged', data: {
    oldStatus: string
    newStatus: string
    entityIds: number[]
    reason?: string
  }): void
}>()

const userStore = useUserStore()

// 状态
const isTransitioning = ref(false)
const isBatchTransitioning = ref(false)
const targetStatus = ref('')
const batchTargetStatus = ref('')
const showConfirmDialog = ref(false)
const pendingTransition = ref<EnumItem | null>(null)
const transitionReason = ref('')

// 计算枚举类型
const enumType = computed((): EnumType => {
  const typeMap = {
    product: 'PRODUCT_STATUS',
    order: 'ORDER_STATUS',
    expert: 'PRODUCT_STATUS', // 假设专家也用类似状态
    course: 'PRODUCT_STATUS',  // 假设课程也用类似状态
    consultation: 'ORDER_STATUS' // 假设咨询用订单状态
  } as const
  
  return typeMap[props.entityType] || 'PRODUCT_STATUS'
})

// 可用的状态转换
const availableTransitions = computed(() => {
  const nextStates = EnumService.getNextStates(enumType.value, props.currentStatus)
  return nextStates
    .map(state => EnumService.getEnumItem(enumType.value, state))
    .filter((item): item is EnumItem => item !== undefined)
    .filter(item => canTransitionTo(item))
})

// 批量操作的通用转换
const commonTransitions = computed(() => {
  // 找出所有选中项都支持的转换
  // 这里简化处理，实际应该根据选中项的状态计算交集
  return availableTransitions.value.filter(transition => 
    ['ACTIVE', 'INACTIVE', 'APPROVED', 'REJECTED'].includes(transition.code)
  )
})

// 获取状态标签
const getStatusLabel = (status: string) => {
  return EnumService.getEnumLabel(enumType.value, status)
}

// 获取状态颜色
const getStatusColor = (status: string) => {
  return EnumService.getEnumColor(enumType.value, status)
}

// 获取状态标签类型
const getStatusTagType = (status: string) => {
  const colorMap: Record<string, string> = {
    '#67C23A': 'success',
    '#E6A23C': 'warning', 
    '#F56C6C': 'danger',
    '#409EFF': 'primary',
    '#909399': 'info'
  }
  const color = getStatusColor(status)
  return colorMap[color] || 'info'
}

// 获取按钮类型
const getButtonType = (status: string) => {
  const statusTypeMap: Record<string, string> = {
    'ACTIVE': 'success',
    'APPROVED': 'success',
    'INACTIVE': 'warning',
    'REJECTED': 'danger',
    'CANCELLED': 'danger',
    'PENDING': 'primary'
  }
  return statusTypeMap[status] || 'default'
}

// 检查是否可以转换到目标状态
const canTransitionTo = (transition: EnumItem) => {
  // 权限检查
  if (transition.requiredPermissions.length > 0) {
    const hasPermission = transition.requiredPermissions.some(permission => 
      userStore.hasPermission(permission) || userStore.isAdmin()
    )
    if (!hasPermission) return false
  }

  return true
}

// 操作标签
const actionLabel = computed(() => {
  return pendingTransition.value?.zh || '变更状态'
})

// 表单验证规则
const reasonRules = [
  { required: true, message: '请输入变更原因', trigger: 'blur' },
  { min: 5, message: '原因至少5个字符', trigger: 'blur' }
]

// 处理状态转换
const handleTransition = async (transition: EnumItem) => {
  if (props.needConfirm) {
    pendingTransition.value = transition
    showConfirmDialog.value = true
    return
  }

  await executeTransition(transition)
}

// 执行状态转换
const executeTransition = async (transition: EnumItem) => {
  try {
    isTransitioning.value = true
    targetStatus.value = transition.code

    // 这里应该调用实际的API
    // await statusApi.changeStatus({
    //   entityType: props.entityType,
    //   entityId: props.entityId,
    //   newStatus: transition.code,
    //   reason: transitionReason.value
    // })

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    emit('statusChanged', {
      oldStatus: props.currentStatus,
      newStatus: transition.code,
      entityId: props.entityId,
      reason: transitionReason.value || undefined
    })

    ElMessage.success(`状态已更新为: ${transition.zh}`)
    
  } catch (error: any) {
    ElMessage.error(`状态转换失败: ${error.message}`)
  } finally {
    isTransitioning.value = false
    targetStatus.value = ''
    showConfirmDialog.value = false
    transitionReason.value = ''
  }
}

// 处理批量转换
const handleBatchTransition = async (transition: EnumItem) => {
  try {
    const result = await ElMessageBox.confirm(
      `确认批量将 ${props.selectedCount} 个项目的状态变更为「${transition.zh}」？`,
      '批量状态变更',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    if (result) {
      await executeBatchTransition(transition)
    }
  } catch {
    // 用户取消操作
  }
}

// 执行批量状态转换
const executeBatchTransition = async (transition: EnumItem) => {
  try {
    isBatchTransitioning.value = true
    batchTargetStatus.value = transition.code

    // 实际API调用
    // await statusApi.batchChangeStatus({
    //   entityType: props.entityType,
    //   entityIds: props.entityIds,
    //   newStatus: transition.code
    // })

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1500))

    emit('batchStatusChanged', {
      oldStatus: props.currentStatus,
      newStatus: transition.code,
      entityIds: props.entityIds || []
    })

    ElMessage.success(`批量状态变更完成: ${transition.zh}`)

  } catch (error: any) {
    ElMessage.error(`批量状态变更失败: ${error.message}`)
  } finally {
    isBatchTransitioning.value = false
    batchTargetStatus.value = ''
  }
}

// 确认转换
const confirmTransition = async () => {
  if (pendingTransition.value) {
    await executeTransition(pendingTransition.value)
  }
}

// 对话框关闭处理
const handleDialogClose = () => {
  if (!isTransitioning.value) {
    showConfirmDialog.value = false
    transitionReason.value = ''
  }
}
</script>

<style scoped>
.status-transition {
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-status .status-tag-content {
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}

.status-indicator.small {
  width: 4px;
  height: 4px;
}

.status-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.transition-buttons {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.transition-button {
  margin: 0 2px 4px 0;
}

.button-content {
  display: flex;
  align-items: center;
  gap: 4px;
}

.batch-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.batch-info {
  font-size: 12px;
  color: #909399;
}

.confirm-content {
  padding: 16px 0;
}

.reason-form {
  margin-top: 16px;
}

.transition-description {
  margin-top: 12px;
  padding: 8px;
  background: #f5f7fa;
  border-radius: 4px;
}
</style>