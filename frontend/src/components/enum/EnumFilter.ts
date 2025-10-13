import type { EnumItem } from '@/services/EnumService'
import { useUserStore } from '@/stores/user'

export interface EnumFilterOptions {
  excludeCodes?: string[]
  includeCodes?: string[]
  filterByPermission?: boolean
  userRole?: string
}

export class EnumFilter {
  private userStore = useUserStore()

  /**
   * 过滤枚举选项
   */
  filter(options: EnumItem[], filterOptions: EnumFilterOptions = {}): EnumItem[] {
    let filtered = [...options]

    const {
      excludeCodes = [],
      includeCodes = [],
      filterByPermission = false
    } = filterOptions

    // 包含指定代码
    if (includeCodes.length > 0) {
      filtered = filtered.filter(item => includeCodes.includes(item.code))
    }

    // 排除指定代码
    if (excludeCodes.length > 0) {
      filtered = filtered.filter(item => !excludeCodes.includes(item.code))
    }

    // 权限过滤
    if (filterByPermission) {
      filtered = this.filterByUserPermission(filtered)
    }

    return filtered.sort((a, b) => (a.order || 0) - (b.order || 0))
  }

  /**
   * 基于用户权限过滤
   */
  private filterByUserPermission(options: EnumItem[]): EnumItem[] {
    const userRole = this.userStore.user?.role
    if (!userRole) return options

    return options.filter(item => {
      if (!item.required_permissions || item.required_permissions.length === 0) {
        return true
      }
      return this.hasPermission(userRole, item.required_permissions)
    })
  }

  /**
   * 检查用户是否有指定权限
   */
  private hasPermission(userRole: string, requiredPermissions: string[]): boolean {
    // 超级管理员拥有所有权限
    if (userRole === 'SUPER_ADMIN') return true

    // 管理员权限
    if (userRole === 'ADMIN') {
      return !requiredPermissions.includes('SUPER_ADMIN')
    }

    // 其他角色
    return !requiredPermissions.some(permission =>
      ['ADMIN', 'SUPER_ADMIN'].includes(permission)
    )
  }

  /**
   * 检查选项是否被禁用
   */
  isOptionDisabled(item: EnumItem, currentState?: string): boolean {
    // 如果有next_states定义，检查状态转换是否合法
    if (currentState && item.next_states) {
      return !item.next_states.includes(currentState)
    }

    return false
  }
}