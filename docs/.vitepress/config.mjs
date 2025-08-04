import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Twin AI Documentation',
  description: 'Tài liệu hướng dẫn sử dụng Twin AI - Nền tảng AI thông minh',
  base: '/docs/',
  ignoreDeadLinks: true,
  
  head: [
    ['link', { rel: 'icon', href: '/docs/favicon.ico' }]
  ],

  themeConfig: {
    logo: '/logo.svg',
    
    nav: [
      { text: 'Trang chủ', link: '/' },
      { text: 'Bắt đầu nhanh', link: '/quickstart' },
      { text: 'Hướng dẫn', link: '/guides/' },
      { text: 'API', link: '/api/' },
      { text: 'Hỗ trợ', link: '/support/' }
    ],

    sidebar: {
      '/': [
        {
          text: 'Bắt đầu',
          collapsed: false,
          items: [
            { text: 'Chào mừng đến với Twin AI', link: '/' },
            { text: 'Bắt đầu nhanh', link: '/quickstart' },
            { text: 'Twin AI dành cho ai?', link: '/who-is-twin-ai-for' },
            { text: 'Twin AI hoạt động như thế nào?', link: '/how-twin-ai-works' }
          ]
        },
        {
          text: '1. Khởi tạo và Quản lý Tài khoản',
          collapsed: false,
          items: [
            { text: '1.1. Đăng ký và Đăng nhập', link: '/account/signup-signin' },
            { text: '1.2. Thiết lập Hồ sơ cá nhân', link: '/account/profile-setup' }
          ]
        },
        {
          text: '2. Gói Dịch vụ và Thanh toán',
          collapsed: false,
          items: [
            { text: '2.1. Tổng quan các Gói dịch vụ', link: '/pricing/service-packages' },
            { text: '2.2. Hướng dẫn Thanh toán', link: '/pricing/payment-guide' }
          ]
        },
        {
          text: '3. Nền tảng (The Basics)',
          collapsed: false,
          items: [
            { text: '3.1. Không gian làm việc của bạn', link: '/basics/workspace' },
            { text: '3.2. Nghệ thuật Đối thoại cùng Twin AI', link: '/basics/conversation-art' },
            { text: '3.3. Quản lý công việc với Projects', link: '/basics/project-management' }
          ]
        },
        {
          text: "4. Quản lý Teams",
          collapsed: false,
          items: [
            { text: "Tổng quan Teams", link: "/teams/" },
            { text: "4.1. Quản lý Đội ngũ", link: "/teams/team-management" },
            { text: "4.2. Cộng tác trong Projects", link: "/teams/project-collaboration" }
          ]
        },
        {
          text: '5. Dành cho Nhà phát triển',
          collapsed: false,
          items: [
            { text: '5.1. Bắt đầu với API', link: '/api/getting-started' },
            { text: '5.2. Xác thực', link: '/api/authentication' },
            { text: '5.3. API Endpoints', link: '/api/endpoints' },
            { text: '5.4. Ví dụ', link: '/api/examples' },
            { text: '5.5. Rate Limiting', link: '/api/rate-limiting' },
            { text: '5.6. Xử lý lỗi', link: '/api/error-handling' }
          ]
        },
        {
          text: '6. Tài nguyên & Hỗ trợ',
          collapsed: false,
          items: [
            { text: '6.1. Các câu hỏi thường gặp (FAQs)', link: '/support/faqs' },
            { text: '6.2. Các kênh hỗ trợ', link: '/support/channels' },
            { text: '6.3. Bảng thuật ngữ', link: '/support/glossary' }
          ]
        },
        {
          text: 'Lộ trình phát triển',
          collapsed: true,
          items: [
            { text: 'Roadmap', link: '/roadmap' },
            { text: 'Phần 1: Dành cho người mới bắt đầu', link: '/guides/beginners' },
            { text: 'Phần 2: Tìm hiểu về các Gói và Tính năng', link: '/guides/packages-features' },
            { text: 'Phần 3: Dành cho người dùng chuyên sâu', link: '/guides/advanced-users' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/twin-ai' }
    ],

    footer: {
      message: 'Tài liệu Twin AI - Nền tảng AI thông minh',
      copyright: 'Copyright © 2024 Twin AI. All rights reserved.'
    },

    search: {
      provider: 'local'
    },

    editLink: {
      pattern: 'https://github.com/twin-ai/docs/edit/main/docs/:path',
      text: 'Chỉnh sửa trang này trên GitHub'
    },

    lastUpdated: {
      text: 'Cập nhật lần cuối',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium'
      }
    }
  },

  markdown: {
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    },
    lineNumbers: true
  }
})
