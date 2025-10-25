<template>
  <div class="course-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h2>📚 课程管理</h2>
        <p>管理平台课程内容、分类和发布状态</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="createNewCourse">
          <el-icon><Plus /></el-icon>
          新增课程
        </el-button>
        <el-button @click="refreshCourses" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <div class="filter-row">
        <el-input
          v-model="searchText"
          placeholder="搜索课程标题或讲师"
          style="width: 300px"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-select
          v-model="categoryFilter"
          placeholder="筛选分类"
          style="width: 150px"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部分类" value="" />
          <el-option label="理论基础" value="THEORY" />
          <el-option label="临床实践" value="CLINICAL" />
          <el-option label="养生保健" value="WELLNESS" />
          <el-option label="针灸推拿" value="ACUPUNCTURE" />
          <el-option label="中药方剂" value="PHARMACY" />
          <el-option label="逐病精讲" value="DISEASE_SPECIFIC" />
          <el-option label="全面学医" value="COMPREHENSIVE" />
        </el-select>
        
        <el-select
          v-model="statusFilter"
          placeholder="发布状态"
          style="width: 120px"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部状态" value="" />
          <el-option label="已发布" value="published" />
          <el-option label="草稿" value="draft" />
        </el-select>
        
        <el-select
          v-model="priceFilter"
          placeholder="价格筛选"
          style="width: 120px"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部价格" value="" />
          <el-option label="免费" value="free" />
          <el-option label="付费" value="paid" />
        </el-select>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card" @click="filterByStatus('all')">
        <div class="stat-icon total">📚</div>
        <div class="stat-info">
          <div class="stat-number">{{ totalCourses }}</div>
          <div class="stat-label">总课程数</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByStatus('published')">
        <div class="stat-icon published">✅</div>
        <div class="stat-info">
          <div class="stat-number">{{ publishedCourses }}</div>
          <div class="stat-label">已发布</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByPrice('free')">
        <div class="stat-icon free">🆓</div>
        <div class="stat-info">
          <div class="stat-number">{{ freeCourses }}</div>
          <div class="stat-label">免费课程</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByPrice('paid')">
        <div class="stat-icon paid">💰</div>
        <div class="stat-info">
          <div class="stat-number">{{ paidCourses }}</div>
          <div class="stat-label">付费课程</div>
        </div>
      </div>
    </div>

    <!-- 课程表格 -->
    <div class="table-section">
      <el-table
        :data="paginatedCourses"
        style="width: 100%"
        v-loading="loading"
        row-key="id"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column label="课程信息" min-width="350">
          <template #default="scope">
            <div class="course-info">
              <div class="course-cover">
                <el-image
                  :src="scope.row.image_url"
                  fit="cover"
                  style="width: 60px; height: 40px; border-radius: 4px;"
                >
                  <template #error>
                    <div class="image-placeholder">📚</div>
                  </template>
                </el-image>
              </div>
              <div class="course-details">
                <div class="course-title">
                  <strong>{{ scope.row.title }}</strong>
                  <el-tag
                    :type="getCategoryTagType(scope.row.category)"
                    size="small"
                    style="margin-left: 8px"
                  >
                    {{ getCategoryText(scope.row.category) }}
                  </el-tag>
                </div>
                <div class="course-meta">
                  <span v-if="scope.row.instructor">👨‍🏫 {{ scope.row.instructor }}</span>
                  <span v-if="scope.row.total_lessons">📖 {{ scope.row.total_lessons }}课时</span>
                  <span v-if="scope.row.duration">⏱️ {{ formatDuration(scope.row.duration) }}</span>
                </div>
                <div class="course-description" v-if="scope.row.description">
                  {{ truncateText(scope.row.description, 80) }}
                </div>
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
              {{ scope.row.is_published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="学员数" width="100">
          <template #default="scope">
            <div class="enrollment-info">
              <span class="enrollment-count">{{ scope.row.enrollment_count || 0 }}</span>
              <div class="enrollment-label">学员</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="120">
          <template #default="scope">
            <div class="time-info">
              {{ formatSimpleDate(scope.row.created_at) }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button size="small" @click="viewCourse(scope.row)">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editCourse(scope.row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button 
                size="small"
                :type="scope.row.is_published ? 'warning' : 'success'"
                @click="togglePublishStatus(scope.row)"
              >
                <el-icon><Switch /></el-icon>
                {{ scope.row.is_published ? '下架' : '发布' }}
              </el-button>
              <el-dropdown @command="handleCourseAction">
                <el-button size="small" type="info">
                  更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="`lessons-${scope.row.id}`">管理课时</el-dropdown-item>
                    <el-dropdown-item :command="`copy-${scope.row.id}`">复制课程</el-dropdown-item>
                    <el-dropdown-item divided :command="`delete-${scope.row.id}`">删除课程</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredCourses.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 批量操作 -->
    <div class="batch-actions" v-if="selectedCourses.length > 0">
      <div class="batch-info">
        已选择 {{ selectedCourses.length }} 个课程
      </div>
      <div class="batch-buttons">
        <el-button @click="batchPublish">批量发布</el-button>
        <el-button @click="batchUnpublish">批量下架</el-button>
        <el-button type="danger" @click="batchDelete">批量删除</el-button>
      </div>
    </div>

    <!-- 课程详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="课程详情" width="800px">
      <div v-if="currentCourse" class="course-detail">
        <div class="detail-header">
          <div class="course-cover-large">
            <el-image
              :src="currentCourse.image_url"
              fit="cover"
              style="width: 200px; height: 120px; border-radius: 8px;"
            >
              <template #error>
                <div class="image-placeholder-large">📚</div>
              </template>
            </el-image>
          </div>
          <div class="course-basic-info">
            <h3>{{ currentCourse.title }}</h3>
            <div class="course-tags">
              <el-tag :type="getCategoryTagType(currentCourse.category)">
                {{ getCategoryText(currentCourse.category) }}
              </el-tag>
              <el-tag :type="currentCourse.is_published ? 'success' : 'warning'">
                {{ currentCourse.is_published ? '已发布' : '草稿' }}
              </el-tag>
              <el-tag :type="currentCourse.is_free ? 'success' : 'warning'">
                {{ currentCourse.is_free ? '免费' : `¥${currentCourse.price}` }}
              </el-tag>
            </div>
            <div class="course-stats">
              <div class="stat-item">
                <span class="label">讲师：</span>
                <span class="value">{{ currentCourse.instructor || '未设置' }}</span>
              </div>
              <div class="stat-item">
                <span class="label">课时：</span>
                <span class="value">{{ currentCourse.total_lessons || 0 }}节</span>
              </div>
              <div class="stat-item">
                <span class="label">学员：</span>
                <span class="value">{{ currentCourse.enrollment_count || 0 }}人</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="detail-section">
            <h4>课程描述</h4>
            <p>{{ currentCourse.description || '暂无描述' }}</p>
          </div>
          
          <div class="detail-section">
            <h4>创建信息</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">创建时间：</span>
                <span class="value">{{ formatDate(currentCourse.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="label">最后更新：</span>
                <span class="value">{{ formatDate(currentCourse.updated_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
        <el-button type="primary" @click="editCourse(currentCourse)">编辑</el-button>
      </template>
    </el-dialog>

    <!-- 编辑课程对话框 -->
    <el-dialog 
      v-model="showEditDialog" 
      :title="editingCourseId ? '编辑课程' : '新增课程'" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="courseForm" :rules="courseRules" ref="courseFormRef" label-width="100px">
        <el-form-item label="课程标题" prop="title">
          <el-input 
            v-model="courseForm.title" 
            placeholder="请输入课程标题"
            show-word-limit
            maxlength="100"
          />
        </el-form-item>
        
        <el-form-item label="课程分类" prop="category">
          <el-select v-model="courseForm.category" style="width: 100%" placeholder="请选择分类">
            <el-option label="理论基础" value="THEORY" />
            <el-option label="临床实践" value="CLINICAL" />
            <el-option label="养生保健" value="WELLNESS" />
            <el-option label="针灸推拿" value="ACUPUNCTURE" />
            <el-option label="中药方剂" value="PHARMACY" />
            <el-option label="逐病精讲" value="DISEASE_SPECIFIC" />
            <el-option label="全面学医" value="COMPREHENSIVE" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="讲师" prop="instructor">
          <el-input v-model="courseForm.instructor" placeholder="请输入讲师姓名" />
        </el-form-item>
        
        <el-form-item label="课程描述" prop="description">
          <el-input 
            v-model="courseForm.description" 
            type="textarea" 
            :rows="4"
            placeholder="请输入课程描述"
            show-word-limit
            maxlength="500"
          />
        </el-form-item>
        
        <el-form-item label="价格设置">
          <div class="price-setting">
            <el-switch
              v-model="courseForm.is_free"
              active-text="免费"
              inactive-text="付费"
              style="margin-right: 16px"
            />
            <el-input-number
              v-model="courseForm.price"
              :min="0"
              :precision="2"
              :disabled="courseForm.is_free"
              placeholder="课程价格"
              style="width: 150px"
            />
            <span v-if="!courseForm.is_free" style="margin-left: 8px">元</span>
          </div>
        </el-form-item>
        
        <el-form-item label="封面图片">
          <div class="image-upload">
            <el-input 
              v-model="courseForm.image_url" 
              placeholder="请输入图片URL或上传图片"
              style="width: 300px"
            />
            <el-button style="margin-left: 12px" @click="handleImageUpload">上传图片</el-button>
          </div>
          <div class="image-preview" v-if="courseForm.image_url">
            <el-image
              :src="courseForm.image_url"
              fit="cover"
              style="width: 120px; height: 80px; border-radius: 4px; margin-top: 8px"
            >
              <template #error>
                <div class="image-error">图片加载失败</div>
              </template>
            </el-image>
          </div>
        </el-form-item>

        <el-form-item label="课程视频">
          <div class="video-upload-section">
            <el-upload
              class="video-uploader"
              :action="'/api/admin/upload/video'"
              :show-file-list="false"
              :before-upload="beforeVideoUpload"
              :on-success="handleVideoSuccess"
              :on-error="handleVideoError"
              :on-progress="handleVideoProgress"
              :headers="uploadHeaders"
              accept="video/*"
            >
              <el-button size="default" type="primary" :loading="videoUploading">
                <el-icon><VideoCamera /></el-icon>
                {{ videoUploading ? '上传中...' : '上传视频' }}
              </el-button>
              <template #tip>
                <div class="upload-tip">
                  支持 MP4、AVI、MOV 等格式，文件大小不超过 500MB
                </div>
              </template>
            </el-upload>
            
            <!-- 视频上传进度 -->
            <div v-if="videoUploading" class="upload-progress">
              <el-progress 
                :percentage="videoUploadProgress" 
                :show-text="true"
                :format="formatProgress"
              />
            </div>
            
            <!-- 视频预览 -->
            <div v-if="courseForm.video_url && !videoUploading" class="video-preview">
              <div class="video-info">
                <el-icon class="video-icon"><VideoCamera /></el-icon>
                <div class="video-details">
                  <div class="video-name">{{ courseForm.video_name || '课程视频.mp4' }}</div>
                  <div class="video-size">{{ formatFileSize(courseForm.video_size) }}</div>
                  <div class="video-url">{{ courseForm.video_url }}</div>
                </div>
              </div>
              <div class="video-actions">
                <el-button size="small" @click="previewVideo">预览</el-button>
                <el-button size="small" type="danger" @click="removeVideo">删除</el-button>
              </div>
            </div>
            
            <!-- 视频URL输入（备用方案） -->
            <div class="video-url-input" style="margin-top: 12px;">
              <el-input 
                v-model="courseForm.video_url" 
                placeholder="或者直接输入视频URL地址"
                style="width: 400px"
              />
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="发布状态">
          <el-switch
            v-model="courseForm.is_published"
            active-text="立即发布"
            inactive-text="保存为草稿"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveCourse" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  Plus, Refresh, Search, View, Edit, Switch, ArrowDown, VideoCamera
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const courses = ref([])
const filteredCourses = ref([])
const loading = ref(false)
const saving = ref(false)

// 搜索和筛选
const searchText = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')
const priceFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(20)

// 选择的课程
const selectedCourses = ref([])

// 对话框状态
const showDetailDialog = ref(false)
const showEditDialog = ref(false)
const showCreateDialog = ref(false)
const currentCourse = ref(null)
const editingCourseId = ref(null)

// 表单引用
const courseFormRef = ref(null)

// 视频上传状态
const videoUploading = ref(false)
const videoUploadProgress = ref(0)

// 上传相关配置  
const uploadHeaders = computed(() => ({
  'Authorization': `Bearer ${localStorage.getItem('admin_token') || ''}`
}))

// 表单数据
const courseForm = ref({
  title: '',
  description: '',
  category: 'THEORY',
  instructor: '',
  price: 0,
  is_free: true,
  image_url: '',
  video_url: '',
  video_name: '',
  video_size: 0,
  is_published: false
})

// 表单验证规则
const courseRules = {
  title: [
    { required: true, message: '请输入课程标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度应为2-100字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择课程分类', trigger: 'change' }
  ],
  instructor: [
    { required: true, message: '请输入讲师姓名', trigger: 'blur' }
  ]
}

// 计算属性
const totalCourses = computed(() => courses.value.length)
const publishedCourses = computed(() => courses.value.filter(c => c.is_published).length)
const freeCourses = computed(() => courses.value.filter(c => c.is_free).length)
const paidCourses = computed(() => courses.value.filter(c => !c.is_free).length)

const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredCourses.value.slice(start, end)
})

// 方法
const loadCourses = async () => {
  try {
    loading.value = true
    // 直接使用公共API，不需要管理员认证
    const response = await fetch('/api/courses/?limit=100')

    if (response.ok) {
      courses.value = await response.json()
      filteredCourses.value = courses.value
    } else {
      // 加载失败时显示空列表
      courses.value = []
      filteredCourses.value = []
      ElMessage.warning('无法加载课程列表')
    }
  } catch (error) {
    console.error('加载课程失败:', error)
    ElMessage.error('加载课程失败，请检查网络连接')
    courses.value = []
    filteredCourses.value = []
  } finally {
    loading.value = false
  }
}

const refreshCourses = () => {
  loadCourses()
}

const handleSearch = () => {
  applyFilters()
}

const handleFilter = () => {
  applyFilters()
}

const applyFilters = () => {
  let result = [...courses.value]
  
  // 搜索筛选
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(course =>
      course.title.toLowerCase().includes(search) ||
      (course.instructor && course.instructor.toLowerCase().includes(search))
    )
  }
  
  // 分类筛选
  if (categoryFilter.value) {
    result = result.filter(course => course.category === categoryFilter.value)
  }
  
  // 状态筛选
  if (statusFilter.value) {
    result = result.filter(course => {
      if (statusFilter.value === 'published') return course.is_published
      if (statusFilter.value === 'draft') return !course.is_published
      return true
    })
  }
  
  // 价格筛选
  if (priceFilter.value) {
    result = result.filter(course => {
      if (priceFilter.value === 'free') return course.is_free
      if (priceFilter.value === 'paid') return !course.is_free
      return true
    })
  }
  
  filteredCourses.value = result
  currentPage.value = 1 // 重置到第一页
}

const filterByStatus = (status: string) => {
  if (status === 'all') {
    statusFilter.value = ''
  } else {
    statusFilter.value = status
  }
  applyFilters()
}

const filterByPrice = (price: string) => {
  priceFilter.value = price
  applyFilters()
}

const viewCourse = (course: any) => {
  currentCourse.value = course
  showDetailDialog.value = true
}

const createNewCourse = () => {
  resetCourseForm()
  editingCourseId.value = null
  showEditDialog.value = true
}

const editCourse = (course: any) => {
  editingCourseId.value = course.id
  courseForm.value = {
    title: course.title,
    description: course.description || '',
    category: course.category,
    instructor: course.instructor || '',
    price: course.price || 0,
    is_free: course.is_free,
    image_url: course.image_url || '',
    is_published: course.is_published
  }
  showEditDialog.value = true
  showDetailDialog.value = false
}

const saveCourse = async () => {
  try {
    // 表单验证
    await courseFormRef.value?.validate()
    
    saving.value = true
    
    if (editingCourseId.value) {
      // 编辑现有课程 - 调用后端API
      const courseData = {
        title: courseForm.value.title,
        description: courseForm.value.description,
        category: courseForm.value.category,
        instructor: courseForm.value.instructor,
        price: courseForm.value.price,
        is_free: courseForm.value.is_free,
        image_url: courseForm.value.image_url,
        is_published: courseForm.value.is_published
        // 注意：不发送video_url，因为Course模型中没有这个字段
      }
      
      const response = await fetch(`/api/admin/courses/${editingCourseId.value}`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify(courseData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '更新失败')
      }

      const updatedCourse = await response.json()
      
      // 更新本地数据
      const courseIndex = courses.value.findIndex(c => c.id === editingCourseId.value)
      if (courseIndex !== -1) {
        courses.value[courseIndex] = updatedCourse
      }
      
      ElMessage.success('课程更新成功')
      // 如果有视频URL，创建或更新课时      if (courseForm.value.video_url) {        createOrUpdateLesson(editingCourseId.value)      }
    } else {
      // 创建新课程 - 调用后端API
      const courseData = {
        title: courseForm.value.title,
        description: courseForm.value.description,
        category: courseForm.value.category,
        instructor: courseForm.value.instructor,
        price: courseForm.value.price,
        is_free: courseForm.value.is_free,
        image_url: courseForm.value.image_url,
        is_published: courseForm.value.is_published,
        total_lessons: 0,
        total_duration: 0
      }
      
      const response = await fetch('/api/admin/courses', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify(courseData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '创建失败')
      }

      const newCourse = await response.json()
      console.log('新课程创建成功:', newCourse)
      
      // 如果有视频URL，需要为这个课程创建第一个课时
      if (courseForm.value.video_url) {
        console.log('正在为课程创建视频课时...')
        const lessonData = {
          course_id: newCourse.id,
          title: `${courseForm.value.title} - 第一课`,
          description: courseForm.value.description || '课程主要内容',
          order: 1,
          video_url: courseForm.value.video_url,
          is_free: courseForm.value.is_free || false,
          status: 'ready'
        }
        
        try {
          const lessonResponse = await fetch(`/api/admin/courses/${newCourse.id}/lessons`, {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
            },
            body: JSON.stringify(lessonData)
          })
          
          if (lessonResponse.ok) {
            console.log('课时创建成功')
            // 更新课程的总课时数
            newCourse.total_lessons = 1
          } else {
            console.error('课时创建失败')
          }
        } catch (error) {
          console.error('创建课时时出错:', error)
        }
      }
      
      // 更新本地数据
      courses.value.unshift(newCourse)
      ElMessage.success('课程创建成功！')
      // 如果有视频URL，创建或更新课时      if (courseForm.value.video_url) {        createOrUpdateLesson(editingCourseId.value)      }
    }
    
    // 更新筛选后的课程列表
    applyFilters()
    
    showEditDialog.value = false
    editingCourseId.value = null
    resetCourseForm()
    
  } catch (error) {
    console.error('保存课程失败:', error)
    if (error.name === 'ValidationError') {
      ElMessage.warning('请完善必填信息')
    } else {
      // 改进错误信息显示
      let errorMsg = '保存失败'
      if (error.message) {
        errorMsg += `: ${error.message}`
      } else if (typeof error === 'string') {
        errorMsg += `: ${error}`
      } else if (error.detail) {
        errorMsg += `: ${error.detail}`
      }
      ElMessage.error(errorMsg)
    }
  } finally {
    saving.value = false
  }
}

const togglePublishStatus = async (course: any) => {
  const newStatus = !course.is_published
  const actionText = newStatus ? '发布' : '下架'

  const oldStatus = course.is_published

  try {
    // 先更新本地状态（乐观更新）
    course.is_published = newStatus

    // 调用后端API保存到数据库
    const response = await fetch(`/api/courses/${course.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify({ is_published: newStatus })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || errorData.message || `${actionText}失败`)
    }

    ElMessage.success(`课程${actionText}成功`)
      // 如果有视频URL，创建或更新课时      if (courseForm.value.video_url) {        createOrUpdateLesson(editingCourseId.value)      }
  } catch (error: any) {
    console.error(`课程${actionText}失败:`, error)
    ElMessage.error(error.message || `课程${actionText}失败`)
    // 回滚状态
    course.is_published = oldStatus
  }
}

const handleCourseAction = (command: string) => {
  const [action, courseId] = command.split('-')
  
  switch (action) {
    case 'lessons':
      ElMessage.info('课时管理功能开发中...')
      break
    case 'copy':
      ElMessage.info('复制课程功能开发中...')
      break
    case 'delete':
      handleDeleteCourse(parseInt(courseId))
      break
  }
}

const handleDeleteCourse = async (courseId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个课程吗？此操作不可恢复！', '删除确认', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 调用删除API
    const response = await fetch(`/api/admin/courses/${courseId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || errorData.message || '删除失败')
    }
    
    ElMessage.success('课程删除成功')
      // 如果有视频URL，创建或更新课时      if (courseForm.value.video_url) {        createOrUpdateLesson(editingCourseId.value)      }
    await loadCourses()  // 重新加载课程列表
  } catch (error) {
    if (error.message && error.message !== 'cancel') {
      // 显示删除错误，但排除用户取消的情况
      ElMessage.error(`删除失败: ${error.message}`)
    }
    // 用户取消删除时不显示错误
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedCourses.value = selection
}

const batchPublish = () => {
  ElMessage.info('批量发布功能开发中...')
}

const batchUnpublish = () => {
  ElMessage.info('批量下架功能开发中...')
}

const batchDelete = () => {
  ElMessage.info('批量删除功能开发中...')
}

const handleImageUpload = () => {
  ElMessage.info('图片上传功能开发中...')
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// 视频上传相关方法
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

  videoUploading.value = true
  videoUploadProgress.value = 0
  return true
}

const handleVideoSuccess = (response: any, file: any) => {
  videoUploading.value = false
  videoUploadProgress.value = 100
  
  console.log('视频上传成功响应:', response)
  
  // 根据admin API的响应格式设置视频URL
  if (response.upload_url) {
    courseForm.value.video_url = `http://localhost:8001${response.upload_url}`
  } else if (response.file_path) {
    courseForm.value.video_url = `http://localhost:8001/${response.file_path.replace(/\\/g, '/')}`
  }
  
  courseForm.value.video_name = response.original_filename || file.name
  courseForm.value.video_size = response.file_size || file.size || 0
  
  ElMessage.success('视频上传成功!')
      // 如果有视频URL，创建或更新课时      if (courseForm.value.video_url) {        createOrUpdateLesson(editingCourseId.value)      }
}

const handleVideoError = (error: any) => {
  videoUploading.value = false
  videoUploadProgress.value = 0
  console.error('视频上传失败:', error)
  
  // 检查具体错误信息
  let errorMessage = '视频上传失败，请重试'
  if (error && error.status === 401) {
    errorMessage = '认证失败，请重新登录管理员账户'
  } else if (error && error.status === 413) {
    errorMessage = '文件太大，请选择小于500MB的视频文件'
  } else if (error && error.message) {
    errorMessage = error.message
  }
  
  ElMessage.error(errorMessage)
  
  // 输出详细调试信息
  console.log('当前admin_token:', localStorage.getItem('admin_token'))
  console.log('上传错误详情:', error)
}

const handleVideoProgress = (event: any) => {
  if (event.percent) {
    videoUploadProgress.value = Math.round(event.percent)
  }
}

const previewVideo = () => {
  if (courseForm.value.video_url) {
    // 在新窗口中打开视频预览
    window.open(courseForm.value.video_url, '_blank')
  } else {
    ElMessage.warning('没有可预览的视频')
  }
}

const removeVideo = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个视频吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    courseForm.value.video_url = ''
    courseForm.value.video_name = ''
    courseForm.value.video_size = 0
    
    ElMessage.success('视频已删除')
      // 如果有视频URL，创建或更新课时      if (courseForm.value.video_url) {        createOrUpdateLesson(editingCourseId.value)      }
  } catch {
    // 用户取消删除
  }
}

const formatProgress = (percentage: number) => {
  return `${percentage}%`
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 工具方法
const getCategoryText = (category: string) => {
  const categoryMap = {
    'THEORY': '理论基础',
    'CLINICAL': '临床实践',
    'WELLNESS': '养生保健',
    'ACUPUNCTURE': '针灸推拿',
    'PHARMACY': '中药方剂',
    'DISEASE_SPECIFIC': '逐病精讲',
    'COMPREHENSIVE': '全面学医'
  }
  return categoryMap[category] || category
}

const getCategoryTagType = (category: string) => {
  const typeMap = {
    'THEORY': 'primary',
    'CLINICAL': 'success',
    'WELLNESS': 'warning',
    'ACUPUNCTURE': 'info',
    'PHARMACY': 'danger',
    'DISEASE_SPECIFIC': '',
    'COMPREHENSIVE': 'primary'
  }
  return typeMap[category] || 'info'
}

const formatDuration = (minutes: number) => {
  if (!minutes) return '未知'
  if (minutes < 60) return `${minutes}分钟`
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  return `${hours}小时${remainingMinutes > 0 ? remainingMinutes + '分钟' : ''}`
}

const formatDate = (date: string | Date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatSimpleDate = (date: string | Date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  })
}

const truncateText = (text: string, length: number) => {
  if (!text) return ''
  return text.length > length ? text.slice(0, length) + '...' : text
}

const resetCourseForm = () => {
  courseForm.value = {
    title: '',
    description: '',
    category: 'THEORY',
    instructor: '',
    price: 0,
    is_free: true,
    image_url: '',
    video_url: '',
    video_name: '',
    video_size: 0,
    is_published: false
  }
  
  // 重置视频上传状态
  videoUploading.value = false
  videoUploadProgress.value = 0
}

// 生命周期
onMounted(() => {
  loadCourses()
})
</script>

<style scoped>
.course-management {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.filter-section {
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.filter-row {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 16px;
}

.stat-icon.total { background: #e6f7ff; }
.stat-icon.published { background: #f6ffed; }
.stat-icon.free { background: #fff0e6; }
.stat-icon.paid { background: #f9f0ff; }

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.table-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.course-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.course-cover {
  flex-shrink: 0;
}

.image-placeholder {
  width: 60px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 20px;
  color: #999;
}

.course-details {
  flex: 1;
  min-width: 0;
}

.course-title {
  display: flex;
  align-items: center;
  font-size: 14px;
  margin-bottom: 6px;
}

.course-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.course-description {
  font-size: 12px;
  color: #999;
  line-height: 1.3;
}

.price-info, .enrollment-info, .time-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.enrollment-count {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.enrollment-label {
  font-size: 12px;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.pagination-section {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.batch-actions {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 16px;
  z-index: 1000;
}

.batch-info {
  font-size: 14px;
  color: #666;
}

.batch-buttons {
  display: flex;
  gap: 8px;
}

/* 课程详情对话框 */
.course-detail {
  padding: 0;
}

.detail-header {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.course-cover-large {
  flex-shrink: 0;
}

.image-placeholder-large {
  width: 200px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  font-size: 48px;
  color: #999;
}

.course-basic-info {
  flex: 1;
}

.course-basic-info h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: #333;
}

.course-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.course-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  gap: 8px;
}

.stat-item .label {
  color: #666;
  font-size: 14px;
}

.stat-item .value {
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  color: #333;
}

.detail-section p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.info-item {
  display: flex;
  gap: 8px;
}

.info-item .label {
  color: #666;
  font-size: 14px;
  min-width: 80px;
}

.info-item .value {
  color: #333;
  font-size: 14px;
}

/* 编辑表单 */
.price-setting {
  display: flex;
  align-items: center;
}

.image-upload {
  display: flex;
  align-items: center;
}

.image-preview {
  margin-top: 8px;
}

.image-error {
  width: 120px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 4px;
  color: #999;
  font-size: 12px;
}

/* 视频上传相关样式 */
.video-upload-section {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  background: #fafbfc;
}

.video-uploader {
  margin-bottom: 12px;
}

.upload-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 8px;
  line-height: 1.4;
}

.upload-progress {
  margin: 12px 0;
}

.video-preview {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  padding: 12px;
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.video-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.video-icon {
  color: #409eff;
  font-size: 24px;
}

.video-details {
  flex: 1;
}

.video-name {
  font-weight: 500;
  color: #333;
  font-size: 14px;
  margin-bottom: 4px;
}

.video-size {
  color: #909399;
  font-size: 12px;
  margin-bottom: 2px;
}

.video-url {
  color: #909399;
  font-size: 11px;
  word-break: break-all;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.video-actions {
  display: flex;
  gap: 8px;
}

.video-url-input {
  border-top: 1px dashed #e4e7ed;
  padding-top: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-row .el-input,
  .filter-row .el-select {
    width: 100% !important;
  }
  
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .detail-header {
    flex-direction: column;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .course-info {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
// 创建或更新课时
const createOrUpdateLesson = async (courseId) => {
  try {
    const lessonData = {
      title: courseForm.value.title + ' - 主课',
      description: courseForm.value.description || '课程主要内容',
      order: 1,
      duration: 1800, // 默认30分钟
      video_url: courseForm.value.video_url,
      is_free: courseForm.value.is_free,
      video_id: courseForm.value.video_id || null,
      cover_url: courseForm.value.cover_url || null
    }
    
    // 检查是否已有课时
    const lessonsResponse = await fetch()
    if (lessonsResponse.ok) {
      const existingLessons = await lessonsResponse.json()
      
      if (existingLessons.length > 0) {
        // 更新第一个课时
        await fetch(, {
          method: 'PUT',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': 
          },
          body: JSON.stringify(lessonData)
        })
        console.log('课时更新成功')
      } else {
        // 创建新课时
        await fetch(, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': 
          },
          body: JSON.stringify(lessonData)
        })
        console.log('课时创建成功')
      }
    }
  } catch (error) {
    console.error('创建/更新课时失败:', error)
    // 不阻止课程保存，只记录错误
  }
}
