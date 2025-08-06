---
title: "Ví dụ"
description: "Twin AI API - Ví dụ"
---

# 5.4. Ví dụ

Các ví dụ code thực tế để bắt đầu nhanh với TwinExpert API.

## 1. Lấy danh sách AI Twins

Xem tất cả AI twins mà bạn có thể truy cập.

### GET `/api/v1/twins`

::: code-group

```javascript [JavaScript]
// Lấy danh sách twins
const response = await fetch('https://api.twinexpert.com/api/v1/twins', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});

const twins = await response.json();
console.log('Available twins:', twins.data);
```

```python [Python]
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

```bash [cURL]
# Lấy danh sách twins
curl -X GET "https://api.twinexpert.com/api/v1/twins" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

:::

## 2. Chat với AI Twin

Tạo cuộc trò chuyện và gửi tin nhắn đến AI twin.

::: code-group

```javascript [JavaScript]
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
      title: 'API Chat Session'
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
chatWithTwin('twin-id', 'Xin chào!').then(result => {
  console.log('Response:', result);
});
```

```python [Python]
import requests

class TwinExpertAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.twinexpert.com/api/v1'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def create_conversation(self, twin_id, title="API Chat"):
        response = requests.post(
            f'{self.base_url}/conversations',
            headers=self.headers,
            json={'twinId': twin_id, 'title': title}
        )
        return response.json()['data']
    
    def send_message(self, conversation_id, message):
        response = requests.post(
            f'{self.base_url}/conversations/{conversation_id}/messages',
            headers=self.headers,
            json={'content': message}
        )
        return response.json()['data']
    
    def chat_with_twin(self, twin_id, message):
        # Tạo cuộc trò chuyện
        conversation = self.create_conversation(twin_id)
        
        # Gửi tin nhắn
        result = self.send_message(conversation['id'], message)
        return result

# Sử dụng
api = TwinExpertAPI('YOUR_API_KEY')
response = api.chat_with_twin('twin-id', 'Xin chào!')
print(response)
```

```bash [cURL]
# 1. Tạo cuộc trò chuyện mới
curl -X POST "https://api.twinexpert.com/api/v1/conversations" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "twinId": "twin-id",
    "title": "API Chat Session"
  }'

# 2. Gửi tin nhắn (với conversation ID từ response trên)
curl -X POST "https://api.twinexpert.com/api/v1/conversations/CONVERSATION_ID/messages" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Xin chào!"
  }'
```

:::

## 3. Streaming Chat

Nhận phản hồi real-time bằng Server-Sent Events.

### Streaming Response

Endpoint streaming trả về Server-Sent Events với các event types:

- **`progress`** - Thông tin tiến trình
- **`delta`** - Từng phần của response  
- **`complete`** - Hoàn thành message
- **`error`** - Lỗi xảy ra

::: code-group

```javascript [JavaScript]
// Streaming chat với EventSource
function streamChat(conversationId, message) {
  const eventSource = new EventSource(
    `https://api.twinexpert.com/api/v1/conversations/${conversationId}/messages/stream`,
    {
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content: message })
    }
  );

  eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
      case 'progress':
        console.log('Progress:', data.progress);
        break;
      case 'delta':
        console.log('Delta:', data.content);
        break;
      case 'complete':
        console.log('Complete:', data.message);
        eventSource.close();
        break;
      case 'error':
        console.error('Error:', data.error);
        eventSource.close();
        break;
    }
  };
}
```

```python [Python]
import requests
import json

def stream_chat(conversation_id, message, api_key):
    url = f'https://api.twinexpert.com/api/v1/conversations/{conversation_id}/messages/stream'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {'content': message}
    
    with requests.post(url, headers=headers, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                event_data = json.loads(line.decode('utf-8'))
                
                if event_data['type'] == 'progress':
                    print(f"Progress: {event_data['progress']}")
                elif event_data['type'] == 'delta':
                    print(f"Delta: {event_data['content']}")
                elif event_data['type'] == 'complete':
                    print(f"Complete: {event_data['message']}")
                    break
                elif event_data['type'] == 'error':
                    print(f"Error: {event_data['error']}")
                    break

# Sử dụng
stream_chat('conversation-id', 'Xin chào!', 'YOUR_API_KEY')
```

:::

---

::: tip API Testing
Bạn có thể test các API endpoints này bằng cách tham khảo [API Documentation](/api/) để hiểu cách sử dụng từng endpoint.
:::

::: tip Cần hỗ trợ?
Nếu bạn gặp vấn đề với API, vui lòng liên hệ qua [email hỗ trợ](mailto:agent.twinai@gmail.com).
:::