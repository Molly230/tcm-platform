"use strict";
const common_vendor = require("../../common/vendor.js");
const utils_api = require("../../utils/api.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      form: {
        username: "",
        password: ""
      },
      loading: false
    };
  },
  methods: {
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        common_vendor.index.showToast({
          title: "请填写完整信息",
          icon: "none"
        });
        return;
      }
      this.loading = true;
      try {
        const response = await utils_api.apiRequest("/api/auth/login", {
          method: "POST",
          data: {
            username: this.form.username,
            password: this.form.password
          }
        });
        if (response.access_token) {
          common_vendor.index.setStorageSync("token", response.access_token);
          common_vendor.index.setStorageSync("user", response.user);
          common_vendor.index.showToast({
            title: "登录成功",
            icon: "success"
          });
          setTimeout(() => {
            common_vendor.index.switchTab({
              url: "/pages/index/index"
            });
          }, 1500);
        }
      } catch (error) {
        common_vendor.index.showToast({
          title: error.message || "登录失败",
          icon: "none"
        });
      } finally {
        this.loading = false;
      }
    },
    async handleWechatLogin() {
      try {
        const res = await common_vendor.index.login({
          provider: "weixin"
        });
        if (res.code) {
          const response = await utils_api.apiRequest("/api/auth/wechat-login", {
            method: "POST",
            data: {
              code: res.code
            }
          });
          if (response.access_token) {
            common_vendor.index.setStorageSync("token", response.access_token);
            common_vendor.index.setStorageSync("user", response.user);
            common_vendor.index.showToast({
              title: "登录成功",
              icon: "success"
            });
            setTimeout(() => {
              common_vendor.index.switchTab({
                url: "/pages/index/index"
              });
            }, 1500);
          }
        }
      } catch (error) {
        common_vendor.index.showToast({
          title: "微信登录失败",
          icon: "none"
        });
      }
    },
    goToRegister() {
      common_vendor.index.showModal({
        title: "注册功能",
        content: "请通过网页版注册账号，或联系客服开通账户",
        showCancel: false
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_assets._imports_0,
    b: $data.form.username,
    c: common_vendor.o(($event) => $data.form.username = $event.detail.value),
    d: $data.form.password,
    e: common_vendor.o(($event) => $data.form.password = $event.detail.value),
    f: $data.loading
  }, $data.loading ? {} : {}, {
    g: common_vendor.o((...args) => $options.handleLogin && $options.handleLogin(...args)),
    h: $data.loading,
    i: common_vendor.o((...args) => $options.handleWechatLogin && $options.handleWechatLogin(...args)),
    j: common_vendor.o((...args) => $options.goToRegister && $options.goToRegister(...args))
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-cdfe2409"]]);
wx.createPage(MiniProgramPage);
