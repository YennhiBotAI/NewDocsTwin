# 5.3. API Endpoints

Danh sách đầy đủ các endpoints có sẵn

## 📋 Twins API

### GET `/api/v1/twins` 
<span class="scope-badge">🔸 Chỉ đọc</span>

Lấy danh sách tất cả twins

**Parameters:**
- `page` (integer) - Số trang (1-based)
- `limit` (integer) - Số items mỗi trang (max 100)

---

### GET `/api/v1/twins/{id}` 
<span class="scope-badge">🔸 Chỉ đọc</span>

Lấy thông tin chi tiết twin theo ID

**Parameters:**
- `id` (string, required) - ID của twin

---

### POST `/api/v1/twins/{id}` 
<span class="scope-badge">🔷 Toàn quyền</span>

Tạo cuộc trò chuyện mới với twin

**Parameters:**
- `id` (string, required) - ID của twin  
- `title` (string) - Tiêu đề cuộc trò chuyện

---

## 💬 Conversations API

### GET `/api/v1/conversations` 
<span class="scope-badge">🔸 Chỉ đọc</span>

Lấy danh sách cuộc trò chuyện

**Parameters:**
- `page` (integer) - Số trang
- `limit` (integer) - Số items mỗi trang
- `twinId` (string) - Lọc theo twin ID

---

### POST `/api/v1/conversations/{id}/messages` 
<span class="scope-badge">🔷 Toàn quyền</span>

Gửi tin nhắn vào cuộc trò chuyện

**Parameters:**
- `id` (string, required) - ID cuộc trò chuyện
- `content` (string, required) - Nội dung tin nhắn

---

### POST `/api/v1/conversations/{id}/messages/stream` 
<span class="scope-badge">🔷 Toàn quyền</span>

Gửi tin nhắn với streaming response

**Parameters:**
- `id` (string, required) - ID cuộc trò chuyện
- `content` (string, required) - Nội dung tin nhắn

---

## 📊 Response Format

Tất cả responses đều có format:

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Success"
}
```

## 🔧 Rate Limiting

| Scope | Limit |
|-------|--------|
| `read_only` | 100 requests/giờ |
| `full_access` | 500 requests/giờ |

---

📚 **Tiếp theo:** [5.4. Ví dụ](/api-examples) | [📖 Swagger Docs](https://api.twinexpert.com/api/v1/docs)
