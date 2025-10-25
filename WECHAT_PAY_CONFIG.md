# 微信支付配置文档

## 📋 目录
- [概述](#概述)
- [环境配置](#环境配置)
- [支付类型](#支付类型)
- [API接口](#api接口)
- [测试流程](#测试流程)
- [常见问题](#常见问题)

---

## 概述

本项目集成了**微信支付**官方接口，基于 `wechatpy` 库实现，支持三种支付方式：

1. **Native扫码支付** - PC网站、后台管理扫码支付
2. **H5支付** - 移动端浏览器内支付
3. **JSAPI支付** - 微信公众号、小程序内支付

### 核心特性
- ✅ 统一服务层封装（`app/core/wechat_pay.py`）
- ✅ 完整的API路由（`app/api/wechat_pay.py`）
- ✅ 自动从环境变量读取配置
- ✅ 支持模拟模式（开发测试）
- ✅ 支付回调自动验证签名
- ✅ 订单状态自动更新

---

## 环境配置

### 1. 修改 `.env` 文件

```bash
# 微信支付配置
WECHAT_APP_ID=wxXXXXXXXXXXXXXXXX          # 微信公众号AppID（替换为你的真实AppID）
WECHAT_MCH_ID=1234567890                 # 微信商户号（替换为你的真实商户号）
WECHAT_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  # API密钥（32位，替换为你的真实密钥）
WECHAT_NOTIFY_URL=https://your-domain.com/api/wechat-pay/notify  # 支付回调地址
WECHAT_H5_DOMAIN=your-domain.com         # H5支付域名
WECHAT_PAYMENT_TYPE=JSAPI                # 默认支付类型：NATIVE/H5/JSAPI

# 模拟模式（开发测试用）
WECHAT_MOCK_MODE=true                    # true启用模拟，false使用真实支付
```

### 2. 配置说明

| 配置项 | 必填 | 说明 | 获取方式 |
|--------|------|------|----------|
| `WECHAT_APP_ID` | ✅ | 微信公众号AppID | 微信公众平台 > 开发 > 基本配置 |
| `WECHAT_MCH_ID` | ✅ | 微信商户号 | 微信支付商户平台 > 账户中心 |
| `WECHAT_API_KEY` | ✅ | API密钥（32位） | 微信支付商户平台 > 账户中心 > API安全 |
| `WECHAT_NOTIFY_URL` | ✅ | 支付回调URL | 自定义，需配置为公网可访问的HTTPS地址 |
| `WECHAT_H5_DOMAIN` | H5支付必填 | H5支付授权域名 | 微信支付商户平台 > 产品中心 > H5支付 |
| `WECHAT_PAYMENT_TYPE` | ❌ | 默认支付类型 | 可选：NATIVE/H5/JSAPI |
| `WECHAT_MOCK_MODE` | ❌ | 是否模拟模式 | true/false，默认false |

### 3. 微信商户平台配置

#### 3.1 配置支付回调URL
1. 登录 [微信支付商户平台](https://pay.weixin.qq.com/)
2. 产品中心 > 开发配置 > 支付配置
3. 添加回调域名：`tcmlife.top`

#### 3.2 配置H5支付域名（如需H5支付）
1. 产品中心 > H5支付 > 开通配置
2. 添加授权域名：`tcmlife.top`

#### 3.3 获取API密钥
1. 账户中心 > API安全
2. 设置API密钥（32位随机字符串）
3. **重要**：密钥设置后无法查看，请妥善保管

---

## 支付类型

### 1. Native扫码支付

**适用场景**：PC网站、后台管理系统

**支付流程**：
1. 前端调用创建支付接口
2. 后端返回二维码URL（`qr_code_url`）
3. 前端使用 `qrcode` 库生成二维码图片
4. 用户使用微信扫码支付
5. 支付成功后微信回调通知
6. 前端轮询查询支付状态

**API端点**：`POST /api/wechat-pay/native`

**请求示例**：
```json
{
  "order_id": 123,
  "detail": "商品详情说明"
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "支付创建成功",
  "data": {
    "success": true,
    "payment_method": "wechat_native",
    "order_id": "ORDER202501010001",
    "amount": 168.80,
    "qr_code_url": "weixin://wxpay/bizpayurl?pr=xxxxx",
    "prepay_id": "wx2024010100000001",
    "subject": "订单 ORDER202501010001",
    "expires_at": 1704096000
  }
}
```

---

### 2. H5支付

**适用场景**：移动端浏览器（非微信内）

**支付流程**：
1. 前端调用创建支付接口
2. 后端返回支付跳转URL（`mweb_url`）
3. 前端直接跳转到该URL
4. 用户完成支付后返回
5. 微信回调通知后端
6. 前端查询支付状态

**API端点**：`POST /api/wechat-pay/h5`

**请求示例**：
```json
{
  "order_id": 123,
  "detail": "商品详情说明"
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "支付创建成功",
  "data": {
    "success": true,
    "payment_method": "wechat_h5",
    "order_id": "ORDER202501010001",
    "amount": 168.80,
    "mweb_url": "https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?prepay_id=xxx&package=xxx",
    "prepay_id": "wx2024010100000001",
    "subject": "订单 ORDER202501010001"
  }
}
```

---

### 3. JSAPI支付

**适用场景**：微信公众号、微信小程序内

**支付流程**：
1. 前端先获取用户OpenID（需授权）
2. 调用创建支付接口（传入OpenID）
3. 后端返回JSAPI支付参数
4. 前端调用微信JSAPI发起支付
5. 用户完成支付
6. 微信回调通知后端

**API端点**：`POST /api/wechat-pay/jsapi`

**请求示例**：
```json
{
  "order_id": 123,
  "openid": "oUpF8uMuAJO_M2pxb1Q9zNjWeS6o",
  "detail": "商品详情说明"
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "支付创建成功",
  "data": {
    "success": true,
    "payment_method": "wechat_jsapi",
    "order_id": "ORDER202501010001",
    "amount": 168.80,
    "prepay_id": "wx2024010100000001",
    "jsapi_params": {
      "appId": "wxXXXXXXXXXXXXXX",
      "timeStamp": "1704067200",
      "nonceStr": "abc123",
      "package": "prepay_id=wx2024010100000001",
      "signType": "MD5",
      "paySign": "C380BEC2BFD727A4B6845133519F3AD6"
    },
    "subject": "订单 ORDER202501010001"
  }
}
```

**前端调用示例（微信公众号）**：
```javascript
function onBridgeReady(jsapi_params) {
  WeixinJSBridge.invoke('getBrandWCPayRequest', jsapi_params, function(res) {
    if (res.err_msg == "get_brand_wcpay_request:ok") {
      // 支付成功
      alert('支付成功');
    } else {
      // 支付失败
      alert('支付失败: ' + res.err_msg);
    }
  });
}

// 确保微信JSAPI已加载
if (typeof WeixinJSBridge == "undefined") {
  document.addEventListener('WeixinJSBridgeReady', function() {
    onBridgeReady(jsapi_params);
  }, false);
} else {
  onBridgeReady(jsapi_params);
}
```

---

## API接口

### 1. 获取配置信息

```http
GET /api/wechat-pay/config
Authorization: Bearer {token}
```

**响应**：
```json
{
  "service_name": "微信支付",
  "version": "v1.0",
  "supported_types": ["NATIVE", "H5", "JSAPI"],
  "config": {
    "app_id": "wxXXXXXXXXXXXXXX",
    "mch_id": "1234567890",
    "payment_type": "JSAPI",
    "notify_url": "https://your-domain.com/api/wechat-pay/notify",
    "h5_domain": "your-domain.com",
    "mock_mode": true
  }
}
```

---

### 2. 查询支付状态

```http
POST /api/wechat-pay/query
Authorization: Bearer {token}
Content-Type: application/json

{
  "order_number": "ORDER202501010001"
}
```

**响应**：
```json
{
  "success": true,
  "message": "查询成功",
  "data": {
    "success": true,
    "order_id": "ORDER202501010001",
    "transaction_id": "4200001234567890",
    "trade_state": "SUCCESS",
    "trade_state_desc": "支付成功",
    "total_fee": 168.80,
    "paid_at": "20250101120000",
    "openid": "oUpF8uMuAJO_M2pxb1Q9zNjWeS6o"
  }
}
```

**支付状态说明**：
- `SUCCESS` - 支付成功
- `REFUND` - 转入退款
- `NOTPAY` - 未支付
- `CLOSED` - 已关闭
- `REVOKED` - 已撤销（付款码支付）
- `USERPAYING` - 用户支付中（付款码支付）
- `PAYERROR` - 支付失败

---

### 3. 支付回调（微信服务器调用）

```http
POST /api/wechat-pay/notify
Content-Type: application/xml

<xml>
  <return_code><![CDATA[SUCCESS]]></return_code>
  <return_msg><![CDATA[OK]]></return_msg>
  <appid><![CDATA[wxXXXXXXXXXXXXXX]]></appid>
  <mch_id><![CDATA[1234567890]]></mch_id>
  <nonce_str><![CDATA[abc123]]></nonce_str>
  <sign><![CDATA[C380BEC2BFD727A4B6845133519F3AD6]]></sign>
  <result_code><![CDATA[SUCCESS]]></result_code>
  <out_trade_no><![CDATA[ORDER202501010001]]></out_trade_no>
  <transaction_id><![CDATA[4200001234567890]]></transaction_id>
  <total_fee>16880</total_fee>
  <time_end><![CDATA[20250101120000]]></time_end>
</xml>
```

**响应（成功）**：
```xml
<xml>
  <return_code><![CDATA[SUCCESS]]></return_code>
  <return_msg><![CDATA[OK]]></return_msg>
</xml>
```

**响应（失败）**：
```xml
<xml>
  <return_code><![CDATA[FAIL]]></return_code>
  <return_msg><![CDATA[签名验证失败]]></return_msg>
</xml>
```

---

### 4. 模拟支付成功（仅开发测试）

```http
GET /api/wechat-pay/mock/simulate-success/{order_number}
```

**注意**：此接口仅在 `WECHAT_MOCK_MODE=true` 时可用

---

## 测试流程

### 1. 启动后端服务

```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

### 2. 运行测试脚本

```bash
cd backend
python test_wechat_pay.py
```

### 3. 测试步骤

脚本会自动执行以下测试：

1. ✅ 用户登录
2. ✅ 创建测试订单
3. ✅ 检查微信支付配置
4. ✅ 测试Native扫码支付
5. ✅ 测试H5支付
6. ✅ 测试JSAPI支付
7. ✅ 查询支付状态
8. ✅ 模拟支付成功
9. ✅ 确认订单状态更新

### 4. 查看API文档

访问 Swagger 文档：http://localhost:8001/docs

找到 **"微信支付"** 分组，查看所有接口定义

---

## 常见问题

### 1. 配置不生效怎么办？

**检查步骤**：
1. 确认 `.env` 文件在 `backend/` 目录下
2. 重启后端服务（uvicorn）
3. 调用 `/api/wechat-pay/config` 接口查看配置是否读取成功
4. 检查环境变量是否被正确加载

### 2. 支付回调签名验证失败

**可能原因**：
1. API密钥配置错误
2. 回调数据被中间件修改
3. 签名算法不匹配

**解决方案**：
1. 确认 `WECHAT_API_KEY` 与商户平台一致
2. 检查服务器日志中的签名对比
3. 确保回调URL支持HTTPS

### 3. H5支付域名校验失败

**错误信息**：`商家参数格式有误，请联系商家解决`

**解决方案**：
1. 登录微信支付商户平台
2. 产品中心 > H5支付 > 开通配置
3. 添加授权域名（不带http://）
4. 等待配置生效（约5分钟）

### 4. JSAPI支付提示"缺少openid"

**原因**：JSAPI支付必须传入用户的OpenID

**解决方案**：
1. 前端先引导用户授权获取OpenID
2. 参考微信公众号开发文档：[网页授权](https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html)
3. 将OpenID传递给后端

### 5. 模拟模式下无法切换到真实支付

**检查步骤**：
1. 修改 `.env` 中 `WECHAT_MOCK_MODE=false`
2. 重启后端服务
3. 调用 `/api/wechat-pay/config` 确认 `mock_mode: false`
4. 确保所有配置项都已正确填写

### 6. 订单状态未自动更新

**可能原因**：
1. 支付回调URL配置错误
2. 服务器防火墙阻止微信服务器访问
3. 签名验证失败导致回调处理失败

**解决方案**：
1. 确保回调URL可公网访问且支持HTTPS
2. 检查服务器日志中的回调记录
3. 手动调用查询接口确认支付状态

---

## 生产环境部署清单

部署到生产环境前，请确认：

- [ ] 已在微信支付商户平台完成所有配置
- [ ] 已获取正式的AppID、商户号、API密钥
- [ ] 回调URL配置为正式域名（HTTPS）
- [ ] `.env` 中 `WECHAT_MOCK_MODE=false`
- [ ] H5支付域名已配置（如需H5支付）
- [ ] 已测试所有支付类型
- [ ] 已配置异常告警监控
- [ ] 已准备好客服联系方式

---

## 联系支持

- 微信支付官方文档：https://pay.weixin.qq.com/wiki/doc/api/index.html
- wechatpy 文档：https://wechatpy.readthedocs.io/
- 项目Issue：https://github.com/yourusername/yourproject/issues

---

**最后更新**：2025-01-01
**文档版本**：v1.0.0
