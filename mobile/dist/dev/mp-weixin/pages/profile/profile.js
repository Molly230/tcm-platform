"use strict";
const common_vendor = require("../../common/vendor.js");
const utils_api = require("../../utils/api.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      user: null
    };
  },
  computed: {
    isUserLoggedIn() {
      return utils_api.isLoggedIn() && this.user;
    }
  },
  onShow() {
    this.loadUserInfo();
  },
  methods: {
    loadUserInfo() {
      if (utils_api.isLoggedIn()) {
        this.user = utils_api.getCurrentUser();
      } else {
        this.user = null;
      }
    },
    getRoleText(role) {
      const roleMap = {
        "USER": "普通用户",
        "VIP": "VIP用户",
        "EXPERT": "专家",
        "ADMIN": "管理员",
        "SUPER_ADMIN": "超级管理员"
      };
      return roleMap[role] || "用户";
    },
    goToLogin() {
      common_vendor.index.navigateTo({
        url: "/pages/login/login"
      });
    },
    goToOrders() {
      if (!this.checkLogin())
        return;
      common_vendor.index.navigateTo({
        url: "/pages/my-orders/my-orders"
      });
    },
    goToCourses() {
      if (!this.checkLogin())
        return;
      common_vendor.index.navigateTo({
        url: "/pages/my-courses/my-courses"
      });
    },
    goToConsultation() {
      common_vendor.index.switchTab({
        url: "/pages/consultation/consultation"
      });
    },
    goToAssessment() {
      common_vendor.index.navigateTo({
        url: "/pages/assessment/assessment"
      });
    },
    goToAbout() {
      common_vendor.index.navigateTo({
        url: "/pages/about/about"
      });
    },
    contactService() {
      common_vendor.index.showModal({
        title: "联系客服",
        content: "客服热线：400-123-4567\n工作时间：9:00-18:00",
        showCancel: false
      });
    },
    checkLogin() {
      if (!this.isUserLoggedIn) {
        common_vendor.index.showModal({
          title: "需要登录",
          content: "请先登录后再使用此功能",
          success: (res) => {
            if (res.confirm) {
              this.goToLogin();
            }
          }
        });
        return false;
      }
      return true;
    },
    handleLogout() {
      common_vendor.index.showModal({
        title: "确认退出",
        content: "确定要退出登录吗？",
        success: (res) => {
          if (res.confirm) {
            utils_api.logout();
            this.loadUserInfo();
          }
        }
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: !$options.isUserLoggedIn
  }, !$options.isUserLoggedIn ? {
    b: common_assets._imports_0$2,
    c: common_vendor.o((...args) => $options.goToLogin && $options.goToLogin(...args))
  } : {
    d: $data.user.avatar || "/static/default-avatar.png",
    e: common_vendor.t($data.user.username || $data.user.email),
    f: common_vendor.t($options.getRoleText($data.user.role))
  }, {
    g: common_vendor.o((...args) => $options.goToOrders && $options.goToOrders(...args)),
    h: common_vendor.o((...args) => $options.goToCourses && $options.goToCourses(...args)),
    i: common_vendor.o((...args) => $options.goToConsultation && $options.goToConsultation(...args)),
    j: common_vendor.o((...args) => $options.goToAssessment && $options.goToAssessment(...args)),
    k: common_vendor.o((...args) => $options.goToAbout && $options.goToAbout(...args)),
    l: common_vendor.o((...args) => $options.contactService && $options.contactService(...args)),
    m: $options.isUserLoggedIn
  }, $options.isUserLoggedIn ? {
    n: common_vendor.o((...args) => $options.handleLogout && $options.handleLogout(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-04d37cba"]]);
wx.createPage(MiniProgramPage);
