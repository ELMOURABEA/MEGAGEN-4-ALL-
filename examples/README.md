# MEGA-Bot Examples

This directory contains example scripts demonstrating different aspects of MEGA-Bot functionality.

## Examples Overview

### 1. Basic Usage (`basic_usage.py`)

Demonstrates fundamental MEGA-Bot operations:
- Initializing and starting the bot
- Simple queries to all platforms
- Basic research operations
- Status checking
- Getting capabilities

**Run:**
```bash
python examples/basic_usage.py
```

**What it shows:**
- Query execution across platforms
- Research with different depths
- Bot status and health check
- Capability listing

---

### 2. Advanced Research (`advanced_research.py`)

Shows advanced research capabilities:
- Deep research on multiple topics
- Comprehensive analysis workflow
- Result synthesis and aggregation
- Platform-specific insights

**Run:**
```bash
python examples/advanced_research.py
```

**What it shows:**
- Multi-topic deep research
- Workflow execution
- Finding aggregation
- Key insights extraction

---

### 3. Workflow Automation (`workflow_automation.py`)

Demonstrates workflow and automation features:
- Pre-built workflow execution
- Custom workflow creation
- Document synchronization
- Update management

**Run:**
```bash
python examples/workflow_automation.py
```

**What it shows:**
- Comprehensive analysis workflow
- Multi-platform query workflow
- Deep dive research workflow
- Document sync operations

---

### 4. Validation Example (`validation_example.py`) [NEW in v1.1.0]

Demonstrates input validation and security features:
- Query validation and sanitization
- Topic validation
- Automatic input security checks
- Logging configuration
- Error handling examples

**Run:**
```bash
python examples/validation_example.py
```

**What it shows:**
- Input validation for queries and topics
- Automatic sanitization of dangerous content
- Logging system configuration
- Security best practices
- Error message handling

---

## Running Examples

### Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Configure API keys:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Note: Examples work without API keys in demo mode with simulated responses.

### Execute Examples

```bash
# From project root
python examples/basic_usage.py
python examples/advanced_research.py
python examples/workflow_automation.py
python examples/validation_example.py  # New in v1.1.0
```

### Expected Output

Without API keys (demo mode):
- Examples run successfully
- Show 0 active integrations
- Demonstrate architecture and flow
- Display simulated operations

With API keys (live mode):
- Real responses from AI platforms
- Actual research results
- Live document updates
- Full integration testing

---

## Creating Your Own Examples

### Template

```python
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from megabot import MegaBot

async def my_example():
    """Your custom example"""
    bot = MegaBot()
    await bot.start()
    
    # Your code here
    result = await bot.query("Your query")
    print(result)
    
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(my_example())
```

---

## Common Use Cases

### 1. Multi-Platform Query

```python
result = await bot.query("Explain quantum computing")
for platform, response in result['responses'].items():
    print(f"{platform}: {response['response']}")
```

### 2. Deep Research

```python
research = await bot.research("machine learning", depth="deep")
print(f"Findings: {len(research['findings'])}")
print(f"Sources: {research['aggregated_sources']}")
```

### 3. Workflow Execution

```python
result = await bot.execute_workflow(
    "comprehensive_analysis",
    topic="artificial intelligence"
)
print(result['final_analysis'])
```

### 4. Status Monitoring

```python
status = bot.get_status()
print(f"Active platforms: {status['integrations']['active']}")
print(f"Permissions: {status['permissions']}")
```

### 5. Update Sync

```python
await bot.sync_documents()
updates = bot.get_updates(limit=10)
for update in updates:
    print(f"[{update['platform']}] {update['title']}")
```

---

## Troubleshooting

### Import Errors

If you get import errors, ensure you're running from the project root or the examples directory:

```bash
# From project root
python examples/basic_usage.py

# From examples directory
cd examples
python basic_usage.py
```

### No Active Integrations

This is normal without API keys. The bot runs in demo mode. To enable live integrations:

1. Get API keys from respective platforms
2. Add to `.env` or `config.json`
3. Restart the examples

### Async Warnings

If you see warnings about event loops, ensure you're using Python 3.8+:

```bash
python --version  # Should be 3.8 or higher
```

---

## Next Steps

After running the examples:

1. **Explore the Code**: Read through example code to understand patterns
2. **Check Documentation**: See `DOCUMENTATION.md` for detailed API reference
3. **Review Architecture**: See `ARCHITECTURE.md` for system design
4. **Run Tests**: Execute `pytest tests/` to see unit tests
5. **Create Custom Examples**: Build your own using the templates above

---

## Additional Resources

- **Main Documentation**: `../DOCUMENTATION.md`
- **Architecture Guide**: `../ARCHITECTURE.md`
- **API Reference**: `../DOCUMENTATION.md#api-reference`
- **Testing Guide**: `../tests/test_megabot.py`

---

## Support

For issues or questions:
- Check the main README.md
- Review documentation
- Open an issue on GitHub
- Review existing examples for patterns
