"use strict";
Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const common_vendor = require("./common/vendor.js");
if (!Math) {
  "./pages/index/index.js";
  "./pages/login/login.js";
  "./pages/products/products.js";
  "./pages/product-detail/product-detail.js";
  "./pages/cart/cart.js";
  "./pages/checkout/checkout.js";
  "./pages/payment/payment.js";
  "./pages/courses/courses.js";
  "./pages/course-detail/course-detail.js";
  "./pages/consultation/consultation.js";
  "./pages/expert-consultation/expert-consultation.js";
  "./pages/assessment/assessment.js";
  "./pages/profile/profile.js";
  "./pages/my-orders/my-orders.js";
  "./pages/my-courses/my-courses.js";
  "./pages/video-player/video-player.js";
  "./pages/about/about.js";
}
const _sfc_main = {
  name: "App"
};
if (!Array) {
  const _component_router_view = common_vendor.resolveComponent("router-view");
  _component_router_view();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {};
}
const App = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
function createApp() {
  const app = common_vendor.createSSRApp(App);
  return {
    app
  };
}
createApp().app.mount("#app");
exports.createApp = createApp;
