# 5.6. Xử lý lỗi

## Tổng quan
Xử lý lỗi đúng cách là yếu tố quan trọng để xây dựng ứng dụng ổn định với TwinExpert API. Tài liệu này cung cấp hướng dẫn chi tiết về các loại lỗi và cách xử lý.

## Error Response Format

Tất cả API errors có format chuẩn:

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "missing_parameter",
    "message": "Missing required parameter: 'message'",
    "param": "message",
    "request_id": "req_123abc456def"
  }
}
```

### Error Object Fields

- `type`: Loại lỗi (xem danh sách bên dưới)
- `code`: Mã lỗi cụ thể
- `message`: Mô tả lỗi cho con người đọc
- `param`: Tham số gây ra lỗi (nếu có)
- `request_id`: ID để debug và support

## HTTP Status Codes

| Status | Meaning | Description |
|--------|---------|-------------|
| 200 | OK | Request thành công |
| 400 | Bad Request | Request không hợp lệ |
| 401 | Unauthorized | API key không hợp lệ |
| 403 | Forbidden | Không có quyền truy cập |
| 404 | Not Found | Resource không tồn tại |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Lỗi server |
| 502 | Bad Gateway | Temporary server issue |
| 503 | Service Unavailable | Service maintenance |

## Error Types

### 1. Authentication Errors (401)

```json
{
  "error": {
    "type": "authentication_error",
    "code": "invalid_api_key",
    "message": "Invalid API key provided"
  }
}
```

**Xử lý:**
```javascript
if (error.status === 401) {
  // API key invalid - user needs to re-authenticate
  console.error('Authentication failed. Please check your API key.');
  redirectToLogin();
}
```

### 2. Permission Errors (403)

```json
{
  "error": {
    "type": "permission_error", 
    "code": "insufficient_permissions",
    "message": "Your API key does not have permission to access this resource"
  }
}
```

**Xử lý:**
```javascript
if (error.status === 403) {
  console.error('Insufficient permissions for this operation');
  showPermissionError();
}
```

### 3. Rate Limit Errors (429)

```json
{
  "error": {
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded", 
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "retry_after": 60
  }
}
```

**Xử lý:**
```javascript
if (error.status === 429) {
  const retryAfter = error.retry_after || 60;
  console.log(`Rate limited. Retrying in ${retryAfter} seconds...`);
  setTimeout(() => retryRequest(), retryAfter * 1000);
}
```

### 4. Validation Errors (422)

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "validation_error",
    "message": "Twin name must be between 1 and 100 characters",
    "param": "name"
  }
}
```

### 5. Server Errors (500+)

```json
{
  "error": {
    "type": "api_error",
    "code": "internal_error", 
    "message": "An internal error occurred. Please try again later."
  }
}
```

## JavaScript Error Handling

### Basic Error Handling
```javascript
import TwinExpert from '@twinexpert/js-sdk';

const client = new TwinExpert({
  apiKey: process.env.TWINEXPERT_API_KEY
});

async function chatWithErrorHandling(twinId, message) {
  try {
    const response = await client.twins.chat({
      twinId,
      message
    });
    return response;
  } catch (error) {
    console.error('Chat error:', error);
    
    switch (error.status) {
      case 400:
        throw new Error('Invalid request. Please check your input.');
        
      case 401:
        throw new Error('Authentication failed. Please check your API key.');
        
      case 403:
        throw new Error('Permission denied. Upgrade your plan or check API key permissions.');
        
      case 404:
        throw new Error(`Twin ${twinId} not found.`);
        
      case 422:
        throw new Error(`Validation error: ${error.message}`);
        
      case 429:
        throw new Error('Rate limit exceeded. Please try again later.');
        
      case 500:
      case 502:
      case 503:
        throw new Error('Server error. Please try again later.');
        
      default:
        throw new Error(`Unknown error: ${error.message}`);
    }
  }
}
```

### Advanced Error Handler Class
```javascript
class TwinExpertErrorHandler {
  constructor(options = {}) {
    this.maxRetries = options.maxRetries || 3;
    this.baseDelay = options.baseDelay || 1000;
    this.onError = options.onError || console.error;
  }

  async executeWithRetry(operation, context = {}) {
    let lastError;
    
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error;
        
        // Log error
        this.onError(`Attempt ${attempt} failed:`, {
          error: error.message,
          status: error.status,
          context
        });

        // Don't retry certain errors
        if (this.shouldNotRetry(error)) {
          throw this.transformError(error);
        }

        // Don't wait after last attempt
        if (attempt === this.maxRetries) {
          break;
        }

        // Calculate delay (exponential backoff)
        const delay = this.calculateDelay(attempt, error);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    throw this.transformError(lastError);
  }

  shouldNotRetry(error) {
    // Don't retry client errors (4xx except 429)
    return error.status >= 400 && error.status < 500 && error.status !== 429;
  }

  calculateDelay(attempt, error) {
    // Use retry_after header for rate limits
    if (error.status === 429 && error.retry_after) {
      return error.retry_after * 1000;
    }

    // Exponential backoff for other errors
    return this.baseDelay * Math.pow(2, attempt - 1);
  }

  transformError(error) {
    const userFriendlyMessages = {
      401: 'Please check your API key and try again.',
      403: 'You don\'t have permission to perform this action.',
      404: 'The requested resource was not found.',
      422: 'Please check your input and try again.',
      429: 'Too many requests. Please wait a moment and try again.',
      500: 'Server error. Please try again later.',
      502: 'Service temporarily unavailable. Please try again.',
      503: 'Service under maintenance. Please try again later.'
    };

    return new Error(
      userFriendlyMessages[error.status] || 
      `Unexpected error: ${error.message}`
    );
  }
}

// Usage
const errorHandler = new TwinExpertErrorHandler({
  maxRetries: 3,
  onError: (message, details) => {
    console.error(message, details);
    // Send to logging service
    logger.error(message, details);
  }
});

const response = await errorHandler.executeWithRetry(
  () => client.twins.chat({ twinId: 'twin_123', message: 'Hello' }),
  { operation: 'chat', twinId: 'twin_123' }
);
```

## Python Error Handling

### Using try/except
```python
import twinexpert
from twinexpert.exceptions import (
    TwinExpertError,
    AuthenticationError,
    PermissionError,
    RateLimitError,
    ValidationError,
    APIError
)

client = twinexpert.TwinExpert(api_key=os.environ['TWINEXPERT_API_KEY'])

def chat_with_error_handling(twin_id: str, message: str):
    try:
        response = client.twins.chat(
            twin_id=twin_id,
            message=message
        )
        return response
    
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        # Handle auth error - maybe refresh token
        
    except PermissionError as e:
        print(f"Permission denied: {e}")
        # Handle permission error
        
    except RateLimitError as e:
        print(f"Rate limited: {e}")
        # Wait and retry
        time.sleep(e.retry_after or 60)
        return chat_with_error_handling(twin_id, message)
        
    except ValidationError as e:
        print(f"Validation error: {e}")
        # Handle validation error
        
    except APIError as e:
        print(f"API error: {e}")
        # Handle server errors
        
    except TwinExpertError as e:
        print(f"General TwinExpert error: {e}")
        # Handle any other TwinExpert errors
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Handle unexpected errors
```

### Decorator for Error Handling
```python
import functools
import time
import random

def handle_twinexpert_errors(max_retries=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                
                except RateLimitError as e:
                    if attempt == max_retries:
                        raise
                    
                    delay = e.retry_after or (base_delay * (2 ** attempt))
                    print(f"Rate limited. Waiting {delay}s before retry...")
                    time.sleep(delay)
                    last_exception = e
                    
                except (APIError, ConnectionError) as e:
                    if attempt == max_retries:
                        raise
                    
                    # Exponential backoff with jitter
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"Server error. Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    last_exception = e
                    
                except (AuthenticationError, PermissionError, ValidationError):
                    # Don't retry these errors
                    raise
                    
            raise last_exception
            
        return wrapper
    return decorator

# Usage
@handle_twinexpert_errors(max_retries=3)
def create_twin(name: str, instructions: str):
    return client.twins.create(
        name=name,
        instructions=instructions
    )
```

## Error Monitoring

### Structured Logging
```javascript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

class MonitoredTwinExpert {
  constructor(client) {
    this.client = client;
  }

  async chat(params) {
    const startTime = Date.now();
    let success = false;
    
    try {
      const result = await this.client.twins.chat(params);
      success = true;
      
      logger.info('API call successful', {
        operation: 'chat',
        twinId: params.twinId,
        duration: Date.now() - startTime,
        success: true
      });
      
      return result;
    } catch (error) {
      logger.error('API call failed', {
        operation: 'chat',
        twinId: params.twinId,
        duration: Date.now() - startTime,
        success: false,
        error: {
          status: error.status,
          type: error.type,
          code: error.code,
          message: error.message,
          requestId: error.request_id
        }
      });
      
      throw error;
    }
  }
}
```

### Error Metrics
```javascript
class ErrorMetrics {
  constructor() {
    this.metrics = {
      totalRequests: 0,
      totalErrors: 0,
      errorsByStatus: {},
      errorsByType: {},
      responseTimeSum: 0
    };
  }

  recordRequest(duration, error = null) {
    this.metrics.totalRequests++;
    this.metrics.responseTimeSum += duration;

    if (error) {
      this.metrics.totalErrors++;
      
      const status = error.status || 'unknown';
      this.metrics.errorsByStatus[status] = 
        (this.metrics.errorsByStatus[status] || 0) + 1;
        
      const type = error.type || 'unknown';
      this.metrics.errorsByType[type] = 
        (this.metrics.errorsByType[type] || 0) + 1;
    }
  }

  getStats() {
    return {
      totalRequests: this.metrics.totalRequests,
      errorRate: this.metrics.totalErrors / this.metrics.totalRequests,
      avgResponseTime: this.metrics.responseTimeSum / this.metrics.totalRequests,
      errorsByStatus: this.metrics.errorsByStatus,
      errorsByType: this.metrics.errorsByType
    };
  }

  reset() {
    this.metrics = {
      totalRequests: 0,
      totalErrors: 0,
      errorsByStatus: {},
      errorsByType: {},
      responseTimeSum: 0
    };
  }
}

// Usage
const metrics = new ErrorMetrics();

setInterval(() => {
  const stats = metrics.getStats();
  console.log('Error Statistics:', stats);
  
  // Send to monitoring service
  sendToMonitoring(stats);
  
  metrics.reset();
}, 60000); // Every minute
```

## Best Practices

### 1. Implement Circuit Breaker
```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async execute(operation) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}
```

### 2. User-Friendly Error Messages
```javascript
const errorMessages = {
  'rate_limit_exceeded': 'You\'re sending messages too quickly. Please wait a moment and try again.',
  'invalid_api_key': 'There\'s an issue with your account. Please contact support.',
  'insufficient_permissions': 'You don\'t have permission to perform this action.',
  'twin_not_found': 'The AI assistant you\'re trying to reach is not available.',
  'validation_error': 'Please check your input and try again.',
  'internal_error': 'Something went wrong on our end. Please try again in a moment.'
};

function getUserFriendlyMessage(error) {
  return errorMessages[error.code] || 
         'An unexpected error occurred. Please try again.';
}
```

### 3. Progressive Error Handling
```javascript
class ProgressiveErrorHandler {
  constructor() {
    this.errorCounts = new Map();
    this.userNotified = new Set();
  }

  handleError(error, userId) {
    const errorKey = `${error.type}_${error.code}`;
    const count = this.errorCounts.get(errorKey) || 0;
    this.errorCounts.set(errorKey, count + 1);

    // Progressive response based on error frequency
    if (count === 1) {
      // First occurrence - show simple retry message
      this.showRetryMessage(error);
    } else if (count === 3) {
      // Third occurrence - suggest checking documentation
      this.showDocumentationSuggestion(error);
    } else if (count >= 5 && !this.userNotified.has(userId)) {
      // Frequent errors - offer to contact support
      this.offerSupport(error, userId);
      this.userNotified.add(userId);
    }
  }

  showRetryMessage(error) {
    console.log('Temporary issue. Please try again.');
  }

  showDocumentationSuggestion(error) {
    console.log('Having trouble? Check our documentation at docs.twinexpert.ai');
  }

  offerSupport(error, userId) {
    console.log('Persistent issues detected. Contact support: support@twinexpert.ai');
  }
}
```

## Testing Error Scenarios

### Mock Error Responses
```javascript
// Jest test example
describe('Error Handling', () => {
  test('should handle rate limit errors', async () => {
    // Mock rate limit response
    mockTwinExpert.twins.chat.mockRejectedValueOnce({
      status: 429,
      type: 'rate_limit_error',
      code: 'rate_limit_exceeded',
      retry_after: 60
    });

    const handler = new TwinExpertErrorHandler();
    
    await expect(
      handler.executeWithRetry(() => mockTwinExpert.twins.chat({}))
    ).rejects.toThrow('Too many requests');
  });

  test('should retry server errors', async () => {
    // Mock server error then success
    mockTwinExpert.twins.chat
      .mockRejectedValueOnce({ status: 500 })
      .mockResolvedValueOnce({ message: 'Success' });

    const handler = new TwinExpertErrorHandler();
    const result = await handler.executeWithRetry(
      () => mockTwinExpert.twins.chat({})
    );

    expect(result.message).toBe('Success');
    expect(mockTwinExpert.twins.chat).toHaveBeenCalledTimes(2);
  });
});
```

---

**Cần hỗ trợ debug errors?**
- 📧 Support: developers@twinexpert.ai
- 📖 Status Page: [status.twinexpert.ai](https://status.twinexpert.ai)
- 💬 Discord: [discord.gg/twinexpert](https://discord.gg/twinexpert)