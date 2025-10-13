"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      showModal: false
    };
  },
  methods: {
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
    a: common_vendor.o((...args) => $options.showJoinModal && $options.showJoinModal(...args)),
    b: $data.showModal
  }, $data.showModal ? {
    c: common_vendor.o((...args) => $options.closeModal && $options.closeModal(...args)),
    d: common_vendor.o(() => {
    }),
    e: common_vendor.o((...args) => $options.closeModal && $options.closeModal(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
