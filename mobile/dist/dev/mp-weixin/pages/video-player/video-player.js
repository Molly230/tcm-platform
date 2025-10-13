"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      videoId: "secureVideo",
      lessonId: 0,
      userId: "",
      videoUrl: "",
      accessToken: "",
      // 视频状态
      isLoading: true,
      isPlaying: false,
      isBlocked: false,
      currentTime: 0,
      duration: 0,
      // 界面状态
      showControls: true,
      controlsTimer: null,
      // 安全相关
      watermarkText: "",
      watermarkPosition: "top-right",
      watermarkTimer: null,
      heartbeatTimer: null,
      // 课程信息
      lessonInfo: {}
    };
  },
  computed: {
    progressPercent() {
      return this.duration > 0 ? this.currentTime / this.duration * 100 : 0;
    }
  },
  onLoad(options) {
    this.lessonId = parseInt(options.lessonId);
    this.userId = options.userId || "user_123";
    this.initializePlayer();
  },
  onUnload() {
    this.cleanup();
  },
  onHide() {
    this.pauseVideo();
    this.blockVideo("检测到页面切换");
  },
  onShow() {
    if (this.isBlocked) {
      this.resumeVideo();
    }
  },
  methods: {
    // 初始化播放器
    async initializePlayer() {
      var _a;
      try {
        const response = await common_vendor.index.request({
          url: `/api/video/lessons/${this.lessonId}/play-url`,
          method: "GET",
          data: {
            user_id: this.userId
          }
        });
        if (response.data) {
          const data = response.data;
          this.videoUrl = data.video_url;
          this.accessToken = data.access_token;
          this.watermarkText = ((_a = data.watermark_config) == null ? void 0 : _a.content) || "";
          this.lessonInfo = data.lesson_info || {};
          this.setupWatermark(data.watermark_config);
          this.startHeartbeat(data.security_config);
        }
      } catch (error) {
        console.error("初始化播放器失败:", error);
        common_vendor.index.showToast({ title: "视频加载失败", icon: "error" });
      } finally {
        this.isLoading = false;
      }
    },
    // 设置水印
    setupWatermark(config) {
      if (!config || !config.interval)
        return;
      this.watermarkTimer = setInterval(() => {
        const positions = ["top-left", "top-right", "bottom-left", "bottom-right"];
        this.watermarkPosition = positions[Math.floor(Math.random() * positions.length)];
      }, config.interval * 1e3);
    },
    // 开始心跳检测
    startHeartbeat(config) {
      if (!(config == null ? void 0 : config.heartbeat_interval))
        return;
      this.heartbeatTimer = setInterval(async () => {
        var _a;
        try {
          const response = await common_vendor.index.request({
            url: `/api/video/lessons/${this.lessonId}/heartbeat`,
            method: "POST",
            data: {
              user_id: this.userId,
              current_time: Math.floor(this.currentTime),
              token: this.accessToken
            }
          });
          if (!((_a = response.data) == null ? void 0 : _a.continue_play)) {
            this.blockVideo("会话已过期");
          }
        } catch (error) {
          console.error("心跳检测失败:", error);
        }
      }, config.heartbeat_interval * 1e3);
    },
    // 视频控制
    togglePlay() {
      if (this.isBlocked)
        return;
      if (this.isPlaying) {
        this.pauseVideo();
      } else {
        this.playVideo();
      }
    },
    playVideo() {
      if (this.isBlocked)
        return;
      const videoContext = common_vendor.index.createVideoContext(this.videoId, this);
      videoContext.play();
      this.isPlaying = true;
    },
    pauseVideo() {
      const videoContext = common_vendor.index.createVideoContext(this.videoId, this);
      videoContext.pause();
      this.isPlaying = false;
    },
    seekTo(event) {
      if (this.isBlocked || !this.duration)
        return;
      event.detail || event.target.getBoundingClientRect();
      const percent = 0.5;
      const newTime = percent * this.duration;
      const videoContext = common_vendor.index.createVideoContext(this.videoId, this);
      videoContext.seek(newTime);
      this.currentTime = newTime;
    },
    // 控制栏显示/隐藏
    toggleControls() {
      this.showControls = !this.showControls;
      if (this.showControls) {
        clearTimeout(this.controlsTimer);
        this.controlsTimer = setTimeout(() => {
          this.showControls = false;
        }, 3e3);
      }
    },
    // 阻止播放
    blockVideo(reason) {
      this.isBlocked = true;
      this.pauseVideo();
      common_vendor.index.showToast({
        title: `视频已暂停: ${reason}`,
        icon: "error",
        duration: 3e3
      });
      this.recordViolation(reason);
    },
    // 恢复播放
    resumeVideo() {
      this.isBlocked = false;
    },
    // 记录违规
    async recordViolation(reason) {
      try {
        await common_vendor.index.request({
          url: `/api/video/lessons/${this.lessonId}/violation`,
          method: "POST",
          data: {
            user_id: this.userId,
            reason,
            timestamp: Date.now()
          }
        });
      } catch (error) {
        console.error("记录违规失败:", error);
      }
    },
    // 视频事件处理
    onVideoLoaded(event) {
      this.duration = event.detail.duration;
      this.isLoading = false;
    },
    onTimeUpdate(event) {
      this.currentTime = event.detail.currentTime;
    },
    onVideoEnded() {
      this.isPlaying = false;
      this.markLessonCompleted();
    },
    onVideoError(event) {
      console.error("视频播放错误:", event);
      common_vendor.index.showToast({ title: "播放失败", icon: "error" });
    },
    // 标记完成
    async markLessonCompleted() {
      try {
        await common_vendor.index.request({
          url: `/api/video/lessons/${this.lessonId}/complete`,
          method: "POST",
          data: {
            user_id: this.userId,
            token: this.accessToken
          }
        });
        common_vendor.index.showToast({ title: "课程已完成", icon: "success" });
      } catch (error) {
        console.error("标记完成失败:", error);
      }
    },
    // 工具方法
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    },
    formatDuration(seconds) {
      const minutes = Math.floor(seconds / 60);
      return `${minutes}分${seconds % 60}秒`;
    },
    // 返回
    goBack() {
      common_vendor.index.navigateBack();
    },
    // 清理
    cleanup() {
      if (this.watermarkTimer)
        clearInterval(this.watermarkTimer);
      if (this.heartbeatTimer)
        clearInterval(this.heartbeatTimer);
      if (this.controlsTimer)
        clearTimeout(this.controlsTimer);
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.o((...args) => $options.goBack && $options.goBack(...args)),
    b: common_vendor.t($data.lessonInfo.title),
    c: !$data.isBlocked
  }, !$data.isBlocked ? common_vendor.e({
    d: $data.videoId,
    e: $data.videoUrl,
    f: common_vendor.o((...args) => $options.onVideoLoaded && $options.onVideoLoaded(...args)),
    g: common_vendor.o((...args) => $options.onTimeUpdate && $options.onTimeUpdate(...args)),
    h: common_vendor.o((...args) => $options.onVideoEnded && $options.onVideoEnded(...args)),
    i: common_vendor.o((...args) => $options.onVideoError && $options.onVideoError(...args)),
    j: $data.watermarkText
  }, $data.watermarkText ? {
    k: common_vendor.t($data.watermarkText),
    l: common_vendor.n($data.watermarkPosition)
  } : {}, {
    m: common_vendor.t($data.isPlaying ? "⏸️" : "▶️"),
    n: common_vendor.o((...args) => $options.togglePlay && $options.togglePlay(...args)),
    o: $options.progressPercent + "%",
    p: common_vendor.o((...args) => $options.seekTo && $options.seekTo(...args)),
    q: common_vendor.t($options.formatTime($data.currentTime)),
    r: common_vendor.t($options.formatTime($data.duration)),
    s: $data.showControls,
    t: common_vendor.o((...args) => $options.toggleControls && $options.toggleControls(...args))
  }) : {}, {
    v: $data.isBlocked
  }, $data.isBlocked ? {
    w: common_vendor.o((...args) => $options.resumeVideo && $options.resumeVideo(...args))
  } : {}, {
    x: $data.isLoading
  }, $data.isLoading ? {} : {}, {
    y: $data.lessonInfo.title
  }, $data.lessonInfo.title ? common_vendor.e({
    z: common_vendor.t($data.lessonInfo.title),
    A: $data.lessonInfo.description
  }, $data.lessonInfo.description ? {
    B: common_vendor.t($data.lessonInfo.description)
  } : {}, {
    C: common_vendor.t($data.lessonInfo.order),
    D: $data.lessonInfo.duration
  }, $data.lessonInfo.duration ? {
    E: common_vendor.t($options.formatDuration($data.lessonInfo.duration))
  } : {}) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
