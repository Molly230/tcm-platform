# 移动端项目 (UniApp)

## 项目结构

```
src/
├── main.js          # 应用入口
├── App.vue          # 根组件
├── pages/           # 页面
│   ├── index/       # 首页
│   │   └── index.vue
│   ├── consultation/ # 健康咨询
│   │   └── consultation.vue
│   ├── expert-consultation/ # 专家咨询
│   │   └── expert-consultation.vue
│   ├── courses/     # 课程中心
│   │   └── courses.vue
│   └── about/       # 关于我们
│       └── about.vue
├── components/      # 公共组件
├── utils/           # 工具函数
├── api/             # API接口
└── pages.json       # 页面配置
```

## 安装依赖

```bash
npm install
```

## 开发运行

```bash
# 运行到H5
npm run dev:h5

# 运行到微信小程序
npm run dev:mp-weixin
```

## 构建生产版本

```bash
# 构建H5
npm run build:h5

# 构建微信小程序
npm run build:mp-weixin
```

## 技术栈

- UniApp (跨平台开发框架)
- Vue 3
- 支持H5、微信小程序、APP等多端