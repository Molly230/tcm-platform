"use strict";
const common_vendor = require("../../common/vendor.js");
const utils_api = require("../../utils/api.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      cartItems: []
    };
  },
  computed: {
    selectedItems() {
      return this.cartItems.filter((item) => item.selected);
    },
    allSelected() {
      return this.cartItems.length > 0 && this.cartItems.every((item) => item.selected);
    },
    totalPrice() {
      return this.selectedItems.reduce((total, item) => total + item.price * item.quantity, 0);
    }
  },
  onShow() {
    this.loadCartData();
  },
  methods: {
    loadCartData() {
      const cart = common_vendor.index.getStorageSync("cart") || [];
      this.cartItems = cart.map((item) => ({
        ...item,
        selected: item.selected !== void 0 ? item.selected : true
      }));
    },
    saveCartData() {
      common_vendor.index.setStorageSync("cart", this.cartItems);
    },
    toggleSelect(index) {
      this.cartItems[index].selected = !this.cartItems[index].selected;
      this.saveCartData();
    },
    toggleSelectAll() {
      const newState = !this.allSelected;
      this.cartItems.forEach((item) => {
        item.selected = newState;
      });
      this.saveCartData();
    },
    increaseQuantity(index) {
      const item = this.cartItems[index];
      if (item.quantity < item.stock) {
        item.quantity++;
        this.saveCartData();
      } else {
        common_vendor.index.showToast({
          title: "库存不足",
          icon: "none"
        });
      }
    },
    decreaseQuantity(index) {
      const item = this.cartItems[index];
      if (item.quantity > 1) {
        item.quantity--;
        this.saveCartData();
      }
    },
    removeItem(index) {
      common_vendor.index.showModal({
        title: "确认删除",
        content: "确定要从购物车移除这件商品吗？",
        success: (res) => {
          if (res.confirm) {
            this.cartItems.splice(index, 1);
            this.saveCartData();
            common_vendor.index.showToast({
              title: "已移除",
              icon: "success"
            });
          }
        }
      });
    },
    goShopping() {
      common_vendor.index.switchTab({
        url: "/pages/products/products"
      });
    },
    goCheckout() {
      if (this.selectedItems.length === 0) {
        common_vendor.index.showToast({
          title: "请选择要结算的商品",
          icon: "none"
        });
        return;
      }
      if (!utils_api.isLoggedIn()) {
        common_vendor.index.showModal({
          title: "需要登录",
          content: "请先登录后再结算",
          success: (res) => {
            if (res.confirm) {
              common_vendor.index.navigateTo({
                url: "/pages/login/login"
              });
            }
          }
        });
        return;
      }
      const selectedData = JSON.stringify(this.selectedItems);
      common_vendor.index.navigateTo({
        url: `/pages/checkout/checkout?items=${encodeURIComponent(selectedData)}`
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.cartItems.length === 0
  }, $data.cartItems.length === 0 ? {
    b: common_assets._imports_0$1,
    c: common_vendor.o((...args) => $options.goShopping && $options.goShopping(...args))
  } : {
    d: common_vendor.f($data.cartItems, (item, index, i0) => {
      return {
        a: item.selected,
        b: common_vendor.o(($event) => $options.toggleSelect(index), item.id),
        c: item.image,
        d: common_vendor.t(item.name),
        e: common_vendor.t(item.price),
        f: common_vendor.t(item.stock),
        g: common_vendor.o(($event) => $options.decreaseQuantity(index), item.id),
        h: item.quantity <= 1,
        i: common_vendor.t(item.quantity),
        j: common_vendor.o(($event) => $options.increaseQuantity(index), item.id),
        k: item.quantity >= item.stock,
        l: common_vendor.o(($event) => $options.removeItem(index), item.id),
        m: item.id
      };
    }),
    e: $options.allSelected,
    f: common_vendor.o((...args) => $options.toggleSelectAll && $options.toggleSelectAll(...args)),
    g: common_vendor.t($options.totalPrice.toFixed(2)),
    h: common_vendor.t($options.selectedItems.length),
    i: common_vendor.o((...args) => $options.goCheckout && $options.goCheckout(...args)),
    j: $options.selectedItems.length === 0
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-fb6ea9e5"]]);
wx.createPage(MiniProgramPage);
