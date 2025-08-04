# 5.3. API Endpoints

## Base URL
```
Production: https://api.twinexpert.ai/v1
Staging: https://staging-api.twinexpert.ai/v1
```

## Authentication
Tất cả endpoints yêu cầu authentication với API key trong header:
```
Authorization: Bearer te_live_sk_your_api_key_here
```

---

## Account Management

### GET /account
Lấy thông tin account hiện tại.

**Request:**
```http
GET /v1/account
Authorization: Bearer te_live_sk_...
```

**Response:**
```json
{
  "id": "acc_123abc",
  "email": "user@example.com",
  "plan": "pro",
  "usage": {
    "twins": 5,
    "max_twins": 10,
    "messages_this_month": 2500,
    "message_quota": 10000
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## Twin Management

### POST /twins
Tạo AI twin mới.

**Request:**
```http
POST /v1/twins
Authorization: Bearer te_live_sk_...
Content-Type: application/json

{
  "name": "Customer Support Bot",
  "personality": "helpful",
  "instructions": "You are a helpful customer support assistant.",
  "model": "gpt-4-turbo",
  "temperature": 0.7,
  "metadata": {
    "department": "support",
    "version": "1.0"
  }
}
```

**Response:**
```json
{
  "id": "twin_456def",
  "name": "Customer Support Bot",
  "personality": "helpful",
  "instructions": "You are a helpful customer support assistant.",
  "model": "gpt-4-turbo",
  "temperature": 0.7,
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "metadata": {
    "department": "support",
    "version": "1.0"
  }
}
```

### GET /twins
Lấy danh sách twins.

**Parameters:**
- `limit` (optional): Số lượng kết quả (mặc định: 20, tối đa: 100)
- `offset` (optional): Vị trí bắt đầu (mặc định: 0)
- `status` (optional): Filter theo status (`active`, `inactive`)

**Request:**
```http
GET /v1/twins?limit=10&status=active
Authorization: Bearer te_live_sk_...
```

**Response:**
```json
{
  "twins": [
    {
      "id": "twin_456def",
      "name": "Customer Support Bot",
      "personality": "helpful",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 5,
  "has_more": false
}
```

### GET /twins/{twin_id}
Lấy thông tin chi tiết của một twin.

**Request:**
```http
GET /v1/twins/twin_456def
Authorization: Bearer te_live_sk_...
```

### PUT /twins/{twin_id}
Cập nhật thông tin twin.

**Request:**
```http
PUT /v1/twins/twin_456def
Authorization: Bearer te_live_sk_...
Content-Type: application/json

{
  "name": "Updated Support Bot",
  "instructions": "Updated instructions here",
  "temperature": 0.8
}
```

### DELETE /twins/{twin_id}
Xóa twin.

**Request:**
```http
DELETE /v1/twins/twin_456def
Authorization: Bearer te_live_sk_...
```

**Response:**
```json
{
  "deleted": true,
  "id": "twin_456def"
}
```

---

## Chat/Conversation

### POST /twins/{twin_id}/chat
Gửi tin nhắn và nhận phản hồi từ twin.

**Request:**
```http
POST /v1/twins/twin_456def/chat
Authorization: Bearer te_live_sk_...
Content-Type: application/json

{
  "message": "Xin chào, tôi cần hỗ trợ về sản phẩm",
  "conversation_id": "conv_789ghi", // optional
  "stream": false,
  "max_tokens": 150,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "id": "msg_abc123",
  "conversation_id": "conv_789ghi",
  "message": "Xin chào! Tôi sẵn sàng hỗ trợ bạn về sản phẩm. Bạn cần hỗ trợ gì cụ thể?",
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 32,
    "total_tokens": 57
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

### POST /twins/{twin_id}/chat (Streaming)
Chat với streaming response.

**Request:**
```http
POST /v1/twins/twin_456def/chat
Authorization: Bearer te_live_sk_...
Content-Type: application/json

{
  "message": "Explain quantum computing",
  "stream": true
}
```

**Response (Server-Sent Events):**
```
data: {"delta": {"content": "Quantum"}}

data: {"delta": {"content": " computing"}}

data: {"delta": {"content": " is"}}

data: {"delta": {"content": "..."}}

data: [DONE]
```

---

## Knowledge Base

### POST /twins/{twin_id}/knowledge
Upload tài liệu vào knowledge base của twin.

**Request (File Upload):**
```http
POST /v1/twins/twin_456def/knowledge
Authorization: Bearer te_live_sk_...
Content-Type: multipart/form-data

file: document.pdf
metadata: {"category": "product_docs", "version": "2.1"}
```

**Request (Text Content):**
```http
POST /v1/twins/twin_456def/knowledge
Authorization: Bearer te_live_sk_...
Content-Type: application/json

{
  "content": "This is important information about our product...",
  "title": "Product Information",
  "metadata": {
    "category": "product_docs",
    "version": "2.1"
  }
}
```

**Response:**
```json
{
  "id": "kb_item_123",
  "title": "Product Information", 
  "status": "processing",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET /twins/{twin_id}/knowledge
Lấy danh sách knowledge base items.

**Request:**
```http
GET /v1/twins/twin_456def/knowledge
Authorization: Bearer te_live_sk_...
```

---

## Conversations

### GET /conversations
Lấy danh sách conversations.

**Request:**
```http
GET /v1/conversations?twin_id=twin_456def&limit=20
Authorization: Bearer te_live_sk_...
```

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv_789ghi",
      "twin_id": "twin_456def",
      "title": "Product Support Request",
      "message_count": 5,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T01:00:00Z"
    }
  ],
  "total": 25,
  "has_more": true
}
```

### GET /conversations/{conversation_id}/messages
Lấy messages trong conversation.

**Request:**
```http
GET /v1/conversations/conv_789ghi/messages
Authorization: Bearer te_live_sk_...
```

---

## Error Responses

Tất cả error responses có format:

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "missing_parameter", 
    "message": "Missing required parameter: 'message'",
    "param": "message"
  }
}
```

### Error Codes

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 400 | `invalid_request_error` | Request không hợp lệ |
| 401 | `authentication_error` | API key không hợp lệ |
| 403 | `permission_error` | Không có quyền truy cập |
| 404 | `not_found_error` | Resource không tồn tại |
| 429 | `rate_limit_error` | Vượt quá rate limit |
| 500 | `api_error` | Lỗi server internal |

---

## Rate Limits

| Endpoint | Rate Limit |
|----------|------------|
| POST /twins/*/chat | 60 requests/minute |
| POST /twins | 10 requests/minute |
| GET endpoints | 300 requests/minute |
| File uploads | 5 requests/minute |

Rate limit headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59  
X-RateLimit-Reset: 1640995200
```

---

## SDK Examples

### JavaScript
```javascript
// Tạo twin
const twin = await client.twins.create({
  name: "My Assistant",
  instructions: "Be helpful and concise"
});

// Chat
const response = await client.twins.chat({
  twinId: twin.id,
  message: "Hello!"
});

// Upload knowledge
await client.twins.knowledge.upload({
  twinId: twin.id,
  file: fs.createReadStream('document.pdf')
});
```

### Python
```python
# Tạo twin
twin = client.twins.create(
    name="My Assistant",
    instructions="Be helpful and concise"
)

# Chat  
response = client.twins.chat(
    twin_id=twin.id,
    message="Hello!"
)

# Upload knowledge
with open('document.pdf', 'rb') as f:
    client.twins.knowledge.upload(
        twin_id=twin.id,
        file=f
    )
```

---

**Xem thêm:**
- 💡 [Examples](./examples) - Ví dụ thực tế với code
- ⚡ [Rate Limiting](./rate-limiting) - Chi tiết về limits
- 🚨 [Error Handling](./error-handling) - Xử lý errors

*API documentation đầy đủ có thể xem tại [Swagger UI](https://api.twinexpert.ai/docs)*