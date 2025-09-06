<template>
  <div class="product-management">
    <div class="page-header">
      <div class="header-content">
        <h2>🛍️ 商品管理</h2>
        <p>管理平台商品信息、价格和库存状态</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="createNewProduct">
          <el-icon><Plus /></el-icon>
          新增商品
        </el-button>
        <el-button :loading="loading" @click="loadProducts">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon total">🛍️</div>
        <div class="stat-info">
          <div class="stat-number">{{ productStats.total }}</div>
          <div class="stat-label">商品总数</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon active">✅</div>
        <div class="stat-info">
          <div class="stat-number">{{ productStats.active }}</div>
          <div class="stat-label">在售商品</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon stock">📦</div>
        <div class="stat-info">
          <div class="stat-number">{{ productStats.lowStock }}</div>
          <div class="stat-label">库存不足</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon revenue">💰</div>
        <div class="stat-info">
          <div class="stat-number">¥{{ productStats.revenue.toLocaleString() }}</div>
          <div class="stat-label">本月销售额</div>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-card>
        <div class="filter-content">
          <el-input
            v-model="searchQuery"
            placeholder="搜索商品名称、描述..."
            style="width: 300px"
            clearable
            @input="searchProducts"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="selectedCategory"
            placeholder="选择分类"
            style="width: 180px"
            clearable
            @change="filterByCategory"
          >
            <el-option label="全部分类" value="" />
            <el-option label="中药材" value="中药材" />
            <el-option label="养生产品" value="养生产品" />
            <el-option label="医疗器械" value="医疗器械" />
            <el-option label="保健食品" value="保健食品" />
            <el-option label="中医书籍" value="中医书籍" />
            <el-option label="配套用品" value="配套用品" />
          </el-select>
          
          <el-select
            v-model="selectedStatus"
            placeholder="选择状态"
            style="width: 150px"
            clearable
            @change="filterByStatus"
          >
            <el-option label="全部状态" value="" />
            <el-option label="在售" value="active" />
            <el-option label="下架" value="inactive" />
            <el-option label="缺货" value="out_of_stock" />
          </el-select>
        </div>
      </el-card>
    </div>

    <!-- 商品列表 -->
    <div class="table-section">
      <el-card>
        <el-table
          :data="filteredProducts"
          v-loading="loading"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          
          <el-table-column prop="image" label="商品图片" width="100">
            <template #default="scope">
              <el-avatar
                :size="60"
                :src="scope.row.images && scope.row.images.length > 0 ? scope.row.images[0] : scope.row.image"
                shape="square"
                fit="cover"
              >
                <el-icon><Picture /></el-icon>
              </el-avatar>
            </template>
          </el-table-column>
          
          <el-table-column prop="name" label="商品名称" min-width="200">
            <template #default="scope">
              <div>
                <div class="product-name">{{ scope.row.name }}</div>
                <div class="product-desc">{{ scope.row.description }}</div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="category" label="分类" width="120">
            <template #default="scope">
              <el-tag :type="getCategoryTagType(scope.row.category)" size="small">
                {{ getCategoryName(scope.row.category) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="price" label="价格" width="120" sortable>
            <template #default="scope">
              <span class="price">¥{{ scope.row.price.toFixed(2) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="stock" label="库存" width="100" sortable>
            <template #default="scope">
              <el-tag 
                :type="scope.row.stock > 10 ? 'success' : scope.row.stock > 0 ? 'warning' : 'danger'"
                size="small"
              >
                {{ scope.row.stock }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="sales" label="销量" width="100" sortable />
          
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'" size="small">
                {{ scope.row.status === 'active' ? '在售' : '下架' }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="160" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="editProduct(scope.row)">编辑</el-button>
              <el-button
                size="small"
                :type="scope.row.status === 'active' ? 'warning' : 'success'"
                @click="toggleProductStatus(scope.row)"
              >
                {{ scope.row.status === 'active' ? '下架' : '上架' }}
              </el-button>
              <el-button size="small" type="danger" @click="deleteProduct(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 批量操作 -->
        <div class="batch-actions" v-if="selectedProducts.length > 0">
          <span>已选择 {{ selectedProducts.length }} 个商品</span>
          <el-button size="small" @click="batchUpdateStatus('active')">批量上架</el-button>
          <el-button size="small" @click="batchUpdateStatus('inactive')">批量下架</el-button>
          <el-button size="small" type="danger" @click="batchDelete">批量删除</el-button>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="totalProducts"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 新增/编辑商品对话框 -->
    <el-dialog
      v-model="showProductDialog"
      :title="isEditing ? '编辑商品' : '新增商品'"
      width="800px"
      @close="resetProductForm"
    >
      <el-form
        ref="productFormRef"
        :model="productForm"
        :rules="productRules"
        label-width="100px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="商品名称" prop="name">
              <el-input v-model="productForm.name" placeholder="请输入商品名称" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="商品分类" prop="category">
              <el-select v-model="productForm.category" placeholder="选择商品分类" style="width: 100%">
                <el-option label="中药材" value="中药材" />
                <el-option label="养生产品" value="养生产品" />
                <el-option label="医疗器械" value="医疗器械" />
                <el-option label="保健食品" value="保健食品" />
                <el-option label="中医书籍" value="中医书籍" />
                <el-option label="配套用品" value="配套用品" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="商品价格" prop="price">
              <el-input-number
                v-model="productForm.price"
                :min="0"
                :precision="2"
                style="width: 100%"
                placeholder="请输入价格"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="库存数量" prop="stock">
              <el-input-number
                v-model="productForm.stock"
                :min="0"
                style="width: 100%"
                placeholder="请输入库存数量"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="productForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入商品描述"
          />
        </el-form-item>

        <el-form-item label="商品详情">
          <el-input
            v-model="productForm.details"
            type="textarea"
            :rows="6"
            placeholder="请输入商品详细信息"
          />
        </el-form-item>

        <el-form-item label="商品图片">
          <el-upload
            class="image-uploader"
            :show-file-list="false"
            :before-upload="beforeImageUpload"
            action="/api/upload/image"
          >
            <img v-if="productForm.image" :src="productForm.image" class="uploaded-image" />
            <el-icon v-else class="image-uploader-icon"><Plus /></el-icon>
            <div slot="tip" class="upload-tip">只能上传jpg/png文件，且不超过2MB</div>
          </el-upload>
        </el-form-item>

        <el-form-item label="商品状态">
          <el-radio-group v-model="productForm.status">
            <el-radio label="active">在售</el-radio>
            <el-radio label="inactive">下架</el-radio>
            <el-radio label="out_of_stock">缺货</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showProductDialog = false">取消</el-button>
        <el-button type="primary" @click="saveProduct" :loading="saving">
          {{ isEditing ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules, UploadProps } from 'element-plus'
import { Plus, Refresh, Search, Picture } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const saving = ref(false)
const showProductDialog = ref(false)
const isEditing = ref(false)
const selectedProducts = ref<any[]>([])
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 表单引用
const productFormRef = ref<FormInstance>()

// 统计数据
const productStats = ref({
  total: 156,
  active: 134,
  lowStock: 12,
  revenue: 85420
})

// 商品表单数据
const productForm = ref({
  id: '',
  name: '',
  description: '',
  details: '',
  category: '',
  price: 0,
  stock: 0,
  image: '',
  status: 'active',
  sales: 0
})

// 表单验证规则
const productRules = ref<FormRules>({
  name: [
    { required: true, message: '请输入商品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '商品名称长度在2-50个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入商品描述', trigger: 'blur' },
    { max: 200, message: '商品描述不能超过200个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择商品分类', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入商品价格', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '商品价格必须大于0', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存数量', trigger: 'blur' },
    { type: 'number', min: 0, message: '库存数量不能小于0', trigger: 'blur' }
  ]
})

// 商品数据
const allProducts = ref([])

// 计算属性
const filteredProducts = computed(() => {
  let products = allProducts.value

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    products = products.filter(product =>
      product.name.toLowerCase().includes(query) ||
      product.description.toLowerCase().includes(query)
    )
  }

  // 分类过滤
  if (selectedCategory.value) {
    products = products.filter(product => product.category === selectedCategory.value)
  }

  // 状态过滤
  if (selectedStatus.value) {
    if (selectedStatus.value === 'low_stock') {
      products = products.filter(product => product.stock <= 10)
    } else {
      products = products.filter(product => product.status === selectedStatus.value)
    }
  }

  return products
})

const totalProducts = computed(() => filteredProducts.value.length)

// 方法
const createNewProduct = () => {
  isEditing.value = false
  showProductDialog.value = true
  resetProductForm()
}

const resetProductForm = () => {
  productForm.value = {
    id: '',
    name: '',
    description: '',
    details: '',
    category: '中药材', // 默认选择第一个分类
    price: 0,
    stock: 0,
    image: '',
    status: 'active',
    sales: 0
  }
  if (productFormRef.value) {
    productFormRef.value.clearValidate()
  }
}

const editProduct = (product: any) => {
  isEditing.value = true
  productForm.value = {
    id: product.id,
    name: product.name,
    description: product.description,
    details: product.usage_instructions || '',
    category: product.category,
    price: product.price,
    stock: product.stock_quantity || 0,
    image: (product.images && product.images.length > 0) ? product.images[0] : '',
    status: product.status,
    sales: product.sales_count || 0
  }
  showProductDialog.value = true
}

const saveProduct = async () => {
  if (!productFormRef.value) return

  try {
    await productFormRef.value.validate()
    saving.value = true

    const token = localStorage.getItem('admin_token')
    const apiUrl = isEditing.value 
      ? `/api/admin/products/${productForm.value.id}`
      : '/api/admin/products'
    
    const method = isEditing.value ? 'PUT' : 'POST'
    
    // 准备发送的数据，确保字段名称与后端匹配
    const productData = {
      name: productForm.value.name,
      description: productForm.value.description,
      category: productForm.value.category,
      price: productForm.value.price,
      stock_quantity: productForm.value.stock,
      images: productForm.value.image ? [productForm.value.image] : [],
      status: productForm.value.status,
      usage_instructions: productForm.value.details,
      is_featured: false,
      is_common: false
    }

    const response = await fetch(apiUrl, {
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(productData)
    })

    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status}`)
    }

    const savedProduct = await response.json()
    
    if (isEditing.value) {
      // 更新本地数据
      const index = allProducts.value.findIndex(p => p.id === productForm.value.id)
      if (index !== -1) {
        allProducts.value[index] = savedProduct
      }
      ElMessage.success('商品更新成功')
    } else {
      // 添加到本地数据
      allProducts.value.unshift(savedProduct)
      ElMessage.success('商品创建成功')
    }

    // 更新统计数据
    updateProductStats()
    
    showProductDialog.value = false
    resetProductForm()
  } catch (error) {
    console.error('保存商品失败:', error)
    ElMessage.error('保存失败，请检查网络连接和表单信息')
  } finally {
    saving.value = false
  }
}

const toggleProductStatus = async (product: any) => {
  const newStatus = product.status === 'active' ? 'inactive' : 'active'
  const action = newStatus === 'active' ? '上架' : '下架'
  
  try {
    await ElMessageBox.confirm(
      `确认${action}商品"${product.name}"吗？`,
      '状态变更确认',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const token = localStorage.getItem('admin_token')
    const response = await fetch(`/api/admin/products/${product.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: newStatus })
    })

    if (!response.ok) {
      throw new Error(`状态更新失败: ${response.status}`)
    }

    // 更新本地数据
    product.status = newStatus
    
    // 重新计算统计数据
    updateProductStats()
    
    ElMessage.success(`商品已${action}`)
  } catch (error) {
    if (error.message && error.message.includes('状态更新失败')) {
      ElMessage.error(`${action}失败，请检查网络连接`)
    }
    // 其他情况是用户取消操作，不显示错误
  }
}

const deleteProduct = async (product: any) => {
  try {
    await ElMessageBox.confirm(
      `确认删除商品"${product.name}"吗？此操作不可撤销。`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const token = localStorage.getItem('admin_token')
    const response = await fetch(`/api/admin/products/${product.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error(`删除商品失败: ${response.status}`)
    }

    // 从本地数据中移除
    const index = allProducts.value.findIndex(p => p.id === product.id)
    if (index !== -1) {
      allProducts.value.splice(index, 1)
    }
    
    // 更新统计数据
    updateProductStats()
    
    ElMessage.success('商品删除成功')
  } catch (error) {
    if (error.message && error.message.includes('删除商品失败')) {
      ElMessage.error('删除失败，请检查网络连接')
    }
    // 其他情况是用户取消操作，不显示错误
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedProducts.value = selection
}

const batchUpdateStatus = async (status: string) => {
  const action = status === 'active' ? '上架' : '下架'
  
  try {
    await ElMessageBox.confirm(
      `确认批量${action}选中的 ${selectedProducts.value.length} 个商品吗？`,
      `批量${action}确认`,
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const token = localStorage.getItem('admin_token')
    const updatePromises = selectedProducts.value.map(product => 
      fetch(`/api/admin/products/${product.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status })
      })
    )

    const results = await Promise.allSettled(updatePromises)
    
    // 检查是否有失败的请求
    const failedCount = results.filter(result => result.status === 'rejected').length
    const successCount = selectedProducts.value.length - failedCount

    if (failedCount > 0) {
      ElMessage.warning(`成功${action} ${successCount} 个商品，${failedCount} 个失败`)
    } else {
      ElMessage.success(`已批量${action} ${successCount} 个商品`)
    }

    // 更新本地数据
    selectedProducts.value.forEach((product, index) => {
      if (results[index].status === 'fulfilled') {
        product.status = status
      }
    })
    
    // 重新计算统计数据
    updateProductStats()
    
    selectedProducts.value = []
  } catch {
    // 用户取消操作
  }
}

const batchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确认删除选中的 ${selectedProducts.value.length} 个商品吗？此操作不可撤销。`,
      '批量删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const token = localStorage.getItem('admin_token')
    const deletePromises = selectedProducts.value.map(product => 
      fetch(`/api/admin/products/${product.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
    )

    const results = await Promise.allSettled(deletePromises)
    
    // 检查是否有失败的请求
    const failedCount = results.filter(result => result.status === 'rejected').length
    const successCount = selectedProducts.value.length - failedCount

    if (failedCount > 0) {
      ElMessage.warning(`成功删除 ${successCount} 个商品，${failedCount} 个失败`)
    } else {
      ElMessage.success(`已删除 ${successCount} 个商品`)
    }

    // 从本地数据中移除成功删除的商品
    selectedProducts.value.forEach((product, index) => {
      if (results[index].status === 'fulfilled') {
        const localIndex = allProducts.value.findIndex(p => p.id === product.id)
        if (localIndex !== -1) {
          allProducts.value.splice(localIndex, 1)
        }
      }
    })
    
    // 重新计算统计数据
    updateProductStats()
    
    selectedProducts.value = []
  } catch {
    // 用户取消操作
  }
}

const searchProducts = () => {
  // 搜索功能通过computed属性自动实现
}

const filterByCategory = () => {
  // 分类过滤通过computed属性自动实现
}

const filterByStatus = () => {
  // 状态过滤通过computed属性自动实现
}

const loadProducts = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('admin_token')
    const response = await fetch('/api/admin/products', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status}`)
    }
    
    const data = await response.json()
    allProducts.value = data || []
    
    // 更新统计数据
    updateProductStats()
    
    ElMessage.success('商品数据加载成功')
  } catch (error) {
    console.error('加载商品失败:', error)
    ElMessage.error('商品数据加载失败')
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

const updateProductStats = () => {
  const products = allProducts.value
  productStats.value = {
    total: products.length,
    active: products.filter(p => p.status === 'active').length,
    lowStock: products.filter(p => p.stock <= 10).length,
    revenue: products.reduce((sum, p) => sum + (p.price * (p.sales || 0)), 0)
  }
}

const getCategoryName = (category: string) => {
  // 直接返回分类名称，因为后端已经使用中文
  return category || '未分类'
}

const getCategoryTagType = (category: string) => {
  const typeMap: Record<string, string> = {
    '中药材': '',
    '养生产品': 'success', 
    '医疗器械': 'warning',
    '保健食品': 'info',
    '中医书籍': 'primary',
    '配套用品': 'success'
  }
  return typeMap[category] || ''
}

const beforeImageUpload: UploadProps['beforeUpload'] = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('上传图片只能是 JPG/PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('上传图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 生命周期
onMounted(() => {
  // 加载商品数据
  loadProducts()
})
</script>

<style scoped>
.product-management {
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
.stat-icon.active { background: #f6ffed; }
.stat-icon.stock { background: #fff0e6; }
.stat-icon.revenue { background: #f9f0ff; }

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

/* 搜索和筛选区域 */
.filter-section {
  margin-bottom: 24px;
}

.filter-content {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

/* 表格区域 */
.table-section {
  margin-bottom: 24px;
}

.product-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.product-desc {
  font-size: 12px;
  color: #999;
  line-height: 1.2;
}

.price {
  color: #f56c6c;
  font-weight: 500;
}

/* 批量操作 */
.batch-actions {
  margin-top: 16px;
  padding: 12px 0;
  border-top: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.batch-actions span {
  color: #666;
  font-size: 14px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* 图片上传 */
.image-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
  width: 178px;
  height: 178px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-uploader:hover {
  border-color: #409eff;
}

.image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.uploaded-image {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    align-self: flex-end;
  }

  .filter-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-content > * {
    width: 100%;
    max-width: 300px;
  }

  .batch-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>