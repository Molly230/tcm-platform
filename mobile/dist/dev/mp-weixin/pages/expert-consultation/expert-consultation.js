"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      categories: ["全部", "中医内科", "中医妇科", "中医儿科", "针灸推拿", "中医养生"],
      selectedCategory: "全部",
      searchKeyword: "",
      experts: [
        {
          id: 1,
          name: "张医师",
          title: "主任医师",
          category: "中医内科",
          avatar: "https://via.placeholder.com/100x100?text=张医师",
          description: "从事中医内科临床工作20年，擅长治疗消化系统疾病和呼吸系统疾病。",
          rating: 98,
          consultations: 1200,
          textPrice: 50,
          voicePrice: 100,
          videoPrice: 200
        },
        {
          id: 2,
          name: "李医师",
          title: "副主任医师",
          category: "中医妇科",
          avatar: "https://via.placeholder.com/100x100?text=李医师",
          description: "专注于妇科疾病治疗15年，对月经不调、不孕不育等有丰富经验。",
          rating: 96,
          consultations: 800,
          textPrice: 60,
          voicePrice: 120,
          videoPrice: 250
        }
      ]
    };
  },
  computed: {
    filteredExperts() {
      let result = this.experts;
      if (this.selectedCategory !== "全部") {
        result = result.filter((expert) => expert.category.includes(this.selectedCategory));
      }
      if (this.searchKeyword) {
        result = result.filter(
          (expert) => expert.name.includes(this.searchKeyword) || expert.title.includes(this.searchKeyword)
        );
      }
      return result;
    }
  },
  methods: {
    onCategoryChange(e) {
      this.selectedCategory = this.categories[e.detail.value];
    },
    searchExperts() {
      console.log("搜索专家:", this.searchKeyword);
    },
    bookConsultation(expertId) {
      console.log("预约咨询:", expertId);
      common_vendor.index.showToast({
        title: "预约成功",
        icon: "success"
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.t($data.selectedCategory),
    b: $data.categories,
    c: common_vendor.o((...args) => $options.onCategoryChange && $options.onCategoryChange(...args)),
    d: $data.searchKeyword,
    e: common_vendor.o(($event) => $data.searchKeyword = $event.detail.value),
    f: common_vendor.o((...args) => $options.searchExperts && $options.searchExperts(...args)),
    g: common_vendor.f($options.filteredExperts, (expert, k0, i0) => {
      return {
        a: expert.avatar,
        b: common_vendor.t(expert.name),
        c: common_vendor.t(expert.title),
        d: common_vendor.t(expert.category),
        e: common_vendor.t(expert.description),
        f: common_vendor.t(expert.rating),
        g: common_vendor.t(expert.consultations),
        h: common_vendor.t(expert.textPrice),
        i: common_vendor.t(expert.voicePrice),
        j: common_vendor.t(expert.videoPrice),
        k: expert.id,
        l: common_vendor.o(($event) => $options.bookConsultation(expert.id), expert.id)
      };
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
