<template>
  <div class="three-layer-system-page">
    <!-- 返回按钮 -->
    <div class="back-button-section">
      <el-button @click="goBack" icon="ArrowLeft">返回课程介绍</el-button>
    </div>

    <!-- 页面标题 -->
    <div class="page-header">
      <h1>📚 三层递进学习体系</h1>
      <p class="subtitle">用培训医生的专业体系，让普通人掌握健康管理技能</p>
    </div>

    <!-- 3层递进结构详细展示 -->
    <div class="three-layer-system-wrapper">
      <div class="three-layer-system">
        <div class="layer-progression">
          <div class="layer">
            <div class="layer-header">
              <div class="layer-number">1</div>
              <div class="layer-title">健康常识层</div>
              <div class="layer-subtitle">先搞懂什么是健康</div>
            </div>
            <div class="layer-content">
              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">健康本质理解</div>
                <div class="skill-desc">从"有病找医生"到"健康触手可及"的认知转变</div>
                <div class="skill-detail">
                  <strong>具体内容：</strong><br>
                  • 健康不等于没有症状，而是身心平衡状态<br>
                  • 疾病是身体的预警信号，需要倾听和理解<br>
                  • 预防重于治疗，投资健康认知比治病更划算<br>
                  • 每个人都是自己健康的第一责任人
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">身体运行规律</div>
                <div class="skill-desc">用大白话讲清楚身体怎么工作</div>
                <div class="skill-detail">
                  <strong>身体就像一家公司：</strong><br>
                  • 内脏器官 = 各个部门，各司其职<br>
                  • 血液循环 = 物流系统，运送营养和垃圾<br>
                  • 身体通道 = 信息网络，传递指令和反馈<br>
                  • 身心平衡 = 公司运营稳定，不出乱子
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">身体在"说话"</div>
                <div class="skill-desc">身体不舒服时会给你信号，学会听懂</div>
                <div class="skill-detail">
                  <strong>身体的求救信号：</strong><br>
                  • 脸色不好：说明身体内部有问题<br>
                  • 舌头变化：显示身体是上火还是受寒<br>
                  • 心情不好：会影响身体各器官工作<br>
                  • 睡不好觉：是身心健康的晴雨表
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">预防思维建立</div>
                <div class="skill-desc">从被动治疗转向主动预防</div>
                <div class="skill-detail">
                  <strong>思维转换：</strong><br>
                  • 未病先防：健康时就开始养生<br>
                  • 既病防变：有症状时防止加重<br>
                  • 瘥后防复：康复后防止复发<br>
                  • 因时制宜：根据季节调整方案<br>
                  • 投资思维：把健康当作最重要的资产管理
                </div>
              </div>
            </div>
          </div>

          <div class="layer">
            <div class="layer-header">
              <div class="layer-number">2</div>
              <div class="layer-title">实用工具层</div>
              <div class="layer-subtitle">掌握具体操作方法</div>
            </div>
            <div class="layer-content">
              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">常见病症解析</div>
                <div class="skill-desc">把常见问题掰开了揉碎了讲明白</div>
                <div class="skill-detail">
                  <strong>精讲病症：</strong><br>
                  • 消化系统：胃痛、腹泻、便秘<br>
                  • 呼吸系统：咳嗽、哮喘、感冒<br>
                  • 心血管系统：高血压、心悸<br>
                  • 妇科疾病：月经不调、更年期
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">身体类型判断</div>
                <div class="skill-desc">同样的病，不同的人，调理方法完全不同</div>
                <div class="skill-detail">
                  <strong>疾病体质分型：</strong><br>
                  • 胃病：寒胃型、热胃型、虚胃型、郁胃型<br>
                  • 失眠：心火型、肝郁型、脾虚型、肾虚型<br>
                  • 咳嗽：风寒型、风热型、痰湿型、肺虚型<br>
                  • 月经不调：气滞型、血瘀型、气血虚型、肾虚型<br>
                  • 高血压：肝阳型、痰湿型、肾虚型、血瘀型<br>
                  • 等等...
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">食疗配方库</div>
                <div class="skill-desc">把厨房变成你的私人药房</div>
                <div class="skill-detail">
                  <strong>精准食疗方案：</strong><br>
                  • 胃痛喝错汤只会越来越痛，教你分清寒热虚实<br>
                  • 失眠别再喝牛奶了，根据不同原因选对食材<br>
                  • 咳嗽分风寒风热，梨和姜可不能乱用<br>
                  • 大姨妈不调？红糖水不是万能的<br>
                  • 降压药膳，比单纯忌口更有效<br>
                  • 300+实用食疗方，每道都有具体制作方法
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">运动养生方案</div>
                <div class="skill-desc">不同身体状况，运动方式差别很大</div>
                <div class="skill-detail">
                  <strong>个性化运动指导：</strong><br>
                  • 气虚体质：太极拳、八段锦等柔和运动<br>
                  • 阳虚体质：慢跑、游泳等有氧运动<br>
                  • 痰湿体质：快走、爬山等强度运动<br>
                  • 血瘀体质：舞蹈、球类等活动性运动<br>
                  • 疾病康复期的运动禁忌和注意事项<br>
                  • 不同年龄段的运动强度调整
                </div>
              </div>
            </div>
          </div>

          <div class="layer">
            <div class="layer-header">
              <div class="layer-number">3</div>
              <div class="layer-title">实践应用层</div>
              <div class="layer-subtitle">形成可持续健康习惯</div>
            </div>
            <div class="layer-content">
              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">健康记录本</div>
                <div class="skill-desc">记录自己身体变化，越来越了解自己</div>
                <div class="skill-detail">
                  <strong>档案内容：</strong><br>
                  • 基础信息：年龄、性别、职业、家族史<br>
                  • 体质评估：九大体质测试结果<br>
                  • 症状记录：不适症状及变化趋势<br>
                  • 调理方案：个性化养生方案记录
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">家庭健康管理</div>
                <div class="skill-desc">一人学习全家受益</div>
                <div class="skill-detail">
                  <strong>管理体系：</strong><br>
                  • 家庭成员体质档案建立<br>
                  • 不同年龄段养生重点<br>
                  • 常见疾病家庭应对方案<br>
                  • 家庭药材储备清单
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">什么时候该看医生</div>
                <div class="skill-desc">自己能解决和必须找医生，界限要分清</div>
                <div class="skill-detail">
                  <strong>决策标准：</strong><br>
                  • 绿灯：可自我调理的症状<br>
                  • 黄灯：需要观察的症状<br>
                  • 红灯：必须就医的症状<br>
                  • 急诊指征：危及生命的症状
                </div>
              </div>

              <div class="skill-item" @click="toggleDetail($event)">
                <div class="skill-title">慢性病不可怕</div>
                <div class="skill-desc">学会和慢性病和平共处，生活质量一样高</div>
                <div class="skill-detail">
                  <strong>慢病管理策略：</strong><br>
                  • 高血压：不只是吃药，生活方式更重要<br>
                  • 糖尿病：血糖控制的中医智慧<br>
                  • 失眠症：找到根源，告别安眠药依赖<br>
                  • 慢性胃炎：养胃护胃的正确打开方式<br>
                  • 建立个人慢病管理档案和追踪系统
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

// 返回上一页
const goBack = () => {
  router.push('/courses')
}

// 切换详情显示
const toggleDetail = (event: Event) => {
  const element = event.currentTarget as HTMLElement
  const detail = element.querySelector('.skill-detail') as HTMLElement
  if (detail.style.display === 'none' || !detail.style.display) {
    detail.style.display = 'block'
    element.style.backgroundColor = '#fff'
  } else {
    detail.style.display = 'none'
    element.style.backgroundColor = ''
  }
}
</script>

<style scoped>
.three-layer-system-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 60px;
}

/* 返回按钮 */
.back-button-section {
  padding: 20px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 页面标题 */
.page-header {
  text-align: center;
  padding: 60px 20px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  font-weight: 700;
}

.page-header .subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

/* 3层递进结构外层容器 */
.three-layer-system-wrapper {
  padding: 60px 20px;
  background-color: #f5f5f5;
}

/* 3层递进结构样式 - 卡片式框架 */
.three-layer-system {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.layer-progression {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0;
  gap: 30px;
}

.layer {
  flex: 1;
  max-width: 420px;
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  border: 2px solid transparent;
}

.layer:hover {
  transform: translateY(-12px);
  box-shadow: 0 25px 50px rgba(255, 107, 53, 0.15);
  border-color: #FF6B35;
}

.layer-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 3px solid #f0f0f0;
}

.layer-number {
  background: linear-gradient(135deg, #FF6B35, #F9D949);
  color: white;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5em;
  font-weight: bold;
  margin: 0 auto 20px;
  box-shadow: 0 10px 25px rgba(255, 107, 53, 0.3);
}

.layer-title {
  font-size: 1.8em;
  color: #333;
  font-weight: bold;
  margin-bottom: 10px;
}

.layer-subtitle {
  color: #666;
  font-size: 1.1em;
}

.layer-content {
  background: transparent;
  border-radius: 0;
  padding: 0;
  min-height: auto;
}

.skill-item {
  background: #f8f9fa;
  margin-bottom: 15px;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #FF6B35;
  transition: all 0.3s ease;
  cursor: pointer;
}

.skill-item:hover {
  transform: translateX(10px);
  background: #fff;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.skill-item:last-child {
  margin-bottom: 0;
}

.skill-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-size: 1.05em;
}

.skill-desc {
  color: #666;
  font-size: 0.9em;
}

.skill-detail {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
  display: none;
  color: #555;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .layer-progression {
    flex-direction: column;
    align-items: center;
  }

  .layer {
    max-width: 600px;
    margin-bottom: 40px;
  }
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }

  .page-header .subtitle {
    font-size: 1rem;
  }

  .three-layer-system-wrapper {
    padding: 40px 20px;
  }

  .three-layer-system {
    padding: 40px 20px;
  }

  .layer {
    max-width: 100%;
    padding: 25px 20px;
    margin-bottom: 25px;
  }

  .layer:last-child {
    margin-bottom: 0;
  }

  .layer-number {
    width: 80px;
    height: 80px;
    font-size: 2em;
  }

  .layer-title {
    font-size: 1.5em;
  }

  .layer-subtitle {
    font-size: 1em;
  }

  .skill-item {
    padding: 15px;
  }
}
</style>
