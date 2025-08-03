# Twin AI Documentation

Đây là source code cho trang tài liệu chính thức của Twin AI, được xây dựng bằng VitePress với thiết kế tương tự GitBook.

## 🚀 Bắt đầu nhanh

### Yêu cầu hệ thống
- Node.js 18+
- npm hoặc yarn

### Cài đặt và chạy local

```bash
# Clone repository
git clone https://github.com/twin-ai/docs.git
cd docs

# Cài đặt dependencies
npm install

# Chạy development server
npm run docs:dev

# Build cho production
npm run docs:build

# Preview build
npm run docs:preview
```

## 📁 Cấu trúc thư mục

```
├── docs/
│   ├── .vitepress/
│   │   ├── config.mjs          # Cấu hình VitePress
│   │   └── theme/
│   │       ├── index.js        # Custom theme
│   │       └── custom.css      # GitBook-like styling
│   ├── account/                # Tài liệu quản lý tài khoản
│   ├── pricing/                # Thông tin gói dịch vụ
│   ├── basics/                 # Hướng dẫn cơ bản
│   ├── teams/                  # Quản lý teams
│   ├── api/                    # API documentation
│   ├── support/                # Hỗ trợ & FAQ
│   ├── public/                 # Static assets
│   └── index.md                # Trang chủ
├── .github/workflows/          # GitHub Actions
└── vercel.json                 # Vercel deployment config
```

## 🎨 Thiết kế và Theme

Trang tài liệu được thiết kế để giống với GitBook với:

- ✅ **Layout tương tự GitBook**: Sidebar, navigation, content area
- ✅ **Color scheme nhất quán**: Brand colors của Twin AI
- ✅ **Typography tối ưu**: Dễ đọc trên mọi thiết bị
- ✅ **Responsive design**: Hoạt động tốt trên mobile/tablet
- ✅ **Dark mode**: Hỗ trợ chế độ tối
- ✅ **Search functionality**: Tìm kiếm nội dung tích hợp
- ✅ **Custom components**: Callouts, cards, buttons

## 📝 Viết nội dung

### Markdown basics

Tất cả nội dung được viết bằng Markdown với một số extension:

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
`Inline code`

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2
```

### Custom components

#### Callout blocks
```markdown
::: tip Mẹo
Đây là một mẹo hữu ích
:::

::: warning Cảnh báo
Hãy chú ý điều này
:::

::: danger Nguy hiểm
Thao tác này có thể gây lỗi
:::
```

#### Code blocks với syntax highlighting
```markdown
```javascript
const hello = () => {
  console.log('Hello Twin AI!')
}
```
```

### Assets và hình ảnh

```markdown
![Alt text](/images/screenshot.png)

# Hoặc với title
![Alt text](/images/screenshot.png "Image title")
```

## 🚀 Deployment

### Automatic deployment (Vercel)

Mỗi khi push code lên `main` branch, GitHub Actions sẽ tự động:

1. Build VitePress site
2. Deploy lên Vercel
3. Update domain tại `docs.twinexxpert.com`

### Manual deployment

```bash
# Build site
npm run docs:build

# Deploy using Vercel CLI
npx vercel --prod
```

## 🔧 Cấu hình

### VitePress config (`docs/.vitepress/config.mjs`)

```javascript
export default defineConfig({
  title: 'Twin AI Documentation',
  description: 'Tài liệu hướng dẫn sử dụng Twin AI',
  base: '/docs/',
  
  themeConfig: {
    // Navigation, sidebar, etc.
  }
})
```

### Custom styling (`docs/.vitepress/theme/custom.css`)

Tất cả custom CSS để tạo giao diện giống GitBook.

## 📦 Scripts

- `npm run docs:dev` - Start development server
- `npm run docs:build` - Build for production
- `npm run docs:preview` - Preview production build

## 🤝 Đóng góp

### Quy trình đóng góp

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/new-content`
3. Commit changes: `git commit -am 'Add new content'`
4. Push to branch: `git push origin feature/new-content`
5. Tạo Pull Request

### Quy tắc viết

- ✅ Sử dụng tiếng Việt cho nội dung chính
- ✅ Sử dụng tiếng Anh cho technical terms khi cần thiết
- ✅ Viết rõ ràng, súc tích
- ✅ Sử dụng headings để tổ chức nội dung
- ✅ Thêm examples và screenshots khi có thể
- ✅ Test links và images trước khi commit

### Content style guide

#### Headings
```markdown
# Page Title (H1 - một lần duy nhất)
## Main Sections (H2)
### Sub-sections (H3)
#### Details (H4)
```

#### Voice and tone
- **Friendly**: Sử dụng ngôn ngữ thân thiện
- **Clear**: Rõ ràng, dễ hiểu
- **Helpful**: Tập trung vào việc giúp đỡ user
- **Consistent**: Nhất quán trong cách diễn đạt

## 🐛 Báo lỗi

Nếu bạn tìm thấy lỗi trong tài liệu:

1. Kiểm tra [Issues](https://github.com/twin-ai/docs/issues) hiện có
2. Nếu chưa có, tạo issue mới với:
   - Mô tả rõ lỗi
   - URL trang bị lỗi
   - Screenshots nếu có
   - Cách tái tạo lỗi

## 📞 Liên hệ

- **Email**: docs@twinexxpert.com
- **Slack**: #docs-team
- **GitHub**: [twin-ai/docs](https://github.com/twin-ai/docs)

## 📄 License

Tài liệu này được phát hành dưới [MIT License](LICENSE).

---

**Được xây dựng với ❤️ bởi Twin AI Team**
