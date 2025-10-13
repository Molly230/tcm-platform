import type { EnumItem } from '@/services/EnumService'

export interface GroupedOptions {
  label: string
  options: EnumItem[]
}

export type GroupByType = 'category' | 'status' | 'level'

export class EnumGrouper {
  /**
   * 对枚举选项进行分组
   */
  group(options: EnumItem[], groupBy: GroupByType): GroupedOptions[] {
    switch (groupBy) {
      case 'category':
        return this.groupByCategory(options)
      case 'status':
        return this.groupByStatus(options)
      case 'level':
        return this.groupByLevel(options)
      default:
        return [{ label: '全部', options }]
    }
  }

  /**
   * 按类别分组
   */
  private groupByCategory(options: EnumItem[]): GroupedOptions[] {
    const groups = new Map<string, EnumItem[]>()

    options.forEach(item => {
      const category = this.getCategoryFromCode(item.code)
      if (!groups.has(category)) {
        groups.set(category, [])
      }
      groups.get(category)!.push(item)
    })

    return Array.from(groups.entries()).map(([label, options]) => ({
      label: this.getCategoryLabel(label),
      options: options.sort((a, b) => (a.order || 0) - (b.order || 0))
    }))
  }

  /**
   * 按状态分组
   */
  private groupByStatus(options: EnumItem[]): GroupedOptions[] {
    const activeStates = ['ACTIVE', 'READY', 'COMPLETED', 'SUCCESS', 'APPROVED']
    const pendingStates = ['PENDING', 'PROCESSING', 'ONGOING', 'UPLOADING']
    const inactiveStates = ['INACTIVE', 'CANCELLED', 'FAILED', 'REJECTED', 'ERROR']

    const groups: GroupedOptions[] = [
      { label: '活跃状态', options: [] },
      { label: '处理中', options: [] },
      { label: '非活跃', options: [] },
      { label: '其他', options: [] }
    ]

    options.forEach(item => {
      if (activeStates.includes(item.code)) {
        groups[0].options.push(item)
      } else if (pendingStates.includes(item.code)) {
        groups[1].options.push(item)
      } else if (inactiveStates.includes(item.code)) {
        groups[2].options.push(item)
      } else {
        groups[3].options.push(item)
      }
    })

    return groups.filter(group => group.options.length > 0)
  }

  /**
   * 按级别分组
   */
  private groupByLevel(options: EnumItem[]): GroupedOptions[] {
    const highLevel = ['SUPER_ADMIN', 'ADMIN', 'CHIEF', 'SENIOR']
    const midLevel = ['EXPERT', 'INTERMEDIATE', 'VIP']
    const lowLevel = ['USER', 'JUNIOR']

    const groups: GroupedOptions[] = [
      { label: '高级', options: [] },
      { label: '中级', options: [] },
      { label: '初级', options: [] },
      { label: '其他', options: [] }
    ]

    options.forEach(item => {
      if (highLevel.includes(item.code)) {
        groups[0].options.push(item)
      } else if (midLevel.includes(item.code)) {
        groups[1].options.push(item)
      } else if (lowLevel.includes(item.code)) {
        groups[2].options.push(item)
      } else {
        groups[3].options.push(item)
      }
    })

    return groups.filter(group => group.options.length > 0)
  }

  /**
   * 从代码获取类别
   */
  private getCategoryFromCode(code: string): string {
    if (code.includes('USER')) return 'user'
    if (code.includes('EXPERT')) return 'expert'
    if (code.includes('PRODUCT')) return 'product'
    if (code.includes('ORDER')) return 'order'
    if (code.includes('COURSE')) return 'course'
    if (code.includes('CONSULTATION')) return 'consultation'
    return 'other'
  }

  /**
   * 获取类别标签
   */
  private getCategoryLabel(category: string): string {
    const labels: Record<string, string> = {
      user: '用户相关',
      expert: '专家相关',
      product: '商品相关',
      order: '订单相关',
      course: '课程相关',
      consultation: '咨询相关',
      other: '其他'
    }
    return labels[category] || category
  }
}