<template>
  <div class="about">
    <PageContainer>
      <!-- 头部介绍 -->
      <div class="hero-section">
        <h1 class="main-title">传承中医智慧，赋能全民健康</h1>
        <p class="intro-text">
          传承千年智慧，赋能健康未来<br>
          中西医融合创新，让专业中医服务惠及全民
        </p>
      </div>

      <!-- 使命与愿景 -->
      <div class="section mission-vision-section">
        <el-row :gutter="40">
          <el-col :xs="24" :sm="12">
            <el-card class="info-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24" color="#67C23A"><Aim /></el-icon>
                  <span class="card-title">核心价值观</span>
                </div>
              </template>
              <div class="values-grid">
                <div class="value-item">
                  <el-tag type="success" effect="plain" size="large">关爱</el-tag>
                  <p>服务动力</p>
                </div>
                <div class="value-item">
                  <el-tag type="primary" effect="plain" size="large">专业</el-tag>
                  <p>发展根基</p>
                </div>
                <div class="value-item">
                  <el-tag type="warning" effect="plain" size="large">创新</el-tag>
                  <p>效率提升</p>
                </div>
                <div class="value-item">
                  <el-tag type="danger" effect="plain" size="large">共赢</el-tag>
                  <p>生态链接</p>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-card class="info-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <el-icon :size="24" color="#409EFF"><TrendCharts /></el-icon>
                  <span class="card-title">发展愿景</span>
                </div>
              </template>
              <ul class="vision-list">
                <li><el-icon color="#67C23A"><Check /></el-icon> 传承中医文化</li>
                <li><el-icon color="#67C23A"><Check /></el-icon> 推动中医食养一体化</li>
                <li><el-icon color="#67C23A"><Check /></el-icon> 构建全生命周期健康生态</li>
              </ul>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 核心优势 -->
      <div class="section advantages-section">
        <h2 class="section-title">核心优势</h2>
        <el-row :gutter="30">
          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="advantage-card" shadow="hover">
              <div class="advantage-icon">
                <el-icon :size="48" color="#409EFF"><Position /></el-icon>
              </div>
              <h3>差异化定位</h3>
              <p class="highlight-text">医养一体化方案 + 轻资产连锁模式</p>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="advantage-card" shadow="hover">
              <div class="advantage-icon">
                <el-icon :size="48" color="#67C23A"><Connection /></el-icon>
              </div>
              <h3>全链条服务</h3>
              <p class="highlight-text">评测 → 方案 → 产品 → 社区</p>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="advantage-card" shadow="hover">
              <div class="advantage-icon">
                <el-icon :size="48" color="#E6A23C"><User /></el-icon>
              </div>
              <h3>专业人才</h3>
              <p class="highlight-text">完善培训体系</p>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 业务链条 -->
      <div class="section business-chain-section">
        <h2 class="section-title">业务链条</h2>
        <p class="section-subtitle">评测 - 方案 - 产品 - 社区</p>

        <!-- 2x2 方框布局 -->
        <div class="business-grid">
          <!-- 第一行 -->
          <el-row :gutter="30">
            <el-col :xs="24" :md="12">
              <el-card shadow="hover" class="business-box business-box-1">
                <div class="business-number">01</div>
                <div class="business-header">
                  <el-icon :size="50" color="#409EFF"><DataAnalysis /></el-icon>
                  <h3>智能评测</h3>
                </div>
                <ul class="business-list">
                  <li><el-icon><Check /></el-icon> AI智能问诊</li>
                  <li><el-icon><Check /></el-icon> 体质量表测评</li>
                  <li><el-icon><Check /></el-icon> 健康档案管理</li>
                  <li><el-icon><Check /></el-icon> 数据分析</li>
                </ul>
                <el-tag type="primary" effect="dark" class="business-tag">5分钟完成评测</el-tag>
              </el-card>
            </el-col>

            <el-col :xs="24" :md="12">
              <el-card shadow="hover" class="business-box business-box-2">
                <div class="business-number">02</div>
                <div class="business-header">
                  <el-icon :size="50" color="#67C23A"><Document /></el-icon>
                  <h3>定制方案</h3>
                </div>
                <ul class="business-list">
                  <li><el-icon><Check /></el-icon> 个性化调理方案</li>
                  <li><el-icon><Check /></el-icon> 专家一对一指导</li>
                  <li><el-icon><Check /></el-icon> 智能食谱配送</li>
                  <li><el-icon><Check /></el-icon> 周期健康管理</li>
                </ul>
                <el-tag type="success" effect="dark" class="business-tag">精准调理</el-tag>
              </el-card>
            </el-col>
          </el-row>

          <!-- 中间箭头指示 -->
          <div class="flow-arrows">
            <el-icon :size="40" color="#909399"><Bottom /></el-icon>
          </div>

          <!-- 第二行 -->
          <el-row :gutter="30">
            <el-col :xs="24" :md="12">
              <el-card shadow="hover" class="business-box business-box-3">
                <div class="business-number">03</div>
                <div class="business-header">
                  <el-icon :size="50" color="#E6A23C"><ShoppingCart /></el-icon>
                  <h3>优质产品</h3>
                </div>
                <ul class="business-list">
                  <li><el-icon><Check /></el-icon> 中药材品质保障</li>
                  <li><el-icon><Check /></el-icon> 理疗服务支持</li>
                  <li><el-icon><Check /></el-icon> 健康产品供应</li>
                  <li><el-icon><Check /></el-icon> 食疗配送到家</li>
                </ul>
                <el-tag type="warning" effect="dark" class="business-tag">全渠道供应</el-tag>
              </el-card>
            </el-col>

            <el-col :xs="24" :md="12">
              <el-card shadow="hover" class="business-box business-box-4">
                <div class="business-number">04</div>
                <div class="business-header">
                  <el-icon :size="50" color="#F56C6C"><ChatDotRound /></el-icon>
                  <h3>健康社区</h3>
                </div>
                <ul class="business-list">
                  <li><el-icon><Check /></el-icon> 知识分享交流</li>
                  <li><el-icon><Check /></el-icon> 养生课程学习</li>
                  <li><el-icon><Check /></el-icon> 用户互助分享</li>
                  <li><el-icon><Check /></el-icon> 专家健康讲座</li>
                  <li><el-icon><Check /></el-icon> 理疗服务预约</li>
                </ul>
                <el-divider content-position="left">
                  <span style="color: #909399; font-size: 14px;">线下节点</span>
                </el-divider>
                <div class="offline-nodes">
                  <div class="node-item">
                    <el-icon color="#F56C6C"><Location /></el-icon>
                    <span>养生驿站</span>
                  </div>
                  <div class="node-item">
                    <el-icon color="#F56C6C"><Location /></el-icon>
                    <span>旗舰中心</span>
                  </div>
                </div>
                <el-tag type="danger" effect="dark" class="business-tag">长效管理</el-tag>
              </el-card>
            </el-col>
          </el-row>
        </div>

      </div>

      <!-- 发展历程 -->
      <div class="section history-section">
        <h2 class="section-title">发展历程</h2>
        <el-row :gutter="30">
          <el-col :xs="24" :md="8">
            <el-card shadow="hover" class="history-card history-card-1">
              <div class="history-year">2019-2021</div>
              <div class="history-icon">
                <el-icon :size="50" color="#409EFF"><User /></el-icon>
              </div>
              <h3>人才培养</h3>
              <p>搭建专业人才梯队，输送优质中医力量</p>
              <el-divider />
              <div class="stats">
                <div class="stat-item">
                  <span class="stat-number">20+</span>
                  <span class="stat-label">培训班</span>
                </div>
                <div class="stat-item">
                  <span class="stat-number">2000+</span>
                  <span class="stat-label">人才</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="24" :md="8">
            <el-card shadow="hover" class="history-card history-card-2">
              <div class="history-year">2021-2023</div>
              <div class="history-icon">
                <el-icon :size="50" color="#67C23A"><Document /></el-icon>
              </div>
              <h3>专科深耕</h3>
              <p>打造特色专科，形成全周期调理方案</p>
              <el-divider content-position="center">
                <span style="color: #909399; font-size: 14px;">专病专科</span>
              </el-divider>
              <div class="specialty-tags">
                <el-tag type="primary" effect="plain">亚健康</el-tag>
                <el-tag type="success" effect="plain">失眠</el-tag>
                <el-tag type="warning" effect="plain">三高</el-tag>
                <el-tag type="danger" effect="plain">脾胃</el-tag>
                <el-tag type="info" effect="plain">妇科</el-tag>
                <el-tag effect="plain">抗衰</el-tag>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="24" :md="8">
            <el-card shadow="hover" class="history-card history-card-3">
              <div class="history-year">2024至今</div>
              <div class="history-icon">
                <el-icon :size="50" color="#E6A23C"><Connection /></el-icon>
              </div>
              <h3>生态共建</h3>
              <p>构建健康生态，拓展服务边界</p>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 联系我们 -->
      <div class="section contact-section">
        <el-card class="contact-card" shadow="hover">
          <h2>携手共创健康未来</h2>
          <p class="contact-desc">欢迎了解我们的服务或洽谈合作</p>
          <el-button type="primary" size="large" @click="handleContact">
            <el-icon><Message /></el-icon>
            <span>联系我们</span>
          </el-button>
        </el-card>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import {
  Aim,
  TrendCharts,
  Check,
  Position,
  Connection,
  User,
  Monitor,
  Location,
  Document,
  Message,
  DataAnalysis,
  ShoppingCart,
  ChatDotRound,
  Refresh,
  Bottom
} from '@element-plus/icons-vue'
import PageContainer from '../components/PageContainer.vue'

const handleContact = () => {
  ElMessage.info('联系功能开发中，敬请期待')
}
</script>

<style scoped>
.about {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f5f7fa 0%, #ffffff 100%);
}

/* 头部区域 */
.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  margin-bottom: 40px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.main-title {
  font-size: 42px;
  font-weight: bold;
  margin-bottom: 24px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.intro-text {
  font-size: 16px;
  line-height: 1.8;
  opacity: 0.9;
  max-width: 800px;
  margin: 0 auto;
}

/* 通用区块样式 */
.section {
  margin-bottom: 50px;
}

.section-title {
  text-align: center;
  font-size: 32px;
  color: #303133;
  margin-bottom: 40px;
  position: relative;
  padding-bottom: 15px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(to right, #409EFF, #67C23A);
  border-radius: 2px;
}

/* 使命愿景区域 */
.mission-vision-section {
  margin-top: 40px;
}

.info-card {
  height: 100%;
  transition: all 0.3s;
  border: 2px solid #EBEEF5;
}

.info-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  border-color: #67C23A;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.card-title {
  font-size: 20px;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.value-item {
  text-align: center;
}

.value-item p {
  margin-top: 10px;
  color: #606266;
  font-size: 14px;
}

.vision-list {
  list-style: none;
  padding: 0;
}

.vision-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  font-size: 16px;
  color: #606266;
  border-bottom: 1px solid #EBEEF5;
}

.vision-list li:last-child {
  border-bottom: none;
}

/* 核心优势区域 */
.advantage-card {
  height: 100%;
  min-height: 200px;
  text-align: center;
  transition: all 0.3s;
  border: 2px solid #EBEEF5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 30px 20px;
}

.advantage-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  border-color: #409EFF;
}

.advantage-icon {
  margin-bottom: 20px;
}

.advantage-card h3 {
  font-size: 22px;
  color: #303133;
  margin-bottom: 15px;
}

.advantage-card p {
  color: #606266;
  line-height: 1.8;
  margin-bottom: 10px;
}

.highlight-text {
  color: #409EFF;
  font-weight: bold;
  font-size: 15px;
}

.service-list {
  list-style: none;
  padding: 0;
  text-align: left;
}

.service-list li {
  padding: 8px 0;
  color: #606266;
  border-bottom: 1px dashed #EBEEF5;
}

.service-list li:last-child {
  border-bottom: none;
}

.stats {
  display: flex;
  justify-content: space-around;
  margin-top: 15px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #E6A23C;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

/* 业务链条区域 */
.business-chain-section {
  max-width: 1200px;
  margin: 0 auto 50px;
}

.section-subtitle {
  text-align: center;
  font-size: 18px;
  color: #909399;
  margin-top: -30px;
  margin-bottom: 40px;
}

.business-grid {
  margin-top: 40px;
}

.business-box {
  height: 100%;
  min-height: 450px;
  position: relative;
  transition: all 0.3s;
  border: 3px solid transparent;
}

.business-box:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.business-box-1 {
  border-color: #409EFF;
}

.business-box-1:hover {
  border-color: #66B1FF;
  background: linear-gradient(to bottom, #ECF5FF 0%, #ffffff 20%);
}

.business-box-2 {
  border-color: #67C23A;
}

.business-box-2:hover {
  border-color: #85CE61;
  background: linear-gradient(to bottom, #F0F9FF 0%, #ffffff 20%);
}

.business-box-3 {
  border-color: #E6A23C;
}

.business-box-3:hover {
  border-color: #EEBC6C;
  background: linear-gradient(to bottom, #FDF6EC 0%, #ffffff 20%);
}

.business-box-4 {
  border-color: #F56C6C;
}

.business-box-4:hover {
  border-color: #F78989;
  background: linear-gradient(to bottom, #FEF0F0 0%, #ffffff 20%);
}

.business-number {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.business-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  padding: 20px 0;
  border-bottom: 2px solid #EBEEF5;
}

.business-header h3 {
  font-size: 26px;
  color: #303133;
  margin: 0;
  font-weight: bold;
}

.flow-arrows {
  text-align: center;
  margin: 30px 0;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(10px);
  }
}

.business-list {
  list-style: none;
  padding: 0;
  margin: 20px 0;
}

.business-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  color: #606266;
  font-size: 15px;
  border-bottom: 1px dashed #EBEEF5;
}

.business-list li:last-child {
  border-bottom: none;
}

.business-tag {
  width: 100%;
  text-align: center;
  padding: 10px;
  font-size: 15px;
  font-weight: bold;
}

.specialty-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 15px 0 20px;
  justify-content: center;
}

.specialty-tags .el-tag {
  font-size: 14px;
  padding: 8px 16px;
}

.offline-nodes {
  display: flex;
  gap: 20px;
  margin: 15px 0 20px;
  justify-content: space-around;
}

.node-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #FEF0F0;
  border-radius: 20px;
  color: #606266;
  font-size: 14px;
  transition: all 0.3s;
}

.node-item:hover {
  background: #FDE2E2;
  transform: scale(1.05);
}

/* 发展历程卡片 */
.history-section {
  margin-bottom: 50px;
}

.history-card {
  height: 100%;
  min-height: 360px;
  text-align: center;
  position: relative;
  transition: all 0.3s;
  border: 3px solid transparent;
  padding: 30px 20px;
}

.history-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.history-card-1 {
  border-color: #409EFF;
}

.history-card-1:hover {
  border-color: #66B1FF;
  background: linear-gradient(to bottom, #ECF5FF 0%, #ffffff 30%);
}

.history-card-2 {
  border-color: #67C23A;
}

.history-card-2:hover {
  border-color: #85CE61;
  background: linear-gradient(to bottom, #F0F9FF 0%, #ffffff 30%);
}

.history-card-3 {
  border-color: #E6A23C;
}

.history-card-3:hover {
  border-color: #EEBC6C;
  background: linear-gradient(to bottom, #FDF6EC 0%, #ffffff 30%);
}

.history-year {
  position: absolute;
  top: 15px;
  right: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.history-icon {
  margin-bottom: 20px;
}

.history-card h3 {
  font-size: 22px;
  color: #303133;
  margin-bottom: 15px;
  font-weight: bold;
}

.history-card p {
  color: #606266;
  line-height: 1.8;
  font-size: 15px;
}

/* 联系我们区域 */
.contact-section {
  max-width: 800px;
  margin: 0 auto;
}

.contact-card {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.contact-card h2 {
  font-size: 32px;
  margin-bottom: 20px;
  color: white;
}

.contact-desc {
  font-size: 16px;
  margin-bottom: 30px;
  opacity: 0.9;
}

.contact-card :deep(.el-button) {
  font-size: 18px;
  padding: 15px 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-title {
    font-size: 28px;
  }

  .intro-text {
    font-size: 14px;
  }

  .section-title {
    font-size: 24px;
  }

  .values-grid {
    grid-template-columns: 1fr;
  }

  .hero-section {
    padding: 40px 15px;
  }

  .contact-card h2 {
    font-size: 24px;
  }

  .business-box {
    min-height: auto;
    margin-bottom: 20px;
  }

  .business-header h3 {
    font-size: 22px;
  }

  .business-number {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .flow-arrows {
    margin: 20px 0;
  }

  .offline-nodes {
    flex-direction: column;
    gap: 10px;
  }

  .specialty-tags {
    gap: 8px;
  }

  .specialty-tags .el-tag {
    font-size: 12px;
    padding: 6px 12px;
  }

  .history-card {
    min-height: auto;
    margin-bottom: 20px;
  }

  .history-card h3 {
    font-size: 20px;
  }

  .history-year {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>