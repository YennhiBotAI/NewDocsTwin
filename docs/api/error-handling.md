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
Request không hợp lệ hoặc thiếu parameters.

**Ví dụ:**
```json
{
  "success": false,
  "message": "Thiếu trường bắt buộc 'content'",
  "error": "MISSING_REQUIRED_FIELD",
  "statusCode": 400,
  "details": {
    "field": "content",
    "required": true
  }
}
```

### 401 Unauthorized
API key không hợp lệ hoặc đã hết hạn.

**Ví dụ:**
```json
{
  "success": false,
  "message": "API key không hợp lệ",
  "error": "INVALID_API_KEY",
  "statusCode": 401
}
```

### 403 Forbidden
API key không có quyền truy cập resource này.

**Ví dụ:**
```json
{
  "success": false,
  "message": "Không có quyền truy cập twin này",
  "error": "FORBIDDEN_ACCESS",
  "statusCode": 403,
  "details": {
    "resource": "twin",
    "resourceId": "twin-123",
    "requiredScope": "full_access"
  }
}
```

### 404 Not Found
Resource không tồn tại.

**Ví dụ:**
```json
{
  "success": false,
  "message": "Không tìm thấy cuộc trò chuyện",
  "error": "CONVERSATION_NOT_FOUND",
  "statusCode": 404,
  "details": {
    "conversationId": "conv-456"
  }
}
```

### 429 Too Many Requests
Vượt quá rate limit.

**Ví dụ:**
```json
{
  "success": false,
  "message": "Vượt quá giới hạn tần suất gọi API",
  "error": "RATE_LIMIT_EXCEEDED",
  "statusCode": 429,
  "meta": {
    "retryAfter": 3600
  }
}
```

### 500 Internal Server Error
Lỗi server, vui lòng thử lại sau.

**Ví dụ:**
```json
{
  "success": false,
  "message": "Lỗi server nội bộ, vui lòng thử lại sau",
  "error": "INTERNAL_SERVER_ERROR",
  "statusCode": 500,
  "meta": {
    "requestId": "req_abc123"
  }
}
```

## Best Practices xử lý lỗi

### 1. Kiểm tra status code

::: code-group

```javascript [JavaScript]
async function handleApiCall(url, options) {
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (!response.ok) {
      // Xử lý các loại lỗi khác nhau
      switch (response.status) {
        case 400:
          console.error('Bad Request:', data.message);
          break;
        case 401:
          console.error('Unauthorized:', data.message);
          // Redirect to login
          break;
        case 403:
          console.error('Forbidden:', data.message);
          break;
        case 404:
          console.error('Not Found:', data.message);
          break;
        case 429:
          console.error('Rate Limited:', data.message);
          // Implement retry logic
          break;
        case 500:
          console.error('Server Error:', data.message);
          // Show user-friendly error message
          break;
        default:
          console.error('Unknown Error:', data.message);
      }
      
      throw new Error(data.message);
    }
    
    return data;
  } catch (error) {
    console.error('API Call failed:', error);
    throw error;
  }
}
```

```python [Python]
import requests
import time

def handle_api_call(url, headers, data=None):
    try:
        if data:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)
        
        response_data = response.json()
        
        if not response.ok:
            error_code = response_data.get('error', 'UNKNOWN_ERROR')
            message = response_data.get('message', 'Unknown error occurred')
            
            if response.status_code == 400:
                print(f'Bad Request: {message}')
            elif response.status_code == 401:
                print(f'Unauthorized: {message}')
                # Handle authentication
            elif response.status_code == 403:
                print(f'Forbidden: {message}')
            elif response.status_code == 404:
                print(f'Not Found: {message}')
            elif response.status_code == 429:
                print(f'Rate Limited: {message}')
                # Implement retry
                retry_after = response_data.get('meta', {}).get('retryAfter', 60)
                time.sleep(retry_after)
            elif response.status_code == 500:
                print(f'Server Error: {message}')
            
            raise Exception(f'{error_code}: {message}')
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        raise
```

:::

### 2. Implement retry logic cho lỗi tạm thời

```javascript
async function retryApiCall(apiCall, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await apiCall();
    } catch (error) {
      // Retry cho lỗi server hoặc network
      if (attempt < maxRetries && (error.status >= 500 || !error.status)) {
        const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      
      throw error;
    }
  }
}
```

### 3. Log errors để debug

```javascript
function logError(error, context) {
  console.error('API Error:', {
    message: error.message,
    code: error.code,
    status: error.status,
    timestamp: new Date().toISOString(),
    context: context,
    requestId: error.requestId
  });
}
```

---

::: tip Debug Tips
Luôn lưu `requestId` từ error response để có thể trace và debug với support team.
:::

::: tip Cần hỗ trợ?
Nếu bạn gặp lỗi không mong muốn, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com) kèm theo `requestId`.
:::
