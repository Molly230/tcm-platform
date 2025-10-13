"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      showAIForm: false,
      symptoms: "",
      duration: "",
      medicalHistory: ""
    };
  },
  methods: {
    selectAIConsultation() {
      this.showAIForm = true;
    },
    selectExpertConsultation() {
      common_vendor.index.navigateTo({
        url: "/pages/expert-consultation/expert-consultation"
      });
    },
    submitAIConsultation() {
      console.log("提交AI问诊:", {
        symptoms: this.symptoms,
        duration: this.duration,
        medicalHistory: this.medicalHistory
      });
      common_vendor.index.showToast({
        title: "问诊已提交",
        icon: "success"
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.o((...args) => $options.selectAIConsultation && $options.selectAIConsultation(...args)),
    b: common_vendor.o((...args) => $options.selectExpertConsultation && $options.selectExpertConsultation(...args)),
    c: $data.showAIForm
  }, $data.showAIForm ? {
    d: $data.symptoms,
    e: common_vendor.o(($event) => $data.symptoms = $event.detail.value),
    f: $data.duration,
    g: common_vendor.o(($event) => $data.duration = $event.detail.value),
    h: $data.medicalHistory,
    i: common_vendor.o(($event) => $data.medicalHistory = $event.detail.value),
    j: common_vendor.o((...args) => $options.submitAIConsultation && $options.submitAIConsultation(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
