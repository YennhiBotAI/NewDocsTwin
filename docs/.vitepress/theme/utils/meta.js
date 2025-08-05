// docs/.vitepress/theme/utils/meta.js

export function createSEOMeta(page) {
  const baseUrl = 'https://your-domain.com' // Thay bằng domain thực tế
  const defaultImage = '/docs/og-image.png'
  
  // Tạo title và description động dựa trên trang
  const pageConfig = {
    '/': {
      title: 'Twin AI Documentation - Nền tảng AI thông minh',
      description: 'Tài liệu hướng dẫn sử dụng Twin AI - Nền tảng AI thông minh cho mọi người',
      image: defaultImage
    },
    '/quickstart': {
      title: 'Bắt đầu nhanh với Twin AI',
      description: 'Hướng dẫn bắt đầu nhanh sử dụng Twin AI trong 5 phút',
      image: defaultImage
    },
    '/account/': {
      title: 'Quản lý Tài khoản Twin AI',
      description: 'Hướng dẫn đăng ký, đăng nhập và thiết lập tài khoản Twin AI',
      image: defaultImage
    },
    '/api/': {
      title: 'Twin AI API Documentation',
      description: 'Tài liệu API đầy đủ cho nhà phát triển sử dụng Twin AI',
      image: defaultImage
    }
  }
  
  const config = pageConfig[page] || pageConfig['/']
  
  return [
    ['meta', { property: 'og:title', content: config.title }],
    ['meta', { property: 'og:description', content: config.description }],
    ['meta', { property: 'og:image', content: `${baseUrl}${config.image}` }],
    ['meta', { property: 'og:url', content: `${baseUrl}${page}` }],
    ['meta', { name: 'twitter:title', content: config.title }],
    ['meta', { name: 'twitter:description', content: config.description }],
    ['meta', { name: 'twitter:image', content: `${baseUrl}${config.image}` }]
  ]
}
