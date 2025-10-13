"use strict";
const common_vendor = require("../common/vendor.js");
const BASE_URL = "http://localhost:8001";
function apiRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const token = common_vendor.index.getStorageSync("token");
    const header = {
      "Content-Type": "application/json",
      ...options.header
    };
    if (token) {
      header["Authorization"] = `Bearer ${token}`;
    }
    common_vendor.index.request({
      url: BASE_URL + url,
      method: options.method || "GET",
      data: options.data,
      header,
      success: (res) => {
        var _a;
        console.log("API Response:", res);
        if (res.statusCode === 200) {
          resolve(res.data);
        } else if (res.statusCode === 401) {
          common_vendor.index.removeStorageSync("token");
          common_vendor.index.removeStorageSync("user");
          common_vendor.index.showModal({
            title: "登录过期",
            content: "请重新登录",
            showCancel: false,
            success: () => {
              common_vendor.index.navigateTo({
                url: "/pages/login/login"
              });
            }
          });
          reject(new Error("登录过期"));
        } else {
          reject(new Error(((_a = res.data) == null ? void 0 : _a.detail) || `请求失败 ${res.statusCode}`));
        }
      },
      fail: (error) => {
        console.error("API Error:", error);
        reject(new Error("网络请求失败"));
      }
    });
  });
}
function getCurrentUser() {
  return common_vendor.index.getStorageSync("user");
}
function isLoggedIn() {
  const token = common_vendor.index.getStorageSync("token");
  const user = common_vendor.index.getStorageSync("user");
  return !!(token && user);
}
function logout() {
  common_vendor.index.removeStorageSync("token");
  common_vendor.index.removeStorageSync("user");
  common_vendor.index.removeStorageSync("cart");
  common_vendor.index.showToast({
    title: "已退出登录",
    icon: "success"
  });
  setTimeout(() => {
    common_vendor.index.switchTab({
      url: "/pages/index/index"
    });
  }, 1500);
}
exports.apiRequest = apiRequest;
exports.getCurrentUser = getCurrentUser;
exports.isLoggedIn = isLoggedIn;
exports.logout = logout;
