# 5.5. Rate Limiting

TwinExpert API áp dụng rate limiting để đảm bảo chất lượng dịch vụ và công bằng cho tất cả người dùng. Tìm hiểu cách hoạt động và cách tối ưu hóa usage.

## 📊 Giới hạn theo Plan

### Free Plan
- **1,000 requests/hour**
- **50,000 tokens/month**
- **5 concurrent requests**
- **Basic experts only**

### Pro Plan
- **10,000 requests/hour**
- **1,000,000 tokens/month**
- **20 concurrent requests**
- **All experts + premium features**

### Enterprise Plan
- **Unlimited requests/hour**
- **Unlimited tokens**
- **100 concurrent requests**
- **Custom experts + white-label**

## 🔢 Rate Limit Headers

Mọi API response đều chứa rate limit headers:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9875
X-RateLimit-Reset: 1640995200
X-RateLimit-Type: hourly
X-RateLimit-Plan: pro
```

### Header Definitions

| Header | Mô tả |
|--------|-------|
| `X-RateLimit-Limit` | Tổng số requests cho phép trong window |
| `X-RateLimit-Remaining` | Số requests còn lại trong window hiện tại |
| `X-RateLimit-Reset` | Unix timestamp khi rate limit reset |
| `X-RateLimit-Type` | Loại rate limit (hourly, daily, monthly) |
| `X-RateLimit-Plan` | Plan hiện tại của bạn |

## ⚠️ Rate Limit Exceeded Response

Khi vượt quá giới hạn, API sẽ trả về HTTP 429:

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Too Many Requests",
    "details": "You have exceeded your hourly rate limit of 1000 requests",
    "retry_after": 3600,
    "current_usage": {
      "requests_made": 1000,
      "requests_limit": 1000,
      "window_reset": "2024-01-01T15:00:00Z"
    },
    "upgrade_info": {
      "current_plan": "free",
      "suggested_plan": "pro",
      "upgrade_url": "https://twinexpert.com/upgrade"
    }
  }
}
```

## 🛠️ Cách xử lý Rate Limiting

### 1. Check Rate Limit trước khi Request

```javascript
class RateLimitAwareClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.lastRateLimitCheck = null;
    this.remainingRequests = null;
    this.resetTime = null;
  }

  async checkRateLimit() {
    try {
      const response = await axios.get('https://api.twinexpert.com/v1/usage', {
        headers: { 'Authorization': `Bearer ${this.apiKey}` }
      });

      this.remainingRequests = parseInt(response.headers['x-ratelimit-remaining']);
      this.resetTime = parseInt(response.headers['x-ratelimit-reset']);
      this.lastRateLimitCheck = Date.now();

      return {
        remaining: this.remainingRequests,
        resetTime: this.resetTime,
        canMakeRequest: this.remainingRequests > 0
      };
    } catch (error) {
      console.error('Error checking rate limit:', error);
      return { canMakeRequest: true }; // Assume OK if check fails
    }
  }

  async safeRequest(expert, message, context = {}) {
    // Check rate limit if we haven't checked recently
    if (!this.lastRateLimitCheck || Date.now() - this.lastRateLimitCheck > 60000) {
      const rateLimitStatus = await this.checkRateLimit();
      
      if (!rateLimitStatus.canMakeRequest) {
        const waitTime = (this.resetTime * 1000) - Date.now();
        throw new Error(`Rate limit exceeded. Wait ${Math.ceil(waitTime / 1000)} seconds`);
      }
    }

    // Make the actual request
    return await this.makeRequest(expert, message, context);
  }

  async makeRequest(expert, message, context) {
    try {
      const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', {
        expert, message, context
      }, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        }
      });

      // Update rate limit info from response headers
      this.remainingRequests = parseInt(response.headers['x-ratelimit-remaining']);
      this.resetTime = parseInt(response.headers['x-ratelimit-reset']);

      return response.data;
    } catch (error) {
      if (error.response?.status === 429) {
        const retryAfter = error.response.headers['retry-after'] || 3600;
        throw new Error(`Rate limited. Retry after ${retryAfter} seconds`);
      }
      throw error;
    }
  }
}

// Sử dụng
const client = new RateLimitAwareClient(process.env.TWIN_API_KEY);

client.safeRequest('marketing', 'Create social media strategy')
  .then(result => console.log(result.response))
  .catch(error => console.error(error.message));
```

### 2. Exponential Backoff Retry

```javascript
async function requestWithBackoff(requestFn, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      if (error.response?.status === 429) {
        const retryAfter = error.response.headers['retry-after'];
        const backoffTime = retryAfter ? parseInt(retryAfter) * 1000 : Math.pow(2, attempt) * 1000;
        
        console.log(`Rate limited. Waiting ${backoffTime/1000}s before retry ${attempt + 1}/${maxRetries}`);
        
        if (attempt < maxRetries - 1) {
          await new Promise(resolve => setTimeout(resolve, backoffTime));
          continue;
        }
      }
      throw error;
    }
  }
}

// Sử dụng
const makeRequest = () => axios.post('https://api.twinexpert.com/v1/chat/completions', {
  expert: 'copywriter',
  message: 'Write product description'
}, {
  headers: { 'Authorization': `Bearer ${process.env.TWIN_API_KEY}` }
});

requestWithBackoff(makeRequest)
  .then(response => console.log(response.data))
  .catch(error => console.error('All retries failed:', error.message));
```

### 3. Request Queue với Rate Limiting

```javascript
class RequestQueue {
  constructor(apiKey, requestsPerSecond = 2) {
    this.apiKey = apiKey;
    this.requestsPerSecond = requestsPerSecond;
    this.queue = [];
    this.processing = false;
    this.lastRequestTime = 0;
  }

  async addRequest(expert, message, context = {}) {
    return new Promise((resolve, reject) => {
      this.queue.push({
        expert,
        message,
        context,
        resolve,
        reject,
        timestamp: Date.now()
      });

      if (!this.processing) {
        this.processQueue();
      }
    });
  }

  async processQueue() {
    this.processing = true;

    while (this.queue.length > 0) {
      const request = this.queue.shift();
      
      try {
        // Ensure minimum delay between requests
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequestTime;
        const minDelay = 1000 / this.requestsPerSecond;
        
        if (timeSinceLastRequest < minDelay) {
          await new Promise(resolve => setTimeout(resolve, minDelay - timeSinceLastRequest));
        }

        const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', {
          expert: request.expert,
          message: request.message,
          context: request.context
        }, {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        });

        this.lastRequestTime = Date.now();
        request.resolve(response.data);

      } catch (error) {
        if (error.response?.status === 429) {
          // Put request back in queue and wait
          this.queue.unshift(request);
          const retryAfter = error.response.headers['retry-after'] || 60;
          console.log(`Rate limited. Pausing queue for ${retryAfter} seconds`);
          await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        } else {
          request.reject(error);
        }
      }
    }

    this.processing = false;
  }

  getQueueStatus() {
    return {
      queueLength: this.queue.length,
      processing: this.processing,
      estimatedWaitTime: this.queue.length / this.requestsPerSecond
    };
  }
}

// Sử dụng Request Queue
const queue = new RequestQueue(process.env.TWIN_API_KEY, 2); // 2 requests per second

// Add multiple requests
const requests = [
  queue.addRequest('marketing', 'Create campaign for product A'),
  queue.addRequest('copywriter', 'Write email for product B'),
  queue.addRequest('social_media', 'Create Instagram posts'),
  queue.addRequest('business_analyst', 'Analyze market trends')
];

Promise.all(requests)
  .then(results => {
    console.log('All requests completed:');
    results.forEach((result, index) => {
      console.log(`Request ${index + 1}: ${result.response.substring(0, 100)}...`);
    });
  })
  .catch(error => console.error('Queue processing failed:', error));

// Monitor queue status
setInterval(() => {
  const status = queue.getQueueStatus();
  if (status.queueLength > 0) {
    console.log(`Queue: ${status.queueLength} requests, ETA: ${status.estimatedWaitTime.toFixed(1)}s`);
  }
}, 5000);
```

## 📈 Token-based Rate Limiting

Ngoài request limiting, TwinExpert còn có token limiting:

### Token Usage Monitoring

```javascript
class TokenManager {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.monthlyTokensUsed = 0;
    this.monthlyTokensLimit = 50000; // Free plan
    this.resetDate = new Date();
    this.resetDate.setMonth(this.resetDate.getMonth() + 1, 1);
  }

  async getTokenUsage() {
    try {
      const response = await axios.get('https://api.twinexpert.com/v1/usage', {
        headers: { 'Authorization': `Bearer ${this.apiKey}` }
      });

      const usage = response.data.current_period;
      this.monthlyTokensUsed = usage.tokens_used;
      this.monthlyTokensLimit = usage.tokens_limit;

      return {
        used: this.monthlyTokensUsed,
        limit: this.monthlyTokensLimit,
        remaining: this.monthlyTokensLimit - this.monthlyTokensUsed,
        percentage: (this.monthlyTokensUsed / this.monthlyTokensLimit) * 100
      };
    } catch (error) {
      console.error('Error fetching token usage:', error);
      return null;
    }
  }

  async checkTokenAvailability(estimatedTokens = 100) {
    const usage = await this.getTokenUsage();
    if (!usage) return true; // Assume OK if check fails

    const remaining = usage.remaining;
    
    if (remaining < estimatedTokens) {
      throw new Error(`Not enough tokens. Remaining: ${remaining}, Needed: ${estimatedTokens}`);
    }

    // Warning when close to limit
    if (usage.percentage > 90) {
      console.warn(`⚠️  Token usage warning: ${usage.percentage.toFixed(1)}% used (${usage.used}/${usage.limit})`);
    }

    return true;
  }

  estimateTokens(message, expert = 'general') {
    // Rough estimation: 1 token ≈ 4 characters for input
    // Output usually 2-3x input length
    const inputTokens = Math.ceil(message.length / 4);
    const outputMultiplier = expert === 'copywriter' ? 3 : 2; // Copywriter generates more content
    return inputTokens * (1 + outputMultiplier);
  }
}

// Sử dụng Token Management
const tokenManager = new TokenManager(process.env.TWIN_API_KEY);

async function smartRequest(expert, message, context = {}) {
  try {
    // Estimate token usage
    const estimatedTokens = tokenManager.estimateTokens(message, expert);
    
    // Check availability
    await tokenManager.checkTokenAvailability(estimatedTokens);
    
    // Make request
    const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', {
      expert, message, context
    }, {
      headers: {
        'Authorization': `Bearer ${tokenManager.apiKey}`,
        'Content-Type': 'application/json'
      }
    });

    console.log(`✅ Request completed. Tokens used: ${response.data.tokens_used}`);
    return response.data;

  } catch (error) {
    console.error('Request failed:', error.message);
    throw error;
  }
}

// Sử dụng
smartRequest('copywriter', 'Viết bài blog chi tiết về AI marketing trends 2024')
  .then(result => console.log(result.response))
  .catch(error => console.error(error.message));
```

## 🔧 Optimization Strategies

### 1. Batch Similar Requests

```javascript
// ❌ Không hiệu quả - nhiều requests riêng lẻ
async function inefficientApproach() {
  const products = ['Product A', 'Product B', 'Product C'];
  
  for (const product of products) {
    await callExpert('copywriter', `Write description for ${product}`);
  }
}

// ✅ Hiệu quả - batch request
async function efficientApproach() {
  const products = ['Product A', 'Product B', 'Product C'];
  
  const result = await callExpert('copywriter', 
    `Write product descriptions for the following products: ${products.join(', ')}. 
     Provide each description separately with clear product names.`
  );
  
  return result;
}
```

### 2. Context Reuse

```javascript
// ❌ Lặp lại context cho mỗi request
async function inefficientContext() {
  const brandContext = { brand: 'TechStore', tone: 'professional', audience: 'tech enthusiasts' };
  
  await callExpert('copywriter', 'Write email subject', brandContext);
  await callExpert('copywriter', 'Write email body', brandContext);
  await callExpert('copywriter', 'Write CTA button', brandContext);
}

// ✅ Tối ưu với conversation context
async function efficientContext() {
  const conversation = await startConversation('copywriter', {
    brand: 'TechStore',
    tone: 'professional', 
    audience: 'tech enthusiasts',
    project: 'email_campaign'
  });

  // Subsequent messages in same conversation retain context
  const subject = await continueConversation(conversation.id, 'Write email subject line');
  const body = await continueConversation(conversation.id, 'Write email body');
  const cta = await continueConversation(conversation.id, 'Write CTA button text');
  
  return { subject, body, cta };
}
```

### 3. Caching Strategy

```javascript
class CachedTwinClient {
  constructor(apiKey, cacheTTL = 3600000) { // 1 hour cache
    this.apiKey = apiKey;
    this.cache = new Map();
    this.cacheTTL = cacheTTL;
  }

  getCacheKey(expert, message, context) {
    return Buffer.from(JSON.stringify({ expert, message, context })).toString('base64');
  }

  isValidCache(timestamp) {
    return Date.now() - timestamp < this.cacheTTL;
  }

  async callExpertWithCache(expert, message, context = {}) {
    const cacheKey = this.getCacheKey(expert, message, context);
    const cached = this.cache.get(cacheKey);

    // Return cached result if valid
    if (cached && this.isValidCache(cached.timestamp)) {
      console.log('📦 Cache hit');
      return cached.data;
    }

    // Make API call
    console.log('🌐 API call');
    const result = await this.callExpert(expert, message, context);

    // Cache the result
    this.cache.set(cacheKey, {
      data: result,
      timestamp: Date.now()
    });

    // Clean old cache entries periodically
    if (this.cache.size > 1000) {
      this.cleanCache();
    }

    return result;
  }

  cleanCache() {
    const now = Date.now();
    for (const [key, value] of this.cache.entries()) {
      if (!this.isValidCache(value.timestamp)) {
        this.cache.delete(key);
      }
    }
    console.log(`🧹 Cache cleaned. Size: ${this.cache.size}`);
  }

  async callExpert(expert, message, context) {
    const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', {
      expert, message, context
    }, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  }
}

// Sử dụng với cache
const cachedClient = new CachedTwinClient(process.env.TWIN_API_KEY);

// First call - API request
cachedClient.callExpertWithCache('marketing', 'Create hashtags for coffee shop')
  .then(result => console.log('First call:', result.response));

// Second call - cached result
setTimeout(() => {
  cachedClient.callExpertWithCache('marketing', 'Create hashtags for coffee shop')
    .then(result => console.log('Second call (cached):', result.response));
}, 5000);
```

## 📊 Monitoring & Alerts

```javascript
class UsageMonitor {
  constructor(apiKey, alertThresholds = { requests: 80, tokens: 85 }) {
    this.apiKey = apiKey;
    this.alertThresholds = alertThresholds;
    this.alertSent = { requests: false, tokens: false };
  }

  async monitorUsage() {
    try {
      const response = await axios.get('https://api.twinexpert.com/v1/usage', {
        headers: { 'Authorization': `Bearer ${this.apiKey}` }
      });

      const usage = response.data.current_period;
      
      // Calculate percentages
      const requestPercentage = (usage.requests_made / usage.requests_limit) * 100;
      const tokenPercentage = (usage.tokens_used / usage.tokens_limit) * 100;

      // Check request threshold
      if (requestPercentage >= this.alertThresholds.requests && !this.alertSent.requests) {
        this.sendAlert('requests', requestPercentage, usage);
        this.alertSent.requests = true;
      }

      // Check token threshold  
      if (tokenPercentage >= this.alertThresholds.tokens && !this.alertSent.tokens) {
        this.sendAlert('tokens', tokenPercentage, usage);
        this.alertSent.tokens = true;
      }

      return {
        requests: { used: usage.requests_made, limit: usage.requests_limit, percentage: requestPercentage },
        tokens: { used: usage.tokens_used, limit: usage.tokens_limit, percentage: tokenPercentage },
        resetDate: usage.end_date
      };

    } catch (error) {
      console.error('Error monitoring usage:', error);
      return null;
    }
  }

  sendAlert(type, percentage, usage) {
    const message = `🚨 ${type.toUpperCase()} USAGE ALERT: ${percentage.toFixed(1)}% used (${usage[type + '_used']}/${usage[type + '_limit']})`;
    
    console.warn(message);
    
    // Send to monitoring service (Slack, email, etc.)
    // this.sendToSlack(message);
    // this.sendEmail(message);
  }

  resetAlerts() {
    this.alertSent = { requests: false, tokens: false };
  }
}

// Setup monitoring
const monitor = new UsageMonitor(process.env.TWIN_API_KEY, { 
  requests: 80, // Alert at 80%
  tokens: 85    // Alert at 85%
});

// Monitor every 5 minutes
setInterval(async () => {
  const usage = await monitor.monitorUsage();
  if (usage) {
    console.log(`📊 Usage: Requests ${usage.requests.percentage.toFixed(1)}%, Tokens ${usage.tokens.percentage.toFixed(1)}%`);
  }
}, 5 * 60 * 1000);

// Reset alerts at the beginning of each month
const now = new Date();
const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);
const msUntilNextMonth = nextMonth - now;

setTimeout(() => {
  monitor.resetAlerts();
  console.log('🔄 Monthly usage alerts reset');
}, msUntilNextMonth);
```

## 💡 Best Practices Summary

### ✅ Do's
- **Monitor rate limits** trước khi gửi request
- **Implement retry logic** với exponential backoff
- **Use request queuing** cho high-volume applications
- **Cache responses** khi phù hợp
- **Batch similar requests** để tối ưu token usage
- **Set up usage alerts** trước khi đạt giới hạn
- **Upgrade plan** khi cần thiết

### ❌ Don'ts
- **Không ignore** rate limit headers
- **Không spam requests** khi bị rate limited
- **Không hardcode delays** - sử dụng retry-after header
- **Không cache sensitive data** quá lâu
- **Không assume unlimited usage** ngay cả với Enterprise plan

---

**Tiếp theo**: [Error Handling →](./error-handling)

