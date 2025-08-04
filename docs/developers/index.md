# 5. DÀNH CHO NHÀ PHÁT TRIỂN (TwinExpert API Documentation)

Tích hợp AI twins vào ứng dụng của bạn với API RESTful mạnh mẽ và dễ sử dụng.

<div class="api-actions">
  <div class="action-card">
    <a href="./bat-dau-voi-api" class="action-button primary">
      <span class="button-icon">🚀</span>
      <span class="button-text">Bắt Đầu</span>
    </a>
  </div>

  <div class="action-card">
    <a href="https://twinexpert.com/profile/api-keys" class="action-button primary" target="_blank">
      <span class="button-icon">🔑</span>
      <span class="button-text">Lấy API Key</span>
    </a>
  </div>

  <div class="action-card">
    <a href="https://api.twinexpert.com/api/v1/docs" class="action-button primary" target="_blank">
      <span class="button-icon">🛡️</span>
      <span class="button-text">Tài liệu API</span>
    </a>
  </div>
</div>

## 📋 Nội dung tài liệu

<div class="docs-grid">
  <div class="doc-section">
    <h3><a href="./bat-dau-voi-api">5.1. Bắt đầu với API</a></h3>
    <p>Hướng dẫn nhanh để bắt đầu sử dụng TwinExpert API, yêu cầu hệ thống và cài đặt.</p>
    <ul>
      <li>Quickstart guide</li>
      <li>Environment setup</li>
      <li>First API call</li>
    </ul>
  </div>

  <div class="doc-section">
    <h3><a href="./xac-thuc">5.2. Xác thực</a></h3>
    <p>Tìm hiểu về các phương thức xác thực và bảo mật API.</p>
    <ul>
      <li>API Key authentication</li>
      <li>Bearer tokens</li>
      <li>Security best practices</li>
    </ul>
  </div>

  <div class="doc-section">
    <h3><a href="./api-endpoints">5.3. API Endpoints</a></h3>
    <p>Danh sách đầy đủ các API endpoints và cách sử dụng.</p>
    <ul>
      <li>Twin management</li>
      <li>Conversation API</li>
      <li>Knowledge base</li>
    </ul>
  </div>

  <div class="doc-section">
    <h3><a href="./vi-du">5.4. Ví dụ</a></h3>
    <p>Các ví dụ thực tế và code samples cho different use cases.</p>
    <ul>
      <li>Basic integration</li>
      <li>Advanced features</li>
      <li>Multiple languages</li>
    </ul>
  </div>

  <div class="doc-section">
    <h3><a href="./rate-limiting">5.5. Rate Limiting</a></h3>
    <p>Hiểu về giới hạn tốc độ và cách tối ưu hóa API calls.</p>
    <ul>
      <li>Rate limits</li>
      <li>Quota management</li>
      <li>Optimization tips</li>
    </ul>
  </div>

  <div class="doc-section">
    <h3><a href="./xu-ly-loi">5.6. Xử lý lỗi</a></h3>
    <p>Cách xử lý lỗi và troubleshooting các vấn đề thường gặp.</p>
    <ul>
      <li>Error codes</li>
      <li>Common issues</li>
      <li>Debug strategies</li>
    </ul>
  </div>
</div>

## �️ Tài nguyên phát triển

<div class="dev-resources">
  <div class="resource-item">
    <h4>📚 SDKs & Libraries</h4>
    <p>Official SDKs cho các ngôn ngữ phổ biến:</p>
    <ul>
      <li>JavaScript/Node.js</li>
      <li>Python</li>
      <li>PHP</li>
      <li>Java</li>
    </ul>
  </div>

  <div class="resource-item">
    <h4>🧪 Testing Tools</h4>
    <p>Tools để test và debug API:</p>
    <ul>
      <li>Postman Collection</li>
      <li>OpenAPI Spec</li>
      <li>Swagger UI</li>
      <li>Test Environment</li>
    </ul>
  </div>

  <div class="resource-item">
    <h4>📖 Code Examples</h4>
    <p>Ví dụ implementation:</p>
    <ul>
      <li>Basic chatbot</li>
      <li>Knowledge Q&A</li>
      <li>Multi-twin system</li>
      <li>Webhook integration</li>
    </ul>
  </div>
</div>

<style>
.api-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.action-card {
  display: flex;
  justify-content: center;
}

.action-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: var(--vp-c-brand);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  min-width: 160px;
  justify-content: center;
}

.action-button:hover {
  background: var(--vp-c-brand-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.button-icon {
  font-size: 1.2em;
}

.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.doc-section {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.doc-section:hover {
  border-color: var(--vp-c-brand);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.doc-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
}

.doc-section h3 a {
  color: var(--vp-c-text-1);
  text-decoration: none;
}

.doc-section h3 a:hover {
  color: var(--vp-c-brand);
}

.doc-section p {
  margin: 0 0 1rem 0;
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.doc-section ul {
  margin: 0;
  padding-left: 1rem;
  color: var(--vp-c-text-2);
}

.doc-section li {
  margin: 0.25rem 0;
}

.dev-resources {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.resource-item {
  background: var(--vp-c-bg-alt);
  border-radius: 8px;
  padding: 1.5rem;
  border-left: 4px solid var(--vp-c-brand);
}

.resource-item h4 {
  margin: 0 0 1rem 0;
  color: var(--vp-c-text-1);
  font-size: 1.1rem;
}

.resource-item p {
  margin: 0 0 1rem 0;
  color: var(--vp-c-text-2);
  font-size: 0.95rem;
}

.resource-item ul {
  margin: 0;
  padding-left: 1rem;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
}

.resource-item li {
  margin: 0.25rem 0;
}

@media (max-width: 768px) {
  .api-actions {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .action-button {
    padding: 0.875rem 1.5rem;
    font-size: 1rem;
  }
  
  .docs-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .doc-section {
    padding: 1rem;
  }
  
  .dev-resources {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .resource-item {
    padding: 1rem;
  }
}
</style>
- Cách lấy và sử dụng API keys
- Token-based authentication
- Security best practices

### 🔌 [5.3. API Endpoints](./endpoints)
- Danh sách đầy đủ các endpoints
- Request/response schemas
- Code examples cho từng endpoint

### 💡 [5.4. Ví dụ](./examples)
- Ví dụ thực tế với code samples
- Use cases phổ biến
- Best practices và patterns

### ⚡ [5.5. Rate Limiting](./rate-limiting)
- Giới hạn request rate
- Quota management
- Cách xử lý rate limit errors

### 🚨 [5.6. Xử lý lỗi](./error-handling)
- Error codes và messages
- Cách xử lý exceptions
- Debugging và troubleshooting

## Base URL

```
Production: https://api.twinexpert.ai/v1
Staging: https://staging-api.twinexpert.ai/v1
```

## Supported Languages

TwinExpert API cung cấp SDKs chính thức cho:

- **JavaScript/Node.js** - [@twinexpert/js-sdk](https://npm.im/@twinexpert/js-sdk)
- **Python** - [twinexpert-python](https://pypi.org/project/twinexpert/)
- **PHP** - [twinexpert/php-sdk](https://packagist.org/packages/twinexpert/php-sdk)
- **Java** - [com.twinexpert:java-sdk](https://central.sonatype.com/artifact/com.twinexpert/java-sdk)

## Quick Start

Bắt đầu trong 5 phút với ví dụ đơn giản:

```javascript
import TwinExpert from '@twinexpert/js-sdk';

const client = new TwinExpert({
  apiKey: 'your-api-key-here'
});

// Tạo conversation với AI twin
const response = await client.twins.chat({
  twinId: 'twin_123',
  message: 'Xin chào, bạn có thể giúp tôi không?'
});

console.log(response.message);
```

## Support & Community

- 📧 **Developer Support**: developers@twinexpert.ai
- 📚 **Documentation**: [docs.twinexpert.ai](https://docs.twinexpert.ai)
- 💬 **Discord**: [discord.gg/twinexpert](https://discord.gg/twinexpert)
- 🐛 **Issue Tracker**: [github.com/twinexpert/issues](https://github.com/twinexpert/issues)

---

*Sẵn sàng bắt đầu? Hãy chuyển đến [5.1. Bắt đầu với API](./getting-started) để bắt đầu journey phát triển với TwinExpert API!*