# 微信支付生产环境部署清单

## ✅ 配置已完成

### 1. 环境变量配置（backend/.env）
```bash
WECHAT_APP_ID=wx8ef971d8efa87ffb          ✅ 已配置
WECHAT_MCH_ID=1727330435                 ✅ 已配置
WECHAT_API_KEY=50f96b28cbce26aaaf1e9fd1f5aebbe2  ✅ 已更正为真实密钥
WECHAT_NOTIFY_URL=https://tcmlife.top/api/wechat-pay/notify  ✅ 已修正路径
WECHAT_H5_DOMAIN=tcmlife.top             ✅ 已配置
WECHAT_PAYMENT_TYPE=JSAPI                ✅ 已配置
WECHAT_MOCK_MODE=true                    ⏳ 生产部署时改为 false
```

### 2. 代码文件已就绪
- ✅ `backend/app/core/wechat_pay.py` - 微信支付服务类
- ✅ `backend/app/api/wechat_pay.py` - 微信支付API路由
- ✅ `backend/app/api/api.py` - 已集成路由
- ✅ `backend/test_wechat_pay.py` - 完整测试脚本
- ✅ `WECHAT_PAY_CONFIG.md` - 详细配置文档

---

## 🚀 生产环境部署步骤

### 步骤1：确认微信商户平台配置

登录 https://pay.weixin.qq.com/

#### 1.1 配置API密钥
路径：`账户中心 > API安全 > API密钥`
- 密钥：`50f96b28cbce26aaaf1e9fd1f5aebbe2`
- **重要**：密钥设置后无法查看，确保与`.env`中一致

#### 1.2 配置回调域名
路径：`产品中心 > 开发配置 > 支付配置`
- 添加授权域名：`tcmlife.top`（不带http://）

#### 1.3 配置H5支付域名（如需H5支付）
路径：`产品中心 > H5支付 > 开通配置`
- 添加授权域名：`tcmlife.top`

#### 1.4 确认支付产品已开通
路径：`产品中心 > 我的产品`
- [  ] Native支付（扫码支付）
- [  ] H5支付（移动浏览器支付）
- [  ] JSAPI支付（公众号/小程序支付）

---

### 步骤2：本地模拟模式测试

```bash
# 1. 确保配置为模拟模式
WECHAT_MOCK_MODE=true

# 2. 启动后端服务
cd backend
uvicorn app.main:app --reload --port 8001

# 3. 运行完整测试
python test_wechat_pay.py
```

**预期结果**：
- ✅ 所有接口返回成功
- ✅ mock_mode: true
- ✅ 订单状态更新正常

---

### 步骤3：服务器环境准备

#### 3.1 确认服务器配置
- [  ] 域名 `tcmlife.top` 已解析到服务器IP
- [  ] SSL证书已安装且有效
- [  ] Nginx/Apache 反向代理已配置
- [  ] 防火墙允许外部访问

#### 3.2 测试回调URL可访问性
```bash
# 在服务器上执行
curl -I https://tcmlife.top/api/wechat-pay/notify
```

**预期结果**：
- HTTP/1.1 405 Method Not Allowed（因为回调应该用POST）
- 不应该是 404/502/503 错误

#### 3.3 Nginx配置示例
```nginx
server {
    listen 443 ssl;
    server_name tcmlife.top;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 步骤4：切换到真实支付模式

#### 4.1 修改环境变量
编辑 `backend/.env`：
```bash
# 将模拟模式改为false
WECHAT_MOCK_MODE=false
```

#### 4.2 重启后端服务
```bash
# 如果使用supervisor
supervisorctl restart tcm_backend

# 或使用systemd
systemctl restart tcm_backend

# 或直接重启uvicorn
pkill -f "uvicorn app.main:app"
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

#### 4.3 检查服务状态
```bash
# 查看日志
tail -f backend/logs/app.log

# 或uvicorn输出
ps aux | grep uvicorn
```

---

### 步骤5：真实支付测试

#### 5.1 小额测试（0.01元）

**测试Native支付（扫码）**：
```bash
curl -X POST "https://tcmlife.top/api/wechat-pay/native" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}'
```

**预期返回**：
```json
{
  "success": true,
  "data": {
    "success": true,
    "payment_method": "wechat_native",
    "qr_code_url": "weixin://wxpay/bizpayurl?pr=xxxxx",
    "mock_mode": false  // ⚠️ 必须是false
  }
}
```

#### 5.2 扫码支付测试
1. 使用微信扫描返回的二维码
2. 完成0.01元支付
3. 等待回调通知（约3-5秒）
4. 查询订单状态确认

#### 5.3 查询支付状态
```bash
curl -X POST "https://tcmlife.top/api/wechat-pay/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"order_number": "ORDER202501010001"}'
```

**预期返回**：
```json
{
  "success": true,
  "data": {
    "trade_state": "SUCCESS",
    "trade_state_desc": "支付成功"
  }
}
```

---

### 步骤6：监控与异常处理

#### 6.1 日志监控
```bash
# 实时查看微信支付相关日志
tail -f backend/logs/app.log | grep "wechat"
```

**关键日志**：
- `✅ 微信支付初始化成功` - 服务启动正常
- `✅ Native支付创建成功` - 支付订单创建成功
- `收到微信支付回调` - 收到支付回调
- `✅ 订单支付成功（回调）` - 回调处理成功

#### 6.2 常见错误处理

**错误1：签名验证失败**
```
原因：API密钥配置错误
解决：确认.env中的WECHAT_API_KEY与商户平台一致
```

**错误2：回调URL无法访问**
```
原因：防火墙阻止或域名未解析
解决：检查防火墙规则和域名解析
```

**错误3：参数格式有误**
```
原因：H5支付域名未配置
解决：登录商户平台配置H5支付域名
```

---

## 📊 生产环境检查清单

### 配置检查
- [  ] `.env` 文件中所有微信支付配置项已填写
- [  ] API密钥与微信商户平台一致
- [  ] 回调URL路径正确（/api/wechat-pay/notify）
- [  ] `WECHAT_MOCK_MODE=false`

### 商户平台检查
- [  ] API密钥已设置
- [  ] 回调域名已添加
- [  ] H5支付域名已添加（如需H5支付）
- [  ] 支付产品已开通

### 服务器检查
- [  ] 域名已解析
- [  ] SSL证书有效
- [  ] 回调URL可公网访问
- [  ] 防火墙规则正确

### 功能测试
- [  ] 模拟模式测试通过
- [  ] 真实支付模式启动成功
- [  ] 0.01元小额支付测试通过
- [  ] 支付回调接收成功
- [  ] 订单状态更新正常

---

## 🆘 紧急回滚方案

如果生产环境出现问题，立即执行：

```bash
# 1. 切回模拟模式
sed -i 's/WECHAT_MOCK_MODE=false/WECHAT_MOCK_MODE=true/' backend/.env

# 2. 重启服务
supervisorctl restart tcm_backend

# 3. 检查日志
tail -f backend/logs/app.log

# 4. 通知用户支付暂时不可用
```

---

## 📞 支持联系方式

- 微信支付商户客服：95017
- 微信支付官方文档：https://pay.weixin.qq.com/wiki/doc/api/index.html
- 项目配置文档：`WECHAT_PAY_CONFIG.md`

---

## 🎯 部署时间建议

**推荐部署时间**：
- 工作日 22:00 - 24:00（低峰期）
- 避免周末和节假日
- 提前通知用户维护时间

**部署前准备**：
- ✅ 完整测试通过
- ✅ 备份当前配置
- ✅ 准备回滚方案
- ✅ 技术人员在线待命

---

**最后更新**：2025-01-01
**文档版本**：v1.0
**状态**：准备部署
