# MEGA-Bot Quick Start Guide

Get up and running with MEGA-Bot in 5 minutes!

## 1. Install MEGA-Bot

```bash
pip install megaagent
```

## 2. Verify Installation

```bash
megabot --version
```

## 3. Choose Your Usage Mode

### Option A: Try Demo Mode (Fastest)

```bash
megabot
```

This will:
- Show bot status and capabilities
- Demonstrate multi-platform queries
- Show research capabilities
- Display workflow automation

### Option B: Interactive Mode

```bash
megabot --interactive
```

Then try these commands:
```
MEGA-Bot> status
MEGA-Bot> query What is artificial intelligence?
MEGA-Bot> research machine learning
MEGA-Bot> exit
```

### Option C: Single Commands

```bash
# Quick query
megabot query "What is AI?"

# Deep research
megabot research "quantum computing" --depth deep
```

### Option D: API Server (For Integrations)

```bash
# Start server
megabot-server --port 5000

# In another terminal, test it:
curl http://localhost:5000/health
```

## 4. Use in Your Python Code

### Simple Script

```python
from megabot import MegaBot
import asyncio

async def main():
    bot = MegaBot()
    await bot.start()
    
    result = await bot.query("What is AI?")
    print(result)
    
    await bot.stop()

asyncio.run(main())
```

### Using API Client

```python
from megabot.api.client import APIClient

# Start server first: megabot-server

with APIClient("http://localhost:5000") as client:
    result = client.query("What is AI?")
    print(result)
```

## 5. Deploy with Docker

```bash
# Pull and run
docker run -p 5000:5000 elmourabea/megabot:latest

# Or use Docker Compose
docker-compose up -d
```

## 6. Configure API Keys (Optional)

For real AI integrations, add API keys:

Create `.env` file:
```bash
COPILOT_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
CHATGPT_API_KEY=your-key-here
GROK_API_KEY=your-key-here
```

**Note**: MEGA-Bot works in demo mode without API keys!

## Common Use Cases

### Q&A Bot
```bash
megabot --interactive
> query How does machine learning work?
```

### Research Assistant
```bash
megabot research "artificial intelligence" --depth deep
```

### Web Service
```bash
# Terminal 1: Start server
megabot-server --port 5000

# Terminal 2: Make requests
curl -X POST http://localhost:5000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?"}'
```

### Integration in Flask App
```python
from flask import Flask, jsonify
from megabot.api.client import APIClient

app = Flask(__name__)
client = APIClient()
client.start()

@app.route('/ask/<question>')
def ask(question):
    result = client.query(question)
    return jsonify(result)

app.run()
```

## Next Steps

- 📖 Read the [Usage Guide](USAGE_GUIDE.md) for detailed instructions
- 🔌 Check [Integration Examples](examples/integrations/) for more
- 🚀 See [Installation Guide](INSTALLATION.md) for advanced setup
- 📦 Review [Publishing Guide](PUBLISHING.md) to contribute

## Getting Help

- **Issues**: https://github.com/ELMOURABEA/MEGAGENT/issues
- **Documentation**: [DOCUMENTATION.md](DOCUMENTATION.md)
- **Examples**: [examples/](examples/)

## What's Included

✅ Multi-platform AI integration  
✅ Command-line interface  
✅ REST API server  
✅ Python client library  
✅ Docker support  
✅ Comprehensive documentation  
✅ Integration examples  

## System Requirements

- Python 3.8 or higher
- 512MB RAM minimum
- Internet connection (for AI platforms)

## Troubleshooting

### "Command not found: megabot"
```bash
# Ensure installation completed
pip install megaagent

# Check PATH
which megabot
```

### "Module not found"
```bash
# Reinstall
pip uninstall megaagent
pip install megaagent
```

### API server won't start
```bash
# Check port is available
# Try different port
megabot-server --port 5001
```

---

**Happy Bot Building! 🤖**

Need more help? Check the [full documentation](DOCUMENTATION.md) or [open an issue](https://github.com/ELMOURABEA/MEGAGENT/issues).
