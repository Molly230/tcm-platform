<template>
  <div class="misconceptions-view">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">⚠️ 健康养生避坑指南</h1>
        <p class="page-subtitle">停止这些错误的养生方式，健康从正确认知开始</p>
      </div>
    </div>

    <!-- 搜索栏 -->
    <div class="search-section">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索避坑内容（如：喝水、运动、睡眠）"
        prefix-icon="Search"
        size="large"
        clearable
        @input="handleSearch"
      />
    </div>

    <!-- 内容区域 -->
    <div class="content-wrapper">
      <!-- 核心提示 -->
      <el-alert
        title="避坑核心思维"
        type="warning"
        :closable="false"
        show-icon
      >
        <template #default>
          <div class="core-tips">
            <p><strong>❌ 不盲目跟风：</strong>别人用着好的养生方法，不一定适合你（体质不同、基础病不同）</p>
            <p><strong>❌ 不过度追求"效果"：</strong>养生是长期事，急功近利易陷入"过量、极端"误区</p>
            <p><strong>✅ 关注"身体信号"：</strong>运动后关节疼、吃某食物后腹胀，说明方法错了，及时调整</p>
            <p><strong>✅ 优先"基础习惯"：</strong>好好吃饭、好好睡觉、适度运动，比任何"网红养生法"都管用</p>
          </div>
        </template>
      </el-alert>

      <!-- 书签式Tab导航 -->
      <div class="bookmark-tabs">
        <div
          v-for="category in filteredCategories"
          :key="category.id"
          class="bookmark-tab"
          :class="{ active: activeTab === category.id }"
          @click="activeTab = category.id"
        >
          <span class="tab-icon">{{ category.icon }}</span>
          <span class="tab-name">{{ category.name }}</span>
          <span class="tab-count">{{ category.items.length }}</span>
        </div>
      </div>

      <!-- 当前分类内容 -->
      <div v-if="currentCategory" class="tab-content">
        <div class="misconceptions-list">
          <div
            v-for="(item, index) in currentCategory.items"
            :key="index"
            class="misconception-item"
          >
            <div class="item-header">
              <span class="item-number">{{ index + 1 }}</span>
              <h3 class="item-title" v-html="highlightKeyword(item.title)"></h3>
            </div>
            <p class="item-description" v-html="highlightKeyword(item.description)"></p>
          </div>
        </div>
      </div>

      <!-- 搜索无结果提示 -->
      <el-empty
        v-if="filteredCategories.length === 0"
        description="没有找到相关内容，换个关键词试试？"
        :image-size="200"
      />
    </div>

    <!-- 返回首页按钮 -->
    <div class="back-home">
      <el-button type="primary" size="large" @click="$router.push('/')">
        返回首页
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// 搜索关键词
const searchKeyword = ref('')

// 当前激活的Tab（默认第一个）
const activeTab = ref('diet')

// 避坑指南数据
const categories = [
  {
    id: 'diet',
    name: '饮食养生类',
    icon: '🍽️',
    items: [
      {
        title: '只吃粗粮不吃精米白面',
        description: '粗粮纤维多，但过量会加重肠胃负担，尤其老人、胃病患者易腹胀、消化不良。'
      },
      {
        title: '完全不吃油',
        description: '脂肪是人体必需营养素，长期无油会导致激素失衡、皮肤变差，还可能影响脂溶性维生素（A/D/E/K）吸收。'
      },
      {
        title: '每天喝超过 2000ml 水',
        description: '过量饮水会稀释血液，增加肾脏代谢压力，甚至引发"水中毒"（头晕、乏力、电解质紊乱）。'
      },
      {
        title: '早餐只喝豆浆/牛奶 + 鸡蛋',
        description: '缺主食会导致上午血糖不稳、精力不足，应搭配全麦面包、杂粮粥等碳水。'
      },
      {
        title: '长期吃"零添加"手工咸菜',
        description: '即使无防腐剂，咸菜含盐量极高，长期吃会升高血压，增加肾病风险。'
      },
      {
        title: '为"排毒"每天喝果蔬汁',
        description: '果蔬汁过滤掉纤维，糖分吸收快易升血糖，且过量会导致果糖摄入超标。'
      },
      {
        title: '发烧时强制喝大量热水',
        description: '体温升高时，过量热水会让身体散热困难，反而加重不适。应少量多次温水，配合物理降温。'
      },
      {
        title: '长期用"代餐粉"替代正餐',
        description: '代餐营养不均衡，缺蛋白质、膳食纤维，长期吃会导致代谢下降、免疫力变弱。'
      },
      {
        title: '煮菜时放大量"养生药材"（如每顿都加当归、枸杞）',
        description: '药材有药性，比如当归活血，长期吃可能导致上火、月经紊乱（女性）。'
      },
      {
        title: '隔夜菜加热后继续吃（超过48小时）',
        description: '即使冷藏，隔夜菜会产生亚硝酸盐，增加致癌风险，建议每餐做刚好的量，剩菜超24小时就扔。'
      }
    ]
  },
  {
    id: 'exercise',
    name: '运动养生类',
    icon: '🏃',
    items: [
      {
        title: '每天暴走 2 万步以上',
        description: '过量步行会磨损膝关节，尤其老人易引发滑膜炎、软骨损伤，每天 6000-8000 步更合适。'
      },
      {
        title: '早上空腹剧烈运动（如快跑、高强度间歇训练）',
        description: '空腹运动易导致低血糖，出现头晕、心慌，甚至引发肌肉分解。'
      },
      {
        title: '关节疼还坚持"爬楼梯养生"',
        description: '爬楼梯对膝关节压力大，关节不好者会加重磨损，应选游泳、散步等温和运动。'
      },
      {
        title: '为"出汗排毒"穿厚重衣服运动',
        description: '大量出汗会导致脱水、电解质紊乱，且"出汗≠排毒"，身体毒素主要靠肾脏代谢。'
      },
      {
        title: '久坐后突然剧烈运动',
        description: '肌肉处于僵硬状态，突然跑跳易拉伤韧带、肌肉撕裂，应先热身10-15分钟。'
      },
      {
        title: '运动后立刻洗冷水澡',
        description: '剧烈运动后血管扩张，冷水刺激会导致血管急剧收缩，易引发心脏问题（尤其老人）。'
      },
      {
        title: '每天只做"拉伸"不做力量训练',
        description: '肌肉量减少会导致基础代谢下降、骨质疏松风险增加，应搭配深蹲、俯卧撑等力量练习。'
      },
      {
        title: '"痛就是在长功"（运动时忍痛继续）',
        description: '疼痛是身体警告信号，继续运动会造成永久损伤（如半月板撕裂），应立即停止并就医。'
      },
      {
        title: '为减肥每天只吃一餐 + 高强度运动',
        description: '极端节食 + 运动会导致低血糖、内分泌紊乱、暴食反弹，减肥应循序渐进。'
      },
      {
        title: '老人练"撞树"养生',
        description: '撞击会损伤内脏、脊柱，老人骨质疏松更易骨折，应选太极、八段锦等柔和运动。'
      }
    ]
  },
  {
    id: 'sleep',
    name: '睡眠养生类',
    icon: '😴',
    items: [
      {
        title: '睡前喝红酒助眠',
        description: '红酒中的酒精会抑制深度睡眠，导致半夜易醒、晨起头痛，长期喝还伤肝。'
      },
      {
        title: '靠"褪黑素"长期助眠',
        description: '长期吃会产生依赖，且掩盖真正失眠原因（如焦虑、呼吸暂停），还可能导致头晕、恶心。'
      },
      {
        title: '睡前长时间听"助眠白噪音"（音量大）',
        description: '噪音会刺激听觉神经，反而让大脑处于浅睡眠状态，应选轻柔、低音量白噪音。'
      },
      {
        title: '"趴着睡"能缓解腰酸',
        description: '趴着睡会压迫颈椎、腰椎，导致脊柱变形，还会压迫胸腔影响呼吸，腰酸应选侧睡 + 腰垫。'
      },
      {
        title: '凌晨 2 点睡、中午 12 点起"保证 8 小时就行"',
        description: '违背"日出而作、日落而息"的生物钟，长期会导致内分泌紊乱（如长痘、月经不调）。'
      },
      {
        title: '睡前做"高强度脑力活动"（如刷题、玩游戏）',
        description: '大脑处于兴奋状态，会延长入睡时间，睡前 1 小时应做温和活动（如看书、泡脚）。'
      },
      {
        title: '老人为"少起夜"睡前完全不喝水',
        description: '夜间缺水会导致血液黏稠、增加血栓风险，应睡前1小时喝50-100ml温水。'
      },
      {
        title: '周末"补觉"睡到下午',
        description: '打乱生物钟，导致下周一更难起床（"社交时差"），应保持规律作息，周末最多晚起1小时。'
      },
      {
        title: '睡前泡脚超过 30 分钟',
        description: '长时间泡脚会导致血液集中在下肢，大脑缺氧反而难入睡，泡脚应控制在15-20分钟。'
      },
      {
        title: '床上放手机、平板"方便看时间"',
        description: '蓝光会抑制褪黑素分泌，且易忍不住刷手机，应将电子设备放在床边柜子里。'
      }
    ]
  },
  {
    id: 'supplement',
    name: '保健品/偏方类',
    icon: '💊',
    items: [
      {
        title: '长期吃"阿胶糕"补血',
        description: '阿胶本质是驴皮胶原蛋白，补铁效果远不如猪肝、红肉，且高糖高热量易发胖。'
      },
      {
        title: '天天吃"维生素 C 泡腾片"预防感冒',
        description: '过量VC（超过1000mg/天）会增加肾结石风险，且无法预防感冒，应优先食物补充。'
      },
      {
        title: '老人吃"三七粉"活血化瘀（自行购买）',
        description: '三七有抗凝作用，长期吃可能导致凝血功能异常，尤其正在吃降压药、降糖药的老人，易引发出血。'
      },
      {
        title: '跟风买"网红养生茶"（如蒲公英茶、决明子茶）天天喝',
        description: '蒲公英性寒，长期喝易伤脾胃；决明子通便，但长期喝会导致肠道依赖，还伤肝。'
      },
      {
        title: '用"拔罐"天天祛湿，罐印没消就再拔',
        description: '频繁拔罐会导致皮肤破损、毛细血管破裂，还可能加重气血亏虚（如罐印长期发紫不消）。'
      },
      {
        title: '小孩吃"成人保健品"（如鱼油、蛋白粉）',
        description: '小孩营养主要靠饮食，过量补保健品会导致性早熟（含激素）、肝肾负担。'
      },
      {
        title: '长期用"漱口水"代替刷牙',
        description: '漱口水无法清洁牙菌斑，长期用还会破坏口腔菌群平衡，导致口腔异味、牙龈出血。'
      },
      {
        title: '为"护眼"每天戴"防蓝光眼镜"超过 12 小时',
        description: '普通防蓝光眼镜会影响色觉，且非长时间看电子屏（如每天超6小时）无需戴，反而让眼睛适应"过滤光"。'
      },
      {
        title: '用"生姜擦头皮"治脱发',
        description: '生姜刺激性强，会损伤毛囊、加重炎症，导致脱发更严重，应就医查明原因（如雄激素性脱发）。'
      },
      {
        title: '吃"酵素"排毒减肥',
        description: '酵素本质是酶，口服后会被胃酸分解失活，无法"排毒"，且添加糖分高易发胖。'
      }
    ]
  },
  {
    id: 'lifestyle',
    name: '日常习惯类',
    icon: '🏠',
    items: [
      {
        title: '为"排汗"夏天不开空调',
        description: '长期高温会导致中暑、心脏负担加重（尤其老人），应合理使用空调（26-28℃）+ 适度出汗。'
      },
      {
        title: '冬天"春捂秋冻"不穿秋裤',
        description: '"秋冻"指气温微凉时别急着添衣，但严寒天气不保暖会导致关节炎、感冒，应根据体感穿衣。'
      },
      {
        title: '每天用"热水烫脚"缓解静脉曲张',
        description: '静脉曲张患者用热水泡脚会导致血管扩张、加重病情，应选温水（40℃左右）或就医治疗。'
      },
      {
        title: '长期用"颈椎按摩仪"缓解颈椎痛',
        description: '不当使用会损伤颈椎韧带、加重错位，颈椎问题应先就医明确病因（如椎间盘突出）。'
      },
      {
        title: '为"养胃"长期喝粥',
        description: '粥易消化但缺乏咀嚼刺激，会导致胃功能退化、牙齿松动，应搭配固体食物（如馒头、蔬菜）。'
      },
      {
        title: '用"眼药水"缓解眼疲劳（天天滴）',
        description: '眼药水含防腐剂，长期用会破坏泪膜、加重干眼症，应多眨眼、远眺、热敷。'
      },
      {
        title: '饭后立刻躺下"助消化"',
        description: '饭后立刻平躺会导致胃酸反流、胃食管反流病，应饭后站立或慢走30分钟再休息。'
      },
      {
        title: '长期戴"保暖护膝"保护关节',
        description: '长期戴护膝会导致关节周围肌肉萎缩、依赖性增强，应通过力量训练（如靠墙静蹲）强化肌肉。'
      },
      {
        title: '为"清肠"定期灌肠',
        description: '频繁灌肠会破坏肠道菌群、导致肠道依赖（无法自主排便），应通过饮食（高纤维）+ 运动改善便秘。'
      },
      {
        title: '用"生理盐水"洗鼻治鼻炎（自制浓度不准）',
        description: '浓度过高会损伤鼻黏膜，应使用医用生理盐水（0.9%）或专用洗鼻器。'
      }
    ]
  }
]

// 搜索过滤
const filteredCategories = computed(() => {
  if (!searchKeyword.value.trim()) {
    return categories
  }

  const keyword = searchKeyword.value.toLowerCase()
  return categories
    .map(category => ({
      ...category,
      items: category.items.filter(item =>
        item.title.toLowerCase().includes(keyword) ||
        item.description.toLowerCase().includes(keyword)
      )
    }))
    .filter(category => category.items.length > 0)
})

// 当前显示的分类
const currentCategory = computed(() => {
  return filteredCategories.value.find(cat => cat.id === activeTab.value)
})

// 高亮关键词
const highlightKeyword = (text: string) => {
  if (!searchKeyword.value.trim()) {
    return text
  }

  const regex = new RegExp(`(${searchKeyword.value})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

// 搜索处理
const handleSearch = () => {
  // 如果有搜索结果，自动切换到第一个有结果的分类
  if (searchKeyword.value.trim() && filteredCategories.value.length > 0) {
    activeTab.value = filteredCategories.value[0].id
  }
}
</script>

<style scoped>
/* ========== 页面整体布局 ========== */
.misconceptions-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

/* ========== 页面头部 ========== */
.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.header-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 60px 40px;
  background: linear-gradient(135deg, rgba(255, 99, 72, 0.95), rgba(255, 159, 243, 0.95));
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(255, 99, 72, 0.3);
  backdrop-filter: blur(10px);
}

.page-title {
  font-size: 3.5rem;
  color: white;
  margin-bottom: 20px;
  font-weight: 800;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.2);
  animation: fadeInUp 0.8s ease-out;
}

.page-subtitle {
  font-size: 1.4rem;
  color: white;
  opacity: 0.95;
  line-height: 1.8;
  font-weight: 500;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== 搜索栏 ========== */
.search-section {
  max-width: 800px;
  margin: 0 auto 40px;
}

.search-section :deep(.el-input__wrapper) {
  border-radius: 50px;
  padding: 12px 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* ========== 内容容器 ========== */
.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* ========== 核心提示框 ========== */
.core-tips p {
  margin: 12px 0;
  font-size: 1.05rem;
  line-height: 1.8;
  color: #4a5568;
}

.core-tips strong {
  color: #2d3748;
  font-weight: 700;
}

/* ========== 书签式Tab导航 ========== */
.bookmark-tabs {
  display: flex;
  gap: 12px;
  margin-top: 30px;
  padding: 0 20px;
  overflow-x: auto;
  scrollbar-width: thin;
}

.bookmark-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 32px;
  background: white;
  border: 2px solid #e2e8f0;
  border-bottom: none;
  border-radius: 16px 16px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 140px;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}

.bookmark-tab:hover {
  transform: translateY(-4px);
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e0;
}

.bookmark-tab.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
  transform: translateY(-8px);
  box-shadow: 0 -6px 20px rgba(102, 126, 234, 0.3);
  z-index: 10;
}

.bookmark-tab.active .tab-icon {
  font-size: 2.5rem;
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.bookmark-tab.active .tab-name {
  color: white;
  font-weight: 700;
}

.bookmark-tab.active .tab-count {
  background: white;
  color: #667eea;
}

.tab-icon {
  font-size: 2rem;
  transition: all 0.3s ease;
}

.tab-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-count {
  font-size: 0.85rem;
  background: linear-gradient(135deg, #ff6348, #ff9ff3);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

/* ========== Tab内容区域 ========== */
.tab-content {
  background: white;
  border-radius: 0 0 24px 24px;
  padding: 40px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  margin-top: -2px;
  position: relative;
  z-index: 5;
}

/* ========== 避坑内容列表 ========== */
.misconceptions-list {
  display: grid;
  gap: 20px;
}

.misconception-item {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  border-left: 4px solid #ff6348;
}

.misconception-item:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.item-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #ff6348, #ff9ff3);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}

.item-title {
  font-size: 1.2rem;
  color: #2d3748;
  font-weight: 700;
  line-height: 1.5;
  margin: 0;
}

.item-description {
  color: #4a5568;
  font-size: 1.05rem;
  line-height: 1.8;
  margin: 0;
  padding-left: 51px;
}

/* ========== 搜索关键词高亮 ========== */
:deep(mark) {
  background: linear-gradient(135deg, #feca57, #ff9ff3);
  color: #2d3748;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

/* ========== 返回按钮 ========== */
.back-home {
  text-align: center;
  margin-top: 60px;
  padding-bottom: 40px;
}

.back-home .el-button {
  min-width: 200px;
  height: 56px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 28px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.back-home .el-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .page-title {
    font-size: 2.2rem;
  }

  .page-subtitle {
    font-size: 1.1rem;
  }

  .header-content {
    padding: 40px 24px;
  }

  .bookmark-tabs {
    padding: 0 10px;
    gap: 8px;
  }

  .bookmark-tab {
    min-width: 100px;
    padding: 16px 20px;
  }

  .tab-icon {
    font-size: 1.6rem;
  }

  .bookmark-tab.active .tab-icon {
    font-size: 2rem;
  }

  .tab-name {
    font-size: 0.95rem;
  }

  .tab-count {
    font-size: 0.75rem;
    padding: 3px 8px;
  }

  .tab-content {
    padding: 24px 16px;
  }

  .item-title {
    font-size: 1.1rem;
  }

  .item-description {
    font-size: 1rem;
    padding-left: 0;
    margin-top: 12px;
  }

  .misconception-item {
    padding: 20px;
  }

  .core-tips p {
    font-size: 0.95rem;
  }
}
</style>
