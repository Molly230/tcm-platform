<template>
  <div class="admin-layout">
    <!-- 顶部导航栏 -->
    <div class="admin-header">
      <div class="header-left">
        <div class="logo">
          <span class="logo-icon">🏥</span>
          <span class="logo-text">中医平台管理后台</span>
        </div>
      </div>
      
      <div class="header-right">
        <div class="admin-info">
          <el-dropdown @command="handleCommand">
            <span class="admin-avatar">
              <el-avatar :size="32" :src="currentUser?.avatar">
                <span>{{ currentUser?.username?.charAt(0).toUpperCase() || 'A' }}</span>
              </el-avatar>
              <span class="admin-name">{{ currentUser?.username || '管理员' }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="settings">系统设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 主体布局 -->
    <div class="admin-main">
      <!-- 侧边导航 -->
      <div class="admin-sidebar" :class="{ collapsed: sidebarCollapsed }">
        <div class="sidebar-toggle" @click="toggleSidebar">
          <el-icon><Expand v-if="sidebarCollapsed" /><Fold v-else /></el-icon>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          :collapse="sidebarCollapsed"
          class="admin-menu"
          router
          :collapse-transition="false"
        >
          <el-menu-item index="/admin/dashboard">
            <el-icon><House /></el-icon>
            <template #title>仪表板</template>
          </el-menu-item>
          
          <el-sub-menu index="content">
            <template #title>
              <el-icon><Reading /></el-icon>
              <span>内容管理</span>
            </template>
            <el-menu-item index="/admin/courses">
              <el-icon><Reading /></el-icon>
              <template #title>课程管理</template>
            </el-menu-item>
            <el-menu-item index="/admin/experts">
              <el-icon><UserFilled /></el-icon>
              <template #title>专家管理</template>
            </el-menu-item>
            <el-menu-item index="/admin/products">
              <el-icon><ShoppingCart /></el-icon>
              <template #title>商品管理</template>
            </el-menu-item>
            <el-menu-item index="/admin/product-audit">
              <el-icon><DocumentChecked /></el-icon>
              <template #title>产品审核</template>
            </el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="business">
            <template #title>
              <el-icon><Notebook /></el-icon>
              <span>业务管理</span>
            </template>
            <el-menu-item index="/admin/orders">
              <el-icon><Document /></el-icon>
              <template #title>订单管理</template>
            </el-menu-item>
            <el-menu-item index="/admin/shipping">
              <el-icon><Van /></el-icon>
              <template #title>配送管理</template>
            </el-menu-item>
            <el-menu-item index="/admin/consultations">
              <el-icon><ChatLineRound /></el-icon>
              <template #title>咨询管理</template>
            </el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <template #title>用户管理</template>
          </el-menu-item>
          
          <el-sub-menu index="system">
            <template #title>
              <el-icon><Setting /></el-icon>
              <span>系统管理</span>
            </template>
            <el-menu-item index="/admin/export">
              <el-icon><Download /></el-icon>
              <template #title>数据导出</template>
            </el-menu-item>
            <el-menu-item index="/admin/settings">
              <el-icon><Tools /></el-icon>
              <template #title>系统设置</template>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </div>

      <!-- 内容区域 -->
      <div class="admin-content">
        <div class="content-wrapper">
          <!-- 面包屑导航 -->
          <div class="breadcrumb-section">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item to="/admin/dashboard">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <!-- 页面内容 -->
          <div class="page-content">
            <router-view />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  House, Reading, User, Setting, Download, Tools, Notebook, Document,
  UserFilled, ShoppingCart, ChatLineRound, ArrowDown, Expand, Fold, DocumentChecked, Van
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()

// 响应式数据
const currentUser = ref(null)
const sidebarCollapsed = ref(false)

// 计算属性
const activeMenu = computed(() => {
  return route.path
})

const currentPageTitle = computed(() => {
  const titleMap = {
    '/admin/dashboard': '仪表板',
    '/admin/users': '用户管理',
    '/admin/courses': '课程管理',
    '/admin/experts': '专家管理',
    '/admin/products': '商品管理',
    '/admin/product-audit': '产品审核',
    '/admin/orders': '订单管理',
    '/admin/consultations': '咨询管理',
    '/admin/export': '数据导出',
    '/admin/settings': '系统设置'
  }
  return titleMap[route.path] || '管理后台'
})

// 方法
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
  // 保存到localStorage
  localStorage.setItem('admin_sidebar_collapsed', sidebarCollapsed.value.toString())
}

const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
    case 'settings':
      router.push('/admin/settings')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '退出确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 清除本地数据
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
    
    // 跳转到登录页
    router.push('/admin/login')
    ElMessage.success('已成功退出登录')
  } catch {
    // 用户取消退出
  }
}

// 生命周期
onMounted(() => {
  // 获取当前用户信息
  const adminUser = localStorage.getItem('admin_user')
  if (adminUser) {
    try {
      currentUser.value = JSON.parse(adminUser)
    } catch (e) {
      console.error('解析用户数据失败:', e)
    }
  }
  
  // 恢复侧边栏状态
  const collapsed = localStorage.getItem('admin_sidebar_collapsed')
  if (collapsed) {
    sidebarCollapsed.value = collapsed === 'true'
  }
})

// 监听路由变化，确保正确的菜单高亮
watch(() => route.path, (newPath) => {
  // 可以在这里添加路由变化时的逻辑
  console.log('Current route:', newPath)
}, { immediate: true })
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
}

/* 顶部导航栏 */
.admin-header {
  height: 64px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  z-index: 1001;
}

.header-left .logo {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  color: #1890ff;
}

.logo-icon {
  font-size: 24px;
  margin-right: 8px;
}

.logo-text {
  color: #333;
}

.header-right {
  display: flex;
  align-items: center;
}

.admin-avatar {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 12px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.admin-avatar:hover {
  background-color: #f5f5f5;
}

.admin-name {
  margin: 0 8px;
  font-size: 14px;
  color: #333;
}

.dropdown-icon {
  font-size: 12px;
  color: #999;
}

/* 主体布局 */
.admin-main {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 侧边导航 */
.admin-sidebar {
  width: 256px;
  background: #fff;
  border-right: 1px solid #f0f0f0;
  transition: width 0.2s;
  position: relative;
  z-index: 1000;
}

.admin-sidebar.collapsed {
  width: 80px;
}

.sidebar-toggle {
  position: absolute;
  top: 12px;
  right: -12px;
  width: 24px;
  height: 24px;
  background: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1001;
  transition: all 0.2s;
}

.sidebar-toggle:hover {
  border-color: #1890ff;
  color: #1890ff;
}

.admin-menu {
  height: 100%;
  border-right: none;
  padding-top: 40px;
}

.admin-menu:not(.el-menu--collapse) {
  width: 256px;
}

.admin-menu .el-menu-item,
.admin-menu .el-sub-menu__title {
  height: 48px;
  line-height: 48px;
  padding-left: 24px !important;
}

.admin-menu .el-sub-menu .el-menu-item {
  padding-left: 48px !important;
  background-color: #fafafa;
}

.admin-menu .el-menu-item:hover,
.admin-menu .el-sub-menu__title:hover {
  background-color: #e6f7ff;
  color: #1890ff;
}

.admin-menu .el-menu-item.is-active {
  background-color: #e6f7ff;
  color: #1890ff;
  border-right: 3px solid #1890ff;
}

/* 内容区域 */
.admin-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.breadcrumb-section {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #fff;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
}

.page-content {
  flex: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-sidebar {
    position: fixed;
    left: 0;
    top: 64px;
    height: calc(100vh - 64px);
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .admin-sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .admin-sidebar.collapsed {
    width: 256px; /* 移动端不使用折叠模式 */
  }
  
  .admin-content {
    margin-left: 0;
  }
  
  .logo-text {
    display: none;
  }
}

/* 滚动条样式 */
.content-wrapper::-webkit-scrollbar {
  width: 6px;
}

.content-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.content-wrapper::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.content-wrapper::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>