<template>
  <el-select
    v-model="selectedValue"
    :placeholder="placeholder"
    :clearable="clearable"
    :disabled="disabled"
    :multiple="multiple"
    :loading="loading"
    @change="handleChange"
    @clear="handleClear"
  >
    <template #prefix v-if="showIcon && currentItem">
      <EnumColorIndicator :color="currentItem.color" />
    </template>

    <template v-if="grouped">
      <el-option-group
        v-for="group in groupedOptions"
        :key="group.label"
        :label="group.label"
      >
        <EnumOption
          v-for="item in group.options"
          :key="item.code"
          :item="item"
          :show-description="showDescription"
          :disabled="isOptionDisabled(item)"
        />
      </el-option-group>
    </template>

    <template v-else>
      <EnumOption
        v-for="item in filteredOptions"
        :key="item.code"
        :item="item"
        :show-description="showDescription"
        :disabled="isOptionDisabled(item)"
      />
    </template>

    <template #empty>
      <div class="enum-select-empty">
        {{ loading ? '加载中...' : '暂无数据' }}
      </div>
    </template>
  </el-select>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EnumItem } from '@/services/EnumService'
import EnumColorIndicator from './EnumColorIndicator.vue'
import EnumOption from './EnumOption.vue'

interface Props {
  modelValue: string | string[]
  options: EnumItem[]
  placeholder?: string
  clearable?: boolean
  disabled?: boolean
  multiple?: boolean
  loading?: boolean
  showIcon?: boolean
  showDescription?: boolean
  grouped?: boolean
  groupedOptions?: Array<{ label: string; options: EnumItem[] }>
  isOptionDisabled?: (item: EnumItem) => boolean
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请选择',
  clearable: true,
  disabled: false,
  multiple: false,
  loading: false,
  showIcon: true,
  showDescription: false,
  grouped: false,
  isOptionDisabled: () => false
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

const filteredOptions = computed(() => props.options)

const currentItem = computed(() => {
  if (props.multiple || !props.modelValue) return null
  return props.options.find(item => item.code === props.modelValue)
})

const handleChange = (value: string | string[]) => {
  const getItem = (code: string) => props.options.find(item => item.code === code)

  if (props.multiple) {
    const items = (value as string[]).map(code => getItem(code)).filter(Boolean)
    emit('change', value, items as EnumItem[])
  } else {
    const item = getItem(value as string)
    emit('change', value, item)
  }
}

const handleClear = () => {
  emit('clear')
}
</script>

<style scoped>
.enum-select-empty {
  text-align: center;
  color: var(--el-text-color-secondary);
  padding: 10px 0;
}
</style>