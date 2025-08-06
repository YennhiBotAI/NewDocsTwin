---
title: "Rate Limiting"
description: "Twin AI API - Rate Limiting"
---

# 5.5. Rate Limiting

Giới hạn tần suất gọi API để đảm bảo chất lượng dịch vụ cho tất cả người dùng.

## Giới hạn theo loại API Key

| Loại API Key | Requests/giờ | Burst Limit | Mô tả |
|--------------|--------------|-------------|-------|
| **read_only** | 200 | 50 | API Key chỉ đọc |
| **full_access** | 500 | 100 | API Key toàn quyền |

### Burst Limit
Cho phép bạn sử dụng một số lượng requests lớn trong thời gian ngắn, nhưng vẫn phải tuân theo giới hạn tổng thể trong giờ.

## Response Headers

Mọi response đều bao gồm các headers về rate limiting để bạn theo dõi:

| Header | Mô tả |
|--------|-------|
| `X-RateLimit-Limit` | Tổng số requests được phép trong window |
| `X-RateLimit-Remaining` | Số requests còn lại |
| `X-RateLimit-Reset` | Timestamp khi counter reset |
| `X-RateLimit-Window` | Thời gian window (giây) |

### Ví dụ Response Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 487
X-RateLimit-Reset: 1642867200
X-RateLimit-Window: 3600
```

## Xử lý Rate Limiting

### Khi vượt quá giới hạn

Khi bạn vượt quá rate limit, API sẽ trả về:

```json
{
  "success": false,
  "message": "Vượt quá giới hạn tần suất gọi API",
  "error": "RATE_LIMIT_EXCEEDED", 
  "statusCode": 429,
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_abc123",
    "retryAfter": 3600
  }
}
```

### Best Practices

1. **Theo dõi headers**: Luôn kiểm tra `X-RateLimit-Remaining` để biết số requests còn lại
2. **Implement retry logic**: Chờ theo `retryAfter` khi gặp lỗi 429
3. **Cache dữ liệu**: Lưu trữ response để giảm số lượng calls không cần thiết
4. **Batch requests**: Gộp nhiều operations trong một request khi có thể

### Ví dụ Retry Logic

::: code-group

```javascript [JavaScript]
async function apiCallWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url, options);
    
    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After') || 60;
      console.log(`Rate limited. Retrying after ${retryAfter} seconds...`);
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      continue;
    }
    
    return response;
  }
  
  throw new Error('Max retries exceeded');
}
```

```python [Python]
import time
import requests

def api_call_with_retry(url, headers, max_retries=3):
    for i in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f'Rate limited. Retrying after {retry_after} seconds...')
            time.sleep(retry_after)
            continue
            
        return response
    
    raise Exception('Max retries exceeded')
```

:::

---

::: tip Upgrade để tăng giới hạn
Nếu bạn cần rate limit cao hơn, hãy liên hệ với chúng tôi để upgrade gói dịch vụ phù hợp.
:::

::: tip Cần hỗ trợ?
Nếu bạn gặp vấn đề với rate limiting, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com).
:::
