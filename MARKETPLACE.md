# MEGAGENT - GitHub Marketplace Guide

## Overview

MEGAGENT is a unified AI agent that integrates multiple cutting-edge AI platforms (GitHub Copilot, Gemini, ChatGPT, and Grok) into your GitHub workflows. Use it to automate research, analysis, and AI-powered tasks directly in your CI/CD pipelines.

## Installation

### As a GitHub Action

Add MEGAGENT to your workflow:

```yaml
- name: Run MEGAGENT Query
  uses: ELMOURABEA/MEGAGENT@v1.2.0
  with:
    mode: 'query'
    prompt: 'What are the latest AI trends?'
    tier: 'free'
```

### As a Python Package

```bash
pip install git+https://github.com/ELMOURABEA/MEGAGENT.git
```

## Usage Examples

### 1. AI-Powered Code Review

```yaml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Analyze PR with MEGAGENT
        uses: ELMOURABEA/MEGAGENT@v1.2.0
        with:
          mode: 'query'
          prompt: 'Review this code for best practices and potential issues'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          chatgpt-api-key: ${{ secrets.CHATGPT_API_KEY }}
          tier: 'pro'
```

### 2. Deep Research Workflow

```yaml
name: Research Report

on:
  workflow_dispatch:
    inputs:
      topic:
        description: 'Research topic'
        required: true

jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - name: Deep Research
        uses: ELMOURABEA/MEGAGENT@v1.2.0
        id: research
        with:
          mode: 'research'
          prompt: ${{ github.event.inputs.topic }}
          depth: 'deep'
          copilot-api-key: ${{ secrets.COPILOT_API_KEY }}
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          chatgpt-api-key: ${{ secrets.CHATGPT_API_KEY }}
          grok-api-key: ${{ secrets.GROK_API_KEY }}
          tier: 'full_energy'
      
      - name: Process Results
        run: |
          echo "Platforms used: ${{ steps.research.outputs.platforms-used }}"
          echo "Results: ${{ steps.research.outputs.synthesis }}"
```

### 3. Automated Documentation

```yaml
name: Generate Docs

on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Documentation
        uses: ELMOURABEA/MEGAGENT@v1.2.0
        with:
          mode: 'workflow'
          workflow-name: 'comprehensive_analysis'
          prompt: 'Generate comprehensive documentation for this project'
          copilot-api-key: ${{ secrets.COPILOT_API_KEY }}
```

### 4. Multi-Platform Query

```yaml
name: Weekly AI Digest

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM

jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - name: Query All AI Platforms
        uses: ELMOURABEA/MEGAGENT@v1.2.0
        id: digest
        with:
          mode: 'query'
          prompt: 'What are the most important AI developments this week?'
          copilot-api-key: ${{ secrets.COPILOT_API_KEY }}
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          chatgpt-api-key: ${{ secrets.CHATGPT_API_KEY }}
          grok-api-key: ${{ secrets.GROK_API_KEY }}
          tier: 'pro'
      
      - name: Create Issue with Digest
        uses: actions/github-script@v7
        with:
          script: |
            const result = ${{ steps.digest.outputs.result }};
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Weekly AI Digest',
              body: `# AI Digest\n\n${JSON.stringify(result, null, 2)}`
            });
```

## Configuration

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `mode` | Operation mode: `query`, `research`, or `workflow` | Yes | `query` |
| `prompt` | Query prompt or research topic | Yes | - |
| `depth` | Research depth: `shallow`, `medium`, or `deep` | No | `medium` |
| `workflow-name` | Workflow name to execute (for workflow mode) | No | - |
| `copilot-api-key` | GitHub Copilot API key | No | - |
| `gemini-api-key` | Google Gemini API key | No | - |
| `chatgpt-api-key` | OpenAI ChatGPT API key | No | - |
| `grok-api-key` | X.AI Grok API key | No | - |
| `tier` | Subscription tier: `free`, `pro`, or `full_energy` | No | `free` |

### Outputs

| Output | Description |
|--------|-------------|
| `result` | JSON result from the MEGAGENT operation |
| `platforms-used` | Number of AI platforms that responded |
| `synthesis` | Synthesized results from all platforms |

### Subscription Tiers

#### Free Tier
- 10 queries per day
- 5 research operations per day
- Shallow research only
- No concurrent tasks

#### Pro Tier ($9.99/month)
- Unlimited queries
- Unlimited research
- All research depths (shallow, medium, deep)
- Up to 10 concurrent tasks

#### Full Energy Tier ($29.99/month)
- Everything in Pro
- Up to 20 concurrent tasks
- Priority support
- Advanced features

## API Keys

Store your API keys as GitHub secrets:

1. Go to your repository settings
2. Navigate to Secrets and variables → Actions
3. Add new secrets:
   - `COPILOT_API_KEY`
   - `GEMINI_API_KEY`
   - `CHATGPT_API_KEY`
   - `GROK_API_KEY`

## Features

- **Multi-Platform Integration**: Query multiple AI platforms simultaneously
- **Deep Research**: Comprehensive research with result synthesis
- **Workflow Automation**: Complex multi-step workflows
- **Intelligent Caching**: Fast response times with smart caching
- **Flexible Configuration**: Customizable through inputs and environment
- **Subscription Management**: Multiple tiers for different needs

## Security

- API keys are securely stored as GitHub secrets
- Input validation and sanitization
- No data retention between runs
- Comprehensive security features (see SECURITY.md)

## Support

- **Documentation**: [Full documentation](https://github.com/ELMOURABEA/MEGAGENT/blob/main/DOCUMENTATION.md)
- **Issues**: [Report bugs or request features](https://github.com/ELMOURABEA/MEGAGENT/issues)
- **Discussions**: [Community discussions](https://github.com/ELMOURABEA/MEGAGENT/discussions)
- **Security**: [Report security issues](https://github.com/ELMOURABEA/MEGAGENT/blob/main/SECURITY.md)

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Links

- **Repository**: https://github.com/ELMOURABEA/MEGAGENT
- **Issues**: https://github.com/ELMOURABEA/MEGAGENT/issues
- **Marketplace**: https://github.com/marketplace/actions/megagent-ai-multi-platform-integration
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

**Built with ❤️ by the MEGAGENT Team**

*Integrating the power of multiple AI platforms into your GitHub workflows*
