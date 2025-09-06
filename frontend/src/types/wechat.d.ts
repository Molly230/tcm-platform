// 微信JSSDK类型声明

interface WxAddressResult {
  userName: string
  telNumber: string
  provinceName: string
  cityName: string
  countryName: string
  detailInfo: string
  postalCode?: string
}

interface WxError {
  errMsg: string
  errCode?: number
}

interface Wx {
  chooseAddress(options: {
    success: (result: WxAddressResult) => void
    fail?: (error: WxError) => void
    cancel?: () => void
    complete?: () => void
  }): void
  
  config(options: {
    debug?: boolean
    appId: string
    timestamp: number
    nonceStr: string
    signature: string
    jsApiList: string[]
  }): void
  
  ready(callback: () => void): void
  error(callback: (error: WxError) => void): void
}

declare global {
  interface Window {
    wx?: Wx
  }
  
  const wx: Wx | undefined
}

export {}