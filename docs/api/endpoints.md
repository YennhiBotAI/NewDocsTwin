---
title: "API Endpoints"
description: "Twin AI API - API Endpoints"
---

# 5.3. API Endpoints

Danh sách đầy đủ các endpoints có sẵn trong TwinExpert API.

## Twins Management

### GET `/api/v1/twins` 
::: tip Quyền cần thiết
Chỉ đọc
:::

Lấy danh sách Twins có thể truy cập.

**Parameters:**
- `page` (integer) - Số trang (1-based)
- `limit` (integer) - Số items mỗi trang (max 100)

### GET `/api/v1/twins/{id}`
::: tip Quyền cần thiết
Chỉ đọc
:::

Lấy thông tin chi tiết twin.

**Parameters:**
- `id` (string, required) - ID của twin

## Conversations Management

### POST `/api/v1/conversations`
::: tip Quyền cần thiết
Toàn quyền
:::

Tạo cuộc trò chuyện mới.

**Parameters:**
- `twinId` (string, required) - ID của twin
- `title` (string, optional) - Tiêu đề cuộc trò chuyện

### GET `/api/v1/conversations`
::: tip Quyền cần thiết
Chỉ đọc
:::

Lấy danh sách cuộc trò chuyện.

**Parameters:**
- `page` (integer) - Số trang
- `limit` (integer) - Số items mỗi trang
- `twinId` (string) - Lọc theo twin ID

## Messages

### POST `/api/v1/conversations/{id}/messages`
::: tip Quyền cần thiết
Toàn quyền
:::

Gửi tin nhắn.

**Parameters:**
- `id` (string, required) - ID cuộc trò chuyện
- `content` (string, required) - Nội dung tin nhắn

### POST `/api/v1/conversations/{id}/messages/stream`
::: tip Quyền cần thiết
Toàn quyền
:::

Gửi tin nhắn với phản hồi streaming.

**Parameters:**
- `id` (string, required) - ID cuộc trò chuyện
- `content` (string, required) - Nội dung tin nhắn

**Response:** Server-Sent Events với các event types:
- `progress` - Thông tin tiến trình
- `delta` - Từng phần của response
- `complete` - Hoàn thành message
- `error` - Lỗi xảy ra

---

::: tip Cần hỗ trợ?
Nếu bạn gặp vấn đề với API, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com).
:::
