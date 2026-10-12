# Learnify AI — API Reference

Complete API documentation for Learnify AI backend services.

---

## Base URL

```
http://localhost:8000
```

For production, replace with your deployed backend URL.

---

## Authentication

**Current Version:** No authentication required (v0.1.0)

**Future Versions:** Will support JWT-based authentication.

---

## Endpoints

### 1. Root / Health

#### GET `/`

Get API information and available capabilities.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response:** `200 OK`
```json
{
  "name": "Learnify AI",
  "description": "AI-Powered Chatbot for Student Queries",
  "version": "0.1.0",
  "status": "operational",
  "ai_capabilities": [
    "Knowledge Representation",
    "Search Algorithms",
    "Logical Reasoning",
    "Rule-Based Inference",
    "Expert Systems"
  ]
}
```

---

#### GET `/api/health`

Health check endpoint to verify backend service status.

**Request:**
```http
GET /api/health HTTP/1.1
Host: localhost:8000
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "Learnify AI Backend"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is down

---

### 2. Chat Endpoints

#### POST `/api/chat/`

Send a message to the AI chatbot and receive a response.

**Request:**
```http
POST /api/chat/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "message": "What is artificial intelligence?",
  "context": [
    {
      "id": "1",
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-15T10:30:00Z",
      "conceptsUsed": null
    },
    {
      "id": "2",
      "role": "assistant",
      "content": "Hi! How can I help you?",
      "timestamp": "2024-01-15T10:30:01Z",
      "conceptsUsed": ["Rule-Based System"]
    }
  ]
}
```

**Request Body Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | User's question or message (1-1000 chars) |
| context | array | No | Previous conversation messages for context |

**Response:** `200 OK`
```json
{
  "response": "Artificial Intelligence is the simulation of human intelligence in machines. It encompasses various areas including machine learning, natural language processing, computer vision, and expert systems. AI systems can learn from data, reason about information, and make decisions to solve complex problems.",
  "conceptsUsed": [
    "Knowledge Representation",
    "Expert System"
  ],
  "confidence": 0.88
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| response | string | AI-generated response text |
| conceptsUsed | array[string] | AI concepts used in generating response |
| confidence | float | Confidence score (0.0 - 1.0) |

**Status Codes:**
- `200 OK` - Success
- `422 Unprocessable Entity` - Invalid request body
- `500 Internal Server Error` - Server error

**Example with cURL:**
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is BFS?",
    "context": []
  }'
```

**Example with JavaScript (axios):**
```javascript
import axios from 'axios';

const response = await axios.post('http://localhost:8000/api/chat/', {
  message: 'Explain A* algorithm',
  context: []
});

console.log(response.data.response);
console.log(response.data.conceptsUsed);
```

**Example with Python (requests):**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/chat/',
    json={
        'message': 'What is propositional logic?',
        'context': []
    }
)

data = response.json()
print(data['response'])
print(data['conceptsUsed'])
```

---

#### GET `/api/chat/concepts`

Get the list of all AI concepts organized by units.

**Request:**
```http
GET /api/chat/concepts HTTP/1.1
Host: localhost:8000
```

**Response:** `200 OK`
```json
{
  "units": [
    {
      "id": 1,
      "name": "Introduction and Knowledge Representation",
      "concepts": [
        "AI Definition and History",
        "Problem Characteristics",
        "Production Systems",
        "Knowledge Representation (Semantic Networks, Frames, Ontologies)"
      ],
      "implemented": false
    },
    {
      "id": 2,
      "name": "Search Algorithms",
      "concepts": [
        "State Space Search",
        "Uninformed Search (BFS, DFS, DLS, IDS)",
        "Informed Search (Best-First, A*, Hill Climbing)",
        "Adversarial Search (Minimax, Alpha-Beta Pruning)",
        "Constraint Satisfaction Problems"
      ],
      "implemented": false
    }
    // ... more units
  ]
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| units | array | Array of AI unit objects |
| units[].id | integer | Unit number (1-5) |
| units[].name | string | Unit name/title |
| units[].concepts | array[string] | List of concepts in this unit |
| units[].implemented | boolean | Whether unit is implemented |

**Example with cURL:**
```bash
curl http://localhost:8000/api/chat/concepts
```

---

## Error Responses

All endpoints may return error responses in the following format:

**Validation Error (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Server Error (500):**
```json
{
  "detail": "Error processing request: <error message>"
}
```

---

## Rate Limiting

**Current Version:** No rate limiting

**Future Versions:** Will implement rate limiting (e.g., 100 requests per minute per IP)

---

## CORS Configuration

The API allows requests from the following origins:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

To add more origins, update `CORS_ORIGINS` in `backend/app/core/config.py`.

---

## Interactive Documentation

FastAPI provides built-in interactive API documentation:

### Swagger UI
```
http://localhost:8000/docs
```
- Try out endpoints directly in browser
- See request/response examples
- View schema definitions

### ReDoc
```
http://localhost:8000/redoc
```
- Alternative documentation interface
- Better for reading and reference

---

## Versioning

**Current Version:** v0.1.0

API versioning will be implemented in future releases:
- `/api/v1/chat/` - Version 1
- `/api/v2/chat/` - Version 2

---

## Response Times

Expected response times (local development):

| Endpoint | Typical | Maximum |
|----------|---------|---------|
| GET `/` | < 10ms | 100ms |
| GET `/api/health` | < 10ms | 100ms |
| GET `/api/chat/concepts` | < 50ms | 200ms |
| POST `/api/chat/` | 100-500ms | 5000ms |

Response times will vary based on:
- Query complexity
- AI model processing
- Server load
- Network conditions

---

## Status Codes Summary

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 422 | Unprocessable Entity | Invalid request data |
| 500 | Internal Server Error | Server error occurred |
| 503 | Service Unavailable | Service is down |

---

## Future Endpoints (Planned)

### User Management
- `POST /api/users/register` - User registration
- `POST /api/users/login` - User authentication
- `GET /api/users/me` - Get current user

### Knowledge Base
- `GET /api/knowledge/search` - Search knowledge base
- `POST /api/knowledge/add` - Add knowledge entry
- `GET /api/knowledge/{id}` - Get specific knowledge

### Analytics
- `GET /api/analytics/usage` - Get usage statistics
- `GET /api/analytics/concepts` - Get concept usage data

---

## Code Examples

### Complete Chat Example (TypeScript)

```typescript
import axios from 'axios';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  conceptsUsed?: string[];
}

interface ChatResponse {
  response: string;
  conceptsUsed: string[];
  confidence: number;
}

async function chat(message: string, context: Message[]): Promise<ChatResponse> {
  try {
    const response = await axios.post<ChatResponse>(
      'http://localhost:8000/api/chat/',
      {
        message,
        context: context.slice(-10) // Last 10 messages
      }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'API error');
    }
    throw error;
  }
}

// Usage
const response = await chat('What is AI?', []);
console.log(response.response);
```

### Health Check Example (Python)

```python
import requests
import time

def check_backend_health(max_retries=3):
    """Check if backend is healthy with retries"""
    for i in range(max_retries):
        try:
            response = requests.get(
                'http://localhost:8000/api/health',
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Backend is {data['status']}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Attempt {i+1} failed: {e}")
            time.sleep(2)
    
    print("✗ Backend is not available")
    return False

# Usage
if check_backend_health():
    print("Ready to send requests!")
```

---

## Testing

### Using Postman

1. Import collection from `docs/postman_collection.json` (coming soon)
2. Set base URL variable to `http://localhost:8000`
3. Run requests from the collection

### Using pytest

```bash
cd backend
pytest tests/test_api.py -v
```

---

## Support

For API issues or questions:
- Check the [Setup Guide](../SETUP_GUIDE.md)
- Review [README](../README.md)
- Open an issue on GitHub

---

**Last Updated:** January 2024  
**API Version:** 0.1.0
