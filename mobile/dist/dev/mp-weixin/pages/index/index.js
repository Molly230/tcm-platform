"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      showModal: false
    };
  },
  methods: {
    handleArticleClick(articleId) {
      console.log("点击文章:", articleId);
      common_vendor.index.navigateTo({
        url: "/pages/health-insights/health-insights"
      });
    },
    goToHealthInsights() {
      common_vendor.index.switchTab({
        url: "/pages/consultation/consultation"
      });
    },
    goToAssessment() {
      common_vendor.index.navigateTo({
        url: "/pages/assessment/assessment"
      });
    },
    showJoinModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.o(($event) => $options.handleArticleClick("health-essence")),
    b: common_vendor.o(($event) => $options.handleArticleClick("thinking-wrong")),
    c: common_vendor.o(($event) => $options.handleArticleClick("doctor-vs-health")),
    d: common_vendor.o(($event) => $options.handleArticleClick("body-system")),
    e: common_vendor.o((...args) => $options.goToHealthInsights && $options.goToHealthInsights(...args)),
    f: common_vendor.o((...args) => $options.goToAssessment && $options.goToAssessment(...args)),
    g: common_vendor.o((...args) => $options.showJoinModal && $options.showJoinModal(...args)),
    h: $data.showModal
  }, $data.showModal ? {
    i: common_vendor.o((...args) => $options.closeModal && $options.closeModal(...args)),
    j: common_vendor.o(() => {
    }),
    k: common_vendor.o((...args) => $options.closeModal && $options.closeModal(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
