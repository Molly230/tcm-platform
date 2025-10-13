<template>
  <SmartEnumSelect
    v-model="selectedValue"
    :enum-type="enumType"
    :placeholder="placeholder"
    :clearable="clearable"
    :disabled="disabled"
    :multiple="multiple"
    :exclude-codes="excludeCodes"
    :include-codes="includeCodes"
    :show-icon="showIcon"
    :show-description="showDescription"
    :grouped="grouped"
    :group-by="groupBy"
    :filter-by-permission="filterByPermission"
    :current-state="currentState"
    @change="handleChange"
    @clear="handleClear"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EnumItem, EnumType } from '@/services/EnumService'
import type { GroupByType } from './enum/EnumGrouper'
import SmartEnumSelect from './enum/SmartEnumSelect.vue'

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

const selectedValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleChange = (value: string | string[], item?: EnumItem | EnumItem[]) => {
  emit('change', value, item)
}

const handleClear = () => {
  emit('clear')
}
</script>