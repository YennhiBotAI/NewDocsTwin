# 5.5. Rate Limiting

## Tổng quan
TwinExpert API sử dụng rate limiting để đảm bảo công bằng và ổn định dịch vụ cho tất cả người dùng. Mỗi API key có giới hạn số requests per minute và quota hàng tháng.

## Rate Limits theo Plan

| Plan | Chat API | Other APIs | Monthly Quota |
|------|----------|------------|---------------|
| **Free** | 20 req/min | 100 req/min | 1,000 messages |
| **Starter** | 60 req/min | 300 req/min | 10,000 messages |
| **Pro** | 120 req/min | 600 req/min | 50,000 messages |
| **Enterprise** | Custom | Custom | Custom |

## Rate Limit Headers

Mỗi API response chứa headers về rate limit:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640995260
X-RateLimit-Retry-After: 60
```

### Header Descriptions

- `X-RateLimit-Limit`: Số requests tối đa per minute
- `X-RateLimit-Remaining`: Số requests còn lại trong window hiện tại
- `X-RateLimit-Reset`: Unix timestamp khi window reset
- `X-RateLimit-Retry-After`: Số seconds để retry (chỉ có khi bị rate limited)

## Xử lý Rate Limit Errors

### Error Response
```json
{
  "error": {
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 30 seconds.",
    "retry_after": 30
  }
}
```

### JavaScript Implementation
```javascript
class RateLimitHandler {
  constructor(client) {
    this.client = client;
    this.requestQueue = [];
    this.processing = false;
  }

  async makeRequest(endpoint, params) {
    return new Promise((resolve, reject) => {
      this.requestQueue.push({ endpoint, params, resolve, reject });
      this.processQueue();
    });
  }

  async processQueue() {
    if (this.processing || this.requestQueue.length === 0) return;
    
    this.processing = true;
    
    while (this.requestQueue.length > 0) {
      const { endpoint, params, resolve, reject } = this.requestQueue.shift();
      
      try {
        const result = await this.executeWithBackoff(endpoint, params);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    }
    
    this.processing = false;
  }

  async executeWithBackoff(endpoint, params, attempt = 1) {
    try {
      return await this.client[endpoint](params);
    } catch (error) {
      if (error.status === 429 && attempt <= 3) {
        const retryAfter = error.retry_after || Math.pow(2, attempt) * 1000;
        console.log(`Rate limited. Waiting ${retryAfter}ms before retry...`);
        
        await new Promise(resolve => setTimeout(resolve, retryAfter));
        return this.executeWithBackoff(endpoint, params, attempt + 1);
      }
      throw error;
    }
  }
}

// Usage
const handler = new RateLimitHandler(twinExpertClient);

// Multiple requests sẽ được queue và xử lý tuần tự
const response1 = await handler.makeRequest('twins.chat', { 
  twinId: 'twin_123', 
  message: 'Hello' 
});

const response2 = await handler.makeRequest('twins.chat', { 
  twinId: 'twin_456', 
  message: 'Hi there' 
});
```

### Python Implementation
```python
import asyncio
import time
from typing import List, Dict, Any

class RateLimitHandler:
    def __init__(self, client, max_retries: int = 3):
        self.client = client
        self.max_retries = max_retries
        self.request_times: List[float] = []
        self.rate_limit = 60  # requests per minute
        
    async def make_request(self, method: str, **kwargs) -> Dict[Any, Any]:
        """Make request with automatic rate limiting"""
        await self._wait_if_needed()
        
        for attempt in range(self.max_retries + 1):
            try:
                # Record request time
                self.request_times.append(time.time())
                
                # Make the actual request
                method_func = getattr(self.client, method)
                return await method_func(**kwargs)
                
            except Exception as error:
                if hasattr(error, 'status') and error.status == 429:
                    if attempt < self.max_retries:
                        retry_after = getattr(error, 'retry_after', 2 ** attempt)
                        print(f"Rate limited. Waiting {retry_after}s...")
                        await asyncio.sleep(retry_after)
                        continue
                raise error
    
    async def _wait_if_needed(self):
        """Wait if we're approaching rate limit"""
        now = time.time()
        
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        # If we're at the limit, wait
        if len(self.request_times) >= self.rate_limit:
            sleep_time = 60 - (now - self.request_times[0])
            if sleep_time > 0:
                print(f"Approaching rate limit. Waiting {sleep_time:.1f}s...")
                await asyncio.sleep(sleep_time)

# Usage
handler = RateLimitHandler(client)

# Tự động handle rate limiting
response = await handler.make_request(
    'twins.chat',
    twin_id='twin_123',
    message='Hello'
)
```

## Batch Processing

### Efficient Batch Operations
```javascript
class BatchProcessor {
  constructor(client, batchSize = 10, delayMs = 1000) {
    this.client = client;
    this.batchSize = batchSize;
    this.delayMs = delayMs;
  }

  async processInBatches(items, processor) {
    const results = [];
    
    for (let i = 0; i < items.length; i += this.batchSize) {
      const batch = items.slice(i, i + this.batchSize);
      
      console.log(`Processing batch ${Math.floor(i / this.batchSize) + 1}...`);
      
      const batchPromises = batch.map(item => processor(item));
      const batchResults = await Promise.allSettled(batchPromises);
      
      results.push(...batchResults);
      
      // Wait before next batch (except for last batch)
      if (i + this.batchSize < items.length) {
        await new Promise(resolve => setTimeout(resolve, this.delayMs));
      }
    }
    
    return results;
  }
}

// Usage - Process multiple conversations
const processor = new BatchProcessor(client, 5, 2000);

const conversations = [
  { twinId: 'twin_1', message: 'Hello' },
  { twinId: 'twin_2', message: 'Hi there' },
  // ... more conversations
];

const results = await processor.processInBatches(
  conversations,
  async (conv) => {
    return await client.twins.chat({
      twinId: conv.twinId,
      message: conv.message
    });
  }
);

// Process results
results.forEach((result, index) => {
  if (result.status === 'fulfilled') {
    console.log(`Conversation ${index}: ${result.value.message}`);
  } else {
    console.error(`Conversation ${index} failed: ${result.reason.message}`);
  }
});
```

## Request Optimization

### Connection Pooling
```javascript
import TwinExpert from '@twinexpert/js-sdk';
import { Agent } from 'https';

// Custom HTTP agent with connection pooling
const agent = new Agent({
  keepAlive: true,
  maxSockets: 10,
  maxFreeSockets: 5,
  timeout: 60000,
  freeSocketTimeout: 30000
});

const client = new TwinExpert({
  apiKey: process.env.TWINEXPERT_API_KEY,
  httpAgent: agent
});
```

### Caching Responses
```javascript
class CachingTwinExpert {
  constructor(client, ttlMs = 60000) {
    this.client = client;
    this.cache = new Map();
    this.ttl = ttlMs;
  }

  async chat(twinId, message) {
    const cacheKey = `${twinId}:${message}`;
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.ttl) {
      console.log('Cache hit');
      return cached.data;
    }

    console.log('Cache miss - making API call');
    const response = await this.client.twins.chat({
      twinId,
      message
    });

    this.cache.set(cacheKey, {
      data: response,
      timestamp: Date.now()
    });

    return response;
  }

  clearCache() {
    this.cache.clear();
  }
}

// Usage
const cachingClient = new CachingTwinExpert(client);

// First call - hits API
const response1 = await cachingClient.chat('twin_123', 'What is AI?');

// Second call within TTL - uses cache
const response2 = await cachingClient.chat('twin_123', 'What is AI?');
```

## Monitoring và Analytics

### Request Tracking
```javascript
class RequestTracker {
  constructor() {
    this.requests = [];
    this.rateLimitHits = 0;
    this.errors = [];
  }

  logRequest(endpoint, duration, status) {
    this.requests.push({
      endpoint,
      duration,
      status,
      timestamp: Date.now()
    });

    if (status === 429) {
      this.rateLimitHits++;
    }

    if (status >= 400) {
      this.errors.push({ endpoint, status, timestamp: Date.now() });
    }
  }

  getStats(timeWindowMs = 60000) {
    const now = Date.now();
    const recentRequests = this.requests.filter(
      r => now - r.timestamp < timeWindowMs
    );

    return {
      totalRequests: recentRequests.length,
      avgDuration: recentRequests.reduce((sum, r) => sum + r.duration, 0) / recentRequests.length,
      rateLimitHits: this.rateLimitHits,
      errorRate: this.errors.length / this.requests.length,
      requestsPerMinute: (recentRequests.length / timeWindowMs) * 60000
    };
  }
}

// Usage with client wrapper
const tracker = new RequestTracker();

const trackedClient = {
  async chat(params) {
    const start = Date.now();
    let status = 200;
    
    try {
      const result = await client.twins.chat(params);
      return result;
    } catch (error) {
      status = error.status || 500;
      throw error;
    } finally {
      tracker.logRequest('chat', Date.now() - start, status);
    }
  }
};

// Monitor stats
setInterval(() => {
  const stats = tracker.getStats();
  console.log('API Stats:', stats);
}, 30000);
```

## Enterprise Rate Limiting

### Custom Limits
Enterprise customers có thể request custom rate limits:

```json
{
  "plan": "enterprise",
  "custom_limits": {
    "chat_api": 1000,        // req/min
    "other_apis": 5000,      // req/min
    "monthly_quota": 1000000, // messages
    "concurrent_connections": 100,
    "burst_allowance": 200   // temporary burst above rate limit
  }
}
```

### Distributed Rate Limiting
```javascript
// Redis-based rate limiting for multiple servers
import Redis from 'ioredis';

class DistributedRateLimit {
  constructor(redisUrl, keyPrefix = 'rl:') {
    this.redis = new Redis(redisUrl);
    this.keyPrefix = keyPrefix;
  }

  async checkLimit(apiKey, limit, windowMs) {
    const key = `${this.keyPrefix}${apiKey}`;
    const now = Date.now();
    const windowStart = now - windowMs;

    // Remove old entries and count current requests
    await this.redis.zremrangebyscore(key, 0, windowStart);
    const currentCount = await this.redis.zcard(key);

    if (currentCount >= limit) {
      const oldestRequest = await this.redis.zrange(key, 0, 0, 'WITHSCORES');
      const resetTime = parseInt(oldestRequest[1]) + windowMs;
      
      throw new Error(`Rate limit exceeded. Reset at ${new Date(resetTime)}`);
    }

    // Add current request
    await this.redis.zadd(key, now, `${now}-${Math.random()}`);
    await this.redis.expire(key, Math.ceil(windowMs / 1000));

    return {
      remaining: limit - currentCount - 1,
      resetTime: now + windowMs
    };
  }
}
```

## Best Practices

### 1. Implement Exponential Backoff
```javascript
async function exponentialBackoff(fn, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status !== 429 || attempt === maxRetries) {
        throw error;
      }
      
      const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### 2. Use Request Queuing
```javascript
class RequestQueue {
  constructor(concurrency = 5) {
    this.concurrency = concurrency;
    this.running = 0;
    this.queue = [];
  }

  async add(fn) {
    return new Promise((resolve, reject) => {
      this.queue.push({ fn, resolve, reject });
      this.process();
    });
  }

  async process() {
    if (this.running >= this.concurrency || this.queue.length === 0) {
      return;
    }

    this.running++;
    const { fn, resolve, reject } = this.queue.shift();

    try {
      const result = await fn();
      resolve(result);
    } catch (error) {
      reject(error);
    } finally {
      this.running--;
      this.process();
    }
  }
}
```

### 3. Monitor và Alert
```javascript
// Set up monitoring
function setupRateLimitMonitoring(client) {
  let consecutiveRateLimits = 0;
  
  client.on('response', (response) => {
    if (response.status === 429) {
      consecutiveRateLimits++;
      
      if (consecutiveRateLimits >= 3) {
        // Alert: Too many rate limits
        console.error('WARNING: Multiple consecutive rate limits detected');
        sendAlert('Rate limit threshold exceeded');
      }
    } else {
      consecutiveRateLimits = 0;
    }
  });
}
```

---

**Cần tăng rate limits?**
- 📧 Contact: enterprise@twinexpert.ai  
- 📈 Upgrade plan: [twinexpert.ai/pricing](https://twinexpert.ai/pricing)
- 📊 Analytics: [dashboard.twinexpert.ai](https://dashboard.twinexpert.ai)