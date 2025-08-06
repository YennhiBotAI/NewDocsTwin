# 5.3. API Endpoints

Tài liệu tham chiếu đầy đủ cho tất cả API endpoints của TwinExpert. Tất cả endpoints sử dụng base URL `https://api.twinexpert.com/v1`.

## 🔗 Base URL & Versioning

```
Base URL: https://api.twinexpert.com/v1
Authentication: Bearer Token (API Key)
Content-Type: application/json
```

## 👥 Experts - Quản lý chuyên gia AI

### GET `/experts`
Lấy danh sách tất cả chuyên gia AI có sẵn.

**Request:**
```bash
curl -X GET "https://api.twinexpert.com/v1/experts" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "experts": [
    {
      "id": "marketing",
      "name": "Marketing Expert",
      "description": "Chuyên gia marketing và branding",
      "capabilities": ["content_creation", "strategy", "analysis"],
      "languages": ["vi", "en"],
      "status": "active"
    },
    {
      "id": "copywriter", 
      "name": "Copywriter",
      "description": "Chuyên gia viết content chuyên nghiệp",
      "capabilities": ["email", "landing_page", "social_media"],
      "languages": ["vi", "en"],
      "status": "active"
    }
  ],
  "total": 10
}
```

### GET `/experts/{expert_id}`
Lấy thông tin chi tiết của một chuyên gia.

**Parameters:**
- `expert_id` (string, required): ID của chuyên gia

**Request:**
```bash
curl -X GET "https://api.twinexpert.com/v1/experts/marketing" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "id": "marketing",
  "name": "Marketing Expert",
  "description": "Chuyên gia marketing, branding và chiến lược quảng cáo",
  "avatar": "https://cdn.twinexpert.com/avatars/marketing.png",
  "capabilities": [
    "content_strategy",
    "brand_positioning", 
    "campaign_planning",
    "market_analysis",
    "competitor_research"
  ],
  "specialties": [
    "Digital Marketing",
    "Content Marketing", 
    "Social Media Strategy",
    "Brand Development"
  ],
  "languages": ["vi", "en"],
  "response_time": "1-3 seconds",
  "status": "active"
}
```

## 💬 Chat - Cuộc hội thoại

### POST `/chat/completions`
Gửi tin nhắn cho chuyên gia AI và nhận phản hồi.

**Request Body:**
```json
{
  "expert": "marketing",
  "message": "Viết một email marketing cho Black Friday",
  "context": {
    "brand": "Fashion Store",
    "target_audience": "Phụ nữ 25-35 tuổi",
    "tone": "friendly, urgent",
    "goal": "increase_sales"
  },
  "conversation_id": "conv_123456789", // Optional
  "stream": false // Optional, default false
}
```

**Response:**
```json
{
  "id": "msg_abcd1234",
  "expert": "marketing", 
  "conversation_id": "conv_123456789",
  "message": "Viết một email marketing cho Black Friday",
  "response": "🛍️ **FLASH SALE BLACK FRIDAY - Chỉ còn 24h!**\n\nChào bạn!\n\nBlack Friday đã đến! Đây là cơ hội VÀNG trong năm để sở hữu những món đồ yêu thích với mức giá không thể tin được.\n\n✨ **GIẢM ĐẾN 70%** toàn bộ bộ sưu tập\n🎁 **MIỄN PHÍ SHIP** đơn từ 500k\n⚡ **QUÀ TẶNG** đặc biệt cho 100 khách hàng đầu tiên\n\n**Nhanh tay click ngay** - Sale kết thúc sau:\n⏰ 23:59 hôm nay!\n\n[SHOP NGAY] [XEM SALE]\n\nYour Fashion Store Team 💕",
  "tokens_used": 156,
  "processing_time": 2.1,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### POST `/chat/completions` (Streaming)
Nhận phản hồi streaming (real-time).

**Request Body:**
```json
{
  "expert": "copywriter",
  "message": "Viết bài blog về benefits của meditation",
  "stream": true
}
```

**Response (Server-Sent Events):**
```
data: {"delta": "# Lợi ích tuyệt vời", "tokens": 4}

data: {"delta": " của meditation\n\n", "tokens": 7}

data: {"delta": "Meditation không chỉ", "tokens": 11}

data: {"delta": " là một phương pháp thư giãn...", "tokens": 18}

data: [DONE]
```

### GET `/conversations`
Lấy danh sách cuộc hội thoại của user.

**Query Parameters:**
- `limit` (integer, optional): Số lượng conversation trả về (default: 20, max: 100)
- `offset` (integer, optional): Offset cho pagination (default: 0)
- `expert` (string, optional): Filter theo chuyên gia

**Request:**
```bash
curl -X GET "https://api.twinexpert.com/v1/conversations?limit=10&expert=marketing" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv_123456789",
      "expert": "marketing",
      "title": "Email marketing campaign",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T12:30:00Z",
      "message_count": 8,
      "status": "active"
    }
  ],
  "total": 25,
  "has_more": true
}
```

### GET `/conversations/{conversation_id}`
Lấy chi tiết một cuộc hội thoại.

**Request:**
```bash
curl -X GET "https://api.twinexpert.com/v1/conversations/conv_123456789" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "id": "conv_123456789",
  "expert": "marketing",
  "title": "Email marketing campaign",
  "created_at": "2024-01-01T10:00:00Z",
  "messages": [
    {
      "id": "msg_001",
      "role": "user",
      "content": "Viết email marketing cho Black Friday",
      "timestamp": "2024-01-01T10:00:00Z"
    },
    {
      "id": "msg_002", 
      "role": "assistant",
      "content": "🛍️ **FLASH SALE BLACK FRIDAY...",
      "tokens_used": 156,
      "timestamp": "2024-01-01T10:00:03Z"
    }
  ],
  "total_messages": 8,
  "total_tokens": 1250
}
```

### DELETE `/conversations/{conversation_id}`
Xóa một cuộc hội thoại.

**Request:**
```bash
curl -X DELETE "https://api.twinexpert.com/v1/conversations/conv_123456789" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "deleted": true,
  "conversation_id": "conv_123456789"
}
```

## 📁 Files - Quản lý tài liệu

### POST `/files/upload`
Upload file để chuyên gia AI phân tích.

**Supported formats:** PDF, DOCX, TXT, CSV, XLSX

**Request (multipart/form-data):**
```bash
curl -X POST "https://api.twinexpert.com/v1/files/upload" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@document.pdf" \
  -F "purpose=analysis"
```

**Response:**
```json
{
  "id": "file_abc123",
  "filename": "document.pdf",
  "size": 1048576,
  "type": "application/pdf",
  "purpose": "analysis",
  "status": "uploaded",
  "upload_url": "https://cdn.twinexpert.com/files/file_abc123",
  "created_at": "2024-01-01T12:00:00Z"
}
```

### GET `/files`
Lấy danh sách files đã upload.

**Request:**
```bash
curl -X GET "https://api.twinexpert.com/v1/files" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "files": [
    {
      "id": "file_abc123",
      "filename": "marketing_plan.pdf",
      "size": 1048576,
      "type": "application/pdf",
      "status": "processed",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 15
}
```

### POST `/files/{file_id}/analyze`
Yêu cầu chuyên gia phân tích file.

**Request Body:**
```json
{
  "expert": "business_analyst",
  "instruction": "Tóm tắt nội dung chính và đưa ra đánh giá",
  "format": "summary" // Options: summary, detailed, bullet_points
}
```

**Response:**
```json
{
  "analysis_id": "analysis_xyz789",
  "file_id": "file_abc123",
  "expert": "business_analyst",
  "status": "processing", // processing, completed, failed
  "result": null, // Will contain analysis when completed
  "created_at": "2024-01-01T12:05:00Z"
}
```

### GET `/files/{file_id}/analysis/{analysis_id}`
Lấy kết quả phân tích file.

**Response:**
```json
{
  "analysis_id": "analysis_xyz789",
  "file_id": "file_abc123",
  "expert": "business_analyst",
  "status": "completed",
  "result": {
    "summary": "Tài liệu này là kế hoạch marketing Q1 2024...",
    "key_insights": [
      "Ngân sách marketing tăng 25% so với năm trước",
      "Focus chính vào digital channels",
      "Target audience mở rộng sang Gen Z"
    ],
    "recommendations": [
      "Nên tăng đầu tư vào TikTok marketing",
      "Cần tracking ROI chi tiết hơn",
      "Đề xuất A/B test cho landing pages"
    ]
  },
  "tokens_used": 450,
  "processing_time": 8.5,
  "created_at": "2024-01-01T12:05:00Z",
  "completed_at": "2024-01-01T12:05:08Z"
}
```

## 📊 Projects - Quản lý dự án

### GET `/projects`
Lấy danh sách projects.

**Response:**
```json
{
  "projects": [
    {
      "id": "proj_123",
      "name": "Website Redesign Campaign",
      "description": "Redesign website và marketing campaign",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z",
      "conversation_count": 15,
      "file_count": 8
    }
  ],
  "total": 5
}
```

### POST `/projects`
Tạo project mới.

**Request Body:**
```json
{
  "name": "Mobile App Launch",
  "description": "Marketing campaign cho việc launch mobile app",
  "experts": ["marketing", "copywriter", "social_media"]
}
```

### GET `/projects/{project_id}/conversations`
Lấy conversations trong project.

### GET `/projects/{project_id}/files`
Lấy files trong project.

## 👥 Teams - Quản lý team

### GET `/teams`
Lấy danh sách teams.

### POST `/teams`
Tạo team mới.

### GET `/teams/{team_id}/members`
Lấy danh sách thành viên.

### POST `/teams/{team_id}/members`
Thêm thành viên mới.

## 📈 Usage - Thống kê sử dụng

### GET `/usage`
Lấy thông tin usage hiện tại.

**Response:**
```json
{
  "current_period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "requests_made": 2847,
    "requests_limit": 10000,
    "tokens_used": 125000,
    "tokens_limit": 1000000
  },
  "today": {
    "requests": 156,
    "tokens": 8500
  },
  "plan": {
    "name": "Pro",
    "features": ["unlimited_experts", "file_upload", "team_collaboration"]
  }
}
```

## ⚠️ Error Responses

Tất cả endpoints đều có thể trả về các error codes sau:

### 400 Bad Request
```json
{
  "error": {
    "code": "bad_request",
    "message": "Invalid request parameters",
    "details": "The 'expert' field is required"
  }
}
```

### 401 Unauthorized
```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid API key"
  }
}
```

### 403 Forbidden
```json
{
  "error": {
    "code": "forbidden", 
    "message": "Insufficient permissions"
  }
}
```

### 404 Not Found
```json
{
  "error": {
    "code": "not_found",
    "message": "Resource not found"
  }
}
```

### 429 Too Many Requests
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

### 500 Internal Server Error
```json
{
  "error": {
    "code": "internal_server_error",
    "message": "Something went wrong on our end"
  }
}
```

## 🔄 Pagination

Các endpoints trả về danh sách hỗ trợ pagination:

**Query Parameters:**
- `limit`: Số items per page (default: 20, max: 100)
- `offset`: Số items bỏ qua (default: 0)

**Response format:**
```json
{
  "data": [...],
  "total": 250,
  "limit": 20,
  "offset": 40,
  "has_more": true
}
```

## 🚀 SDKs & Libraries

### JavaScript/Node.js
```bash
npm install @twinexpert/api
```

### Python
```bash
pip install twinexpert-api
```

### PHP
```bash
composer require twinexpert/api-php
```

---

**Tiếp theo**: [Examples →](./examples)

