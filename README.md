# MEGAGENT - XXXL MEGA BOT

<div align="center">

**Deep Research Database and Action Workflow System**

A unified AI agent integrating multiple cutting-edge platforms for comprehensive research, multi-tasking, and intelligent automation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.2.0-brightgreen.svg)](https://github.com/ELMOURABEA/MEGAGENT/releases/tag/v1.2.0)
[![Tests](https://img.shields.io/badge/tests-39%20passing-success.svg)](tests/)
[![GitHub Action](https://img.shields.io/badge/GitHub%20Action-Ready-blue.svg)](action.yml)
[![Marketplace](https://img.shields.io/badge/GitHub%20Marketplace-Published-orange.svg)](https://github.com/marketplace/actions/megagent-ai-multi-platform-integration)

</div>

## 🚀 Features

- **🔬 Deep Research Engine**: Comprehensive database research across multiple AI platforms
- **🤖 Multi-Platform Integration**: Unified access to Co-Pilot, Gemini 2.5 Pro, ChatGPT 5, and Grok 4 Super
- **⚡ Multi-Tasking**: Concurrent task execution with priority-based scheduling
- **🔄 Auto-Update System**: Automatic synchronization with latest platform documentation
- **🔐 Full Permission Management**: Comprehensive access control system
- **💾 Intelligent Caching**: Fast response times with smart result caching
- **📊 Workflow Automation**: Complex workflow execution with multiple steps
- **💰 Monetization System**: Flexible subscription tiers (Free, Pro, Full Energy)
- **📱 Advertising Integration**: Google AdMob support with banner and rewarded ads

## 🏗️ Architecture

MEGA-Bot integrates four powerful AI platforms:

1. **GitHub Copilot** - Code generation, review, and documentation
2. **Gemini 2.5 Pro** - Multimodal understanding with 2M token context
3. **ChatGPT 5** - Advanced reasoning and problem-solving
4. **Grok 4 Super** - Real-time data and social media insights

## 📦 Installation

### As a GitHub Action

Add to your workflow (`.github/workflows/your-workflow.yml`):

```yaml
- name: Run MEGAGENT
  uses: ELMOURABEA/MEGAGENT@v1.2.0
  with:
    mode: 'query'
    prompt: 'Your AI query here'
    tier: 'free'
```

See [MARKETPLACE.md](MARKETPLACE.md) for complete GitHub Action documentation.

### As a Python Package

```bash
# Clone the repository
git clone https://github.com/ELMOURABEA/MEGAGENT.git
cd MEGAGENT

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

## ⚙️ Configuration

### 1. Set up API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
COPILOT_API_KEY=your-copilot-api-key
GEMINI_API_KEY=your-gemini-api-key
CHATGPT_API_KEY=your-chatgpt-api-key
GROK_API_KEY=your-grok-api-key

# Optional: AdMob IDs for advertising integration
ADMOB_APP_ID=your-admob-app-id
ADMOB_BANNER_ID=your-admob-banner-id
ADMOB_INTERSTITIAL_ID=your-admob-interstitial-id
ADMOB_REWARDED_ID=your-admob-rewarded-id
```

### 2. Configure Settings

Copy the example configuration:

```bash
cp config.example.json config.json
```

Customize `config.json` for your needs.

## 🚀 Quick Start

### Demo Mode

Run the demo to see MEGA-Bot in action:

```bash
python main.py
```

### Interactive Mode

Use the interactive CLI:

```bash
python main.py --interactive
```

### Programmatic Usage

```python
from megabot import MegaBot
import asyncio

async def main():
    # Initialize MEGA-Bot
    bot = MegaBot()
    await bot.start()
    
    # Perform deep research
    result = await bot.research("artificial intelligence", depth="deep")
    print(f"Platforms used: {result['platforms_used']}")
    
    # Query all platforms
    response = await bot.query("What are the latest AI trends?")
    print(f"Responses from {len(response['responses'])} platforms")
    
    # Execute workflow
    workflow_result = await bot.execute_workflow(
        "comprehensive_analysis",
        topic="machine learning"
    )
    
    await bot.stop()

asyncio.run(main())
```

## 📚 Core Capabilities

### Deep Research

Perform comprehensive research across all platforms:

```python
result = await bot.research("quantum computing", depth="deep")
# Returns aggregated findings from all platforms
```

### Multi-Platform Queries

Get responses from all AI platforms simultaneously:

```python
result = await bot.query("Explain transformer architecture")
# Aggregates responses with confidence scores
```

### Workflow Automation

Execute complex multi-step workflows:

```python
result = await bot.execute_workflow(
    "comprehensive_analysis",
    topic="neural networks"
)
```

### Auto-Update System

Automatically sync latest platform updates:

```python
await bot.sync_documents()
updates = bot.get_updates(limit=10)
```

## 🎯 Use Cases

- **Research & Development**: Deep dive into technical topics across multiple sources
- **Code Development**: Leverage multiple AI assistants for code generation and review
- **Data Analysis**: Comprehensive analysis with different AI perspectives
- **Knowledge Synthesis**: Combine insights from multiple AI platforms
- **Automated Workflows**: Complex multi-step processes with intelligent coordination

## 🛠️ Components

### Core Modules

- **`megabot/core.py`** - Main orchestration layer
- **`megabot/integrations/`** - AI platform integrations
- **`megabot/database/`** - Research engine and storage
- **`megabot/workflow/`** - Task scheduling and permissions

### Platform Integrations

Each platform integration provides:
- Async query interface
- Deep research capabilities
- Latest updates retrieval
- Capability reporting

## 📊 Database Schema

MEGA-Bot maintains persistent storage for:

- Research cache (topic, platform, depth, results)
- Query history (queries and responses)
- Document updates (platform updates)
- Workflow tasks (scheduled tasks)

## 🔐 Permission System

Comprehensive permission management:

- **Full**: All operations (default)
- **Admin**: Read, write, execute
- **Write**: Read and write
- **Read**: Read-only

Resource types:
- Database access
- API integration
- Workflow execution
- Research operations

## 🌟 Advanced Features

### Concurrent Task Execution

Up to 10 simultaneous tasks (configurable):

```python
bot = MegaBot()
# Executes multiple research queries in parallel
```

### Intelligent Caching

1-hour cache for research results:

```python
# First call: queries all platforms
await bot.research("topic", depth="deep")

# Second call: uses cache (if within 1 hour)
await bot.research("topic", depth="deep")
```

### Result Synthesis

Automatic aggregation and synthesis of results:

```python
result = await bot.research("topic")
synthesis = result['synthesis']
# Contains unified insights from all platforms
```

### Input Validation & Security

Automatic validation and sanitization of user inputs:

```python
from megabot import validate_query, validate_topic

# Validate queries before processing
is_valid, error = validate_query("Your query here")

# Validate research topics
is_valid, error = validate_topic("Your topic here")
```

### Logging & Monitoring

Comprehensive logging for debugging and monitoring:

```python
from megabot import setup_logging

# Configure logging level
setup_logging("INFO")  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Monetization & Subscription Tiers

MEGA-Bot supports flexible subscription tiers:

```python
from megabot import MegaBot, Config

# Free tier (default)
bot_free = MegaBot()

# Pro tier (unlimited usage)
config = Config()
config.set("monetization.tier", "pro")
bot_pro = MegaBot(config)

# Check tier info
tier_info = bot_pro.get_tier_info()
print(f"Tier: {tier_info['tier']}")
print(f"Queries today: {tier_info['usage']['queries_today']}")
```

**Available Tiers:**
- **Free**: 10 queries/day, 5 research/day, shallow research only
- **Pro** ($9.99/month): Unlimited queries, all research depths, 10 concurrent tasks
- **Full Energy** ($29.99/month): Everything in Pro + 20 concurrent tasks + priority support

### Advertising Integration

Google AdMob integration for monetization:

```python
# Show banner ad
result = bot.show_banner_ad("bottom")

# Show rewarded ad for bonus features
result = bot.show_rewarded_ad("bonus_queries")
print(f"Reward: {result['reward']['description']}")
```

## 📖 Documentation

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

Topics covered:
- Architecture details
- API reference
- Configuration options
- Advanced usage
- Troubleshooting
- Best practices

## 🧪 Testing

Run tests:

```bash
pip install -r requirements.txt
pytest
```

Current test coverage: 39 tests covering:
- Configuration management
- AI platform integrations
- Core functionality
- Database operations
- Workflow components
- Input validation and utilities
- Monetization and subscription tiers
- Advertising integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- GitHub Copilot team
- Google Gemini team
- OpenAI team
- X.AI Grok team

## 📧 Contact

For questions and support, please open an issue on GitHub.

---

<div align="center">

**Built with ❤️ by the MEGAGENT Team**

*Integrating the power of multiple AI platforms into one unified solution*

</div>
