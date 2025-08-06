# 5.6. Xử lý lỗi

Tìm hiểu cách xử lý các error scenarios khi làm việc với TwinExpert API. Từ HTTP status codes đến best practices cho error recovery.

## 🚨 Error Response Format

Tất cả errors từ TwinExpert API đều có format chuẩn:

```json
{
  "error": {
    "code": "error_code",
    "message": "Human readable error message",
    "details": "Detailed explanation of the error",
    "request_id": "req_12345abcde",
    "timestamp": "2024-01-01T12:00:00Z",
    "documentation_url": "https://docs.twinexpert.com/api/errors#error_code"
  }
}
```

## 📋 HTTP Status Codes

### 400 Bad Request
Request không hợp lệ hoặc thiếu parameters bắt buộc.

**Common causes:**
- Missing required fields
- Invalid parameter values
- Malformed JSON
- Invalid expert ID

**Example:**
```json
{
  "error": {
    "code": "bad_request",
    "message": "Invalid request parameters",
    "details": "The 'expert' field is required and must be a valid expert ID",
    "request_id": "req_abc123"
  }
}
```

**Cách xử lý:**
```javascript
if (error.response?.status === 400) {
  const errorData = error.response.data.error;
  console.error(`Validation Error: ${errorData.message}`);
  console.error(`Details: ${errorData.details}`);
  
  // Fix the request parameters and retry
  // Don't retry automatically - fix the issue first
}
```

### 401 Unauthorized
API key không hợp lệ, thiếu, hoặc đã hết hạn.

**Common causes:**
- Missing Authorization header
- Invalid API key format
- Expired API key
- Revoked API key

**Example:**
```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or missing API key",
    "details": "The API key provided is either invalid, expired, or missing from the Authorization header",
    "request_id": "req_def456"
  }
}
```

**Cách xử lý:**
```javascript
if (error.response?.status === 401) {
  console.error('Authentication failed. Check your API key.');
  
  // Check API key configuration
  if (!process.env.TWIN_API_KEY) {
    throw new Error('TWIN_API_KEY environment variable is not set');
  }
  
  // Verify API key format
  if (!process.env.TWIN_API_KEY.startsWith('tk_')) {
    throw new Error('Invalid API key format. Should start with tk_');
  }
  
  // Don't retry - fix authentication first
}
```

### 403 Forbidden
API key hợp lệ nhưng không có quyền truy cập resource này.

**Common causes:**
- Insufficient plan permissions
- Account suspended
- Expert not available for your plan
- Feature not included in current plan

**Example:**
```json
{
  "error": {
    "code": "forbidden",
    "message": "Insufficient permissions",
    "details": "The 'creative_director' expert is only available on Pro and Enterprise plans",
    "request_id": "req_ghi789",
    "upgrade_info": {
      "current_plan": "free",
      "required_plan": "pro",
      "upgrade_url": "https://twinexpert.com/upgrade"
    }
  }
}
```

**Cách xử lý:**
```javascript
if (error.response?.status === 403) {
  const errorData = error.response.data.error;
  
  if (errorData.upgrade_info) {
    console.error(`Plan upgrade required: ${errorData.upgrade_info.current_plan} → ${errorData.upgrade_info.required_plan}`);
    console.error(`Upgrade at: ${errorData.upgrade_info.upgrade_url}`);
  }
  
  // Handle gracefully - maybe fallback to available expert
  // Don't retry with same parameters
}
```

### 404 Not Found
Resource không tồn tại.

**Common causes:**
- Invalid expert ID
- Conversation not found
- File not found
- Project not found

**Example:**
```json
{
  "error": {
    "code": "not_found",
    "message": "Resource not found",
    "details": "Expert 'invalid_expert' does not exist",
    "request_id": "req_jkl012",
    "available_experts": ["marketing", "copywriter", "social_media"]
  }
}
```

### 422 Unprocessable Entity
Request format đúng nhưng nội dung không thể xử lý.

**Common causes:**
- Message too long
- Unsupported file format
- Context too complex
- Invalid combination of parameters

**Example:**
```json
{
  "error": {
    "code": "unprocessable_entity",
    "message": "Request cannot be processed",
    "details": "Message exceeds maximum length of 4000 characters",
    "request_id": "req_mno345",
    "limits": {
      "max_message_length": 4000,
      "current_message_length": 5200
    }
  }
}
```

### 429 Too Many Requests
Vượt quá rate limit.

**Example:**
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Too many requests",
    "details": "You have exceeded your hourly rate limit of 1000 requests",
    "request_id": "req_pqr678",
    "retry_after": 3600,
    "rate_limit_info": {
      "limit": 1000,
      "used": 1000,
      "reset_time": "2024-01-01T15:00:00Z"
    }
  }
}
```

**Cách xử lý:**
```javascript
if (error.response?.status === 429) {
  const retryAfter = error.response.headers['retry-after'] || 
                     error.response.data.error.retry_after;
  
  console.log(`Rate limited. Retrying after ${retryAfter} seconds`);
  
  // Wait and retry
  await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
  return await retryRequest();
}
```

### 500 Internal Server Error
Lỗi server, vui lòng thử lại sau.

**Example:**
```json
{
  "error": {
    "code": "internal_server_error",
    "message": "Something went wrong on our end",
    "details": "Our engineering team has been notified and is working on a fix",
    "request_id": "req_stu901"
  }
}
```

### 502/503/504 Service Unavailable
Service tạm thời không khả dụng.

## 🛠️ Comprehensive Error Handling

### 1. Basic Error Handler

```javascript
class APIError extends Error {
  constructor(response) {
    super(response.data?.error?.message || 'Unknown API error');
    this.name = 'APIError';
    this.status = response.status;
    this.code = response.data?.error?.code;
    this.details = response.data?.error?.details;
    this.requestId = response.data?.error?.request_id;
  }
}

function handleAPIError(error) {
  if (!error.response) {
    // Network error
    throw new Error(`Network error: ${error.message}`);
  }

  const apiError = new APIError(error.response);
  
  switch (apiError.status) {
    case 400:
      throw new Error(`Validation Error: ${apiError.message}. ${apiError.details}`);
    case 401:
      throw new Error('Authentication failed: Please check your API key');
    case 403:
      throw new Error(`Permission denied: ${apiError.message}`);
    case 404:
      throw new Error(`Not found: ${apiError.message}`);
    case 422:
      throw new Error(`Invalid request: ${apiError.details}`);
    case 429:
      throw new Error(`Rate limited: ${apiError.message}`);
    case 500:
    case 502:
    case 503:
    case 504:
      throw new Error(`Server error: ${apiError.message}. Request ID: ${apiError.requestId}`);
    default:
      throw apiError;
  }
}

// Sử dụng
try {
  const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', requestData);
  return response.data;
} catch (error) {
  handleAPIError(error);
}
```

### 2. Advanced Error Handler với Retry Logic

```javascript
class TwinExpertClient {
  constructor(apiKey, options = {}) {
    this.apiKey = apiKey;
    this.baseURL = 'https://api.twinexpert.com/v1';
    this.maxRetries = options.maxRetries || 3;
    this.retryDelay = options.retryDelay || 1000;
    this.timeout = options.timeout || 30000;
  }

  async callExpert(expert, message, context = {}, options = {}) {
    const requestOptions = {
      maxRetries: options.maxRetries || this.maxRetries,
      retryDelay: options.retryDelay || this.retryDelay
    };

    return await this.executeWithRetry(
      () => this.makeRequest(expert, message, context),
      requestOptions
    );
  }

  async executeWithRetry(requestFn, options) {
    let lastError;

    for (let attempt = 1; attempt <= options.maxRetries; attempt++) {
      try {
        return await requestFn();
      } catch (error) {
        lastError = error;
        
        // Check if we should retry
        if (!this.shouldRetry(error) || attempt === options.maxRetries) {
          break;
        }

        // Calculate delay with exponential backoff
        const delay = this.calculateRetryDelay(error, attempt, options.retryDelay);
        
        console.log(`Attempt ${attempt} failed: ${error.message}. Retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    throw this.enhanceError(lastError);
  }

  shouldRetry(error) {
    if (!error.response) return true; // Network errors

    const status = error.response.status;
    const retryableStatuses = [429, 500, 502, 503, 504];
    
    return retryableStatuses.includes(status);
  }

  calculateRetryDelay(error, attempt, baseDelay) {
    // Use retry-after header if available
    if (error.response?.headers['retry-after']) {
      return parseInt(error.response.headers['retry-after']) * 1000;
    }

    // Exponential backoff with jitter
    const exponentialDelay = baseDelay * Math.pow(2, attempt - 1);
    const jitter = Math.random() * 0.1 * exponentialDelay;
    
    return Math.min(exponentialDelay + jitter, 30000); // Max 30 seconds
  }

  enhanceError(error) {
    if (!error.response) {
      return new Error(`Network error: ${error.message}`);
    }

    const { status, data } = error.response;
    const errorInfo = data?.error || {};

    const enhancedError = new Error(errorInfo.message || `HTTP ${status} error`);
    enhancedError.status = status;
    enhancedError.code = errorInfo.code;
    enhancedError.details = errorInfo.details;
    enhancedError.requestId = errorInfo.request_id;
    
    // Add helpful context
    switch (status) {
      case 400:
        enhancedError.type = 'VALIDATION_ERROR';
        enhancedError.fix = 'Check request parameters and format';
        break;
      case 401:
        enhancedError.type = 'AUTHENTICATION_ERROR';
        enhancedError.fix = 'Verify API key is correct and not expired';
        break;
      case 403:
        enhancedError.type = 'PERMISSION_ERROR';
        enhancedError.fix = 'Upgrade plan or check resource permissions';
        break;
      case 404:
        enhancedError.type = 'NOT_FOUND_ERROR';
        enhancedError.fix = 'Check resource ID and endpoint URL';
        break;
      case 429:
        enhancedError.type = 'RATE_LIMIT_ERROR';
        enhancedError.fix = 'Implement rate limiting or upgrade plan';
        break;
      case 500:
        enhancedError.type = 'SERVER_ERROR';
        enhancedError.fix = 'Retry later or contact support';
        break;
    }

    return enhancedError;
  }

  async makeRequest(expert, message, context) {
    try {
      const response = await axios.post(`${this.baseURL}/chat/completions`, {
        expert,
        message,
        context
      }, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        timeout: this.timeout
      });

      return response.data;
    } catch (error) {
      // Add request context to error
      if (error.response) {
        error.response.requestContext = { expert, message: message.substring(0, 100) };
      }
      throw error;
    }
  }
}

// Sử dụng Advanced Client
const client = new TwinExpertClient(process.env.TWIN_API_KEY, {
  maxRetries: 3,
  retryDelay: 1000,
  timeout: 30000
});

try {
  const result = await client.callExpert('marketing', 'Create campaign strategy');
  console.log('Success:', result.response);
} catch (error) {
  console.error(`Error Type: ${error.type}`);
  console.error(`Message: ${error.message}`);
  console.error(`Suggested Fix: ${error.fix}`);
  if (error.requestId) {
    console.error(`Request ID: ${error.requestId} (for support)`);
  }
}
```

### 3. Circuit Breaker Pattern

```javascript
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 60000;
    this.monitoringWindow = options.monitoringWindow || 10000;
    
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.requests = [];
  }

  async execute(requestFn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        this.state = 'HALF_OPEN';
        console.log('Circuit breaker: HALF_OPEN');
      } else {
        throw new Error('Circuit breaker is OPEN - service temporarily unavailable');
      }
    }

    try {
      const result = await requestFn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    if (this.state === 'HALF_OPEN') {
      this.state = 'CLOSED';
      console.log('Circuit breaker: CLOSED');
    }
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    // Clean old requests
    const cutoff = Date.now() - this.monitoringWindow;
    this.requests = this.requests.filter(time => time > cutoff);
    this.requests.push(Date.now());

    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      console.log('Circuit breaker: OPEN');
    }
  }

  getStatus() {
    return {
      state: this.state,
      failureCount: this.failureCount,
      recentRequests: this.requests.length
    };
  }
}

// Sử dụng Circuit Breaker
const circuitBreaker = new CircuitBreaker({
  failureThreshold: 3,
  resetTimeout: 30000,
  monitoringWindow: 60000
});

async function robustAPICall(expert, message) {
  try {
    return await circuitBreaker.execute(async () => {
      const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', {
        expert, message
      }, {
        headers: { 'Authorization': `Bearer ${process.env.TWIN_API_KEY}` }
      });
      return response.data;
    });
  } catch (error) {
    console.error('Request failed:', error.message);
    
    const status = circuitBreaker.getStatus();
    console.log('Circuit breaker status:', status);
    
    if (status.state === 'OPEN') {
      console.log('Service temporarily unavailable. Try again later.');
    }
    
    throw error;
  }
}
```

### 4. Logging & Monitoring

```javascript
class ErrorLogger {
  constructor() {
    this.errors = [];
    this.maxLogSize = 1000;
  }

  logError(error, context = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      error: {
        message: error.message,
        status: error.status,
        code: error.code,
        requestId: error.requestId
      },
      context,
      stack: error.stack
    };

    this.errors.push(logEntry);
    
    // Keep log size manageable
    if (this.errors.length > this.maxLogSize) {
      this.errors = this.errors.slice(-this.maxLogSize);
    }

    // Send to external monitoring (optional)
    this.sendToMonitoring(logEntry);
    
    console.error('API Error:', logEntry);
  }

  sendToMonitoring(logEntry) {
    // Send to services like Sentry, LogRocket, etc.
    // Sentry.captureException(logEntry);
  }

  getErrorStats() {
    const now = Date.now();
    const lastHour = this.errors.filter(e => 
      new Date(e.timestamp).getTime() > now - 3600000
    );

    const errorCounts = {};
    lastHour.forEach(e => {
      const code = e.error.code || 'unknown';
      errorCounts[code] = (errorCounts[code] || 0) + 1;
    });

    return {
      totalErrors: lastHour.length,
      errorTypes: errorCounts,
      timeRange: 'last_hour'
    };
  }
}

// Global error logger
const errorLogger = new ErrorLogger();

// Enhanced client with logging
class LoggedTwinClient extends TwinExpertClient {
  async callExpert(expert, message, context = {}) {
    try {
      return await super.callExpert(expert, message, context);
    } catch (error) {
      errorLogger.logError(error, { expert, message: message.substring(0, 100) });
      throw error;
    }
  }
}

// Usage with monitoring
const client = new LoggedTwinClient(process.env.TWIN_API_KEY);

// Monitor error stats periodically
setInterval(() => {
  const stats = errorLogger.getErrorStats();
  if (stats.totalErrors > 0) {
    console.log('📊 Error Stats:', stats);
  }
}, 5 * 60 * 1000); // Every 5 minutes
```

## 🔧 Error Prevention

### 1. Request Validation

```javascript
function validateRequest(expert, message, context = {}) {
  const errors = [];

  // Validate expert
  const validExperts = ['marketing', 'copywriter', 'social_media', 'business_analyst'];
  if (!expert || !validExperts.includes(expert)) {
    errors.push(`Invalid expert. Must be one of: ${validExperts.join(', ')}`);
  }

  // Validate message
  if (!message || typeof message !== 'string') {
    errors.push('Message is required and must be a string');
  } else if (message.length > 4000) {
    errors.push('Message must be less than 4000 characters');
  } else if (message.length < 10) {
    errors.push('Message must be at least 10 characters');
  }

  // Validate context
  if (context && typeof context !== 'object') {
    errors.push('Context must be an object');
  }

  if (errors.length > 0) {
    throw new Error(`Validation failed: ${errors.join('; ')}`);
  }
}

// Usage
try {
  validateRequest('marketing', 'Create campaign strategy for new product launch');
  // Proceed with API call
} catch (error) {
  console.error('Validation error:', error.message);
  // Fix issues before making API call
}
```

### 2. Health Check

```javascript
async function checkAPIHealth() {
  try {
    const response = await axios.get('https://api.twinexpert.com/v1/health', {
      headers: { 'Authorization': `Bearer ${process.env.TWIN_API_KEY}` },
      timeout: 5000
    });

    return {
      healthy: response.status === 200,
      latency: response.headers['x-response-time'],
      version: response.data.version
    };
  } catch (error) {
    return {
      healthy: false,
      error: error.message,
      status: error.response?.status
    };
  }
}

// Check before important operations
async function safeAPICall(expert, message) {
  const health = await checkAPIHealth();
  
  if (!health.healthy) {
    console.warn('API health check failed:', health.error);
    // Maybe use fallback or queue request
  }
  
  return await callExpert(expert, message);
}
```

## 📚 Error Handling Best Practices

### ✅ Do's

1. **Always handle errors explicitly**
```javascript
// ✅ Good
try {
  const result = await callExpert('marketing', message);
  return result;
} catch (error) {
  // Handle specific error types
  if (error.status === 429) {
    // Rate limit handling
  } else if (error.status === 401) {
    // Auth error handling
  }
  throw error;
}
```

2. **Use request IDs for debugging**
```javascript
catch (error) {
  console.error(`Request failed (ID: ${error.requestId}):`, error.message);
}
```

3. **Implement proper retry logic**
```javascript
// ✅ Good - with exponential backoff
const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
```

4. **Log errors with context**
```javascript
// ✅ Good
logger.error('API call failed', {
  expert,
  message: message.substring(0, 100),
  error: error.message,
  requestId: error.requestId
});
```

### ❌ Don'ts

1. **Don't ignore errors**
```javascript
// ❌ Bad
try {
  await callExpert('marketing', message);
} catch (error) {
  // Ignoring error
}
```

2. **Don't retry non-retryable errors**
```javascript
// ❌ Bad - retrying validation errors
if (error.status === 400) {
  await retry(); // Will keep failing
}
```

3. **Don't expose sensitive error details**
```javascript
// ❌ Bad - exposing internal details
return res.status(500).json({ error: error.stack });

// ✅ Good - user-friendly message
return res.status(500).json({ 
  error: 'Internal server error',
  requestId: error.requestId 
});
```

4. **Don't hardcode retry delays**
```javascript
// ❌ Bad
setTimeout(retry, 5000); // Fixed delay

// ✅ Good
const retryAfter = error.response.headers['retry-after'] || 5;
setTimeout(retry, retryAfter * 1000);
```

---

**🎯 Summary**: Proper error handling là key để build robust applications với TwinExpert API. Implement retry logic, monitor errors, và luôn provide meaningful feedback cho users.

