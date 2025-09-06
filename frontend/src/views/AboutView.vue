<template>
  <div class="about">
    <PageContainer>
      
      <div class="about-content">
        <h2>关于我们</h2>
        <p>中医健康服务平台致力于传承和发扬中医文化，为用户提供专业的中医健康服务。</p>
        
        <el-divider></el-divider>
        
        <div class="mission-section">
          <h3>我们的使命</h3>
          <p>让每一位用户都能享受到专业、便捷、科学的中医健康服务，提升全民健康素养。</p>
        </div>
        
        <div class="vision-section">
          <h3>我们的愿景</h3>
          <p>成为国内领先的中医健康服务平台，推动中医文化的现代化传播。</p>
        </div>
        
        <div class="values-section">
          <h3>核心价值观</h3>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card class="value-card">
                <h4>专业</h4>
                <p>汇聚资深中医专家，提供权威健康指导</p>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="value-card">
                <h4>科学</h4>
                <p>结合现代医学，提供科学的健康方案</p>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="value-card">
                <h4>诚信</h4>
                <p>以用户健康为本，提供真诚服务</p>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import PageContainer from '../components/PageContainer.vue'
// 关于页面组件
</script>

<style scoped>
.about {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.about-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.about-content h2 {
  color: #333;
  text-align: center;
  margin-bottom: 30px;
}

.mission-section, .vision-section {
  margin-bottom: 30px;
}

.mission-section h3, .vision-section h3, .values-section h3 {
  color: #409eff;
  margin-bottom: 15px;
}

.value-card {
  text-align: center;
}

.value-card h4 {
  color: #409eff;
  margin-bottom: 10px;
}
</style>