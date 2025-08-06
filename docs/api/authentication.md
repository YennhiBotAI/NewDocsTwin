---
title: "Xác thực"
description: "Twin AI API - Xác thực"
---

# 5.2. Xác thực

TwinExpert API sử dụng API key để xác thực requests.

## Bảo mật API Key

::: warning Quan trọng
API key của bạn có quyền truy cập vào dữ liệu. Hãy giữ bí mật và không chia sẻ trong code phía client.
:::

## Cách sử dụng API Key

Thêm API key vào header Authorization của mọi request:

### Authorization Header (Khuyến nghị)

```http
Authorization: Bearer YOUR_API_KEY
```

### Hoặc sử dụng X-API-Key header

```http
X-API-Key: YOUR_API_KEY
```

## Tạo API Key mới

### POST `/api/v1/auth/api-keys`

Tạo API key mới bằng JWT token.

### Ví dụ code

::: code-group

```javascript [JavaScript]
// Tạo API key mới
const response = await fetch('https://api.twinexpert.com/api/v1/auth/api-keys', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'My App',
    scope: 'full_access'
  })
});

const data = await response.json();
console.log('API Key:', data.data.key);
```

```bash [cURL]
# Tạo API key mới
curl -X POST "https://api.twinexpert.com/api/v1/auth/api-keys" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My App",
    "scope": "full_access"
  }'
```

```python [Python]
import requests

# Tạo API key mới
headers = {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
}

data = {
    'name': 'My App',
    'scope': 'full_access'
}

response = requests.post(
    'https://api.twinexpert.com/api/v1/auth/api-keys',
    headers=headers,
    json=data
)

api_key = response.json()['data']['key']
print(f'API Key: {api_key}')
```

:::

## Phạm vi quyền (Scopes)

| Scope | Mô tả | Giới hạn |
|-------|-------|----------|
| **read_only** | Chỉ đọc | 200 requests/giờ |
| | • Xem danh sách Twins | |
| | • Đọc thông tin cuộc trò chuyện | |
| | • Xem lịch sử tin nhắn | |
| **full_access** | Toàn quyền | 500 requests/giờ |
| | • Tất cả quyền của read_only | |
| | • Tạo cuộc trò chuyện mới | |
| | • Gửi tin nhắn | |

---

::: tip Cần hỗ trợ?
Nếu bạn gặp vấn đề với API, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com).
:::