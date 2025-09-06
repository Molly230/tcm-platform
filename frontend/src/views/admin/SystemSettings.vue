<template>
  <div class="system-settings">
    <div class="page-header">
      <div class="header-content">
        <h2>⚙️ 系统设置</h2>
        <p>管理系统配置、安全设置和运维工具</p>
      </div>
    </div>

    <div class="settings-grid">
      <!-- 系统状态 -->
      <div class="settings-card">
        <div class="card-header">
          <h3>🔧 系统状态</h3>
          <el-button size="small" @click="refreshStatus">刷新</el-button>
        </div>
        <div class="status-list">
          <div class="status-item">
            <span class="status-label">服务器状态</span>
            <el-tag type="success" size="small">运行中</el-tag>
          </div>
          <div class="status-item">
            <span class="status-label">数据库连接</span>
            <el-tag type="success" size="small">正常</el-tag>
          </div>
          <div class="status-item">
            <span class="status-label">Redis缓存</span>
            <el-tag type="success" size="small">正常</el-tag>
          </div>
          <div class="status-item">
            <span class="status-label">存储空间</span>
            <el-tag type="info" size="small">充足 (75%)</el-tag>
          </div>
          <div class="status-item">
            <span class="status-label">API响应时间</span>
            <el-tag type="success" size="small">85ms</el-tag>
          </div>
        </div>
      </div>

      <!-- 数据备份 -->
      <div class="settings-card">
        <div class="card-header">
          <h3>💾 数据备份</h3>
          <el-button size="small" type="primary" @click="createBackup" :loading="backupLoading">
            创建备份
          </el-button>
        </div>
        <div class="backup-info">
          <div class="backup-item">
            <span class="backup-label">最后备份时间：</span>
            <span class="backup-value">2024-01-15 03:00:00</span>
          </div>
          <div class="backup-item">
            <span class="backup-label">备份文件大小：</span>
            <span class="backup-value">124.5 MB</span>
          </div>
          <div class="backup-item">
            <span class="backup-label">自动备份：</span>
            <el-switch v-model="autoBackup" @change="toggleAutoBackup" />
          </div>
        </div>
      </div>

      <!-- 系统日志 -->
      <div class="settings-card">
        <div class="card-header">
          <h3>📋 系统日志</h3>
          <el-button size="small" @click="loadLogs">查看全部</el-button>
        </div>
        <div class="log-container">
          <div v-for="log in systemLogs" :key="log" class="log-line">
            {{ log }}
          </div>
          <div v-if="systemLogs.length === 0" class="no-logs">
            <el-empty description="暂无系统日志" :image-size="60" />
          </div>
        </div>
      </div>

      <!-- 安全设置 -->
      <div class="settings-card">
        <div class="card-header">
          <h3>🔒 安全设置</h3>
          <el-button size="small" type="warning" @click="showSecurityDialog = true">
            修改设置
          </el-button>
        </div>
        <div class="security-info">
          <div class="security-item">
            <span class="security-label">密码策略：</span>
            <span class="security-value">强密码 (8位+数字+符号)</span>
          </div>
          <div class="security-item">
            <span class="security-label">会话超时：</span>
            <span class="security-value">24小时</span>
          </div>
          <div class="security-item">
            <span class="security-label">双因子认证：</span>
            <el-tag type="warning" size="small">未启用</el-tag>
          </div>
          <div class="security-item">
            <span class="security-label">API限流：</span>
            <el-tag type="success" size="small">已启用</el-tag>
          </div>
        </div>
      </div>

      <!-- 邮件设置 -->
      <div class="settings-card">
        <div class="card-header">
          <h3>📧 邮件设置</h3>
          <el-button size="small" @click="testEmail">测试邮件</el-button>
        </div>
        <div class="email-info">
          <div class="email-item">
            <span class="email-label">SMTP服务器：</span>
            <span class="email-value">smtp.example.com</span>
          </div>
          <div class="email-item">
            <span class="email-label">端口：</span>
            <span class="email-value">587</span>
          </div>
          <div class="email-item">
            <span class="email-label">发件人：</span>
            <span class="email-value">noreply@tcm.com</span>
          </div>
          <div class="email-item">
            <span class="email-label">SSL加密：</span>
            <el-tag type="success" size="small">已启用</el-tag>
          </div>
        </div>
      </div>

      <!-- 缓存管理 -->
      <div class="settings-card">
        <div class="card-header">
          <h3>🗂️ 缓存管理</h3>
          <el-button size="small" type="danger" @click="clearCache" :loading="cacheLoading">
            清空缓存
          </el-button>
        </div>
        <div class="cache-info">
          <div class="cache-item">
            <span class="cache-label">Redis缓存：</span>
            <span class="cache-value">2.4 MB</span>
          </div>
          <div class="cache-item">
            <span class="cache-label">文件缓存：</span>
            <span class="cache-value">156.8 MB</span>
          </div>
          <div class="cache-item">
            <span class="cache-label">图片缓存：</span>
            <span class="cache-value">89.2 MB</span>
          </div>
          <div class="cache-item">
            <span class="cache-label">缓存命中率：</span>
            <span class="cache-value">94.5%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 安全设置对话框 -->
    <el-dialog v-model="showSecurityDialog" title="安全设置" width="500px">
      <el-form label-width="120px">
        <el-form-item label="密码策略">
          <el-select v-model="securitySettings.passwordPolicy" style="width: 100%">
            <el-option label="简单密码 (6位)" value="simple" />
            <el-option label="中等密码 (8位+字母)" value="medium" />
            <el-option label="强密码 (8位+数字+符号)" value="strong" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="会话超时">
          <el-select v-model="securitySettings.sessionTimeout" style="width: 100%">
            <el-option label="1小时" value="1h" />
            <el-option label="8小时" value="8h" />
            <el-option label="24小时" value="24h" />
            <el-option label="7天" value="7d" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="双因子认证">
          <el-switch v-model="securitySettings.twoFactorAuth" />
        </el-form-item>
        
        <el-form-item label="API限流">
          <el-switch v-model="securitySettings.rateLimit" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showSecurityDialog = false">取消</el-button>
        <el-button type="primary" @click="saveSecuritySettings">保存设置</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const backupLoading = ref(false)
const cacheLoading = ref(false)
const autoBackup = ref(true)
const showSecurityDialog = ref(false)

const systemLogs = ref([
  '[2024-01-15 14:30:25] INFO: 用户登录成功 (admin)',
  '[2024-01-15 14:25:18] INFO: 数据库连接正常',
  '[2024-01-15 14:20:45] WARNING: 缓存空间使用率达到80%',
  '[2024-01-15 14:15:32] INFO: 自动备份完成',
  '[2024-01-15 14:10:12] INFO: 系统启动完成'
])

const securitySettings = ref({
  passwordPolicy: 'strong',
  sessionTimeout: '24h',
  twoFactorAuth: false,
  rateLimit: true
})

// 方法
const refreshStatus = () => {
  ElMessage.success('系统状态已刷新')
}

const createBackup = async () => {
  backupLoading.value = true
  try {
    // 模拟创建备份
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('数据备份创建成功')
  } catch (error) {
    ElMessage.error('备份创建失败')
  } finally {
    backupLoading.value = false
  }
}

const toggleAutoBackup = (value: boolean) => {
  ElMessage.info(`自动备份已${value ? '启用' : '禁用'}`)
}

const loadLogs = () => {
  ElMessage.info('查看全部日志功能开发中...')
}

const testEmail = () => {
  ElMessage.info('测试邮件已发送，请检查邮箱')
}

const clearCache = async () => {
  cacheLoading.value = true
  try {
    // 模拟清空缓存
    await new Promise(resolve => setTimeout(resolve, 1500))
    ElMessage.success('缓存已清空')
  } catch (error) {
    ElMessage.error('缓存清空失败')
  } finally {
    cacheLoading.value = false
  }
}

const saveSecuritySettings = () => {
  showSecurityDialog.value = false
  ElMessage.success('安全设置已保存')
}

// 生命周期
onMounted(() => {
  // 组件加载时的初始化逻辑
})
</script>

<style scoped>
.system-settings {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.header-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.settings-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.status-list,
.backup-info,
.security-info,
.email-info,
.cache-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item,
.backup-item,
.security-item,
.email-item,
.cache-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.status-item:last-child,
.backup-item:last-child,
.security-item:last-child,
.email-item:last-child,
.cache-item:last-child {
  border-bottom: none;
}

.status-label,
.backup-label,
.security-label,
.email-label,
.cache-label {
  font-size: 14px;
  color: #666;
}

.backup-value,
.security-value,
.email-value,
.cache-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.log-container {
  max-height: 200px;
  overflow-y: auto;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 12px;
}

.log-line {
  font-size: 12px;
  font-family: 'Courier New', monospace;
  color: #555;
  margin-bottom: 4px;
  line-height: 1.4;
}

.no-logs {
  text-align: center;
  padding: 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

/* 滚动条样式 */
.log-container::-webkit-scrollbar {
  width: 4px;
}

.log-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.log-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.log-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>