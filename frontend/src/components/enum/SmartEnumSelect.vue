<template>
  <BaseEnumSelect
    v-model="selectedValue"
    :options="processedOptions"
    :placeholder="placeholder"
    :clearable="clearable"
    :disabled="disabled"
    :multiple="multiple"
    :loading="loading"
    :show-icon="showIcon"
    :show-description="showDescription"
    :grouped="grouped"
    :grouped-options="groupedOptionsData"
    :is-option-disabled="isOptionDisabled"
    @change="handleChange"
    @clear="handleClear"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import EnumService, { type EnumItem, type EnumType } from '@/services/EnumService'
import { EnumFilter, type EnumFilterOptions } from './EnumFilter'
import { EnumGrouper, type GroupByType } from './EnumGrouper'
import BaseEnumSelect from './BaseEnumSelect.vue'

interface Props {
  modelValue: string | string[]
  enumType: EnumType
  placeholder?: string
  clearable?: boolean
  disabled?: boolean
  multiple?: boolean
  excludeCodes?: string[]
  includeCodes?: string[]
  showIcon?: boolean
  showDescription?: boolean
  grouped?: boolean
  groupBy?: GroupByType
  filterByPermission?: boolean
  currentState?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请选择',
  clearable: true,
  disabled: false,
  multiple: false,
  excludeCodes: () => [],
  includeCodes: () => [],
  showIcon: true,
  showDescription: false,
  grouped: false,
  groupBy: 'category',
  filterByPermission: true
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | string[]): void
  (e: 'change', value: string | string[], item?: EnumItem | EnumItem[]): void
  (e: 'clear'): void
}>()

const loading = ref(false)
const enumFilter = new EnumFilter()
const enumGrouper = new EnumGrouper()

const selectedValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 获取原始枚举选项
const rawOptions = computed(() => {
  return EnumService.getEnum(props.enumType)
})

// 处理后的选项（过滤 + 排序）
const processedOptions = computed(() => {
  const filterOptions: EnumFilterOptions = {
    excludeCodes: props.excludeCodes,
    includeCodes: props.includeCodes,
    filterByPermission: props.filterByPermission
  }

  return enumFilter.filter(rawOptions.value, filterOptions)
})

// 分组选项数据
const groupedOptionsData = computed(() => {
  if (!props.grouped) return []
  return enumGrouper.group(processedOptions.value, props.groupBy)
})

// 检查选项是否被禁用
const isOptionDisabled = (item: EnumItem): boolean => {
  return enumFilter.isOptionDisabled(item, props.currentState)
}

const handleChange = (value: string | string[], item?: EnumItem | EnumItem[]) => {
  emit('change', value, item)
}

const handleClear = () => {
  emit('clear')
}
</script>