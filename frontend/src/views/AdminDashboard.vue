<template>
  <div class="admin-dashboard">
    <!-- 顶部导航 -->
    <div class="admin-header">
      <div class="header-left">
        <h1>中医平台管理后台</h1>
      </div>
      <div class="header-right">
        <span>管理员: {{ currentUser?.username }}</span>
        <el-button type="danger" @click="logout">退出登录</el-button>
      </div>
    </div>

    <!-- 侧边导航栏 -->
    <div class="admin-layout">
      <div class="admin-sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <el-icon><House /></el-icon>
            <span>仪表板</span>
          </el-menu-item>
          <el-menu-item index="courses">
            <el-icon><Reading /></el-icon>
            <span>课程管理</span>
          </el-menu-item>
          <el-menu-item index="videos">
            <el-icon><VideoCamera /></el-icon>
            <span>视频管理</span>
          </el-menu-item>
          <el-menu-item index="users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="export">
            <el-icon><Download /></el-icon>
            <span>数据导出</span>
          </el-menu-item>
          <el-menu-item index="system">
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 主内容区域 -->
      <div class="admin-content">
        <!-- 仪表板 -->
        <div v-if="activeMenu === 'dashboard'" class="dashboard-content">
          <!-- 欢迎信息 -->
          <div class="welcome-section">
            <div class="welcome-content">
              <h2>欢迎回来，{{ currentUser?.username || '管理员' }}！👋</h2>
              <p>今天是 {{ formatDate(new Date()) }}，让我们一起管理好中医健康服务平台</p>
            </div>
            <div class="welcome-actions">
              <el-button type="primary" @click="activeMenu = 'courses'">快速添加课程</el-button>
              <el-button type="success" @click="showUploadDialog = true">上传资源</el-button>
            </div>
          </div>

          <!-- 基础统计卡片 -->
          <div class="stats-cards">
            <div class="stat-card">
              <div class="stat-icon courses">📚</div>
              <div class="stat-info">
                <div class="stat-number">{{ stats.basic_stats?.total_courses || 0 }}</div>
                <div class="stat-label">总课程数</div>
                <div class="stat-detail">发布: {{ stats.basic_stats?.published_courses || 0 }}</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon users">👥</div>
              <div class="stat-info">
                <div class="stat-number">{{ stats.basic_stats?.total_users || 0 }}</div>
                <div class="stat-label">总用户数</div>
                <div class="stat-detail">活跃: {{ stats.user_analysis?.active_users || 0 }}</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon lessons">🎬</div>
              <div class="stat-info">
                <div class="stat-number">{{ stats.basic_stats?.total_lessons || 0 }}</div>
                <div class="stat-label">总课时数</div>
                <div class="stat-detail">{{ stats.learning_stats?.total_watch_time_hours || 0 }}小时</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon enrollments">💰</div>
              <div class="stat-info">
                <div class="stat-number">{{ stats.basic_stats?.total_enrollments || 0 }}</div>
                <div class="stat-label">总报名数</div>
                <div class="stat-detail">完成率: {{ stats.learning_stats?.avg_completion_rate || 0 }}%</div>
              </div>
            </div>
          </div>

          <!-- 详细分析面板 -->
          <div class="analysis-panels">
            <!-- 用户分析 -->
            <div class="analysis-card">
              <h3>👥 用户分析</h3>
              <div class="mini-stats">
                <div class="mini-stat">
                  <span class="label">VIP用户</span>
                  <span class="value">{{ stats.user_analysis?.vip_users || 0 }}</span>
                </div>
                <div class="mini-stat">
                  <span class="label">医生用户</span>
                  <span class="value">{{ stats.user_analysis?.doctor_users || 0 }}</span>
                </div>
                <div class="mini-stat">
                  <span class="label">管理员</span>
                  <span class="value">{{ stats.user_analysis?.admin_users || 0 }}</span>
                </div>
              </div>
            </div>

            <!-- 课程分析 -->
            <div class="analysis-card">
              <h3>📚 课程分析</h3>
              <div class="mini-stats">
                <div class="mini-stat">
                  <span class="label">免费课程</span>
                  <span class="value">{{ stats.course_analysis?.free_courses || 0 }}</span>
                </div>
                <div class="mini-stat">
                  <span class="label">付费课程</span>
                  <span class="value">{{ stats.course_analysis?.paid_courses || 0 }}</span>
                </div>
              </div>
            </div>

            <!-- 近期活动 -->
            <div class="analysis-card">
              <h3>📈 近7天活动</h3>
              <div class="mini-stats">
                <div class="mini-stat">
                  <span class="label">新增用户</span>
                  <span class="value">{{ stats.recent_activity?.new_users_week || 0 }}</span>
                </div>
                <div class="mini-stat">
                  <span class="label">新增课程</span>
                  <span class="value">{{ stats.recent_activity?.new_courses_week || 0 }}</span>
                </div>
                <div class="mini-stat">
                  <span class="label">新增报名</span>
                  <span class="value">{{ stats.recent_activity?.new_enrollments_week || 0 }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="dashboard-actions">
            <el-button type="primary" size="large" @click="activeMenu = 'courses'">
              📚 管理课程
            </el-button>
            <el-button type="success" size="large" @click="showUploadDialog = true">
              📹 上传视频
            </el-button>
            <el-button type="info" size="large" @click="activeMenu = 'users'">
              👥 用户管理
            </el-button>
            <el-button type="warning" size="large" @click="refreshStats" :loading="refreshing">
              🔄 {{ refreshing ? '刷新中...' : '刷新数据' }}
            </el-button>
          </div>

          <div class="recent-courses">
            <h3>最近课程</h3>
            <el-table :data="recentCourses" style="width: 100%">
              <el-table-column prop="title" label="课程名称" />
              <el-table-column prop="instructor" label="讲师" />
              <el-table-column prop="total_lessons" label="课时数" />
              <el-table-column prop="is_published" label="状态">
                <template #default="scope">
                  <el-tag :type="scope.row.is_published ? 'success' : 'warning'">
                    {{ scope.row.is_published ? '已发布' : '草稿' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button size="small" @click="editCourse(scope.row.id)">编辑</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

        <!-- 数据导出 -->
        <div v-if="activeMenu === 'export'" class="export-content">
          <div class="content-header">
            <h2>📊 数据导出</h2>
            <div class="export-actions">
              <el-dropdown @command="handleExport">
                <el-button type="primary">
                  导出数据<el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="users-csv">用户数据 (CSV)</el-dropdown-item>
                    <el-dropdown-item command="users-json">用户数据 (JSON)</el-dropdown-item>
                    <el-dropdown-item command="courses-csv">课程数据 (CSV)</el-dropdown-item>
                    <el-dropdown-item command="courses-json">课程数据 (JSON)</el-dropdown-item>
                    <el-dropdown-item command="enrollments-csv">报名数据 (CSV)</el-dropdown-item>
                    <el-dropdown-item command="enrollments-json">报名数据 (JSON)</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          
          <div class="export-cards">
            <div class="export-card">
              <div class="export-icon">👥</div>
              <div class="export-info">
                <h3>用户数据</h3>
                <p>导出用户注册信息、角色权限等数据</p>
                <div class="export-buttons">
                  <el-button size="small" @click="exportData('users', 'csv')">CSV格式</el-button>
                  <el-button size="small" @click="exportData('users', 'json')">JSON格式</el-button>
                </div>
              </div>
            </div>

            <div class="export-card">
              <div class="export-icon">📚</div>
              <div class="export-info">
                <h3>课程数据</h3>
                <p>导出课程信息、分类、价格等数据</p>
                <div class="export-buttons">
                  <el-button size="small" @click="exportData('courses', 'csv')">CSV格式</el-button>
                  <el-button size="small" @click="exportData('courses', 'json')">JSON格式</el-button>
                </div>
              </div>
            </div>

            <div class="export-card">
              <div class="export-icon">📈</div>
              <div class="export-info">
                <h3>报名数据</h3>
                <p>导出学习进度、完成情况等数据</p>
                <div class="export-buttons">
                  <el-button size="small" @click="exportData('enrollments', 'csv')">CSV格式</el-button>
                  <el-button size="small" @click="exportData('enrollments', 'json')">JSON格式</el-button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 系统管理 -->
        <div v-if="activeMenu === 'system'" class="system-content">
          <div class="content-header">
            <h2>⚙️ 系统管理</h2>
            <div class="system-actions">
              <el-button type="success" @click="createBackup" :loading="backupLoading">
                <el-icon><FolderAdd /></el-icon>
                创建备份
              </el-button>
              <el-button @click="loadSystemLogs">
                <el-icon><Document /></el-icon>
                查看日志
              </el-button>
            </div>
          </div>
          
          <div class="system-cards">
            <div class="system-card">
              <h3>🔧 系统状态</h3>
              <div class="status-info">
                <div class="status-item">
                  <span class="label">服务器状态:</span>
                  <el-tag type="success">运行中</el-tag>
                </div>
                <div class="status-item">
                  <span class="label">数据库连接:</span>
                  <el-tag type="success">正常</el-tag>
                </div>
                <div class="status-item">
                  <span class="label">磁盘空间:</span>
                  <el-tag type="info">充足</el-tag>
                </div>
              </div>
            </div>

            <div class="system-card" v-if="systemLogs.length > 0">
              <h3>📋 系统日志</h3>
              <div class="log-container">
                <div v-for="log in systemLogs.slice(0, 10)" :key="log" class="log-line">
                  {{ log }}
                </div>
              </div>
              <el-button size="small" type="text" @click="showAllLogs">查看全部日志</el-button>
            </div>
          </div>
        </div>

        <!-- 课程管理 -->
        <div v-else-if="activeMenu === 'courses'" class="courses-content">
          <div class="content-header">
            <h2>📚 课程管理</h2>
            <div class="header-actions">
              <el-input 
                v-model="courseSearch" 
                placeholder="搜索课程标题或讲师" 
                style="width: 250px; margin-right: 10px;"
                clearable
                @input="handleCourseSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-select v-model="courseStatusFilter" placeholder="筛选状态" style="width: 120px; margin-right: 10px;" @change="handleCourseFilter">
                <el-option label="全部" value="" />
                <el-option label="已发布" value="published" />
                <el-option label="草稿" value="draft" />
              </el-select>
              <el-button type="primary" @click="showCourseDialog = true">新增课程</el-button>
            </div>
          </div>

          <!-- 课程统计 -->
          <div class="course-stats-cards">
            <div class="mini-stat-card clickable" @click="clearCourseFilters">
              <div class="stat-icon">📚</div>
              <div class="stat-content">
                <div class="stat-number">{{ filteredCourses.length }}</div>
                <div class="stat-label">当前显示课程</div>
              </div>
            </div>
            <div class="mini-stat-card clickable" :class="{ active: courseStatusFilter === 'published' }" @click="filterByStatus('published')">
              <div class="stat-icon">✅</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.basic_stats?.published_courses || 0 }}</div>
                <div class="stat-label">已发布课程</div>
              </div>
            </div>
            <div class="mini-stat-card clickable" :class="{ active: coursePriceFilter === 'paid' }" @click="filterByPrice('paid')">
              <div class="stat-icon">💰</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.course_analysis?.paid_courses || 0 }}</div>
                <div class="stat-label">付费课程</div>
              </div>
            </div>
            <div class="mini-stat-card clickable" :class="{ active: coursePriceFilter === 'free' }" @click="filterByPrice('free')">
              <div class="stat-icon">🆓</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.course_analysis?.free_courses || 0 }}</div>
                <div class="stat-label">免费课程</div>
              </div>
            </div>
          </div>

          <el-table :data="filteredCourses" style="width: 100%" row-key="id">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column label="课程信息" min-width="300">
              <template #default="scope">
                <div class="course-info">
                  <div class="course-title">
                    <strong>{{ scope.row.title }}</strong>
                    <el-tag size="small" :type="getCategoryTagType(scope.row.category)" style="margin-left: 8px">
                      {{ getCategoryText(scope.row.category) }}
                    </el-tag>
                  </div>
                  <div class="course-meta">
                    <span class="instructor">👨‍🏫 {{ scope.row.instructor || '未设置' }}</span>
                    <span class="lessons-count">📚 {{ scope.row.total_lessons || 0 }}课时</span>
                    <span class="duration" v-if="scope.row.total_duration">⏱️ {{ formatCourseDuration(scope.row.total_duration) }}</span>
                  </div>
                  <div class="course-description" v-if="scope.row.description">
                    {{ scope.row.description.slice(0, 80) }}{{ scope.row.description.length > 80 ? '...' : '' }}
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="价格" width="100">
              <template #default="scope">
                <div class="price-info">
                  <el-tag :type="scope.row.is_free ? 'success' : 'warning'" size="small">
                    {{ scope.row.is_free ? '免费' : `¥${scope.row.price}` }}
                  </el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.is_published ? 'success' : 'warning'" size="small">
                  {{ scope.row.is_published ? '✅ 已发布' : '📝 草稿' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="创建时间" width="120">
              <template #default="scope">
                <div class="date-info">
                  {{ formatSimpleDate(scope.row.created_at) }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="260" fixed="right">
              <template #default="scope">
                <div class="action-buttons">
                  <el-button size="small" type="primary" @click="editCourse(scope.row.id)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="info" @click="manageLessons(scope.row.id)">
                    <el-icon><VideoCamera /></el-icon>
                    课时
                  </el-button>
                  <el-button 
                    size="small" 
                    :type="scope.row.is_published ? 'warning' : 'success'"
                    @click="togglePublishStatus(scope.row)"
                  >
                    <el-icon><Switch /></el-icon>
                    {{ scope.row.is_published ? '下架' : '发布' }}
                  </el-button>
                  <el-popconfirm 
                    title="确定要删除这个课程吗？此操作不可恢复！"
                    @confirm="deleteCourse(scope.row.id)"
                    confirm-button-text="确定删除"
                    cancel-button-text="取消"
                  >
                    <template #reference>
                      <el-button size="small" type="danger">
                        <el-icon><Delete /></el-icon>
                        删除
                      </el-button>
                    </template>
                  </el-popconfirm>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 视频管理 -->
        <div v-else-if="activeMenu === 'videos'" class="videos-content">
          <div class="content-header">
            <h2>🎬 视频管理</h2>
            <div class="header-actions">
              <el-input 
                v-model="videoSearch" 
                placeholder="搜索视频标题或课程..."
                prefix-icon="Search"
                style="width: 250px; margin-right: 10px;"
                @input="handleVideoSearch"
              />
              <el-select 
                v-model="videoStatusFilter" 
                placeholder="状态筛选" 
                style="width: 150px; margin-right: 10px;"
                @change="handleVideoFilter"
              >
                <el-option label="全部状态" value="" />
                <el-option label="已就绪" value="ready" />
                <el-option label="处理中" value="processing" />
                <el-option label="错误" value="error" />
              </el-select>
              <el-button type="primary" @click="showVideoUploadDialog = true">
                <el-icon><Plus /></el-icon>
                上传视频
              </el-button>
              <el-button @click="loadVideos" :loading="refreshing">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </div>

          <!-- 视频列表 -->
          <div class="video-list">
            <el-table 
              :data="filteredVideos" 
              style="width: 100%"
              v-loading="loading"
            >
              <el-table-column prop="id" label="ID" width="60" />
              <el-table-column prop="title" label="视频标题" min-width="200">
                <template #default="scope">
                  <div class="video-title">
                    <strong>{{ scope.row.title }}</strong>
                    <div class="video-meta">
                      课程: {{ scope.row.course?.title || '未知课程' }}
                      <span class="order-badge">第{{ scope.row.order }}课</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="duration" label="时长" width="80">
                <template #default="scope">
                  {{ formatDuration(scope.row.duration) }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag 
                    :type="getStatusTagType(scope.row.status)"
                    size="small"
                  >
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="is_free" label="免费" width="60">
                <template #default="scope">
                  <el-icon 
                    :color="scope.row.is_free ? '#67C23A' : '#E6A23C'"
                    size="16"
                  >
                    <Check v-if="scope.row.is_free" />
                    <Close v-else />
                  </el-icon>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="editVideo(scope.row)"
                  >
                    编辑
                  </el-button>
                  <el-button 
                    type="info" 
                    size="small" 
                    @click="viewVideo(scope.row)"
                    v-if="scope.row.status === 'ready'"
                  >
                    预览
                  </el-button>
                  <el-popconfirm 
                    title="确定要删除这个视频吗？"
                    @confirm="deleteVideo(scope.row.id)"
                  >
                    <template #reference>
                      <el-button type="danger" size="small">删除</el-button>
                    </template>
                  </el-popconfirm>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 视频上传对话框 -->
          <el-dialog 
            v-model="showVideoUploadDialog" 
            title="📹 上传视频" 
            width="600px"
            @close="resetVideoForm"
            :close-on-click-modal="false"
          >
            <div class="upload-dialog-content">
              <el-steps :active="uploadStep" align-center style="margin-bottom: 30px">
                <el-step title="基本信息" icon="Edit" />
                <el-step title="上传文件" icon="UploadFilled" />
                <el-step title="完成" icon="Check" />
              </el-steps>

              <!-- 步骤1: 基本信息 -->
              <div v-show="uploadStep === 0" class="upload-step">
                <el-form 
                  :model="videoForm" 
                  :rules="videoRules" 
                  ref="videoFormRef"
                  label-width="100px"
                >
                  <el-form-item label="所属课程" prop="course_id">
                    <el-select 
                      v-model="videoForm.course_id" 
                      placeholder="选择课程" 
                      style="width: 100%"
                      filterable
                    >
                      <el-option 
                        v-for="course in courses" 
                        :key="course.id" 
                        :label="`${course.title} (${getCategoryText(course.category)})`" 
                        :value="course.id"
                      >
                        <span style="float: left">{{ course.title }}</span>
                        <span style="float: right; color: #8492a6; font-size: 12px">
                          {{ getCategoryText(course.category) }}
                        </span>
                      </el-option>
                    </el-select>
                  </el-form-item>
                  
                  <el-form-item label="视频标题" prop="title">
                    <el-input 
                      v-model="videoForm.title" 
                      placeholder="输入视频标题"
                      show-word-limit
                      maxlength="100"
                    />
                  </el-form-item>
                  
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="课程顺序" prop="order">
                        <el-input-number 
                          v-model="videoForm.order" 
                          :min="1" 
                          :max="999"
                          style="width: 100%" 
                          placeholder="第几课"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="是否免费">
                        <el-switch 
                          v-model="videoForm.is_free" 
                          active-text="免费"
                          inactive-text="付费"
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  
                  <el-form-item label="视频描述">
                    <el-input 
                      v-model="videoForm.description" 
                      type="textarea" 
                      :rows="4"
                      placeholder="描述视频内容、重点知识等..."
                      show-word-limit
                      maxlength="500"
                    />
                  </el-form-item>
                </el-form>
              </div>

              <!-- 步骤2: 上传文件 -->
              <div v-show="uploadStep === 1" class="upload-step">
                <div class="upload-info-card">
                  <h4>📋 即将上传的视频信息</h4>
                  <div class="info-row">
                    <span class="label">课程:</span>
                    <span class="value">{{ getSelectedCourseName() }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">标题:</span>
                    <span class="value">{{ videoForm.title }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">顺序:</span>
                    <span class="value">第{{ videoForm.order }}课</span>
                  </div>
                </div>
                
                <el-upload
                  class="enhanced-video-uploader"
                  drag
                  :action="uploadUrl"
                  :headers="uploadHeaders"
                  :data="uploadData"
                  :before-upload="beforeVideoUpload"
                  :on-success="handleVideoSuccess"
                  :on-progress="handleProgress"
                  :on-error="handleUploadError"
                  :file-list="fileList"
                  accept="video/*"
                  :limit="1"
                >
                  <div class="upload-area">
                    <el-icon class="upload-icon"><UploadFilled /></el-icon>
                    <div class="upload-text">
                      <p>将视频文件拖到此处，或<em>点击选择文件</em></p>
                      <div class="upload-hint">
                        <div class="hint-item">✅ 支持格式: MP4, AVI, MOV, WMV</div>
                        <div class="hint-item">📦 文件大小: 最大 500MB</div>
                        <div class="hint-item">⚡ 上传后会自动处理，请耐心等待</div>
                      </div>
                    </div>
                  </div>
                </el-upload>

                <!-- 上传进度 -->
                <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
                  <el-progress 
                    :percentage="uploadProgress" 
                    :stroke-width="6"
                    status="active"
                  />
                  <p class="progress-text">正在上传... {{ uploadProgress }}%</p>
                </div>
              </div>

              <!-- 步骤3: 完成 -->
              <div v-show="uploadStep === 2" class="upload-step upload-success">
                <div class="success-icon">
                  <el-icon size="60" color="#67C23A"><Check /></el-icon>
                </div>
                <h3>🎉 视频上传成功！</h3>
                <p>视频正在后台处理中，处理完成后会自动更新状态</p>
                <div class="success-actions">
                  <el-button type="primary" @click="continueUpload">继续上传</el-button>
                  <el-button @click="closeUploadDialog">完成</el-button>
                </div>
              </div>
            </div>
            
            <template #footer v-if="uploadStep < 2">
              <div class="dialog-footer">
                <el-button @click="showVideoUploadDialog = false">取消</el-button>
                <el-button 
                  v-if="uploadStep === 0" 
                  type="primary" 
                  @click="nextUploadStep"
                  :disabled="!canProceedToUpload"
                >
                  下一步
                </el-button>
                <el-button 
                  v-if="uploadStep === 1" 
                  @click="uploadStep = 0"
                >
                  上一步
                </el-button>
              </div>
            </template>
          </el-dialog>

          <!-- 视频编辑对话框 -->
          <el-dialog 
            v-model="showVideoEditDialog" 
            title="编辑视频" 
            width="500px"
          >
            <el-form 
              :model="editingVideo" 
              :rules="videoRules" 
              ref="editVideoFormRef"
              label-width="80px"
              v-if="editingVideo"
            >
              <el-form-item label="视频标题" prop="title">
                <el-input v-model="editingVideo.title" />
              </el-form-item>
              
              <el-form-item label="课程顺序" prop="order">
                <el-input-number v-model="editingVideo.order" :min="1" style="width: 100%" />
              </el-form-item>
              
              <el-form-item label="视频描述">
                <el-input 
                  v-model="editingVideo.description" 
                  type="textarea" 
                  :rows="3"
                />
              </el-form-item>
              
              <el-form-item label="视频时长">
                <el-input-number v-model="editingVideo.duration" :min="0" style="width: 100%" />
                <span class="form-tip">（秒）</span>
              </el-form-item>
              
              <el-form-item label="是否免费">
                <el-switch v-model="editingVideo.is_free" />
              </el-form-item>
              
              <el-form-item label="视频状态">
                <el-select v-model="editingVideo.status" style="width: 100%">
                  <el-option label="处理中" value="processing" />
                  <el-option label="已就绪" value="ready" />
                  <el-option label="错误" value="error" />
                </el-select>
              </el-form-item>
            </el-form>
            
            <template #footer>
              <el-button @click="showVideoEditDialog = false">取消</el-button>
              <el-button type="primary" @click="updateVideo" :loading="saving">
                保存
              </el-button>
            </template>
          </el-dialog>
        </div>

        <!-- 用户管理 -->
        <div v-else-if="activeMenu === 'users'" class="users-content">
          <div class="content-header">
            <h2>👥 用户管理</h2>
            <div class="header-actions">
              <el-input 
                v-model="userSearch" 
                placeholder="搜索用户名或邮箱" 
                style="width: 250px; margin-right: 10px;"
                clearable
                @input="handleUserSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-select v-model="userRoleFilter" placeholder="筛选角色" style="width: 150px;" @change="handleUserFilter">
                <el-option label="全部用户" value="" />
                <el-option label="普通用户" value="user" />
                <el-option label="VIP用户" value="vip" />
                <el-option label="医生" value="doctor" />
                <el-option label="管理员" value="admin" />
              </el-select>
            </div>
          </div>

          <!-- 用户统计卡片 -->
          <div class="user-stats-cards">
            <div class="mini-stat-card">
              <div class="stat-icon">👤</div>
              <div class="stat-content">
                <div class="stat-number">{{ filteredUsers.length }}</div>
                <div class="stat-label">当前显示用户</div>
              </div>
            </div>
            <div class="mini-stat-card">
              <div class="stat-icon">🔹</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.user_analysis?.active_users || 0 }}</div>
                <div class="stat-label">活跃用户</div>
              </div>
            </div>
            <div class="mini-stat-card">
              <div class="stat-icon">⭐</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.user_analysis?.vip_users || 0 }}</div>
                <div class="stat-label">VIP用户</div>
              </div>
            </div>
            <div class="mini-stat-card">
              <div class="stat-icon">🩺</div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.user_analysis?.doctor_users || 0 }}</div>
                <div class="stat-label">医生用户</div>
              </div>
            </div>
          </div>

          <el-table :data="filteredUsers" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column prop="is_admin" label="管理员">
              <template #default="scope">
                <el-tag :type="scope.row.is_admin ? 'success' : ''">
                  {{ scope.row.is_admin ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="注册时间">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button 
                  size="small" 
                  :type="scope.row.is_admin ? 'danger' : 'primary'"
                  @click="toggleUserRole(scope.row.id, !scope.row.is_admin)"
                >
                  {{ scope.row.is_admin ? '取消管理员' : '设为管理员' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>

    <!-- 新增/编辑课程对话框 -->
    <el-dialog
      v-model="showCourseDialog"
      :title="editingCourse ? '编辑课程' : '新增课程'"
      width="600px"
    >
      <el-form :model="courseForm" :rules="courseRules" ref="courseFormRef" label-width="100px">
        <el-form-item label="课程标题" prop="title">
          <el-input v-model="courseForm.title" />
        </el-form-item>
        <el-form-item label="课程描述" prop="description">
          <el-input v-model="courseForm.description" type="textarea" rows="3" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="courseForm.category" placeholder="请选择分类">
            <el-option label="基础理论" value="basic" />
            <el-option label="四季养生" value="seasonal" />
            <el-option label="食疗养生" value="diet" />
            <el-option label="按摩推拿" value="massage" />
            <el-option label="中草药" value="herb" />
            <el-option label="逐病精讲" value="逐病精讲" />
            <el-option label="全面学医" value="全面学医" />
          </el-select>
        </el-form-item>
        <el-form-item label="讲师" prop="instructor">
          <el-input v-model="courseForm.instructor" />
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="courseForm.price" :min="0" :precision="2" />
          <el-checkbox v-model="courseForm.is_free" style="margin-left: 10px">免费课程</el-checkbox>
        </el-form-item>
        <el-form-item label="封面图片">
          <el-input v-model="courseForm.image_url" placeholder="图片URL" />
        </el-form-item>
        <el-form-item label="发布状态">
          <el-switch v-model="courseForm.is_published" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCourseDialog = false">取消</el-button>
        <el-button type="primary" @click="saveCourse" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { House, Reading, VideoCamera, User, UploadFilled, Download, Setting, ArrowDown, FolderAdd, Document, Search, Plus, Refresh, Check, Close, Edit, Delete, Switch } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const activeMenu = ref('dashboard')
const currentUser = ref({ username: 'admin' })
const stats = ref({
  total_courses: 0,
  total_users: 0,
  total_lessons: 0,
  total_enrollments: 0
})

const courses = ref([])
const filteredCourses = ref([])
const users = ref([])
const filteredUsers = ref([])
const recentCourses = ref([])
const systemLogs = ref([])
const backupLoading = ref(false)
const refreshing = ref(false)

// 搜索和筛选
const userSearch = ref('')
const userRoleFilter = ref('')
const courseSearch = ref('')
const courseStatusFilter = ref('')
const coursePriceFilter = ref('')  // 新增价格筛选
const videoSearch = ref('')
const videoStatusFilter = ref('')

const showCourseDialog = ref(false)
const showUploadDialog = ref(false)
const showVideoUploadDialog = ref(false)
const showVideoEditDialog = ref(false)
const editingCourse = ref(null)
const editingVideo = ref(null)
const saving = ref(false)

// 视频相关数据
const videos = ref([])
const filteredVideos = ref([])
const fileList = ref([])

const uploadUrl = ref('/api/video/admin/lessons/upload')
const uploadHeaders = ref({
  'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
})

// 新增上传流程状态
const uploadStep = ref(0)  // 上传步骤: 0-基本信息, 1-上传文件, 2-完成
const uploadProgress = ref(0)  // 上传进度

// 课程表单
const courseForm = ref({
  title: '',
  description: '',
  category: 'basic',
  instructor: '',
  price: 0,
  is_free: false,
  image_url: '',
  is_published: false
})

const courseRules = {
  title: [{ required: true, message: '请输入课程标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  instructor: [{ required: true, message: '请输入讲师名称', trigger: 'blur' }]
}

// 视频表单
const videoForm = ref({
  course_id: null,
  title: '',
  description: '',
  order: 1,
  is_free: false
})

const videoRules = {
  course_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
  title: [{ required: true, message: '请输入视频标题', trigger: 'blur' }],
  order: [{ required: true, message: '请输入课程顺序', trigger: 'blur' }]
}

// 计算属性
const uploadData = computed(() => ({
  course_id: videoForm.value.course_id,
  title: videoForm.value.title,
  description: videoForm.value.description,
  order: videoForm.value.order,
  is_free: videoForm.value.is_free
}))

const canProceedToUpload = computed(() => {
  return videoForm.value.course_id && 
         videoForm.value.title && 
         videoForm.value.order
})

// 方法
const handleMenuSelect = (index: string) => {
  activeMenu.value = index
  loadData()
}

const loadData = async () => {
  try {
    if (activeMenu.value === 'dashboard') {
      await Promise.all([
        loadStats(),
        loadRecentCourses()
      ])
    } else if (activeMenu.value === 'courses') {
      await loadCourses()
    } else if (activeMenu.value === 'videos') {
      await Promise.all([
        loadVideos(),
        loadCourses() // 加载课程列表用于视频上传时选择
      ])
    } else if (activeMenu.value === 'users') {
      await loadUsers()
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const loadStats = async () => {
  const response = await fetch('/api/admin/statistics', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
  })
  stats.value = await response.json()
}

const loadCourses = async () => {
  const response = await fetch('/api/admin/courses', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
  })
  courses.value = await response.json()
  filteredCourses.value = courses.value
}

// 课程搜索和筛选方法
const handleCourseSearch = () => {
  filterCourses()
}

const handleCourseFilter = () => {
  filterCourses()
}

const filterCourses = () => {
  let result = [...courses.value]
  
  // 按搜索词筛选
  if (courseSearch.value) {
    const searchLower = courseSearch.value.toLowerCase()
    result = result.filter(course => 
      course.title.toLowerCase().includes(searchLower) ||
      (course.instructor && course.instructor.toLowerCase().includes(searchLower))
    )
  }
  
  // 按状态筛选
  if (courseStatusFilter.value) {
    if (courseStatusFilter.value === 'published') {
      result = result.filter(course => course.is_published === true)
    } else if (courseStatusFilter.value === 'draft') {
      result = result.filter(course => course.is_published === false)
    }
  }
  
  // 按价格筛选
  if (coursePriceFilter.value) {
    if (coursePriceFilter.value === 'free') {
      result = result.filter(course => course.is_free === true)
    } else if (coursePriceFilter.value === 'paid') {
      result = result.filter(course => course.is_free === false)
    }
  }
  
  filteredCourses.value = result
}

const loadUsers = async () => {
  const response = await fetch('/api/admin/users', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
  })
  users.value = await response.json()
  filteredUsers.value = users.value
}

// 搜索和筛选方法
const handleUserSearch = () => {
  filterUsers()
}

const handleUserFilter = () => {
  filterUsers()
}

const filterUsers = () => {
  let result = [...users.value]
  
  // 按搜索词筛选
  if (userSearch.value) {
    const searchLower = userSearch.value.toLowerCase()
    result = result.filter(user => 
      user.username.toLowerCase().includes(searchLower) ||
      user.email.toLowerCase().includes(searchLower)
    )
  }
  
  // 按角色筛选
  if (userRoleFilter.value) {
    if (userRoleFilter.value === 'admin') {
      result = result.filter(user => user.is_admin || user.is_super_admin)
    } else {
      result = result.filter(user => user.role === userRoleFilter.value)
    }
  }
  
  filteredUsers.value = result
}

const loadRecentCourses = async () => {
  const response = await fetch('/api/admin/courses?limit=5', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
  })
  recentCourses.value = await response.json()
}

const editCourse = (courseId: number) => {
  const course = courses.value.find(c => c.id === courseId)
  if (course) {
    courseForm.value = { ...course }
    editingCourse.value = courseId
    showCourseDialog.value = true
  }
}

const saveCourse = async () => {
  saving.value = true
  try {
    const url = editingCourse.value 
      ? `/api/admin/courses/${editingCourse.value}`
      : '/api/admin/courses'
    
    const method = editingCourse.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify(courseForm.value)
    })
    
    if (response.ok) {
      ElMessage.success(editingCourse.value ? '课程更新成功' : '课程创建成功')
      showCourseDialog.value = false
      await loadCourses()
      resetCourseForm()
    }
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const deleteCourse = async (courseId: number) => {
  try {
    await ElMessageBox.confirm('确认删除这个课程吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await fetch(`/api/admin/courses/${courseId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    
    if (response.ok) {
      ElMessage.success('删除成功')
      await loadCourses()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const togglePublishStatus = async (course) => {
  const newStatus = !course.is_published
  const actionText = newStatus ? '发布' : '下架'
  
  try {
    const response = await fetch(`/api/admin/courses/${course.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify({
        ...course,
        is_published: newStatus
      })
    })
    
    if (response.ok) {
      ElMessage.success(`课程${actionText}成功`)
      await Promise.all([loadCourses(), loadStats()])
    } else {
      throw new Error(`${actionText}失败`)
    }
  } catch (error) {
    ElMessage.error(`课程${actionText}失败`)
  }
}

const manageLessons = (courseId: number) => {
  // 跳转到课时管理页面（后续实现）
  ElMessage.info('课时管理功能开发中...')
}

const toggleUserRole = async (userId: number, isAdmin: boolean) => {
  try {
    const response = await fetch(`/api/admin/users/${userId}/role`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: `is_admin=${isAdmin}`
    })
    
    if (response.ok) {
      ElMessage.success('权限更新成功')
      await loadUsers()
    }
  } catch (error) {
    ElMessage.error('权限更新失败')
  }
}

const beforeVideoUpload = (file: File) => {
  const isVideo = file.type.startsWith('video/')
  const isLt500M = file.size / 1024 / 1024 < 500

  if (!isVideo) {
    ElMessage.error('只能上传视频文件!')
    return false
  }
  if (!isLt500M) {
    ElMessage.error('视频文件大小不能超过 500MB!')
    return false
  }
  return true
}

const handleVideoSuccess = (response: any) => {
  ElMessage.success('视频上传成功!')
  console.log('上传成功:', response)
  uploadStep.value = 2
  uploadProgress.value = 100
  loadVideos() // 重新加载视频列表
}

const handleProgress = (event: any) => {
  uploadProgress.value = Math.round(event.percent)
  console.log('上传进度:', uploadProgress.value + '%')
}

const handleUploadError = (error: any) => {
  ElMessage.error('视频上传失败，请重试')
  console.error('上传错误:', error)
  uploadProgress.value = 0
}

// 新的上传流程方法
const nextUploadStep = async () => {
  if (uploadStep.value === 0) {
    // 验证表单
    try {
      await videoFormRef.value.validate()
      uploadStep.value = 1
    } catch (error) {
      ElMessage.error('请完善必填信息')
    }
  }
}

const getSelectedCourseName = () => {
  const course = courses.value.find(c => c.id === videoForm.value.course_id)
  return course ? course.title : '未选择课程'
}

const continueUpload = () => {
  resetVideoForm()
  uploadStep.value = 0
  uploadProgress.value = 0
}

const closeUploadDialog = () => {
  showVideoUploadDialog.value = false
  resetVideoForm()
}

// ===============================
// 视频管理相关方法
// ===============================

const loadVideos = async () => {
  try {
    const response = await fetch('/api/video/admin/lessons', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    if (response.ok) {
      videos.value = await response.json()
      filteredVideos.value = videos.value
    }
  } catch (error) {
    console.error('加载视频列表失败:', error)
    ElMessage.error('加载视频列表失败')
  }
}

const handleVideoSearch = () => {
  filterVideos()
}

const handleVideoFilter = () => {
  filterVideos()
}

const filterVideos = () => {
  let result = [...videos.value]
  
  // 按搜索词筛选
  if (videoSearch.value) {
    const searchLower = videoSearch.value.toLowerCase()
    result = result.filter(video => 
      video.title.toLowerCase().includes(searchLower) ||
      (video.course && video.course.title && video.course.title.toLowerCase().includes(searchLower))
    )
  }
  
  // 按状态筛选
  if (videoStatusFilter.value) {
    result = result.filter(video => video.status === videoStatusFilter.value)
  }
  
  filteredVideos.value = result
}

const editVideo = (video) => {
  editingVideo.value = { ...video }
  showVideoEditDialog.value = true
}

const updateVideo = async () => {
  if (!editingVideo.value) return
  
  try {
    saving.value = true
    const response = await fetch(`/api/video/admin/lessons/${editingVideo.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify(editingVideo.value)
    })
    
    if (response.ok) {
      ElMessage.success('视频更新成功')
      showVideoEditDialog.value = false
      loadVideos()
    } else {
      throw new Error('更新失败')
    }
  } catch (error) {
    console.error('更新视频失败:', error)
    ElMessage.error('更新视频失败')
  } finally {
    saving.value = false
  }
}

const deleteVideo = async (videoId) => {
  try {
    const response = await fetch(`/api/video/admin/lessons/${videoId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    
    if (response.ok) {
      ElMessage.success('视频删除成功')
      loadVideos()
    } else {
      throw new Error('删除失败')
    }
  } catch (error) {
    console.error('删除视频失败:', error)
    ElMessage.error('删除视频失败')
  }
}

const viewVideo = (video) => {
  if (video.video_url) {
    window.open(video.video_url, '_blank')
  } else {
    ElMessage.info('视频文件不可用')
  }
}

const resetVideoForm = () => {
  videoForm.value = {
    course_id: null,
    title: '',
    description: '',
    order: 1,
    is_free: false
  }
  fileList.value = []
  uploadStep.value = 0
  uploadProgress.value = 0
}

// 格式化时长显示
const formatDuration = (seconds) => {
  if (!seconds) return '未知'
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  switch (status) {
    case 'ready': return 'success'
    case 'processing': return 'warning'
    case 'error': return 'danger'
    default: return 'info'
  }
}

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case 'ready': return '已就绪'
    case 'processing': return '处理中'
    case 'error': return '错误'
    default: return status
  }
}

const resetCourseForm = () => {
  courseForm.value = {
    title: '',
    description: '',
    category: 'basic',
    instructor: '',
    price: 0,
    is_free: false,
    image_url: '',
    is_published: false
  }
  editingCourse.value = null
}


// 数据导出方法
const exportData = async (type: string, format: string) => {
  try {
    const response = await fetch(`/api/admin/export/${type}?format=${format}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    
    if (format === 'csv') {
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${type}_${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      ElMessage.success(`${type}数据导出成功`)
    } else {
      const data = await response.json()
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${type}_${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      ElMessage.success(`${type}数据导出成功`)
    }
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleExport = (command: string) => {
  const [type, format] = command.split('-')
  exportData(type, format)
}

// 系统管理方法
const createBackup = async () => {
  backupLoading.value = true
  try {
    const response = await fetch('/api/admin/system/backup', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    
    const result = await response.json()
    ElMessage.success(`备份创建成功: ${result.backup_file}`)
  } catch (error) {
    ElMessage.error('备份创建失败')
  } finally {
    backupLoading.value = false
  }
}

const loadSystemLogs = async () => {
  try {
    const response = await fetch('/api/admin/system/logs', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    
    const result = await response.json()
    systemLogs.value = result.logs || []
  } catch (error) {
    ElMessage.error('日志加载失败')
  }
}

const showAllLogs = () => {
  ElMessage.info('完整日志功能开发中...')
}

const refreshStats = async () => {
  refreshing.value = true
  try {
    await Promise.all([
      loadStats(),
      loadRecentCourses()
    ])
    ElMessage.success('数据刷新成功')
  } catch (error) {
    ElMessage.error('数据刷新失败')
  } finally {
    refreshing.value = false
  }
}

const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  window.location.href = '/admin/login'
}

// 课程统计卡片筛选方法
const filterByStatus = (status: string) => {
  courseStatusFilter.value = courseStatusFilter.value === status ? '' : status
  coursePriceFilter.value = '' // 清除价格筛选
  filterCourses()
}

const filterByPrice = (priceType: string) => {
  coursePriceFilter.value = coursePriceFilter.value === priceType ? '' : priceType
  courseStatusFilter.value = '' // 清除状态筛选
  filterCourses()
}

const clearCourseFilters = () => {
  courseStatusFilter.value = ''
  coursePriceFilter.value = ''
  courseSearch.value = ''
  filterCourses()
}

// 工具方法
const formatDate = (date) => {
  if (!date) return '--'
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

const formatSimpleDate = (date) => {
  if (!date) return '--'
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}

const formatCourseDuration = (minutes) => {
  if (!minutes) return '0分钟'
  if (minutes < 60) return `${minutes}分钟`
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  return `${hours}小时${remainingMinutes > 0 ? remainingMinutes + '分钟' : ''}`
}

const getCategoryText = (category) => {
  const categoryMap = {
    'basic': '基础理论',
    'seasonal': '四季养生',
    'diet': '食疗养生',
    'massage': '按摩推拿',
    'herb': '中草药',
    '逐病精讲': '逐病精讲',
    '全面学医': '全面学医'
  }
  return categoryMap[category] || category
}

const getCategoryTagType = (category) => {
  const typeMap = {
    'basic': 'primary',
    'seasonal': 'success',
    'diet': 'warning',
    'massage': 'info',
    'herb': 'danger',
    '逐病精讲': 'primary',
    '全面学医': 'success'
  }
  return typeMap[category] || 'info'
}

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
  
  loadData()
})
</script>

<style scoped>
.admin-dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background: #409eff;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.admin-layout {
  display: flex;
  flex: 1;
}

.admin-sidebar {
  width: 200px;
  background: #f5f5f5;
  border-right: 1px solid #e6e6e6;
}

.sidebar-menu {
  border: none;
  height: 100%;
}

.admin-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.stat-icon.courses { background: #e8f4fd; }
.stat-icon.users { background: #fff0e6; }
.stat-icon.lessons { background: #f0f9e6; }
.stat-icon.enrollments { background: #fef0f0; }

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.dashboard-actions {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 统计卡片样式 */
.user-stats-cards, .course-stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
  padding: 0 20px;
}

.mini-stat-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.mini-stat-card:hover {
  transform: translateY(-2px);
}

.mini-stat-card.clickable {
  cursor: pointer;
  user-select: none;
}

.mini-stat-card.clickable:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.mini-stat-card.clickable:active {
  transform: translateY(-1px);
}

.mini-stat-card.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
}

.mini-stat-card.active .stat-label {
  color: rgba(255, 255, 255, 0.9);
}

.mini-stat-card .stat-icon {
  font-size: 32px;
  margin-right: 15px;
}

.mini-stat-card .stat-content {
  flex: 1;
}

.mini-stat-card .stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #2c3e50;
  line-height: 1;
}

.mini-stat-card .stat-label {
  font-size: 14px;
  color: #7f8c8d;
  margin-top: 4px;
}

/* 欢迎区域样式 */
.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.welcome-content h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
}

.welcome-content p {
  margin: 0;
  opacity: 0.9;
  font-size: 16px;
}

.welcome-actions {
  display: flex;
  gap: 12px;
}

.welcome-actions .el-button {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.welcome-actions .el-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.recent-courses h3 {
  margin-bottom: 15px;
  color: #333;
}

.video-upload-area {
  margin-bottom: 20px;
}

.video-uploader {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 分析面板样式 */
.analysis-panels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.analysis-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.analysis-card h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #333;
}

.mini-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.mini-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.mini-stat .label {
  font-size: 14px;
  color: #666;
}

.mini-stat .value {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.stat-detail {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* 导出页面样式 */
.export-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.export-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.export-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  background: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.export-info {
  flex: 1;
}

.export-info h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
}

.export-info p {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.export-buttons {
  display: flex;
  gap: 8px;
}

/* 系统管理样式 */
.system-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.system-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.system-card h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #333;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.status-item .label {
  font-size: 14px;
  color: #666;
}

.log-container {
  max-height: 300px;
  overflow-y: auto;
  background: #f8f9fa;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 10px;
}

.log-line {
  font-size: 12px;
  font-family: 'Courier New', monospace;
  color: #555;
  margin-bottom: 4px;
  line-height: 1.4;
}

/* 视频管理样式 */
.videos-content {
  padding: 20px;
}

.video-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.video-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
}

.order-badge {
  background: #f0f9ff;
  color: #0369a1;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.video-uploader {
  margin-top: 10px;
}

.video-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: .2s;
}

.video-uploader .el-upload:hover {
  border-color: #409EFF;
}

.video-uploader .el-icon--upload {
  font-size: 67px;
  color: #C0C4CC;
  width: 148px;
  height: 148px;
  line-height: 148px;
  text-align: center;
}

.video-uploader .el-upload__text {
  color: #606266;
  font-size: 14px;
  text-align: center;
}

.video-uploader .el-upload__text em {
  color: #409EFF;
}

.form-tip {
  margin-left: 8px;
  font-size: 12px;
  color: #999;
}

/* 视频状态颜色 */
.video-status-ready {
  color: #67C23A;
}

.video-status-processing {
  color: #E6A23C;
}

.video-status-error {
  color: #F56C6C;
}

/* 视频列表布局改进 */
.video-list .el-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.video-list .el-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.video-list .el-table td {
  border-bottom: 1px solid #f0f0f0;
}

.video-list .el-table .el-button {
  margin-right: 8px;
}

.video-list .el-table .el-button:last-child {
  margin-right: 0;
}

/* 课程管理样式改进 */
.course-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.course-title {
  display: flex;
  align-items: center;
  font-size: 15px;
  line-height: 1.4;
}

.course-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #666;
}

.course-meta span {
  display: flex;
  align-items: center;
  gap: 2px;
}

.course-description {
  font-size: 12px;
  color: #999;
  line-height: 1.3;
  margin-top: 4px;
}

.price-info, .date-info {
  display: flex;
  justify-content: center;
  align-items: center;
}

.date-info {
  font-size: 12px;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  padding: 4px 8px;
  font-size: 12px;
  min-width: 60px;
}

.action-buttons .el-button .el-icon {
  margin-right: 2px;
}

/* 表格行样式改进 */
.el-table .el-table__row {
  transition: all 0.2s ease;
}

.el-table .el-table__row:hover {
  background-color: #f8f9ff;
}

.el-table th {
  background-color: #fafafa;
  font-weight: 600;
  color: #333;
}

.el-table td {
  padding: 12px 8px;
  border-bottom: 1px solid #f0f0f0;
}

/* 增强的视频上传对话框样式 */
.upload-dialog-content {
  padding: 10px 0;
}

.upload-step {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.upload-info-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  border-left: 4px solid #409eff;
}

.upload-info-card h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
}

.info-row {
  display: flex;
  margin-bottom: 8px;
}

.info-row .label {
  width: 60px;
  color: #666;
  font-weight: 500;
}

.info-row .value {
  flex: 1;
  color: #333;
}

.enhanced-video-uploader {
  margin-top: 20px;
}

.upload-area {
  padding: 40px;
  text-align: center;
}

.upload-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 16px;
}

.upload-text p {
  font-size: 16px;
  color: #606266;
  margin: 0 0 16px 0;
}

.upload-text em {
  color: #409eff;
  font-style: normal;
  text-decoration: underline;
}

.upload-hint {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hint-item {
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.upload-progress {
  margin-top: 20px;
  text-align: center;
}

.progress-text {
  margin-top: 10px;
  color: #409eff;
  font-weight: 500;
}

.upload-success {
  text-align: center;
  align-items: center;
}

.success-icon {
  margin-bottom: 20px;
}

.upload-success h3 {
  color: #67C23A;
  margin: 0 0 10px 0;
}

.upload-success p {
  color: #666;
  margin: 0 0 30px 0;
}

.success-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 响应式支持 */
@media (max-width: 768px) {
  .videos-content {
    padding: 10px;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .header-actions .el-input,
  .header-actions .el-select {
    width: 100% !important;
  }
}
</style>