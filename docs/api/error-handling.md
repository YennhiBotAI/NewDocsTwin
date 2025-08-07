---
title: "Xử lý lỗi"
description: "Twin AI API - Xử lý lỗi"
---

# 5.6. Xử lý lỗi

Hiểu các mã lỗi và cách xử lý chúng một cách hiệu quả.

## Định dạng lỗi

Tất cả lỗi API đều trả về theo format chuẩn:

```json
{
  "success": false,
  "message": "Mô tả lỗi cho người dùng",
  "error": "ERROR_CODE",
  "statusCode": 400,
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_abc123"
  },
  "details": {
    // Thông tin chi tiết lỗi (nếu có)
  }
}
```

## Mã lỗi phổ biến

### 400 Bad Request
- **MISSING_REQUIRED_FIELD**: Thiếu trường bắt buộc
- **INVALID_FORMAT**: Định dạng dữ liệu không hợp lệ
- **INVALID_PARAMETER**: Tham số không hợp lệ

### 401 Unauthorized
- **INVALID_API_KEY**: API key không hợp lệ
- **EXPIRED_API_KEY**: API key đã hết hạn
- **MISSING_AUTHORIZATION**: Thiếu header Authorization

### 403 Forbidden
- **FORBIDDEN_ACCESS**: Không có quyền truy cập resource
- **INSUFFICIENT_PERMISSIONS**: Quyền không đủ để thực hiện action
- **ACCOUNT_SUSPENDED**: Tài khoản bị tạm khóa

### 404 Not Found
- **CONVERSATION_NOT_FOUND**: Không tìm thấy cuộc trò chuyện
- **TWIN_NOT_FOUND**: Không tìm thấy twin
- **MESSAGE_NOT_FOUND**: Không tìm thấy tin nhắn

### 429 Too Many Requests
- **RATE_LIMIT_EXCEEDED**: Vượt quá giới hạn tần suất gọi API
- **QUOTA_EXCEEDED**: Vượt quá quota sử dụng

### 500 Internal Server Error
- **INTERNAL_SERVER_ERROR**: Lỗi server nội bộ
- **SERVICE_UNAVAILABLE**: Dịch vụ tạm thời không khả dụng
- **DATABASE_ERROR**: Lỗi cơ sở dữ liệu

---

::: tip Debug Tips
Luôn lưu `requestId` từ error response để có thể trace và debug với support team.
:::

::: tip Cần hỗ trợ?
Nếu bạn gặp lỗi không mong muốn, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com) kèm theo `requestId`.
:::
