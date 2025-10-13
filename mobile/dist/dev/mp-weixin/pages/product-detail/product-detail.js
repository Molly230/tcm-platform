"use strict";
const common_vendor = require("../../common/vendor.js");
const utils_api = require("../../utils/api.js");
const _sfc_main = {
  data() {
    return {
      productId: null,
      product: null,
      loading: true,
      cartCount: 0
    };
  },
  onLoad(options) {
    this.productId = options.id;
    this.loadProductDetail();
    this.updateCartCount();
  },
  onShow() {
    this.updateCartCount();
  },
  methods: {
    async loadProductDetail() {
      this.loading = true;
      try {
        const response = await utils_api.apiRequest(`/api/products/${this.productId}`);
        this.product = response;
      } catch (error) {
        console.error("加载商品详情失败:", error);
        common_vendor.index.showToast({
          title: "加载失败",
          icon: "none"
        });
        setTimeout(() => {
          common_vendor.index.navigateBack();
        }, 1500);
      } finally {
        this.loading = false;
      }
    },
    getImageUrl(image) {
      if (image && image.startsWith("http")) {
        return image;
      }
      return image ? `http://localhost:8001${image}` : "/static/default-product.png";
    },
    addToCart() {
      var _a;
      if (!this.product || this.product.stock_quantity <= 0)
        return;
      try {
        let cart = common_vendor.index.getStorageSync("cart") || [];
        const existingIndex = cart.findIndex((item) => item.id === this.product.id);
        if (existingIndex >= 0) {
          cart[existingIndex].quantity += 1;
          if (cart[existingIndex].quantity > this.product.stock_quantity) {
            cart[existingIndex].quantity = this.product.stock_quantity;
            common_vendor.index.showToast({
              title: "库存不足",
              icon: "none"
            });
            return;
          }
        } else {
          cart.push({
            id: this.product.id,
            name: this.product.name,
            price: this.product.price,
            image: this.getImageUrl((_a = this.product.images) == null ? void 0 : _a[0]),
            quantity: 1,
            stock: this.product.stock_quantity
          });
        }
        common_vendor.index.setStorageSync("cart", cart);
        this.updateCartCount();
        common_vendor.index.showToast({
          title: "已加入购物车",
          icon: "success"
        });
      } catch (error) {
        common_vendor.index.showToast({
          title: "添加失败",
          icon: "none"
        });
      }
    },
    buyNow() {
      var _a;
      if (!utils_api.isLoggedIn()) {
        common_vendor.index.showModal({
          title: "需要登录",
          content: "请先登录后再购买",
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
      const buyItem = {
        id: this.product.id,
        name: this.product.name,
        price: this.product.price,
        image: this.getImageUrl((_a = this.product.images) == null ? void 0 : _a[0]),
        quantity: 1,
        stock: this.product.stock_quantity
      };
      const buyData = JSON.stringify([buyItem]);
      common_vendor.index.navigateTo({
        url: `/pages/checkout/checkout?items=${encodeURIComponent(buyData)}`
      });
    },
    goToCart() {
      common_vendor.index.switchTab({
        url: "/pages/cart/cart"
      });
    },
    updateCartCount() {
      const cart = common_vendor.index.getStorageSync("cart") || [];
      this.cartCount = cart.reduce((total, item) => total + item.quantity, 0);
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.loading
  }, $data.loading ? {} : $data.product ? common_vendor.e({
    c: common_vendor.f($data.product.images, (image, index, i0) => {
      return {
        a: $options.getImageUrl(image),
        b: index
      };
    }),
    d: common_vendor.t($data.product.name),
    e: common_vendor.t($data.product.price),
    f: common_vendor.t($data.product.stock_quantity),
    g: $data.product.is_featured
  }, $data.product.is_featured ? {} : {}, {
    h: $data.product.is_common
  }, $data.product.is_common ? {} : {}, {
    i: $data.product.is_prescription_required
  }, $data.product.is_prescription_required ? {} : {}, {
    j: common_vendor.t($data.product.description),
    k: $data.product.usage_instructions
  }, $data.product.usage_instructions ? {
    l: common_vendor.t($data.product.usage_instructions)
  } : {}) : {}, {
    b: $data.product,
    m: $data.product
  }, $data.product ? common_vendor.e({
    n: $data.cartCount > 0
  }, $data.cartCount > 0 ? {
    o: common_vendor.t($data.cartCount)
  } : {}, {
    p: common_vendor.o((...args) => $options.goToCart && $options.goToCart(...args)),
    q: $data.product.stock_quantity > 0
  }, $data.product.stock_quantity > 0 ? {} : {}, {
    r: common_vendor.o((...args) => $options.addToCart && $options.addToCart(...args)),
    s: $data.product.stock_quantity <= 0,
    t: common_vendor.o((...args) => $options.buyNow && $options.buyNow(...args)),
    v: $data.product.stock_quantity <= 0
  }) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-35f64a8f"]]);
wx.createPage(MiniProgramPage);
