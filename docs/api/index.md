# 5. DÀNH CHO NHÀ PHÁT TRIỂN

Chào mừng đến với TwinExpert API Documentation! Phần này dành cho các nhà phát triển muốn tích hợp sức mạnh của Twin AI vào ứng dụng và hệ thống của riêng mình.

## Tổng quan API

TwinExpert API cho phép bạn:
- **Tạo và quản lý conversations** với các Twin AI chuyên gia
- **Upload và xử lý documents** (PDF, Word, Excel, etc.)
- **Quản lý projects và teams** programmatically  
- **Truy cập knowledge base** và context sharing
- **Tích hợp AI capabilities** vào workflow hiện có

## Bắt đầu nhanh

### 1. Đăng ký và lấy API Key
1. Đăng ký tài khoản tại [twinexpert.com](https://twinexpert.com)
2. Upgrade lên gói Professional hoặc cao hơn
3. Vào Dashboard → Settings → API Keys
4. Tạo API key mới cho ứng dụng của bạn

### 2. Authentication
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.twinexpert.com/v1/conversations
```

### 3. First API Call
```javascript
const response = await fetch('https://api.twinexpert.com/v1/conversations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "Xin chào, tôi cần hỗ trợ viết content marketing",
    twin_type: "content_marketing",
    project_id: "your_project_id"
  })
});
```

## Cấu trúc Documentation

### [5.1. Bắt đầu với API](./getting-started)
🚀 Setup ban đầu, authentication và first API call

### [5.2. Xác thực](./authentication) 
🔐 Chi tiết về API keys, security và rate limiting

### [5.3. API Endpoints](./endpoints)
📝 Danh sách đầy đủ các endpoints và parameters

### [5.4. Ví dụ](./examples)
💡 Code samples và use cases thực tế

### [5.5. Rate Limiting](./rate-limiting)
⚡ Giới hạn request và best practices

### [5.6. Xử lý lỗi](./error-handling)
🛠️ Error codes và cách handle exceptions

## Base URL và Versioning

- **Base URL**: `https://api.twinexpert.com`
- **Current Version**: `v1`
- **API Format**: REST JSON
- **WebSocket**: Available for real-time conversations

## Gói dịch vụ hỗ trợ API

| Gói | API Access | Rate Limit | Support |
|-----|------------|------------|---------|
| Free | ❌ | - | - |
| Creator | ❌ | - | - |
| Professional | ✅ | 1000 req/hour | Email |
| Business | ✅ | 5000 req/hour | Priority |
| Enterprise | ✅ | Custom | Dedicated |

## SDKs và Libraries

### Official SDKs
- **JavaScript/Node.js**: `npm install @twinexpert/sdk`
- **Python**: `pip install twinexpert-python`
- **PHP**: `composer require twinexpert/php-sdk`

### Community SDKs
- **Ruby**: `gem install twinexpert-ruby`
- **Go**: `go get github.com/twinexpert/go-sdk`

## Cần hỗ trợ?

- **API Documentation**: Phần này
- **Code Examples**: [GitHub Repository](https://github.com/twinexpert/examples)
- **Technical Support**: api-support@twinexpert.com
- **Discord Community**: [Join Developer Community](https://discord.gg/twinexpert)

---

**Lưu ý**: API hiện tại đang trong giai đoạn Beta. Một số tính năng có thể thay đổi trong tương lai. Hãy theo dõi changelog để cập nhật mới nhất.
