# 后端项目 (FastAPI)

## 项目结构

```
app/
├── main.py          # 应用入口
├── core/            # 核心配置
│   └── config.py    # 配置文件
├── api/             # API路由
├── models/          # 数据模型
├── schemas/         # 数据验证
├── database/        # 数据库连接
├── utils/           # 工具函数
└── __init__.py      # 包初始化
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
# 开发模式
uvicorn app.main:app --reload

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc