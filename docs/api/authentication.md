# 5.2. Xác thực

TwinExpert API sử dụng API Key authentication để bảo mật và kiểm soát truy cập. Mỗi request cần kèm theo API Key hợp lệ.

## 🔐 API Key Authentication

### Cách hoạt động

TwinExpert API sử dụng **Bearer Token** authentication với API Key của bạn:

```http
Authorization: Bearer YOUR_API_KEY
```

### Lấy API Key

1. **Đăng nhập** vào [TwinExpert Dashboard](https://twinexpert.com/dashboard)
2. **Vào Settings** → **API Keys**
3. **Click "Generate New Key"**
4. **Đặt tên** cho API Key (ví dụ: "Production App", "Testing")
5. **Copy và lưu** API Key an toàn

::: warning Quan trọng
- API Key chỉ hiển thị **một lần** khi tạo
- Lưu API Key ở nơi an toàn
- Không commit API Key vào code repository
:::

## 🛡️ Bảo mật API Key

### Sử dụng Environment Variables

**Node.js (.env file):**
```bash
# .env
TWIN_API_KEY=tk_live_abcd1234...
TWIN_BASE_URL=https://api.twinexpert.com/v1
```

```javascript
// app.js
require('dotenv').config();

const apiKey = process.env.TWIN_API_KEY;
const baseURL = process.env.TWIN_BASE_URL;
```

**Python (.env file):**
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TWIN_API_KEY')
BASE_URL = os.getenv('TWIN_BASE_URL')
```

**PHP (.env file):**
```php
// .env
TWIN_API_KEY=tk_live_abcd1234...

// config.php
$apiKey = $_ENV['TWIN_API_KEY'];
```

### Server-side Only

::: danger Cảnh báo bảo mật
**KHÔNG BAO GIỜ** expose API Key ở client-side:
- ❌ Frontend JavaScript
- ❌ Mobile app code
- ❌ Browser console
- ❌ Client-side config files

**Luôn luôn** gọi API từ server:
- ✅ Backend server
- ✅ Serverless functions
- ✅ API Gateway
- ✅ Server-side middleware
:::

## 📨 Cách sử dụng Authentication

### Basic Request Format

```http
GET /v1/experts HTTP/1.1
Host: api.twinexpert.com
Authorization: Bearer tk_live_abcd1234efgh5678...
Content-Type: application/json
```

### cURL Example

```bash
curl -X GET "https://api.twinexpert.com/v1/experts" \
  -H "Authorization: Bearer tk_live_abcd1234efgh5678..." \
  -H "Content-Type: application/json"
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const headers = {
  'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
  'Content-Type': 'application/json'
};

// GET request
const response = await axios.get('https://api.twinexpert.com/v1/experts', { headers });

// POST request
const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', {
  expert: 'marketing',
  message: 'Viết slogan cho sản phẩm'
}, { headers });
```

### Python

```python
import requests
import os

headers = {
    'Authorization': f'Bearer {os.getenv("TWIN_API_KEY")}',
    'Content-Type': 'application/json'
}

# GET request
response = requests.get('https://api.twinexpert.com/v1/experts', headers=headers)

# POST request
response = requests.post('https://api.twinexpert.com/v1/chat/completions', 
    json={
        'expert': 'marketing',
        'message': 'Viết slogan cho sản phẩm'
    },
    headers=headers
)
```

### PHP

```php
<?php
$headers = [
    'Authorization: Bearer ' . $_ENV['TWIN_API_KEY'],
    'Content-Type: application/json'
];

// GET request
$curl = curl_init();
curl_setopt_array($curl, [
    CURLOPT_URL => 'https://api.twinexpert.com/v1/experts',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => $headers
]);
$response = curl_exec($curl);

// POST request
curl_setopt_array($curl, [
    CURLOPT_URL => 'https://api.twinexpert.com/v1/chat/completions',
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode([
        'expert' => 'marketing',
        'message' => 'Viết slogan cho sản phẩm'
    ]),
    CURLOPT_HTTPHEADER => $headers
]);
$response = curl_exec($curl);
?>
```

## 🔄 Quản lý API Keys

### Kiểm tra API Key

Test API Key có hoạt động không:

```bash
curl -X GET "https://api.twinexpert.com/v1/auth/verify" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response thành công:**
```json
{
  "valid": true,
  "key_id": "tk_live_abcd1234",
  "account": {
    "id": "acc_xyz789",
    "name": "Công ty ABC",
    "plan": "pro"
  },
  "permissions": ["chat", "files", "projects"],
  "rate_limit": {
    "limit": 10000,
    "remaining": 9875,
    "reset_at": "2024-01-01T01:00:00Z"
  }
}
```

### Multiple API Keys

Bạn có thể tạo nhiều API Keys cho các mục đích khác nhau:

| Key Name | Permissions | Use Case |
|----------|-------------|----------|
| `Production` | Full access | Production app |
| `Staging` | Limited access | Testing environment |
| `Analytics` | Read-only | Monitoring & reporting |
| `Mobile App` | Chat only | Mobile application |

### Rotate API Keys

Thay đổi API Key định kỳ để bảo mật:

1. **Tạo API Key mới**
2. **Update ứng dụng** với key mới
3. **Test** hoạt động bình thường
4. **Revoke API Key cũ**

## ⚠️ Error Responses

### 401 Unauthorized

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or missing API key",
    "details": "The API key provided is either invalid, expired, or missing"
  }
}
```

**Nguyên nhân:**
- API Key không hợp lệ
- API Key đã hết hạn
- Thiếu header Authorization
- Sai format Bearer token

### 403 Forbidden

```json
{
  "error": {
    "code": "forbidden",
    "message": "Insufficient permissions",
    "details": "Your API key does not have permission to access this resource"
  }
}
```

**Nguyên nhân:**
- API Key không có quyền truy cập endpoint này
- Account bị suspended
- Vượt quá giới hạn plan

## 🛠️ Debugging Authentication

### Common Issues & Solutions

**1. "Invalid API Key" Error**
```bash
# Kiểm tra API key có đúng format không
echo $TWIN_API_KEY | wc -c  # Phải có độ dài đúng
echo $TWIN_API_KEY | grep "tk_"  # Phải bắt đầu với tk_
```

**2. "Missing Authorization Header" Error**
```javascript
// ❌ Sai
fetch('/api/chat', {
  headers: {
    'Content-Type': 'application/json'
    // Thiếu Authorization
  }
});

// ✅ Đúng
fetch('/api/chat', {
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }
});
```

**3. "CORS Error" (Client-side)**
```javascript
// ❌ Không được gọi API trực tiếp từ browser
const response = await fetch('https://api.twinexpert.com/v1/chat', {
  headers: { 'Authorization': 'Bearer ...' }
});

// ✅ Gọi qua backend server
const response = await fetch('/api/proxy/chat', {
  method: 'POST',
  body: JSON.stringify({ message: '...' })
});
```

## 📚 Best Practices

### 1. Environment-based Keys

```bash
# Development
TWIN_API_KEY=tk_test_dev123...

# Staging  
TWIN_API_KEY=tk_test_staging456...

# Production
TWIN_API_KEY=tk_live_prod789...
```

### 2. Centralized Auth Config

```javascript
// auth.js
class TwinAuth {
  constructor() {
    this.apiKey = process.env.TWIN_API_KEY;
    this.baseURL = process.env.TWIN_BASE_URL;
    
    if (!this.apiKey) {
      throw new Error('TWIN_API_KEY environment variable is required');
    }
  }
  
  getHeaders() {
    return {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    };
  }
}

module.exports = new TwinAuth();
```

### 3. Request Interceptor

```javascript
// axios-config.js
const axios = require('axios');

const twinAPI = axios.create({
  baseURL: 'https://api.twinexpert.com/v1',
  headers: {
    'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
    'Content-Type': 'application/json'
  }
});

// Auto retry on auth errors
twinAPI.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      console.error('Authentication failed. Check your API key.');
    }
    return Promise.reject(error);
  }
);

module.exports = twinAPI;
```

---

**Tiếp theo**: [API Endpoints →](./endpoints)

