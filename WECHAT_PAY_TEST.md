# 微信支付真实测试指南

## ✅ 当前状态
- 微信商户平台回调地址：已配置 ✅
- 真实支付模式：已启用 ✅
- API密钥：已配置 ✅

---

## 🚀 测试步骤

### 步骤1：重启后端服务（必须！）

配置修改后必须重启才能生效：

```bash
# Windows 本地测试
cd backend
# 如果后端正在运行，先停止（Ctrl+C）
# 然后重新启动
uvicorn app.main:app --reload --port 8001
```

**看到这个日志说明成功**：
```
INFO: ✅ 微信支付初始化成功 - AppID: wx8ef971***, 商户号: 1727330435
```

如果看到"模拟模式"，说明配置没生效，需要重启。

---

### 步骤2：通过API文档测试（推荐）

1. **打开Swagger文档**
   ```
   http://localhost:8001/docs
   ```

2. **找到"微信支付"分组**

3. **先获取Token**
   - 点击 `/api/auth/login`
   - 点击 "Try it out"
   - 输入用户名密码：
     ```
     username: user@tcm.com
     password: user123
     ```
   - 点击 Execute
   - 复制返回的 `access_token`

4. **授权Token**
   - 点击页面右上角的 🔓 Authorize 按钮
   - 输入：`Bearer YOUR_TOKEN`（注意Bearer后面有空格）
   - 点击 Authorize

5. **创建测试订单**
   - 找到 `/api/simple-orders/create` 接口
   - 先用 `/api/cart/add` 添加商品到购物车
   - 然后调用创建订单接口
   - 记录返回的订单ID

6. **测试Native支付**
   - 找到 `/api/wechat-pay/native` 接口
   - 点击 "Try it out"
   - 输入：
     ```json
     {
       "order_id": 1
     }
     ```
   - 点击 Execute

7. **检查返回结果**
   ```json
   {
     "success": true,
     "data": {
       "success": true,
       "payment_method": "wechat_native",
       "qr_code_url": "weixin://wxpay/bizpayurl?pr=xxxxx",
       "mock_mode": false  // ⚠️ 必须是false！
     }
   }
   ```

   如果 `mock_mode: true`，说明真实支付没生效，检查：
   - 后端是否重启
   - `.env` 文件是否修改保存

---

### 步骤3：扫码支付测试

**方法1：使用二维码生成器**
1. 复制返回的 `qr_code_url`
2. 打开在线二维码生成器：https://cli.im/
3. 粘贴URL生成二维码
4. 用微信扫描支付

**方法2：使用Python生成二维码**
```bash
cd backend
pip install qrcode pillow
python -c "
import qrcode
qr = qrcode.make('weixin://wxpay/bizpayurl?pr=xxxxx')  # 替换为你的URL
qr.save('wechat_qr.png')
print('二维码已保存到 wechat_qr.png')
"
```

**⚠️ 重要提示**：
- 必须用**真实的微信账号**扫码
- 支付金额会根据订单实际金额计算
- 建议先用**0.01元的订单测试**

---

### 步骤4：查询支付状态

**等待3-5秒后**，调用查询接口确认支付是否成功：

在Swagger文档中：
1. 找到 `/api/wechat-pay/query` 接口
2. 输入订单号：
   ```json
   {
     "order_number": "ORDER202501010001"
   }
   ```
3. 点击 Execute

**预期结果**：
```json
{
  "success": true,
  "data": {
    "order_id": "ORDER202501010001",
    "trade_state": "SUCCESS",
    "trade_state_desc": "支付成功",
    "transaction_id": "4200001234567890",
    "total_fee": 0.01
  }
}
```

---

## 🔍 问题排查

### 问题1：返回 mock_mode: true

**原因**：真实支付没生效

**解决**：
1. 确认 `.env` 文件中 `WECHAT_MOCK_MODE=false`
2. 重启后端服务
3. 查看启动日志

### 问题2：签名错误

**错误信息**：`签名验证失败`

**解决**：
1. 确认API密钥正确：`50f96b28cbce26aaaf1e9fd1f5aebbe2`
2. 确认商户号正确：`1727330435`
3. 登录微信商户平台核对

### 问题3：参数格式有误

**错误信息**：`商家参数格式有误`

**解决**：
1. 检查H5支付域名是否配置
2. 检查回调URL是否HTTPS
3. 确认支付产品已开通

### 问题4：二维码扫描后提示错误

**可能原因**：
- 二维码已过期（2小时有效期）
- 订单已支付
- 商户号未开通Native支付

**解决**：
1. 重新创建订单和支付
2. 登录微信商户平台确认产品开通状态

---

## 📊 监控日志

### 后端日志关键信息

**支付创建成功**：
```
INFO: ✅ Native支付创建 - 用户: user@tcm.com, 订单: ORDER202501010001
```

**收到支付回调**：
```
INFO: 收到微信支付回调: ORDER202501010001
INFO: ✅ 订单支付成功（回调） - 订单号: ORDER202501010001
```

**如果没有收到回调**：
- 检查回调URL是否公网可访问
- 检查HTTPS证书是否有效
- 登录微信商户平台查看"通知记录"

---

## 🎯 小额测试建议

**第一次测试用0.01元**：

1. 创建价格为0.01元的测试商品
2. 添加到购物车
3. 创建订单
4. 扫码支付0.01元
5. 确认回调成功
6. 查询订单状态

**成功后再测试正常金额**。

---

## 📞 问题反馈

测试过程中遇到问题，记录以下信息：

1. **错误信息**（完整的JSON响应）
2. **订单号**
3. **操作步骤**
4. **后端日志**（相关部分）
5. **微信商户平台的交易记录截图**

---

## ✅ 测试通过标准

- [  ] Native支付创建成功（mock_mode: false）
- [  ] 二维码可以正常扫描
- [  ] 支付金额正确
- [  ] 支付成功后收到回调
- [  ] 订单状态自动更新为"已支付"
- [  ] 查询接口返回支付成功

**全部通过后，微信支付功能即可上线！**

---

**测试时间**：2025-01-01
**版本**：v1.0
**状态**：准备测试
