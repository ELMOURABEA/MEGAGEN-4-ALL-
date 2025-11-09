# MEGA-Bot Integration Examples

This directory contains examples of how to integrate MEGA-Bot into different applications and systems.

## Available Examples

### 1. API Client Example (`api_client_example.py`)
Demonstrates how to use the MEGA-Bot API client to integrate with any Python application.

**Features:**
- Basic API client usage
- Context manager pattern
- Custom application integration
- Error handling

**Usage:**
```bash
# Terminal 1: Start the API server
megabot-server --port 5000

# Terminal 2: Run the example
python examples/integrations/api_client_example.py
```

### 2. Flask Integration (`flask_integration.py`)
Example of integrating MEGA-Bot into a Flask web application with a simple UI.

**Features:**
- Web-based interface
- Real-time query processing
- Status monitoring
- Simple HTML/CSS/JavaScript frontend

**Usage:**
```bash
python examples/integrations/flask_integration.py
# Open http://localhost:5001 in your browser
```

## Integration Patterns

### Pattern 1: Direct Integration
Import and use MEGA-Bot directly in your application:

```python
from megabot import MegaBot, Config
import asyncio

async def main():
    bot = MegaBot()
    await bot.start()
    result = await bot.query("Your question")
    await bot.stop()

asyncio.run(main())
```

### Pattern 2: API Client Integration
Use the API client to connect to a running MEGA-Bot server:

```python
from megabot.api.client import APIClient

with APIClient("http://localhost:5000") as client:
    result = client.query("Your question")
    print(result)
```

### Pattern 3: REST API Integration
Use HTTP requests from any language or framework:

```bash
# Start bot
curl -X POST http://localhost:5000/api/v1/start

# Query
curl -X POST http://localhost:5000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?"}'
```

## Creating Your Own Integration

### For Python Applications

1. **Install MEGA-Bot:**
   ```bash
   pip install megaagent
   ```

2. **Direct Integration:**
   ```python
   from megabot import MegaBot
   import asyncio
   
   class YourApp:
       def __init__(self):
           self.bot = MegaBot()
       
       async def start(self):
           await self.bot.start()
       
       async def query(self, prompt):
           return await self.bot.query(prompt)
   ```

3. **API Client Integration:**
   ```python
   from megabot.api.client import APIClient
   
   class YourApp:
       def __init__(self):
           self.client = APIClient("http://localhost:5000")
           self.client.start()
       
       def query(self, prompt):
           return self.client.query(prompt)
   ```

### For Web Applications

1. **Start the API server:**
   ```bash
   megabot-server --port 5000
   ```

2. **Use JavaScript/Fetch API:**
   ```javascript
   // Start bot
   fetch('http://localhost:5000/api/v1/start', {
       method: 'POST'
   });
   
   // Query
   fetch('http://localhost:5000/api/v1/query', {
       method: 'POST',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({prompt: 'What is AI?'})
   })
   .then(r => r.json())
   .then(data => console.log(data));
   ```

### For Other Languages

Use HTTP REST API:

**Node.js:**
```javascript
const axios = require('axios');

const client = axios.create({
    baseURL: 'http://localhost:5000'
});

// Start bot
await client.post('/api/v1/start');

// Query
const result = await client.post('/api/v1/query', {
    prompt: 'What is AI?'
});
```

**cURL:**
```bash
curl -X POST http://localhost:5000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?"}'
```

## API Endpoints

### Bot Control
- `POST /api/v1/start` - Start the bot
- `POST /api/v1/stop` - Stop the bot
- `GET /api/v1/status` - Get bot status

### Operations
- `POST /api/v1/query` - Query all AI platforms
- `POST /api/v1/research` - Perform deep research
- `POST /api/v1/workflow` - Execute a workflow
- `GET /api/v1/updates` - Get platform updates
- `POST /api/v1/sync` - Sync documents

### Monitoring
- `GET /health` - Health check
- `GET /api/v1/capabilities` - Get bot capabilities

## Docker Integration

Run MEGA-Bot in a container:

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t megabot .
docker run -p 5000:5000 -v $(pwd)/data:/data megabot
```

## Best Practices

1. **Error Handling:** Always wrap API calls in try-catch blocks
2. **Timeouts:** Set appropriate timeouts for long-running operations
3. **Resource Management:** Use context managers or ensure proper cleanup
4. **API Keys:** Store API keys securely in environment variables
5. **Rate Limiting:** Implement rate limiting for production use
6. **Logging:** Add logging for debugging and monitoring

## Troubleshooting

### Connection Refused
- Ensure the API server is running: `megabot-server`
- Check the server is listening on the correct port
- Verify firewall settings

### Import Errors
- Install MEGA-Bot: `pip install megaagent`
- Check Python path and virtual environment

### Timeout Errors
- Increase timeout in client: `APIClient(timeout=60)`
- Check API keys are configured correctly
- Verify network connectivity

## Support

For more examples and documentation, see:
- [Main Documentation](../../DOCUMENTATION.md)
- [Architecture](../../ARCHITECTURE.md)
- [GitHub Repository](https://github.com/ELMOURABEA/MEGAGENT)
