# 5.4. Ví dụ

Các ví dụ code thực tế để bắt đầu nhanh

## 📋 1. Lấy danh sách Twins

Lấy danh sách twins có thể truy cập

<div role="tablist" class="tabs">

### JavaScript

```javascript
// Lấy danh sách twins
const response = await fetch('https://api.twinexpert.com/api/v1/twins', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
console.log('Twins:', data.data);
```

### Python

```python
import requests

# Lấy danh sách twins
headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.twinexpert.com/api/v1/twins',
    headers=headers
)

twins = response.json()['data']
print(f'Found {len(twins)} twins')
```

### cURL

```bash
# Lấy danh sách twins
curl -X GET "https://api.twinexpert.com/api/v1/twins" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

</div>

## 💬 2. Chat với AI Twin

Tạo cuộc trò chuyện và gửi tin nhắn đến AI twin

**Endpoints:**
- `GET` `/api/v1/conversations`
- `POST` `/api/v1/conversations/{id}/messages`

<div role="tablist" class="tabs">

### JavaScript

```javascript
// Tạo cuộc trò chuyện và gửi tin nhắn
async function chatWithTwin(twinId, message) {
  // 1. Tạo cuộc trò chuyện mới
  const conversationResponse = await fetch('https://api.twinexpert.com/api/v1/conversations', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      twinId: twinId,
      title: 'New Chat'
    })
  });
  
  const conversation = await conversationResponse.json();
  const conversationId = conversation.data.id;
  
  // 2. Gửi tin nhắn
  const messageResponse = await fetch(`https://api.twinexpert.com/api/v1/conversations/${conversationId}/messages`, {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      content: message
    })
  });
  
  const result = await messageResponse.json();
  return result.data;
}

// Sử dụng
chatWithTwin('twin-id-123', 'Xin chào!').then(response => {
  console.log('AI Response:', response.content);
});
```

### Python

```python
import requests

class TwinExpertAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.twinexpert.com/api/v1'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def chat_with_twin(self, twin_id, message):
        # Tạo cuộc trò chuyện
        conversation = self.create_conversation(twin_id)
        conversation_id = conversation['data']['id']
        
        # Gửi tin nhắn
        response = requests.post(
            f'{self.base_url}/conversations/{conversation_id}/messages',
            headers=self.headers,
            json={'content': message}
        )
        
        return response.json()['data']
    
    def create_conversation(self, twin_id):
        response = requests.post(
            f'{self.base_url}/conversations',
            headers=self.headers,
            json={
                'twinId': twin_id,
                'title': 'New Chat'
            }
        )
        return response.json()

# Sử dụng
api = TwinExpertAPI('YOUR_API_KEY')
result = api.chat_with_twin('twin-id-123', 'Xin chào!')
print(f'AI Response: {result["content"]}')
```

### cURL

```bash
# 1. Tạo cuộc trò chuyện mới
curl -X POST "https://api.twinexpert.com/api/v1/conversations" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "twinId": "twin-id-123",
    "title": "New Chat"
  }'

# 2. Gửi tin nhắn (sử dụng conversation_id từ response trên)
curl -X POST "https://api.twinexpert.com/api/v1/conversations/{CONVERSATION_ID}/messages" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Xin chào!"
  }'
```

</div>

## 🌊 3. Streaming Response

Nhận phản hồi realtime từ AI twin

```javascript
async function streamChat(conversationId, message) {
  const response = await fetch(`https://api.twinexpert.com/api/v1/conversations/${conversationId}/messages/stream`, {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      content: message
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        console.log('Chunk:', data.content);
      }
    }
  }
}
```

## 📊 4. Error Handling

```javascript
async function makeAPICall() {
  try {
    const response = await fetch('https://api.twinexpert.com/api/v1/twins', {
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`API Error: ${errorData.message}`);
    }
    
    const data = await response.json();
    return data;
    
  } catch (error) {
    console.error('Request failed:', error.message);
    
    // Xử lý theo loại lỗi
    if (error.message.includes('401')) {
      console.log('API key không hợp lệ');
    } else if (error.message.includes('429')) {
      console.log('Đã vượt quá rate limit');
    } else {
      console.log('Lỗi không xác định');
    }
  }
}
```

---

📚 **Tiếp theo:** [5.5. Rate Limiting](/api-rate-limiting) | [💡 Tips & Best Practices](https://twinexpert.gitbook.io/docs)
