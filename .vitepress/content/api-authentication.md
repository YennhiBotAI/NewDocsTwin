# 5.2. Xác thực

TwinExpert API sử dụng API key để xác thực requests

## 🔐 Bảo mật API Key

> **⚠️ Lưu ý quan trọng**
> 
> API key của bạn có quyền truy cập vào dữ liệu. Hãy giữ bí mật và không chia sẻ trong code phía client.

## Cách sử dụng API Key

Thêm API key vào header Authorization của mọi request:

### Authorization Header

```http
Authorization: Bearer YOUR_API_KEY
```

**Hoặc sử dụng X-API-Key header**

```http
X-API-Key: YOUR_API_KEY
```

## Ví dụ code

Tạo API key mới bằng JWT token

<div role="tablist" class="tabs">

### JavaScript

```javascript
// Tạo API key mới
const response = await fetch('https://api.twinexpert.com/api/v1/auth/api-keys', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'My API Key',
    scope: 'read_only'
  })
});

const data = await response.json();
console.log('API Key:', data.data.key);
```

### cURL

```bash
# Tạo API key mới
curl -X POST "https://api.twinexpert.com/api/v1/auth/api-keys" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My API Key",
    "scope": "read_only"
  }'
```

### Python

```python
import requests

# Tạo API key mới
headers = {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
}

data = {
    'name': 'My API Key',
    'scope': 'read_only'
}

response = requests.post(
    'https://api.twinexpert.com/api/v1/auth/api-keys',
    headers=headers,
    json=data
)

api_key = response.json()['data']['key']
print(f'API Key: {api_key}')
```

</div>

## Phạm vi quyền (Scopes)

<div class="scope-grid">

### 📖 Chỉ Đọc (`read_only`)

**Quyền bao gồm:**
- Xem danh sách Twins
- Đọc thông tin cuộc trò chuyện
- Truy cập lịch sử chat
- **100 requests/giờ**

### ⚡ Toàn quyền (`full_access`)

**Quyền bao gồm:**
- Tất cả quyền của Read_only
- Tạo cuộc trò chuyện mới
- Gửi tin nhắn
- **500 requests/giờ**

</div>

---

📚 **Tiếp theo:** [5.3. API Endpoints](/api-endpoints) | [📖 Tài liệu API đầy đủ](https://api.twinexpert.com/api/v1/docs)
