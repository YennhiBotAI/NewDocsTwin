# 5.4. Ví dụ

Tìm hiểu cách tích hợp TwinExpert API vào ứng dụng của bạn qua các ví dụ thực tế. Từ basic đến advanced use cases.

## 🚀 Quick Start Examples

### 1. Lấy danh sách chuyên gia

**cURL:**
```bash
curl -X GET "https://api.twinexpert.com/v1/experts" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

**JavaScript:**
```javascript
const axios = require('axios');

async function getExperts() {
  try {
    const response = await axios.get('https://api.twinexpert.com/v1/experts', {
      headers: {
        'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Available experts:', response.data.experts);
    return response.data.experts;
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

getExperts();
```

**Python:**
```python
import requests
import os

def get_experts():
    headers = {
        'Authorization': f'Bearer {os.getenv("TWIN_API_KEY")}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get('https://api.twinexpert.com/v1/experts', headers=headers)
    
    if response.status_code == 200:
        experts = response.json()['experts']
        print(f"Found {len(experts)} experts")
        return experts
    else:
        print(f"Error: {response.status_code}")
        return None

experts = get_experts()
```

### 2. Chat với chuyên gia đơn giản

**JavaScript:**
```javascript
async function chatWithExpert(expertId, message) {
  try {
    const response = await axios.post('https://api.twinexpert.com/v1/chat/completions', {
      expert: expertId,
      message: message
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Expert response:', response.data.response);
    return response.data;
  } catch (error) {
    console.error('Chat error:', error.response.data);
  }
}

// Sử dụng
chatWithExpert('marketing', 'Viết slogan cho cửa hàng coffee');
```

**Python:**
```python
def chat_with_expert(expert_id, message):
    headers = {
        'Authorization': f'Bearer {os.getenv("TWIN_API_KEY")}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'expert': expert_id,
        'message': message
    }
    
    response = requests.post(
        'https://api.twinexpert.com/v1/chat/completions',
        json=payload,
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Expert {expert_id}: {result['response']}")
        return result
    else:
        print(f"Error: {response.status_code}")
        return None

# Sử dụng
chat_with_expert('copywriter', 'Viết email welcome cho khách hàng mới')
```

## 💼 Ví dụ với Context

### 3. Marketing Campaign với Context chi tiết

```javascript
async function createMarketingCampaign() {
  const campaignRequest = {
    expert: 'marketing',
    message: 'Tạo một campaign marketing hoàn chỉnh cho sản phẩm mới',
    context: {
      product: {
        name: 'SmartWatch Pro',
        category: 'Wearable Technology',
        price: '2,990,000 VND',
        target_audience: 'Professionals 25-40 tuổi'
      },
      brand: {
        name: 'TechViet',
        voice: 'modern, trustworthy, innovative',
        values: ['innovation', 'quality', 'vietnamese_pride']
      },
      campaign: {
        goal: 'product_launch',
        budget: '500,000,000 VND',
        duration: '3 months',
        channels: ['social_media', 'digital_ads', 'influencer']
      },
      market: {
        competition: ['Apple Watch', 'Samsung Galaxy Watch'],
        season: 'Back to work after Tet',
        trends: ['health_tracking', 'productivity']
      }
    }
  };

  try {
    const response = await axios.post(
      'https://api.twinexpert.com/v1/chat/completions',
      campaignRequest,
      {
        headers: {
          'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    console.log('Campaign Strategy:', response.data.response);
    return response.data;
  } catch (error) {
    console.error('Campaign creation failed:', error.response.data);
  }
}

createMarketingCampaign();
```

### 4. Content Creation với Multiple Experts

```javascript
class ContentCreationFlow {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://api.twinexpert.com/v1';
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }

  async createContentStrategy(product, audience) {
    // Step 1: Strategy với Marketing Expert
    const strategy = await this.callExpert('marketing', 
      `Tạo content strategy cho ${product.name}`, {
        product,
        audience,
        goal: 'brand_awareness_and_sales'
      }
    );

    // Step 2: Content topics với Business Analyst
    const topics = await this.callExpert('business_analyst',
      `Dựa trên strategy sau, đề xuất 10 content topics cụ thể: ${strategy.response}`, {
        strategy: strategy.response,
        product,
        analysis_focus: 'content_topics'
      }
    );

    // Step 3: Copywriting với Copywriter
    const copy = await this.callExpert('copywriter',
      `Viết content cho 3 topics đầu tiên: ${topics.response}`, {
        topics: topics.response,
        brand_voice: product.brand_voice,
        format: ['social_post', 'blog_intro', 'email_subject']
      }
    );

    return {
      strategy: strategy.response,
      topics: topics.response,
      content: copy.response,
      totalTokens: strategy.tokens_used + topics.tokens_used + copy.tokens_used
    };
  }

  async callExpert(expert, message, context = {}) {
    try {
      const response = await axios.post(`${this.baseURL}/chat/completions`, {
        expert,
        message,
        context
      }, { headers: this.headers });

      return response.data;
    } catch (error) {
      console.error(`Error with ${expert}:`, error.response.data);
      throw error;
    }
  }
}

// Sử dụng
const contentFlow = new ContentCreationFlow(process.env.TWIN_API_KEY);

const product = {
  name: 'Organic Green Tea',
  category: 'F&B',
  brand_voice: 'natural, peaceful, healthy',
  target_audience: 'Health-conscious millennials'
};

contentFlow.createContentStrategy(product, 'millennials_health_conscious')
  .then(result => {
    console.log('Content strategy created:');
    console.log('Strategy:', result.strategy);
    console.log('Topics:', result.topics);
    console.log('Content:', result.content);
    console.log('Total tokens:', result.totalTokens);
  });
```

## 🔄 Streaming Response Example

### 5. Real-time Chat với Streaming

```javascript
async function streamingChat(expert, message) {
  try {
    const response = await fetch('https://api.twinexpert.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        expert,
        message,
        stream: true
      })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop(); // Keep incomplete line in buffer

      for (const line of lines) {
        if (line.trim() === '') continue;
        if (line.trim() === 'data: [DONE]') return;

        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.delta) {
              process.stdout.write(data.delta); // Print real-time
            }
          } catch (e) {
            console.error('Parse error:', e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Streaming error:', error);
  }
}

// Sử dụng
streamingChat('copywriter', 'Viết một bài blog về benefits của yoga');
```

### 6. Streaming với React Component

```jsx
import React, { useState, useEffect } from 'react';

function StreamingChat() {
  const [messages, setMessages] = useState([]);
  const [currentResponse, setCurrentResponse] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async (message) => {
    setIsStreaming(true);
    setCurrentResponse('');
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          expert: 'marketing',
          message,
          stream: true
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantResponse = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.delta) {
                assistantResponse += data.delta;
                setCurrentResponse(assistantResponse);
              }
            } catch (e) {
              // Ignore parse errors
            }
          }
        }
      }

      // Add complete response to messages
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: assistantResponse 
      }]);
      setCurrentResponse('');
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {currentResponse && (
          <div className="message assistant streaming">
            {currentResponse}
            <span className="cursor">|</span>
          </div>
        )}
      </div>
      
      <ChatInput onSend={sendMessage} disabled={isStreaming} />
    </div>
  );
}
```

## 📁 File Upload & Analysis

### 7. Upload và phân tích Document

```javascript
async function analyzeDocument(filePath, expertId = 'business_analyst') {
  const FormData = require('form-data');
  const fs = require('fs');

  try {
    // Step 1: Upload file
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('purpose', 'analysis');

    const uploadResponse = await axios.post(
      'https://api.twinexpert.com/v1/files/upload',
      form,
      {
        headers: {
          ...form.getHeaders(),
          'Authorization': `Bearer ${process.env.TWIN_API_KEY}`
        }
      }
    );

    const fileId = uploadResponse.data.id;
    console.log('File uploaded:', fileId);

    // Step 2: Request analysis
    const analysisResponse = await axios.post(
      `https://api.twinexpert.com/v1/files/${fileId}/analyze`,
      {
        expert: expertId,
        instruction: 'Phân tích tài liệu và đưa ra tóm tắt, insights và recommendations',
        format: 'detailed'
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const analysisId = analysisResponse.data.analysis_id;
    console.log('Analysis started:', analysisId);

    // Step 3: Poll for results
    let result;
    do {
      await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2s
      
      const resultResponse = await axios.get(
        `https://api.twinexpert.com/v1/files/${fileId}/analysis/${analysisId}`,
        {
          headers: {
            'Authorization': `Bearer ${process.env.TWIN_API_KEY}`
          }
        }
      );

      result = resultResponse.data;
      console.log('Analysis status:', result.status);
    } while (result.status === 'processing');

    if (result.status === 'completed') {
      console.log('Analysis completed!');
      console.log('Summary:', result.result.summary);
      console.log('Key Insights:', result.result.key_insights);
      console.log('Recommendations:', result.result.recommendations);
      return result.result;
    } else {
      throw new Error('Analysis failed');
    }

  } catch (error) {
    console.error('Document analysis error:', error.response?.data || error.message);
  }
}

// Sử dụng
analyzeDocument('./business_plan.pdf', 'business_analyst');
```

## 👥 Team Collaboration Example

### 8. Project-based Workflow

```javascript
class TwinExpertProject {
  constructor(apiKey, projectName) {
    this.apiKey = apiKey;
    this.projectName = projectName;
    this.projectId = null;
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }

  async createProject(description, experts = []) {
    try {
      const response = await axios.post(
        'https://api.twinexpert.com/v1/projects',
        {
          name: this.projectName,
          description,
          experts
        },
        { headers: this.headers }
      );

      this.projectId = response.data.id;
      console.log(`Project created: ${this.projectId}`);
      return this.projectId;
    } catch (error) {
      console.error('Project creation failed:', error.response.data);
    }
  }

  async addConversationToProject(expertId, message, context = {}) {
    try {
      const response = await axios.post(
        'https://api.twinexpert.com/v1/chat/completions',
        {
          expert: expertId,
          message,
          context: {
            ...context,
            project_id: this.projectId
          }
        },
        { headers: this.headers }
      );

      console.log(`${expertId} response added to project`);
      return response.data;
    } catch (error) {
      console.error(`Error adding ${expertId} response:`, error.response.data);
    }
  }

  async getProjectSummary() {
    try {
      const [conversations, files] = await Promise.all([
        axios.get(`https://api.twinexpert.com/v1/projects/${this.projectId}/conversations`, 
          { headers: this.headers }),
        axios.get(`https://api.twinexpert.com/v1/projects/${this.projectId}/files`, 
          { headers: this.headers })
      ]);

      return {
        conversations: conversations.data,
        files: files.data,
        totalConversations: conversations.data.length,
        totalFiles: files.data.length
      };
    } catch (error) {
      console.error('Error getting project summary:', error.response.data);
    }
  }
}

// Sử dụng Project Workflow
async function runProjectWorkflow() {
  const project = new TwinExpertProject(
    process.env.TWIN_API_KEY, 
    'E-commerce Website Redesign'
  );

  // Tạo project
  await project.createProject(
    'Redesign website bán hàng online với focus vào UX và conversion rate',
    ['marketing', 'copywriter', 'business_analyst']
  );

  // Thu thập insights từ nhiều chuyên gia
  const marketingAdvice = await project.addConversationToProject(
    'marketing',
    'Phân tích current website và đưa ra strategy cho redesign',
    { 
      current_site: 'fashionstore.vn',
      goals: ['increase_conversion', 'improve_ux', 'mobile_optimization']
    }
  );

  const copyAdvice = await project.addConversationToProject(
    'copywriter', 
    'Viết copy cho landing page mới dựa trên marketing strategy',
    {
      strategy_reference: marketingAdvice.id,
      tone: 'friendly, trustworthy, conversion-focused'
    }
  );

  const analysisAdvice = await project.addConversationToProject(
    'business_analyst',
    'Đánh giá ROI và metrics cần track cho website redesign',
    {
      marketing_reference: marketingAdvice.id,
      copy_reference: copyAdvice.id
    }
  );

  // Lấy tóm tắt project
  const summary = await project.getProjectSummary();
  console.log('Project Summary:', summary);
}

runProjectWorkflow();
```

## 🎯 Advanced Use Cases

### 9. A/B Testing Content

```javascript
async function createABTestContent(baseMessage, variations = 3) {
  const results = [];
  
  for (let i = 0; i < variations; i++) {
    const variation = await axios.post(
      'https://api.twinexpert.com/v1/chat/completions',
      {
        expert: 'copywriter',
        message: `${baseMessage}. Variation ${i + 1}, make it unique and creative.`,
        context: {
          variation_number: i + 1,
          total_variations: variations,
          creativity_level: 'high'
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.TWIN_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    results.push({
      variation: i + 1,
      content: variation.data.response,
      tokens: variation.data.tokens_used
    });
    
    // Delay để tránh rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  return results;
}

// Sử dụng
createABTestContent(
  'Viết email subject line cho campaign Black Friday sale',
  5
).then(variations => {
  console.log('A/B Test Variations:');
  variations.forEach(v => {
    console.log(`\nVariation ${v.variation}:`);
    console.log(v.content);
  });
});
```

### 10. Batch Processing với Rate Limiting

```javascript
class BatchProcessor {
  constructor(apiKey, rateLimit = 5) { // 5 requests per second
    this.apiKey = apiKey;
    this.rateLimit = rateLimit;
    this.queue = [];
    this.processing = false;
  }

  async processRequests(requests) {
    this.queue = [...requests];
    this.processing = true;
    const results = [];

    while (this.queue.length > 0 && this.processing) {
      const batch = this.queue.splice(0, this.rateLimit);
      const batchPromises = batch.map(request => this.makeRequest(request));
      
      try {
        const batchResults = await Promise.all(batchPromises);
        results.push(...batchResults);
        
        console.log(`Processed batch: ${results.length}/${requests.length}`);
        
        // Wait 1 second before next batch
        if (this.queue.length > 0) {
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      } catch (error) {
        console.error('Batch processing error:', error);
        break;
      }
    }

    this.processing = false;
    return results;
  }

  async makeRequest(request) {
    try {
      const response = await axios.post(
        'https://api.twinexpert.com/v1/chat/completions',
        request,
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );
      return { success: true, data: response.data, request };
    } catch (error) {
      return { success: false, error: error.response?.data, request };
    }
  }
}

// Sử dụng Batch Processing
const processor = new BatchProcessor(process.env.TWIN_API_KEY);

const requests = [
  { expert: 'marketing', message: 'Tạo hashtags cho Instagram post about coffee' },
  { expert: 'copywriter', message: 'Viết product description cho áo thun cotton' },
  { expert: 'social_media', message: 'Tạo caption cho Facebook post about healthy eating' },
  { expert: 'business_analyst', message: 'Phân tích trend thị trường F&B 2024' },
  // ... more requests
];

processor.processRequests(requests)
  .then(results => {
    const successful = results.filter(r => r.success);
    const failed = results.filter(r => !r.success);
    
    console.log(`\nBatch completed:`);
    console.log(`✅ Successful: ${successful.length}`);
    console.log(`❌ Failed: ${failed.length}`);
    
    if (failed.length > 0) {
      console.log('\nFailed requests:');
      failed.forEach(f => console.log(f.error));
    }
  });
```

## 📊 Error Handling Best Practices

### 11. Robust Error Handling

```javascript
class TwinExpertClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://api.twinexpert.com/v1';
    this.retryAttempts = 3;
    this.retryDelay = 1000; // 1 second
  }

  async callExpertWithRetry(expert, message, context = {}) {
    for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
      try {
        return await this.callExpert(expert, message, context);
      } catch (error) {
        if (this.shouldRetry(error) && attempt < this.retryAttempts) {
          console.log(`Attempt ${attempt} failed, retrying in ${this.retryDelay}ms...`);
          await new Promise(resolve => setTimeout(resolve, this.retryDelay * attempt));
          continue;
        }
        
        throw this.handleError(error);
      }
    }
  }

  shouldRetry(error) {
    const retryableStatusCodes = [429, 500, 502, 503, 504];
    return error.response && retryableStatusCodes.includes(error.response.status);
  }

  handleError(error) {
    if (!error.response) {
      return new Error(`Network error: ${error.message}`);
    }

    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        return new Error(`Bad Request: ${data.error?.message || 'Invalid parameters'}`);
      case 401:
        return new Error('Authentication failed: Invalid API key');
      case 403:
        return new Error('Forbidden: Insufficient permissions');
      case 404:
        return new Error('Not Found: Resource or expert not found');
      case 429:
        return new Error(`Rate limit exceeded. Retry after: ${data.error?.retry_after || 60}s`);
      case 500:
        return new Error('Internal server error. Please try again later');
      default:
        return new Error(`API Error (${status}): ${data.error?.message || 'Unknown error'}`);
    }
  }

  async callExpert(expert, message, context = {}) {
    const response = await axios.post(`${this.baseURL}/chat/completions`, {
      expert,
      message,
      context
    }, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      timeout: 30000 // 30 second timeout
    });

    return response.data;
  }
}

// Sử dụng với error handling
const client = new TwinExpertClient(process.env.TWIN_API_KEY);

async function robustChatExample() {
  try {
    const result = await client.callExpertWithRetry(
      'marketing',
      'Tạo strategy cho product launch'
    );
    
    console.log('Success:', result.response);
  } catch (error) {
    console.error('Final error:', error.message);
    
    // Log cho monitoring
    console.log('Error details for debugging:', {
      timestamp: new Date().toISOString(),
      expert: 'marketing',
      message: 'Tạo strategy cho product launch',
      error: error.message
    });
  }
}

robustChatExample();
```

---

**Tiếp theo**: [Rate Limiting →](./rate-limiting)

