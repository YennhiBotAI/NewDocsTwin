# 5.1. Bắt đầu với API

Chào mừng bạn đến với TwinExpert API Documentation! API của chúng tôi cho phép bạn tích hợp sức mạnh của Twin AI vào ứng dụng và hệ thống của riêng bạn.

## 🚀 Tổng quan

TwinExpert API là RESTful API cho phép bạn:

- **Gọi các chuyên gia AI**: Truy cập hơn 10 chuyên gia AI khác nhau
- **Quản lý cuộc hội thoại**: Tạo, lưu và quản lý các phiên chat
- **Xử lý file**: Upload và phân tích tài liệu PDF, Word, Excel
- **Quản lý projects**: Tổ chức công việc theo dự án
- **Tích hợp team**: Quản lý thành viên và phân quyền

## 📋 Yêu cầu hệ thống

- **Base URL**: `https://api.twinexpert.com/v1`
- **Authentication**: API Key (Bearer Token)
- **Content-Type**: `application/json`
- **Rate Limiting**: 1000 requests/hour (Free), không giới hạn (Pro+)

## 🔑 Bước 1: Lấy API Key

1. **Đăng ký tài khoản** miễn phí tại [twinexpert.com](https://twinexpert.com)
2. **Đăng nhập** và vào Dashboard
3. **Vào Settings** → API Keys
4. **Tạo API Key** mới
5. **Copy và lưu** API Key an toàn

::: warning Lưu ý bảo mật
- Không chia sẻ API Key với người khác
- Sử dụng biến môi trường để lưu API Key
- Thường xuyên rotate API Key định kỳ
:::

## 📝 Bước 2: Request đầu tiên

### Kiểm tra kết nối

```bash
curl -X GET "https://api.twinexpert.com/v1/health" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

**Response thành công:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Gọi chuyên gia AI đầu tiên

```bash
curl -X POST "https://api.twinexpert.com/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "expert": "marketing",
    "message": "Viết một slogan cho sản phẩm trà sữa",
    "context": {
      "brand": "TeaLover",
      "target_audience": "Gen Z"
    }
  }'
```

**Response mẫu:**
```json
{
  "id": "chat_123456",
  "expert": "marketing",
  "response": "TeaLover - Trà sữa thế hệ mới, vị ngon không thể chối từ! 🧋✨",
  "tokens_used": 45,
  "processing_time": 1.2
}
```

## 🎯 Bước 3: Tích hợp vào ứng dụng

### JavaScript/Node.js

```javascript
const axios = require('axios');

const twinAPI = {
  baseURL: 'https://api.twinexpert.com/v1',
  apiKey: process.env.TWIN_API_KEY,
  
  async callExpert(expert, message, context = {}) {
    try {
      const response = await axios.post(`${this.baseURL}/chat/completions`, {
        expert,
        message,
        context
      }, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('API Error:', error.response.data);
      throw error;
    }
  }
};

// Sử dụng
twinAPI.callExpert('copywriter', 'Viết email marketing cho Black Friday')
  .then(result => console.log(result.response))
  .catch(error => console.error(error));
```

### Python

```python
import requests
import os

class TwinAPI:
    def __init__(self):
        self.base_url = "https://api.twinexpert.com/v1"
        self.api_key = os.getenv("TWIN_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def call_expert(self, expert, message, context=None):
        url = f"{self.base_url}/chat/completions"
        payload = {
            "expert": expert,
            "message": message,
            "context": context or {}
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

# Sử dụng
twin = TwinAPI()
result = twin.call_expert("business_analyst", "Phân tích thị trường trà sữa Việt Nam")
print(result["response"])
```

### PHP

```php
<?php
class TwinAPI {
    private $baseURL = 'https://api.twinexpert.com/v1';
    private $apiKey;
    
    public function __construct($apiKey) {
        $this->apiKey = $apiKey;
    }
    
    public function callExpert($expert, $message, $context = []) {
        $curl = curl_init();
        
        curl_setopt_array($curl, [
            CURLOPT_URL => $this->baseURL . '/chat/completions',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_HTTPHEADER => [
                'Authorization: Bearer ' . $this->apiKey,
                'Content-Type: application/json'
            ],
            CURLOPT_POSTFIELDS => json_encode([
                'expert' => $expert,
                'message' => $message,
                'context' => $context
            ])
        ]);
        
        $response = curl_exec($curl);
        curl_close($curl);
        
        return json_decode($response, true);
    }
}

// Sử dụng
$twin = new TwinAPI($_ENV['TWIN_API_KEY']);
$result = $twin->callExpert('social_media', 'Tạo caption cho bài post Instagram');
echo $result['response'];
?>
```

## 📊 Các chuyên gia có sẵn

| Expert ID | Chuyên môn | Mô tả |
|-----------|------------|-------|
| `marketing` | Marketing & Branding | Chiến lược marketing, branding, positioning |
| `copywriter` | Viết content | Email, landing page, blog, social content |
| `social_media` | Social Media | Content cho Facebook, Instagram, TikTok |
| `business_analyst` | Phân tích kinh doanh | Market research, competitor analysis |
| `creative_director` | Sáng tạo | Concept, storyboard, creative campaign |
| `sales` | Bán hàng | Sales script, proposal, negotiation |
| `hr` | Nhân sự | Job description, interview, employee handbook |
| `finance` | Tài chính | Financial planning, budgeting, analysis |
| `product_manager` | Quản lý sản phẩm | Product roadmap, feature specification |
| `consultant` | Tư vấn chung | Strategy, problem solving, decision making |

## 🔗 Tài liệu tham khảo

- [**Authentication**](./authentication) - Hướng dẫn xác thực API
- [**API Endpoints**](./endpoints) - Danh sách đầy đủ endpoints
- [**Examples**](./examples) - Ví dụ tích hợp thực tế
- [**Rate Limiting**](./rate-limiting) - Giới hạn và tối ưu hóa
- [**Error Handling**](./error-handling) - Xử lý lỗi hiệu quả

## 💡 Tips & Best Practices

### 🎯 **Tối ưu hóa Context**
```javascript
// ❌ Không tốt
{ message: "Viết content" }

// ✅ Tốt
{
  message: "Viết email marketing cho sản phẩm giày thể thao",
  context: {
    product: "Giày chạy bộ UltraBoost",
    target_audience: "Nam 25-35 tuổi, yêu thể thao",
    tone: "friendly, energetic",
    goal: "tăng click-through rate",
    brand_voice: "năng động, đáng tin cậy"
  }
}
```

### 🔄 **Retry Logic**
```javascript
async function callWithRetry(expert, message, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await twinAPI.callExpert(expert, message);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

### 📈 **Monitoring Usage**
```javascript
// Track API usage
const usage = await axios.get('https://api.twinexpert.com/v1/usage', {
  headers: { Authorization: `Bearer ${apiKey}` }
});

console.log(`Requests today: ${usage.data.requests_today}`);
console.log(`Remaining quota: ${usage.data.remaining_quota}`);
```

## 🆘 Cần hỗ trợ?

- **Documentation**: [Xem tài liệu chi tiết](../api/)
- **Support Email**: api-support@twinexpert.com
- **Status Page**: [status.twinexpert.com](https://status.twinexpert.com)
- **Community**: [Discord Channel](https://discord.gg/twinexpert)

---

**Bước tiếp theo**: [Tìm hiểu về Authentication →](./authentication)

