import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Twin AI Docs',
  description: 'Hướng dẫn sử dụng Twin AI - Phân thân của chuyên gia',
  lang: 'vi-VN',
  srcDir: '.',
  srcExclude: ['**/_archive/**', '**/node_modules/**', '**/_temp/**'],
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['link', { rel: 'shortcut icon', href: '/favicon.ico' }],
    ['link', { rel: 'apple-touch-icon', href: '/logo.png' }],
    ['meta', { name: 'theme-color', content: '#346ddb' }]
  ],
  
  themeConfig: {
    logo: '/logo.png',
    siteTitle: 'Twin AI Docs',
    
    nav: [
      { text: 'Trang chủ', link: '/' },
      { text: 'Bắt đầu', link: '/welcome/' },
      { text: 'API Docs', link: '/api/' },
      { text: 'Hỗ trợ', link: '/support/' }
    ],

    sidebar: [
      {
        text: '👋 Welcome to Twin AI',
        collapsed: false,
        items: [
          { text: 'Chào mừng đến với Twin AI', link: '/welcome/' },
          { text: 'Twin AI hoạt động như thế nào?', link: '/welcome/how-it-works' },
          { text: 'Twin AI dành cho ai?', link: '/welcome/twin-ai-danh-cho-ai' },
          { text: 'Bắt đầu nhanh (Quickstart)', link: '/welcome/quickstart' },
          { text: 'Lộ trình phát triển (Roadmap)', link: '/welcome/roadmap' }
        ]
      },
      {
        text: '1. KHỞI TẠO VÀ QUẢN LÝ TÀI KHOẢN',
        collapsed: true,
        items: [
          { text: 'Tổng quan', link: '/account/' },
          { text: '1.1. Đăng ký và Đăng nhập', link: '/account/registration-login' },
          { text: '1.2. Thiết lập Hồ sơ cá nhân', link: '/account/profile-setup' }
        ]
      },
      {
        text: '2. GÓI DỊCH VỤ VÀ THANH TOÁN',
        collapsed: true,
        items: [
          { text: 'Tổng quan', link: '/goi-dich-vu-va-thanh-toan/' },
          { text: '2.1. Tổng quan các Gói dịch vụ', link: '/goi-dich-vu-va-thanh-toan/tong-quan-cac-goi-dich-vu' },
          { text: '2.2. Hướng dẫn Thanh toán', link: '/goi-dich-vu-va-thanh-toan/huong-dan-thanh-toan' }
        ]
      },
      {
        text: '3. NỀN TẢNG (THE BASICS)',
        collapsed: true,
        items: [
          { text: 'Tổng quan', link: '/basics/' },
          { text: '3.1. Không gian làm việc của bạn', link: '/basics/workspace' },
          { text: '3.2. Nghệ thuật Đối thoại cùng Twin AI', link: '/basics/conversation-art' },
          { text: '3.3. Quản lý công việc với "Projects"', link: '/basics/project-management' }
        ]
      },
      {
        text: '4. QUẢN LÝ TEAMS CỦA BẠN',
        collapsed: true,
        items: [
          { text: 'Tổng quan', link: '/teams/' },
          { text: '4.1. Quản lý Đội ngũ (Teams)', link: '/teams/team-management' },
          { text: '4.2. Cộng tác trong "Projects"', link: '/teams/project-collaboration' }
        ]
      },
      {
        text: '5. DÀNH CHO NHÀ PHÁT TRIỂN',
        collapsed: true,
        items: [
          { text: 'Tổng quan', link: '/api/' },
          { text: '5.1. Bắt đầu với API', link: '/api/getting-started' },
          { text: '5.2. Xác thực', link: '/api/authentication' },
          { text: '5.3. API Endpoints', link: '/api/endpoints' },
          { text: '5.4. Ví dụ', link: '/api/examples' },
          { text: '5.5. Rate Limiting', link: '/api/rate-limiting' },
          { text: '5.6. Xử lý lỗi', link: '/api/error-handling' }
        ]
      },
      {
        text: '6. TÀI NGUYÊN & HỖ TRỢ',
        collapsed: true,
        items: [
          { text: 'Tổng quan', link: '/support/' },
          { text: '6.1. Các câu hỏi thường gặp (FAQs)', link: '/support/faqs' },
          { text: '6.2. Các kênh hỗ trợ', link: '/support/support-channels' },
          { text: '6.3. Bảng thuật ngữ', link: '/support/glossary' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/twinai' }
    ],

    footer: {
      message: 'Được xây dựng với ❤️ bởi Twin AI Team',
      copyright: 'Copyright © 2025 Twin AI Solution, Inc.'
    },

    editLink: {
      pattern: 'https://github.com/twinai/docs/edit/main/docs/:path',
      text: 'Đề xuất chỉnh sửa'
    },

    search: {
      provider: 'local',
      options: {
        placeholder: 'Tìm kiếm tài liệu...',
        translations: {
          button: {
            buttonText: 'Tìm kiếm',
            buttonAriaLabel: 'Tìm kiếm tài liệu'
          },
          modal: {
            displayDetails: 'Hiển thị chi tiết',
            resetButtonTitle: 'Xóa tìm kiếm',
            backButtonTitle: 'Đóng tìm kiếm',
            noResultsText: 'Không tìm thấy kết quả cho',
            footer: {
              selectText: 'để chọn',
              navigateText: 'để điều hướng',
              closeText: 'để đóng'
            }
          }
        }
      }
    },

    outline: {
      label: 'Mục lục',
      level: [2, 3]
    },

    returnToTopLabel: 'Về đầu trang',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Chế độ tối',
    lightModeSwitchTitle: 'Chuyển sang chế độ sáng',
    darkModeSwitchTitle: 'Chuyển sang chế độ tối'
  }
})
