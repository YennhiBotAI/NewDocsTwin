---
title: "Bắt đầu với API"
description: "Twin AI API - Bắt đầu với API"
---

# 5.1. Bắt đầu với API

Hướng dẫn nhanh để bắt đầu sử dụng TwinExpert API. Tích hợp AI twins vào ứng dụng của bạn với API RESTful mạnh mẽ và dễ sử dụng.

## Base URL

```
https://api.twinexpert.com/api/v1
```

Tất cả API endpoints đều sử dụng base URL trên.

## Bước 1: Tạo tài khoản

Đăng ký tài khoản miễn phí trên TwinExpert để bắt đầu sử dụng API.

[**Đăng ký ngay**](https://twinexpert.com/auth/register)

## Bước 2: Tạo API Key

Sau khi đăng ký thành công:

1. Vào dashboard của bạn
2. Tìm phần **"Cài đặt API"** 
3. Tạo API key mới trong phần quản lý API keys
4. Sao chép và lưu trữ API key an toàn

## Bước 3: Gọi API đầu tiên

Sử dụng API key để gọi endpoint đầu tiên và kiểm tra kết nối:

```bash
curl -X GET "https://api.twinexpert.com/api/v1/twins" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

## Bước 4: Tích hợp vào ứng dụng

Tích hợp API vào ứng dụng của bạn bằng cách sử dụng thư viện HTTP client phù hợp với ngôn ngữ lập trình của bạn.

### Ví dụ nhanh - JavaScript

```javascript
const response = await fetch('https://api.twinexpert.com/api/v1/twins', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});
const twins = await response.json();
console.log('Available twins:', twins.data);
```

## Tiếp theo

- [**Xem ví dụ chi tiết**](/api/examples) - Các ví dụ code thực tế
- [**API Reference**](/api/endpoints) - Danh sách đầy đủ các endpoints


---

::: tip Cần hỗ trợ?
Nếu bạn gặp vấn đề với API, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com).
:::
