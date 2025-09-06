// 替代 via.placeholder.com 的本地占位符函数
export function createPlaceholder(
  width: number = 300, 
  height: number = 200, 
  text: string = '图片', 
  bgColor: string = '#f0f0f0',
  textColor: string = '#666666'
): string {
  // 创建一个简单的 SVG 占位符
  const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="${bgColor}"/>
      <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="16" 
            fill="${textColor}" text-anchor="middle" dy="0.35em">${text}</text>
    </svg>
  `
  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

// 常用占位符
export const PLACEHOLDER_IMAGES = {
  avatar: createPlaceholder(100, 100, '头像', '#e8f4f8', '#666'),
  product: createPlaceholder(300, 200, '商品图片', '#f8f9fa', '#666'),
  course: createPlaceholder(300, 200, '课程封面', '#e8f4f8', '#666'),
  expert: createPlaceholder(100, 100, '专家', '#fff3e0', '#666'),
}