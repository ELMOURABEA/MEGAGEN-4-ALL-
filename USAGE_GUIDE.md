# MEGA-Bot Usage Guide

Comprehensive guide to using MEGA-Bot as an individual agent or integrated with applications.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Using as Individual Agent](#using-as-individual-agent)
3. [Integration Methods](#integration-methods)
4. [API Reference](#api-reference)
5. [Best Practices](#best-practices)
6. [Examples](#examples)

## Getting Started

### Installation

```bash
# Install MEGA-Bot
pip install megaagent

# Verify installation
megabot --version
```

### Configuration

1. **Environment Variables** (`.env`):
```bash
COPILOT_API_KEY=your-key
GEMINI_API_KEY=your-key
CHATGPT_API_KEY=your-key
GROK_API_KEY=your-key
```

2. **Configuration File** (`config.json`):
```json
{
  "api_keys": {
    "copilot": "",
    "gemini": "",
    "chatgpt": "",
    "grok": ""
  },
  "features": {
    "auto_update": true,
    "document_sync": true,
    "caching": true
  }
}
```

## Using as Individual Agent

### Command Line Interface

#### Demo Mode
```bash
megabot
```

Displays:
- Bot status and capabilities
- Multi-platform query demonstration
- Deep research example
- Workflow automation demo
- Latest platform updates

#### Interactive Mode
```bash
megabot --interactive
```

Available commands:
- `query <prompt>` - Query all AI platforms
- `research <topic>` - Perform deep research
- `status` - Show bot status
- `capabilities` - List all capabilities
- `updates` - Show latest updates
- `sync` - Sync documents from platforms
- `exit` - Exit interactive mode

#### Single Commands

Query mode:
```bash
megabot query "What is artificial intelligence?"
```

Research mode:
```bash
megabot research "machine learning" --depth deep
```

Available depths:
- `shallow` - Quick overview
- `medium` - Balanced analysis (default)
- `deep` - Comprehensive research

### Programmatic Usage

```python
from megabot import MegaBot, Config
import asyncio

async def main():
    # Initialize with default config
    bot = MegaBot()
    
    # Or with custom config
    config = Config()
    config.set("workflow.max_concurrent_tasks", 20)
    bot = MegaBot(config)
    
    # Start the bot
    await bot.start()
    
    # Query all platforms
    result = await bot.query("What is AI?")
    print(f"Platforms responded: {result['synthesis']['platforms_responded']}")
    
    # Deep research
    research = await bot.research("quantum computing", depth="deep")
    print(f"Findings: {research['synthesis']['total_findings']}")
    
    # Execute workflow
    workflow_result = await bot.execute_workflow(
        "comprehensive_analysis",
        topic="neural networks"
    )
    
    # Stop the bot
    await bot.stop()

asyncio.run(main())
```

## Integration Methods

### Method 1: Direct Python Integration

Best for: Python applications that need direct access to MEGA-Bot

```python
from megabot import MegaBot
import asyncio

class MyApplication:
    def __init__(self):
        self.bot = MegaBot()
    
    async def start(self):
        await self.bot.start()
    
    async def process_query(self, user_input):
        result = await self.bot.query(user_input)
        return result['responses']
    
    async def shutdown(self):
        await self.bot.stop()
```

### Method 2: API Server Integration

Best for: Web applications, mobile apps, microservices

**Start the server:**
```bash
megabot-server --port 5000
```

**Use from Python:**
```python
from megabot.api.client import APIClient

client = APIClient("http://localhost:5000")
client.start()

result = client.query("What is AI?")
print(result)

client.stop()
```

**Use from JavaScript:**
```javascript
// Start bot
await fetch('http://localhost:5000/api/v1/start', {
    method: 'POST'
});

// Query
const response = await fetch('http://localhost:5000/api/v1/query', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt: 'What is AI?'})
});

const data = await response.json();
console.log(data);
```

**Use from cURL:**
```bash
# Start bot
curl -X POST http://localhost:5000/api/v1/start

# Query
curl -X POST http://localhost:5000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?"}'
```

### Method 3: Docker Container

Best for: Cloud deployment, microservices architecture

**Using Docker Compose:**
```yaml
version: '3.8'
services:
  megabot:
    image: elmourabea/megabot:latest
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
      - ./.env:/app/.env:ro
    environment:
      - DATABASE_PATH=/data/megabot.db
```

```bash
docker-compose up -d
```

**Manual Docker:**
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/data \
  -v $(pwd)/.env:/app/.env:ro \
  --name megabot \
  elmourabea/megabot:latest
```

### Method 4: System Service

Best for: Always-on deployments, background processing

**Linux (systemd):**
```ini
[Unit]
Description=MEGA-Bot API Server
After=network.target

[Service]
Type=simple
User=megabot
ExecStart=/usr/local/bin/megabot-server --port 5000
Restart=always

[Install]
WantedBy=multi-user.target
```

## API Reference

### REST API Endpoints

#### Bot Control

**Start Bot**
```
POST /api/v1/start
Response: {"message": "Bot started successfully", "status": "running"}
```

**Stop Bot**
```
POST /api/v1/stop
Response: {"message": "Bot stopped successfully", "status": "stopped"}
```

**Get Status**
```
GET /api/v1/status
Response: {
  "running": true,
  "integrations": {
    "active": 4,
    "total": 4,
    "platforms": [...]
  }
}
```

#### Operations

**Query**
```
POST /api/v1/query
Body: {"prompt": "Your question"}
Response: {
  "responses": {...},
  "synthesis": {
    "platforms_responded": 4,
    "average_confidence": 0.85
  }
}
```

**Research**
```
POST /api/v1/research
Body: {"topic": "machine learning", "depth": "deep"}
Response: {
  "topic": "machine learning",
  "depth": "deep",
  "platforms_used": [...],
  "synthesis": {...}
}
```

**Execute Workflow**
```
POST /api/v1/workflow
Body: {
  "workflow_name": "comprehensive_analysis",
  "params": {"topic": "AI ethics"}
}
Response: {...}
```

**Get Updates**
```
GET /api/v1/updates?limit=10
Response: {
  "updates": [...],
  "count": 10
}
```

**Sync Documents**
```
POST /api/v1/sync
Response: {"message": "Documents synchronized successfully"}
```

### Python Client API

```python
from megabot.api.client import APIClient

client = APIClient("http://localhost:5000")

# Health check
health = client.health()

# Bot control
client.start()
client.stop()
status = client.get_status()

# Operations
result = client.query("prompt")
research = client.research("topic", depth="deep")
workflow = client.execute_workflow("name", **params)
updates = client.get_updates(limit=10)
client.sync_documents()

# Capabilities
capabilities = client.get_capabilities()
```

## Best Practices

### 1. Error Handling

Always wrap operations in try-catch blocks:

```python
try:
    result = await bot.query(user_input)
except Exception as e:
    logger.error(f"Query failed: {e}")
    # Handle error appropriately
```

### 2. Resource Management

Use context managers for automatic cleanup:

```python
# API Client
with APIClient() as client:
    result = client.query("prompt")
# Automatically stops

# Direct usage
async with bot:
    result = await bot.query("prompt")
# Automatically stops
```

### 3. Caching

MEGA-Bot caches research results for 1 hour by default:

```python
# First call - queries all platforms
result1 = await bot.research("topic")

# Second call - uses cache (if within 1 hour)
result2 = await bot.research("topic")
```

### 4. Concurrent Operations

For multiple queries, use workflow system:

```python
workflow_result = await bot.execute_workflow(
    "comprehensive_analysis",
    topics=["topic1", "topic2", "topic3"]
)
```

### 5. API Key Management

- Store API keys in environment variables
- Never commit keys to version control
- Use different keys for dev/staging/production
- Rotate keys regularly

### 6. Rate Limiting

Implement rate limiting for production:

```python
from time import sleep

for query in queries:
    result = client.query(query)
    sleep(1)  # Rate limit to 1 query/second
```

### 7. Logging

Enable logging for debugging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('megabot')
```

### 8. Security

- Use HTTPS for API communications
- Implement authentication for API server
- Validate all user inputs
- Keep dependencies updated

## Examples

### Example 1: Simple Q&A Bot

```python
import asyncio
from megabot import MegaBot

async def qa_bot():
    bot = MegaBot()
    await bot.start()
    
    while True:
        question = input("Ask a question (or 'quit'): ")
        if question.lower() == 'quit':
            break
        
        result = await bot.query(question)
        for platform, resp in result['responses'].items():
            print(f"\n[{platform}]")
            print(resp['response'])
    
    await bot.stop()

asyncio.run(qa_bot())
```

### Example 2: Research Assistant

```python
import asyncio
from megabot import MegaBot

async def research_assistant(topic):
    bot = MegaBot()
    await bot.start()
    
    # Perform research
    result = await bot.research(topic, depth="deep")
    
    # Generate report
    report = f"""
    Research Report: {topic}
    ====================
    
    Platforms Used: {len(result['platforms_used'])}
    Total Findings: {result['synthesis']['total_findings']}
    
    Key Insights:
    """
    
    for platform in result['platforms_used']:
        report += f"\n- {platform}: {result['results'][platform]['summary']}"
    
    await bot.stop()
    return report

report = asyncio.run(research_assistant("quantum computing"))
print(report)
```

### Example 3: Web Service Integration

```python
from flask import Flask, request, jsonify
from megabot.api.client import APIClient

app = Flask(__name__)
client = APIClient()
client.start()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    
    try:
        result = client.query(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080)
```

### Example 4: Background Task Processor

```python
import asyncio
from megabot import MegaBot
from queue import Queue

async def process_tasks(task_queue, bot):
    while True:
        if not task_queue.empty():
            task = task_queue.get()
            
            if task['type'] == 'query':
                result = await bot.query(task['data'])
            elif task['type'] == 'research':
                result = await bot.research(task['data'])
            
            # Store result
            store_result(task['id'], result)
        
        await asyncio.sleep(1)

async def main():
    bot = MegaBot()
    await bot.start()
    
    task_queue = Queue()
    await process_tasks(task_queue, bot)

asyncio.run(main())
```

## Troubleshooting

### Common Issues

**Problem: Import Error**
```
Solution: Ensure MEGA-Bot is installed
pip install megaagent
```

**Problem: API Connection Failed**
```
Solution: Check server is running
megabot-server --port 5000
```

**Problem: No API Keys**
```
Solution: Bot works in demo mode without keys
Add keys to .env for real integrations
```

**Problem: Slow Responses**
```
Solution: 
- Check internet connection
- Verify API keys are valid
- Use caching for repeated queries
```

## Additional Resources

- [Installation Guide](INSTALLATION.md)
- [Publishing Guide](PUBLISHING.md)
- [API Documentation](DOCUMENTATION.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Integration Examples](examples/integrations/)

## Support

- GitHub Issues: https://github.com/ELMOURABEA/MEGAGENT/issues
- Documentation: https://github.com/ELMOURABEA/MEGAGENT
- Examples: [examples/](examples/)
