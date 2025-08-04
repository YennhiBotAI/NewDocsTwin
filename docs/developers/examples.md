# 5.4. Ví dụ

## Chatbot Customer Support

### JavaScript (Node.js + Express)
```javascript
import express from 'express';
import TwinExpert from '@twinexpert/js-sdk';

const app = express();
app.use(express.json());

const client = new TwinExpert({
  apiKey: process.env.TWINEXPERT_API_KEY
});

// Tạo support twin
const supportTwin = await client.twins.create({
  name: "Customer Support",
  personality: "helpful",
  instructions: "You are a customer support agent. Be helpful, professional, and concise."
});

// Chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { message, conversationId } = req.body;
    
    const response = await client.twins.chat({
      twinId: supportTwin.id,
      message,
      conversationId
    });
    
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

## Content Generation

### Python Script
```python
import twinexpert
import asyncio

client = twinexpert.TwinExpert(api_key="your_key")

# Tạo content writer twin
async def create_content_twin():
    return await client.twins.create(
        name="Content Writer",
        personality="creative",
        instructions="You are a professional content writer. Create engaging, SEO-friendly content.",
        model="gpt-4-turbo"
    )

# Generate blog post
async def generate_blog_post(topic, keywords):
    twin = await create_content_twin()
    
    prompt = f"""
    Write a blog post about: {topic}
    Keywords to include: {', '.join(keywords)}
    
    Structure:
    - Engaging headline
    - Introduction (2-3 sentences)
    - 3 main sections with subheadings
    - Conclusion with call-to-action
    
    Tone: Professional but friendly
    Length: ~800 words
    """
    
    response = await client.twins.chat(
        twin_id=twin.id,
        message=prompt,
        max_tokens=1500
    )
    
    return response.message

# Usage
content = asyncio.run(generate_blog_post(
    "AI in Healthcare", 
    ["artificial intelligence", "medical diagnosis", "patient care"]
))
print(content)
```

## Knowledge Base Q&A

### React Frontend + Node.js Backend
```javascript
// Backend: app.js
import TwinExpert from '@twinexpert/js-sdk';
import multer from 'multer';

const client = new TwinExpert({ apiKey: process.env.TWINEXPERT_API_KEY });
const upload = multer({ dest: 'uploads/' });

// Upload document to knowledge base
app.post('/api/upload', upload.single('document'), async (req, res) => {
  try {
    const twin = await client.twins.retrieve('twin_kb_assistant');
    
    await client.twins.knowledge.upload({
      twinId: twin.id,
      file: req.file.path,
      metadata: {
        filename: req.file.originalname,
        category: req.body.category
      }
    });
    
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Query knowledge base
app.post('/api/query', async (req, res) => {
  try {
    const { question } = req.body;
    
    const response = await client.twins.chat({
      twinId: 'twin_kb_assistant',
      message: `Based on the uploaded documents, please answer: ${question}`
    });
    
    res.json({ answer: response.message });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```jsx
// Frontend: KnowledgeBase.jsx
import React, { useState } from 'react';

function KnowledgeBase() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      
      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Ask'}
        </button>
      </form>
      
      {answer && (
        <div className="answer">
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
```

## Multi-language Support

### PHP Implementation
```php
<?php
use TwinExpert\Client;

class MultiLanguageBot {
    private $client;
    private $twins = [];
    
    public function __construct($apiKey) {
        $this->client = new Client(['api_key' => $apiKey]);
        $this->initializeTwins();
    }
    
    private function initializeTwins() {
        $languages = ['en', 'vi', 'ja', 'ko'];
        
        foreach ($languages as $lang) {
            $this->twins[$lang] = $this->client->twins->create([
                'name' => "Support Bot - " . strtoupper($lang),
                'personality' => 'helpful',
                'instructions' => $this->getInstructions($lang),
                'metadata' => ['language' => $lang]
            ]);
        }
    }
    
    private function getInstructions($language) {
        $instructions = [
            'en' => 'You are a helpful customer support agent. Respond in English.',
            'vi' => 'Bạn là nhân viên hỗ trợ khách hàng. Trả lời bằng tiếng Việt.',
            'ja' => 'あなたは親切なカスタマーサポートエージェントです。日本語で回答してください。',
            'ko' => '당신은 도움이 되는 고객 지원 에이전트입니다. 한국어로 응답하세요.'
        ];
        
        return $instructions[$language] ?? $instructions['en'];
    }
    
    public function chat($message, $language = 'en') {
        $twin = $this->twins[$language] ?? $this->twins['en'];
        
        return $this->client->twins->chat([
            'twin_id' => $twin->id,
            'message' => $message
        ]);
    }
}

// Usage
$bot = new MultiLanguageBot($_ENV['TWINEXPERT_API_KEY']);

// English
$response = $bot->chat("How can I return a product?", 'en');

// Vietnamese
$response = $bot->chat("Làm sao để trả lại sản phẩm?", 'vi');
```

## Streaming Chat Interface

### JavaScript with Server-Sent Events
```javascript
// Server
app.post('/api/chat/stream', async (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });

  try {
    const stream = await client.twins.chat({
      twinId: 'twin_assistant',
      message: req.body.message,
      stream: true
    });

    for await (const chunk of stream) {
      res.write(`data: ${JSON.stringify(chunk)}\n\n`);
    }
    
    res.write('data: [DONE]\n\n');
  } catch (error) {
    res.write(`data: ${JSON.stringify({error: error.message})}\n\n`);
  }
  
  res.end();
});
```

```javascript
// Client
function streamChat(message) {
  const eventSource = new EventSource('/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data === '[DONE]') {
      eventSource.close();
      return;
    }
    
    if (data.delta?.content) {
      appendToChat(data.delta.content);
    }
  };

  eventSource.onerror = (error) => {
    console.error('Stream error:', error);
    eventSource.close();
  };
}
```

## Analytics Dashboard

### Python + Flask
```python
from flask import Flask, jsonify
import twinexpert
from datetime import datetime, timedelta

app = Flask(__name__)
client = twinexpert.TwinExpert(api_key=os.environ['TWINEXPERT_API_KEY'])

@app.route('/api/analytics/overview')
async def analytics_overview():
    # Get account usage
    account = await client.account.retrieve()
    
    # Get twins statistics
    twins = await client.twins.list(limit=100)
    
    # Calculate metrics
    total_twins = len(twins.twins)
    active_twins = len([t for t in twins.twins if t.status == 'active'])
    
    # Get recent conversations
    conversations = await client.conversations.list(
        created_after=datetime.now() - timedelta(days=7)
    )
    
    return jsonify({
        'usage': {
            'messages_this_month': account.usage.messages_this_month,
            'message_quota': account.usage.message_quota,
            'usage_percentage': (account.usage.messages_this_month / account.usage.message_quota) * 100
        },
        'twins': {
            'total': total_twins,
            'active': active_twins,
            'inactive': total_twins - active_twins
        },
        'activity': {
            'conversations_this_week': len(conversations.conversations),
            'avg_messages_per_conversation': sum(c.message_count for c in conversations.conversations) / len(conversations.conversations) if conversations.conversations else 0
        }
    })

@app.route('/api/analytics/twins/<twin_id>')
async def twin_analytics(twin_id):
    # Get twin details
    twin = await client.twins.retrieve(twin_id)
    
    # Get conversations for this twin
    conversations = await client.conversations.list(
        twin_id=twin_id,
        limit=100
    )
    
    # Calculate metrics
    total_conversations = len(conversations.conversations)
    total_messages = sum(c.message_count for c in conversations.conversations)
    
    return jsonify({
        'twin': twin,
        'metrics': {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'avg_messages_per_conversation': total_messages / total_conversations if total_conversations > 0 else 0
        }
    })
```

## Error Handling Best Practices

### Robust Error Handling
```javascript
class TwinExpertService {
  constructor(apiKey) {
    this.client = new TwinExpert({ apiKey });
    this.retryDelay = 1000;
    this.maxRetries = 3;
  }

  async chatWithRetry(twinId, message, attempt = 1) {
    try {
      return await this.client.twins.chat({
        twinId,
        message
      });
    } catch (error) {
      // Handle specific errors
      if (error.status === 401) {
        throw new Error('Authentication failed. Please check your API key.');
      }
      
      if (error.status === 404) {
        throw new Error(`Twin ${twinId} not found.`);
      }
      
      if (error.status === 429 && attempt <= this.maxRetries) {
        // Rate limited - retry with exponential backoff
        const delay = this.retryDelay * Math.pow(2, attempt - 1);
        console.log(`Rate limited. Retrying in ${delay}ms...`);
        
        await new Promise(resolve => setTimeout(resolve, delay));
        return this.chatWithRetry(twinId, message, attempt + 1);
      }
      
      if (error.status >= 500 && attempt <= this.maxRetries) {
        // Server error - retry
        console.log(`Server error. Retrying attempt ${attempt}...`);
        await new Promise(resolve => setTimeout(resolve, this.retryDelay));
        return this.chatWithRetry(twinId, message, attempt + 1);
      }
      
      throw error;
    }
  }
}

// Usage
const service = new TwinExpertService(process.env.TWINEXPERT_API_KEY);

try {
  const response = await service.chatWithRetry('twin_123', 'Hello');
  console.log(response.message);
} catch (error) {
  console.error('Failed to get response:', error.message);
}
```

---

**Xem thêm:**
- 🚀 [Getting Started](./getting-started) - Bắt đầu với API
- 🔌 [API Endpoints](./endpoints) - Reference đầy đủ
- ⚡ [Rate Limiting](./rate-limiting) - Quản lý limits
- 🚨 [Error Handling](./error-handling) - Best practices