# 5.1. Bắt đầu với API

## Tổng quan
Hướng dẫn nhanh để bắt đầu sử dụng TwinExpert API và tích hợp AI twins vào ứng dụng của bạn.

## Yêu cầu hệ thống

### Môi trường phát triển
- **Node.js**: >= 16.x
- **Python**: >= 3.8
- **PHP**: >= 8.0
- **Java**: >= 11

### Dependencies cơ bản
- HTTP client library (axios, requests, guzzle, okhttp)
- JSON parser
- SSL/TLS support

## Bước 1: Tạo tài khoản và lấy API Key

### 1.1. Đăng ký tài khoản Developer
1. Truy cập [TwinExpert Developer Portal](https://developers.twinexpert.ai)
2. Đăng ký tài khoản hoặc đăng nhập
3. Xác thực email và hoàn tất profile

### 1.2. Tạo API Key
1. Vào Dashboard → API Keys
2. Click "Create New API Key"
3. Chọn permissions phù hợp
4. Lưu lại API key (chỉ hiển thị 1 lần)

```bash
# Ví dụ API key format
TWINEXPERT_API_KEY=te_live_sk_1234567890abcdef...
```

## Bước 2: Cài đặt SDK

### JavaScript/Node.js
```bash
npm install @twinexpert/js-sdk
# hoặc
yarn add @twinexpert/js-sdk
```

### Python
```bash
pip install twinexpert
```

### PHP
```bash
composer require twinexpert/php-sdk
```

### Java (Maven)
```xml
<dependency>
    <groupId>com.twinexpert</groupId>
    <artifactId>java-sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

## Bước 3: Khởi tạo Client

### JavaScript
```javascript
import TwinExpert from '@twinexpert/js-sdk';

const client = new TwinExpert({
  apiKey: process.env.TWINEXPERT_API_KEY,
  environment: 'production' // 'staging' for testing
});
```

### Python
```python
import twinexpert

client = twinexpert.TwinExpert(
    api_key=os.environ['TWINEXPERT_API_KEY'],
    environment='production'
)
```

### PHP
```php
use TwinExpert\Client;

$client = new Client([
    'api_key' => $_ENV['TWINEXPERT_API_KEY'],
    'environment' => 'production'
]);
```

### Java
```java
import com.twinexpert.TwinExpertClient;

TwinExpertClient client = TwinExpertClient.builder()
    .apiKey(System.getenv("TWINEXPERT_API_KEY"))
    .environment("production")
    .build();
```

## Bước 4: First API Call - Lấy thông tin account

### JavaScript
```javascript
async function getAccountInfo() {
  try {
    const account = await client.account.retrieve();
    console.log('Account ID:', account.id);
    console.log('Plan:', account.plan);
    console.log('Usage:', account.usage);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

getAccountInfo();
```

### Python
```python
def get_account_info():
    try:
        account = client.account.retrieve()
        print(f"Account ID: {account.id}")
        print(f"Plan: {account.plan}")
        print(f"Usage: {account.usage}")
    except Exception as error:
        print(f"Error: {error}")

get_account_info()
```

## Bước 5: Tạo Twin AI đầu tiên

### JavaScript
```javascript
async function createFirstTwin() {
  try {
    const twin = await client.twins.create({
      name: "My Assistant",
      personality: "helpful",
      description: "A helpful AI assistant",
      instructions: "You are a helpful assistant that answers questions clearly and concisely.",
      model: "gpt-4-turbo"
    });
    
    console.log('Created Twin:', twin.id);
    return twin;
  } catch (error) {
    console.error('Error creating twin:', error.message);
  }
}
```

### Python
```python
def create_first_twin():
    try:
        twin = client.twins.create(
            name="My Assistant",
            personality="helpful",
            description="A helpful AI assistant",
            instructions="You are a helpful assistant that answers questions clearly and concisely.",
            model="gpt-4-turbo"
        )
        
        print(f"Created Twin: {twin.id}")
        return twin
    except Exception as error:
        print(f"Error creating twin: {error}")
```

## Bước 6: Tạo conversation đầu tiên

### JavaScript
```javascript
async function startConversation(twinId) {
  try {
    const response = await client.twins.chat({
      twinId: twinId,
      message: "Xin chào! Bạn có thể giúp tôi không?",
      stream: false
    });
    
    console.log('AI Response:', response.message);
    console.log('Usage:', response.usage);
    
    return response;
  } catch (error) {
    console.error('Error in conversation:', error.message);
  }
}
```

### Python
```python
def start_conversation(twin_id):
    try:
        response = client.twins.chat(
            twin_id=twin_id,
            message="Xin chào! Bạn có thể giúp tôi không?",
            stream=False
        )
        
        print(f"AI Response: {response.message}")
        print(f"Usage: {response.usage}")
        
        return response
    except Exception as error:
        print(f"Error in conversation: {error}")
```

## Testing với cURL

Nếu bạn muốn test API trực tiếp mà không cần SDK:

```bash
# Test authentication
curl -X GET "https://api.twinexpert.ai/v1/account" \
  -H "Authorization: Bearer your-api-key-here" \
  -H "Content-Type: application/json"

# Tạo twin
curl -X POST "https://api.twinexpert.ai/v1/twins" \
  -H "Authorization: Bearer your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Assistant",
    "personality": "helpful",
    "instructions": "You are a helpful assistant."
  }'

# Chat với twin
curl -X POST "https://api.twinexpert.ai/v1/twins/twin_123/chat" \
  -H "Authorization: Bearer your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?"
  }'
```

## Environment Variables

Để bảo mật, luôn sử dụng environment variables:

```bash
# .env file
TWINEXPERT_API_KEY=te_live_sk_your_key_here
TWINEXPERT_ENVIRONMENT=production
TWINEXPERT_API_URL=https://api.twinexpert.ai/v1
```

## Error Handling cơ bản

```javascript
// JavaScript
try {
  const response = await client.twins.chat({
    twinId: 'twin_123',
    message: 'Hello'
  });
} catch (error) {
  if (error.status === 401) {
    console.error('Invalid API key');
  } else if (error.status === 429) {
    console.error('Rate limit exceeded');
  } else if (error.status === 500) {
    console.error('Server error');
  } else {
    console.error('Unknown error:', error.message);
  }
}
```

## Next Steps

Sau khi hoàn thành quick start:

1. 📖 Đọc [API Endpoints](./endpoints) để hiểu tất cả endpoints
2. 🔑 Thiết lập [Authentication](./authentication) đúng cách
3. 💡 Xem [Examples](./examples) để học patterns thực tế
4. ⚡ Tìm hiểu về [Rate Limiting](./rate-limiting)
5. 🚨 Chuẩn bị [Error Handling](./error-handling) cho production

## Troubleshooting

### Lỗi thường gặp

**"Unauthorized" (401)**
- Kiểm tra API key có đúng không
- Đảm bảo API key có permissions cần thiết

**"Rate limit exceeded" (429)**
- Giảm tần suất requests
- Upgrade plan để có higher limits

**"Twin not found" (404)**
- Kiểm tra twin ID có tồn tại
- Đảm bảo twin thuộc về account của bạn

### Debug mode

```javascript
// Bật debug mode để xem requests/responses
const client = new TwinExpert({
  apiKey: 'your-key',
  debug: true
});
```

---

## Support

**Cần hỗ trợ?**
- 📧 Email: developers@twinexpert.ai
- 💬 Discord: [discord.gg/twinexpert](https://discord.gg/twinexpert)
- 📖 Docs: [docs.twinexpert.ai](https://docs.twinexpert.ai)

*Chúc bạn coding vui vẻ với TwinExpert API! 🚀*