"use strict";
const common_vendor = require("../../common/vendor.js");
const utils_api = require("../../utils/api.js");
const _sfc_main = {
  data() {
    return {
      products: [],
      categories: [],
      searchQuery: "",
      selectedCategory: "",
      loading: false,
      refreshing: false,
      hasMore: true,
      page: 1,
      pageSize: 20,
      cartCount: 0
    };
  },
  onLoad() {
    this.loadCategories();
    this.loadProducts();
    this.updateCartCount();
  },
  onShow() {
    this.updateCartCount();
  },
  methods: {
    async loadCategories() {
      try {
        const response = await utils_api.apiRequest("/api/system/enums/PRODUCT_CATEGORY");
        this.categories = response || [];
      } catch (error) {
        console.error("加载分类失败:", error);
        this.categories = [
          { code: "HERBS", zh: "中药材" },
          { code: "WELLNESS", zh: "养生产品" },
          { code: "HEALTH_FOOD", zh: "保健食品" }
        ];
      }
    },
    async loadProducts(reset = false) {
      if (this.loading)
        return;
      this.loading = true;
      try {
        const params = {
          page: reset ? 1 : this.page,
          page_size: this.pageSize,
          status: "ACTIVE"
          // 只显示在售商品
        };
        if (this.searchQuery) {
          params.search = this.searchQuery;
        }
        if (this.selectedCategory) {
          params.category = this.selectedCategory;
        }
        const response = await utils_api.apiRequest("/api/products/", {
          method: "GET",
          data: params
        });
        if (reset) {
          this.products = response.items || [];
          this.page = 1;
        } else {
          this.products = [...this.products, ...response.items || []];
        }
        this.hasMore = response.items && response.items.length === this.pageSize;
        this.page++;
      } catch (error) {
        console.error("加载商品失败:", error);
        common_vendor.index.showToast({
          title: "加载失败",
          icon: "none"
        });
      } finally {
        this.loading = false;
        this.refreshing = false;
      }
    },
    handleSearch() {
      this.loadProducts(true);
    },
    selectCategory(category) {
      this.selectedCategory = category;
      this.loadProducts(true);
    },
    handleRefresh() {
      this.refreshing = true;
      this.loadProducts(true);
    },
    loadMore() {
      if (this.hasMore && !this.loading) {
        this.loadProducts();
      }
    },
    getProductImage(product) {
      if (product.images && product.images.length > 0) {
        return product.images[0].startsWith("http") ? product.images[0] : `http://localhost:8001${product.images[0]}`;
      }
      return "/static/default-product.png";
    },
    async addToCart(product) {
      if (product.stock_quantity <= 0) {
        common_vendor.index.showToast({
          title: "商品缺货",
          icon: "none"
        });
        return;
      }
      try {
        let cart = common_vendor.index.getStorageSync("cart") || [];
        const existingIndex = cart.findIndex((item) => item.id === product.id);
        if (existingIndex >= 0) {
          cart[existingIndex].quantity += 1;
          if (cart[existingIndex].quantity > product.stock_quantity) {
            cart[existingIndex].quantity = product.stock_quantity;
            common_vendor.index.showToast({
              title: "库存不足",
              icon: "none"
            });
            return;
          }
        } else {
          cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: this.getProductImage(product),
            quantity: 1,
            stock: product.stock_quantity
          });
        }
        common_vendor.index.setStorageSync("cart", cart);
        this.updateCartCount();
        common_vendor.index.showToast({
          title: "已加入购物车",
          icon: "success"
        });
      } catch (error) {
        console.error("添加购物车失败:", error);
        common_vendor.index.showToast({
          title: "添加失败",
          icon: "none"
        });
      }
    },
    updateCartCount() {
      const cart = common_vendor.index.getStorageSync("cart") || [];
      this.cartCount = cart.reduce((total, item) => total + item.quantity, 0);
    },
    goToProductDetail(productId) {
      common_vendor.index.navigateTo({
        url: `/pages/product-detail/product-detail?id=${productId}`
      });
    },
    goToCart() {
      common_vendor.index.switchTab({
        url: "/pages/cart/cart"
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.o((...args) => $options.handleSearch && $options.handleSearch(...args)),
    b: $data.searchQuery,
    c: common_vendor.o(($event) => $data.searchQuery = $event.detail.value),
    d: common_vendor.o((...args) => $options.handleSearch && $options.handleSearch(...args)),
    e: $data.selectedCategory === "" ? 1 : "",
    f: common_vendor.o(($event) => $options.selectCategory("")),
    g: common_vendor.f($data.categories, (category, k0, i0) => {
      return {
        a: common_vendor.t(category.zh),
        b: category.code,
        c: $data.selectedCategory === category.code ? 1 : "",
        d: common_vendor.o(($event) => $options.selectCategory(category.code), category.code)
      };
    }),
    h: common_vendor.f($data.products, (product, k0, i0) => {
      return common_vendor.e({
        a: $options.getProductImage(product),
        b: common_vendor.t(product.name),
        c: common_vendor.t(product.description),
        d: common_vendor.t(product.price),
        e: product.stock_quantity > 0
      }, product.stock_quantity > 0 ? {
        f: common_vendor.t(product.stock_quantity)
      } : {}, {
        g: product.stock_quantity <= 0 ? 1 : "",
        h: product.is_featured
      }, product.is_featured ? {} : {}, {
        i: product.is_common
      }, product.is_common ? {} : {}, {
        j: product.is_prescription_required
      }, product.is_prescription_required ? {} : {}, {
        k: product.stock_quantity > 0
      }, product.stock_quantity > 0 ? {} : {}, {
        l: common_vendor.o(($event) => $options.addToCart(product), product.id),
        m: product.stock_quantity <= 0,
        n: product.id,
        o: common_vendor.o(($event) => $options.goToProductDetail(product.id), product.id)
      });
    }),
    i: $data.loading
  }, $data.loading ? {} : {}, {
    j: !$data.hasMore && $data.products.length > 0
  }, !$data.hasMore && $data.products.length > 0 ? {} : {}, {
    k: !$data.loading && $data.products.length === 0
  }, !$data.loading && $data.products.length === 0 ? {} : {}, {
    l: common_vendor.o((...args) => $options.loadMore && $options.loadMore(...args)),
    m: $data.refreshing,
    n: common_vendor.o((...args) => $options.handleRefresh && $options.handleRefresh(...args)),
    o: $data.cartCount > 0
  }, $data.cartCount > 0 ? {
    p: common_vendor.t($data.cartCount),
    q: common_vendor.o((...args) => $options.goToCart && $options.goToCart(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-f7d9b51c"]]);
wx.createPage(MiniProgramPage);
