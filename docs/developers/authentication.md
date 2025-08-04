# 5.2. Xác thực

## Tổng quan
TwinExpert API sử dụng API keys để xác thực và ủy quyền các requests. Tất cả API calls phải được authenticated với một valid API key.

## Loại API Keys

### 1. **Live Keys** (Production)
- Prefix: `te_live_sk_`
- Sử dụng cho production environment
- Có thể access tất cả features
- Rate limits cao hơn

### 2. **Test Keys** (Development)
- Prefix: `te_test_sk_`
- Sử dụng cho development và testing
- Sandbox environment riêng biệt
- Rate limits thấp hơn

## Tạo API Key

### Bước 1: Truy cập Developer Dashboard
1. Đăng nhập vào [TwinExpert Developer Portal](https://developers.twinexpert.ai)
2. Điều hướng đến **API Keys** section
3. Click **"Create New API Key"**

### Bước 2: Cấu hình Permissions
```json
{
  "name": "My App API Key",
  "permissions": [
    "twins:read",
    "twins:write", 
    "twins:chat",
    "account:read",
    "billing:read"
  ],
  "environment": "live", // hoặc "test"
  "expires_at": "2025-12-31T23:59:59Z" // optional
}
```

### Bước 3: Lưu trữ API Key an toàn
⚠️ **QUAN TRỌNG**: API key chỉ hiển thị một lần. Hãy lưu ngay!

```bash
# Ví dụ API key
te_live_sk_1234567890abcdef1234567890abcdef1234567890abcdef
```

## Cách sử dụng API Key

### Method 1: Authorization Header (Khuyến nghị)
```bash
curl -X GET "https://api.twinexpert.ai/v1/account" \
  -H "Authorization: Bearer te_live_sk_your_key_here"
```

### Method 2: Basic Authentication
```bash
curl -X GET "https://api.twinexpert.ai/v1/account" \
  -u "te_live_sk_your_key_here:"
```

## Implementing Authentication

### JavaScript/Node.js
```javascript
import TwinExpert from '@twinexpert/js-sdk';

// Method 1: Constructor
const client = new TwinExpert({
  apiKey: process.env.TWINEXPERT_API_KEY
});

// Method 2: Set later
const client = new TwinExpert();
client.setApiKey(process.env.TWINEXPERT_API_KEY);

// Method 3: Manual header
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.twinexpert.ai/v1',
  headers: {
    'Authorization': `Bearer ${process.env.TWINEXPERT_API_KEY}`,
    'Content-Type': 'application/json'
  }
});
```

### Python
```python
import twinexpert
import os

# Method 1: Constructor
client = twinexpert.TwinExpert(
    api_key=os.environ['TWINEXPERT_API_KEY']
)

# Method 2: Set later
client = twinexpert.TwinExpert()
client.api_key = os.environ['TWINEXPERT_API_KEY']

# Method 3: Manual requests
import requests

headers = {
    'Authorization': f'Bearer {os.environ["TWINEXPERT_API_KEY"]}',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.twinexpert.ai/v1/account',
    headers=headers
)
```

### PHP
```php
use TwinExpert\Client;

// Method 1: Constructor
$client = new Client([
    'api_key' => $_ENV['TWINEXPERT_API_KEY']
]);

// Method 2: Set later
$client = new Client();
$client->setApiKey($_ENV['TWINEXPERT_API_KEY']);

// Method 3: Manual cURL
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://api.twinexpert.ai/v1/account');
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Authorization: Bearer ' . $_ENV['TWINEXPERT_API_KEY'],
    'Content-Type: application/json'
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);
```

### Java
```java
import com.twinexpert.TwinExpertClient;

// Method 1: Builder pattern
TwinExpertClient client = TwinExpertClient.builder()
    .apiKey(System.getenv("TWINEXPERT_API_KEY"))
    .build();

// Method 2: Manual OkHttp
OkHttpClient httpClient = new OkHttpClient();
Request request = new Request.Builder()
    .url("https://api.twinexpert.ai/v1/account")
    .addHeader("Authorization", "Bearer " + System.getenv("TWINEXPERT_API_KEY"))
    .addHeader("Content-Type", "application/json")
    .build();

Response response = httpClient.newCall(request).execute();
```

## Environment Variables

### .env file (Node.js)
```bash
# Development
TWINEXPERT_API_KEY=te_test_sk_dev_key_here
TWINEXPERT_ENVIRONMENT=test

# Production  
TWINEXPERT_API_KEY=te_live_sk_prod_key_here
TWINEXPERT_ENVIRONMENT=production
```

### Loading environment variables
```javascript
// Node.js
require('dotenv').config();
const apiKey = process.env.TWINEXPERT_API_KEY;

// Python
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('TWINEXPERT_API_KEY')

// PHP
$apiKey = $_ENV['TWINEXPERT_API_KEY'] ?? getenv('TWINEXPERT_API_KEY');
```

## Permission Scopes

### Available Permissions

| Permission | Description |
|------------|-------------|
| `twins:read` | Đọc thông tin twins |
| `twins:write` | Tạo, update, delete twins |
| `twins:chat` | Chat với twins |
| `twins:upload` | Upload files và knowledge base |
| `account:read` | Đọc thông tin account |
| `account:write` | Update account settings |
| `billing:read` | Xem thông tin billing |
| `analytics:read` | Access usage analytics |
| `webhooks:write` | Quản lý webhooks |

### Principle of Least Privilege
```json
{
  "name": "Chat Only Key",
  "permissions": [
    "twins:read",
    "twins:chat"
  ]
}
```

## Token Management

### Checking API Key validity
```javascript
async function validateApiKey() {
  try {
    const account = await client.account.retrieve();
    console.log('API key is valid for account:', account.id);
    return true;
  } catch (error) {
    if (error.status === 401) {
      console.error('Invalid API key');
      return false;
    }
    throw error;
  }
}
```

### Key rotation
```javascript
// Graceful key rotation
class TwinExpertWithRotation {
  constructor(primaryKey, fallbackKey) {
    this.primaryClient = new TwinExpert({ apiKey: primaryKey });
    this.fallbackClient = new TwinExpert({ apiKey: fallbackKey });
  }
  
  async makeRequest(method, ...args) {
    try {
      return await this.primaryClient[method](...args);
    } catch (error) {
      if (error.status === 401) {
        console.warn('Primary key failed, trying fallback');
        return await this.fallbackClient[method](...args);
      }
      throw error;
    }
  }
}
```

## Security Best Practices

### 1. **Environment Variables**
```bash
# ❌ NEVER do this
const apiKey = 'te_live_sk_hardcoded_key';

# ✅ Always use environment variables
const apiKey = process.env.TWINEXPERT_API_KEY;
```

### 2. **API Key Storage**
```javascript
// ❌ Don't commit to git
// const API_KEY = 'te_live_sk_...';

// ✅ Use secure vaults in production
// - AWS Secrets Manager
// - Azure Key Vault  
// - Google Secret Manager
// - HashiCorp Vault
```

### 3. **Client-side Security**
```javascript
// ❌ NEVER expose API keys in frontend
const client = new TwinExpert({
  apiKey: 'te_live_sk_exposed_key' // This will be visible to users!
});

// ✅ Use proxy endpoints
fetch('/api/twins/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello' })
});
```

### 4. **Key Monitoring**
```javascript
// Track API key usage
const client = new TwinExpert({
  apiKey: process.env.TWINEXPERT_API_KEY,
  onRequest: (request) => {
    console.log('API Request:', {
      endpoint: request.url,
      timestamp: new Date().toISOString(),
      keyPrefix: request.headers.Authorization?.substring(0, 20) + '...'
    });
  }
});
```

## Error Handling

### Authentication Errors
```javascript
async function handleAuthErrors() {
  try {
    const response = await client.twins.list();
    return response;
  } catch (error) {
    switch (error.status) {
      case 401:
        console.error('Authentication failed: Invalid API key');
        // Redirect to login or refresh token
        break;
        
      case 403:
        console.error('Authorization failed: Insufficient permissions');
        // Request proper permissions
        break;
        
      case 429:
        console.error('Rate limit exceeded');
        // Implement backoff strategy
        break;
        
      default:
        console.error('Unknown error:', error.message);
        throw error;
    }
  }
}
```

### Retry with Exponential Backoff
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 401 || error.status === 403) {
        throw error; // Don't retry auth errors
      }
      
      if (attempt === maxRetries) {
        throw error;
      }
      
      const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
      console.log(`Retry ${attempt}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

## Webhook Authentication

### Verifying Webhook Signatures
```javascript
import crypto from 'crypto';

function verifyWebhookSignature(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(payload, 'utf8');
  const expectedSignature = `sha256=${hmac.digest('hex')}`;
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

// Express.js middleware
function webhookAuth(req, res, next) {
  const signature = req.headers['x-twinexpert-signature'];
  const payload = JSON.stringify(req.body);
  const secret = process.env.WEBHOOK_SECRET;
  
  if (!verifyWebhookSignature(payload, signature, secret)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  next();
}
```

## Testing Authentication

### Unit Tests
```javascript
// Jest example
describe('TwinExpert Authentication', () => {
  test('should authenticate with valid API key', async () => {
    const client = new TwinExpert({
      apiKey: 'te_test_sk_valid_key'
    });
    
    const account = await client.account.retrieve();
    expect(account.id).toBeDefined();
  });
  
  test('should reject invalid API key', async () => {
    const client = new TwinExpert({
      apiKey: 'invalid_key'
    });
    
    await expect(client.account.retrieve()).rejects.toThrow('Unauthorized');
  });
});
```

---

## Next Steps

1. 🔌 Tìm hiểu [API Endpoints](./endpoints) để biết cách sử dụng API
2. 💡 Xem [Examples](./examples) với authenticated requests
3. ⚡ Đọc về [Rate Limiting](./rate-limiting) và quota management
4. 🚨 Học cách [Error Handling](./error-handling) cho production

---

**Cần hỗ trợ với authentication?**
- 📧 Security Team: security@twinexpert.ai
- 📖 Advanced Auth Guide: [docs.twinexpert.ai/auth](https://docs.twinexpert.ai/auth)