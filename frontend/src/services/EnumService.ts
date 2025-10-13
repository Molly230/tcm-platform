/**
 * 前端枚举服务 - 统一管理系统枚举值
 * 特性：
 * - 动态从后端获取枚举配置
 * - 本地缓存 + 降级策略
 * - 状态机支持
 * - TypeScript 类型安全
 */

import { api } from '@/utils/api'

export interface EnumItem {
  code: string
  zh: string
  en: string
  description: string
  order: number
  nextStates: string[]
  requiredPermissions: string[]
  color: string
}

export interface EnumConfig {
  PRODUCT_CATEGORY: EnumItem[]
  PRODUCT_STATUS: EnumItem[]
  AUDIT_STATUS: EnumItem[]
  ORDER_STATUS: EnumItem[]
  USER_ROLE: EnumItem[]
}

export type EnumType = keyof EnumConfig

class EnumService {
  private static enumCache: EnumConfig | null = null
  private static lastFetchTime = 0
  private static readonly CACHE_TTL = 5 * 60 * 1000 // 5分钟缓存
  private static isLoading = false
  private static loadPromise: Promise<EnumConfig> | null = null

  /**
   * 获取所有枚举配置（带缓存）
   */
  static async getEnums(): Promise<EnumConfig> {
    const now = Date.now()
    
    // 如果正在加载，返回加载Promise
    if (this.isLoading && this.loadPromise) {
      return this.loadPromise
    }
    
    // 缓存有效，直接返回
    if (this.enumCache && (now - this.lastFetchTime < this.CACHE_TTL)) {
      return this.enumCache
    }

    // 开始加载
    this.isLoading = true
    this.loadPromise = this.fetchEnumsFromServer()

    try {
      const result = await this.loadPromise
      this.enumCache = result
      this.lastFetchTime = now
      return result
    } finally {
      this.isLoading = false
      this.loadPromise = null
    }
  }

  /**
   * 从服务器获取枚举配置
   */
  private static async fetchEnumsFromServer(): Promise<EnumConfig> {
    try {
      const response = await api.get('/system/enums')
      
      if (response.success && response.data) {
        console.log('📋 枚举配置已从服务器更新')
        return response.data
      } else {
        throw new Error(response.message || '获取枚举配置失败')
      }
    } catch (error) {
      console.error('❌ 获取枚举配置失败，使用本地默认值:', error)
      return this.getLocalDefaultEnums()
    }
  }

  /**
   * 本地默认枚举（降级策略）
   */
  private static getLocalDefaultEnums(): EnumConfig {
    return {
      PRODUCT_CATEGORY: [
        { code: 'HERBS', zh: '中药材', en: 'Herbs', description: '传统中药材料', order: 1, nextStates: [], requiredPermissions: [], color: '#67C23A' },
        { code: 'WELLNESS', zh: '养生产品', en: 'Wellness Products', description: '养生保健产品', order: 2, nextStates: [], requiredPermissions: [], color: '#E6A23C' },
        { code: 'MEDICAL_DEVICE', zh: '医疗器械', en: 'Medical Device', description: '医疗相关器械', order: 3, nextStates: [], requiredPermissions: [], color: '#F56C6C' },
        { code: 'HEALTH_FOOD', zh: '保健食品', en: 'Health Food', description: '保健功能食品', order: 4, nextStates: [], requiredPermissions: [], color: '#909399' },
        { code: 'TCM_BOOKS', zh: '中医书籍', en: 'TCM Books', description: '中医药相关书籍', order: 5, nextStates: [], requiredPermissions: [], color: '#606266' },
        { code: 'ACCESSORIES', zh: '配套用品', en: 'Accessories', description: '相关配套用品', order: 6, nextStates: [], requiredPermissions: [], color: '#C0C4CC' }
      ],
      
      PRODUCT_STATUS: [
        { code: 'DRAFT', zh: '草稿', en: 'Draft', description: '商品草稿状态', order: 1, nextStates: ['PENDING'], requiredPermissions: [], color: '#909399' },
        { code: 'PENDING', zh: '待审核', en: 'Pending Review', description: '等待管理员审核', order: 2, nextStates: ['APPROVED', 'REJECTED'], requiredPermissions: ['admin'], color: '#E6A23C' },
        { code: 'APPROVED', zh: '审核通过', en: 'Approved', description: '管理员审核通过', order: 3, nextStates: ['ACTIVE', 'INACTIVE'], requiredPermissions: [], color: '#67C23A' },
        { code: 'REJECTED', zh: '审核拒绝', en: 'Rejected', description: '管理员审核拒绝', order: 4, nextStates: ['PENDING'], requiredPermissions: [], color: '#F56C6C' },
        { code: 'ACTIVE', zh: '在售', en: 'Active', description: '商品正在销售', order: 5, nextStates: ['INACTIVE', 'OUT_OF_STOCK'], requiredPermissions: ['admin'], color: '#409EFF' },
        { code: 'INACTIVE', zh: '下架', en: 'Inactive', description: '商品已下架', order: 6, nextStates: ['ACTIVE'], requiredPermissions: ['admin'], color: '#C0C4CC' },
        { code: 'OUT_OF_STOCK', zh: '缺货', en: 'Out of Stock', description: '商品库存不足', order: 7, nextStates: ['ACTIVE', 'INACTIVE'], requiredPermissions: [], color: '#F56C6C' }
      ],
      
      AUDIT_STATUS: [
        { code: 'PENDING', zh: '待审核', en: 'Pending', description: '等待审核', order: 1, nextStates: ['APPROVED', 'REJECTED'], requiredPermissions: [], color: '#E6A23C' },
        { code: 'APPROVED', zh: '已通过', en: 'Approved', description: '审核通过', order: 2, nextStates: [], requiredPermissions: [], color: '#67C23A' },
        { code: 'REJECTED', zh: '已拒绝', en: 'Rejected', description: '审核拒绝', order: 3, nextStates: ['PENDING'], requiredPermissions: [], color: '#F56C6C' }
      ],
      
      ORDER_STATUS: [
        { code: 'PENDING', zh: '待付款', en: 'Pending Payment', description: '等待用户付款', order: 1, nextStates: ['PAID', 'CANCELLED'], requiredPermissions: [], color: '#E6A23C' },
        { code: 'PAID', zh: '已付款', en: 'Paid', description: '用户已付款', order: 2, nextStates: ['SHIPPED', 'CANCELLED'], requiredPermissions: [], color: '#67C23A' },
        { code: 'SHIPPED', zh: '已发货', en: 'Shipped', description: '商品已发货', order: 3, nextStates: ['DELIVERED', 'RETURNED'], requiredPermissions: [], color: '#409EFF' },
        { code: 'DELIVERED', zh: '已送达', en: 'Delivered', description: '商品已送达', order: 4, nextStates: ['COMPLETED', 'RETURNED'], requiredPermissions: [], color: '#67C23A' },
        { code: 'COMPLETED', zh: '已完成', en: 'Completed', description: '订单完成', order: 5, nextStates: [], requiredPermissions: [], color: '#909399' },
        { code: 'CANCELLED', zh: '已取消', en: 'Cancelled', description: '订单已取消', order: 6, nextStates: [], requiredPermissions: [], color: '#F56C6C' },
        { code: 'RETURNED', zh: '已退货', en: 'Returned', description: '商品已退货', order: 7, nextStates: [], requiredPermissions: [], color: '#C0C4CC' }
      ],
      
      USER_ROLE: [
        { code: 'USER', zh: '普通用户', en: 'User', description: '普通注册用户', order: 1, nextStates: [], requiredPermissions: [], color: '#409EFF' },
        { code: 'EXPERT', zh: '专家', en: 'Expert', description: '医疗健康专家', order: 2, nextStates: [], requiredPermissions: [], color: '#67C23A' },
        { code: 'ADMIN', zh: '管理员', en: 'Admin', description: '系统管理员', order: 3, nextStates: [], requiredPermissions: [], color: '#E6A23C' },
        { code: 'SUPER_ADMIN', zh: '超级管理员', en: 'Super Admin', description: '超级管理员', order: 4, nextStates: [], requiredPermissions: [], color: '#F56C6C' }
      ]
    }
  }

  /**
   * 获取指定类型的枚举项
   */
  static getEnum(type: EnumType): EnumItem[] {
    if (!this.enumCache) {
      console.warn(`⚠️  枚举缓存未初始化，使用本地默认值: ${type}`)
      const localEnums = this.getLocalDefaultEnums()
      return localEnums[type] || []
    }
    return this.enumCache[type] || []
  }

  /**
   * 获取枚举显示标签
   */
  static getEnumLabel(type: EnumType, code: string): string {
    const items = this.getEnum(type)
    const item = items.find(item => item.code === code)
    return item?.zh || code
  }

  /**
   * 获取枚举项详情
   */
  static getEnumItem(type: EnumType, code: string): EnumItem | undefined {
    const items = this.getEnum(type)
    return items.find(item => item.code === code)
  }

  /**
   * 获取枚举颜色
   */
  static getEnumColor(type: EnumType, code: string): string {
    const item = this.getEnumItem(type, code)
    return item?.color || '#909399'
  }

  /**
   * 获取状态机的下一步状态
   */
  static getNextStates(type: EnumType, currentState: string): string[] {
    const item = this.getEnumItem(type, currentState)
    return item?.nextStates || []
  }

  /**
   * 检查状态转换是否合法
   */
  static canTransitionTo(type: EnumType, fromState: string, toState: string): boolean {
    const nextStates = this.getNextStates(type, fromState)
    return nextStates.includes(toState)
  }

  /**
   * 获取所有有效的枚举代码
   */
  static getAllCodes(type: EnumType): string[] {
    const items = this.getEnum(type)
    return items.map(item => item.code)
  }

  /**
   * 验证枚举值是否有效
   */
  static isValidEnumValue(type: EnumType, value: string): boolean {
    const codes = this.getAllCodes(type)
    return codes.includes(value)
  }

  /**
   * 获取按顺序排列的枚举选项
   */
  static getOrderedOptions(type: EnumType, excludeCodes: string[] = []) {
    const items = this.getEnum(type)
    return items
      .filter(item => !excludeCodes.includes(item.code))
      .sort((a, b) => a.order - b.order)
      .map(item => ({
        label: item.zh,
        value: item.code,
        color: item.color,
        description: item.description
      }))
  }

  /**
   * 强制刷新枚举缓存
   */
  static async refreshEnums(): Promise<EnumConfig> {
    this.lastFetchTime = 0 // 重置缓存时间
    this.enumCache = null  // 清空缓存
    return this.getEnums()
  }

  /**
   * 初始化枚举服务（应用启动时调用）
   */
  static async initialize(): Promise<void> {
    try {
      await this.getEnums()
      console.log('✅ 枚举服务初始化完成')
    } catch (error) {
      console.error('❌ 枚举服务初始化失败:', error)
    }
  }
}

export default EnumService