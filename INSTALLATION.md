# MEGA-Bot Installation Guide

Complete guide to installing and deploying MEGA-Bot in various environments.

## Quick Install

### Option 1: Install from Source
```bash
git clone https://github.com/ELMOURABEA/MEGAGENT.git
cd MEGAGENT
pip install -e .
```

### Option 2: Install with All Features
```bash
# Install with API server support
pip install megaagent[api]

# Install with development tools
pip install megaagent[dev]

# Install everything
pip install megaagent[all]
```

## System Requirements

- **Operating System:** Linux, macOS, Windows
- **Memory:** Minimum 512MB RAM (1GB recommended)
- **Disk Space:** ~100MB for installation

## Detailed Installation

#### Using venv (Recommended)
```bash
# Create virtual environment
python -m venv megabot-env

# Activate (Linux/Mac)
source megabot-env/bin/activate

# Activate (Windows)
megabot-env\Scripts\activate

# Install MEGA-Bot
pip install megaagent
```

#### Using conda
```bash
# Create conda environment
conda create -n megabot python=3.11

# Activate
conda activate megabot

# Install MEGA-Bot
pip install megaagent
```

### 2. Configuration

#### Environment Variables
Create a `.env` file:
```bash
# Copy example
cp .env.example .env

# Edit with your API keys
nano .env
```

Example `.env` file:
```bash
# AI Platform API Keys (optional - bot works without them in demo mode)
COPILOT_API_KEY=your-copilot-api-key
GEMINI_API_KEY=your-gemini-api-key
CHATGPT_API_KEY=your-chatgpt-api-key
GROK_API_KEY=your-grok-api-key

# Database (optional)
DATABASE_PATH=/path/to/megabot.db

# Features (optional)
AUTO_UPDATE=true
DOCUMENT_SYNC=true
```

#### Configuration File
Create `config.json`:
```bash
cp config.example.json config.json
nano config.json
```

Example `config.json`:
```json
{
  "api_keys": {
    "copilot": "",
    "gemini": "",
    "chatgpt": "",
    "grok": ""
  },
  "database": {
    "path": "megabot.db"
  },
  "workflow": {
    "max_concurrent_tasks": 10,
    "permission_level": "full",
    "auto_update_interval": 3600
  },
  "features": {
    "auto_update": true,
    "document_sync": true,
    "caching": true,
    "cache_ttl": 3600
  }
}
```

### 3. Verify Installation

```bash
# Check version
megabot --version

# Run demo
megabot

# Test import
python -c "from megabot import MegaBot; print('Installation successful!')"
```

## Deployment Options

### Option A: Standalone Bot

Run MEGA-Bot as a standalone application:

```bash
# Demo mode
megabot

# Interactive mode
megabot --interactive

# Single query
megabot query "What is AI?"

# Research
megabot research "machine learning" --depth deep
```

### Option B: API Server

Run MEGA-Bot as an API server for integration:

```bash
# Start API server
megabot-server --port 5000

# With debug mode
megabot-server --port 5000 --debug
```

### Option C: Docker Container

Run MEGA-Bot in a Docker container:

```bash
# Build image
docker build -t megabot .

# Run container
docker run -p 5000:5000 \
  -v $(pwd)/data:/data \
  -v $(pwd)/.env:/app/.env:ro \
  megabot

# Using Docker Compose
docker-compose up -d
```

### Option D: System Service (Linux)

Create a systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/megabot.service
```

Service file content:
```ini
[Unit]
Description=MEGA-Bot API Server
After=network.target

[Service]
Type=simple
User=megabot
WorkingDirectory=/opt/megabot
Environment="PATH=/opt/megabot/venv/bin"
ExecStart=/opt/megabot/venv/bin/megabot-server --port 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable megabot
sudo systemctl start megabot
sudo systemctl status megabot
```

## Platform-Specific Instructions

### Linux

```bash
# Install system dependencies (if needed)
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# Install MEGA-Bot
python3 -m venv venv
source venv/bin/activate
pip install megaagent
```

### macOS

```bash
# Install Python using Homebrew (if needed)
brew install python@3.11

# Install MEGA-Bot
python3 -m venv venv
source venv/bin/activate
pip install megaagent
```

### Windows

```powershell
# Install Python from python.org if needed

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install MEGA-Bot
pip install megaagent
```

## Cloud Deployment

### AWS EC2

```bash
# Launch EC2 instance (Ubuntu)
# SSH into instance

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip

# Install MEGA-Bot
pip3 install megaagent

# Run as service
megabot-server --port 5000 &
```

### Google Cloud Platform

```bash
# Create Compute Engine instance
# SSH into instance

# Install MEGA-Bot
pip3 install megaagent

# Run with PM2 (if installed)
pm2 start megabot-server -- --port 5000
```

### Heroku

Create `Procfile`:
```
web: megabot-server --port $PORT
```

Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
heroku create your-megabot-app
git push heroku main
```

### Docker Hub

```bash
# Pull from Docker Hub (when published)
docker pull elmourabea/megabot:latest

# Run
docker run -p 5000:5000 elmourabea/megabot:latest
```

## Troubleshooting

### Installation Issues

**Problem:** `pip install` fails
```bash
# Solution: Upgrade pip
pip install --upgrade pip setuptools wheel
```

**Problem:** Permission denied
```bash
# Solution: Use virtual environment or --user flag
pip install --user megaagent
```

**Problem:** Python version too old
```bash
# Solution: Install Python 3.8+
# Linux
sudo apt-get install python3.11

# macOS
brew install python@3.11

# Or use pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

### Runtime Issues

**Problem:** Module not found
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

**Problem:** Port already in use
```bash
# Solution: Use different port
megabot-server --port 5001
```

**Problem:** Database permission denied
```bash
# Solution: Check database path permissions
chmod 755 /path/to/data/directory
```

## Upgrading

### From PyPI
```bash
pip install --upgrade megaagent
```

### From Source
```bash
cd MEGAGENT
git pull origin main
pip install --upgrade -e .
```

### Docker
```bash
docker pull elmourabea/megabot:latest
docker-compose up -d --build
```

## Uninstallation

### Remove Package
```bash
pip uninstall megaagent
```

### Remove Data
```bash
# Remove database and cache
rm -rf ~/.megabot
rm -f megabot.db

# Remove Docker volumes
docker-compose down -v
```

## Next Steps

After installation:

1. **Configuration:** Set up API keys and preferences
2. **Testing:** Run `megabot` to test the installation
3. **Integration:** Choose your integration method (CLI, API, or direct)
4. **Documentation:** Read [DOCUMENTATION.md](DOCUMENTATION.md) for detailed usage

## Support

- **Documentation:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Examples:** [examples/](examples/)
- **Issues:** [GitHub Issues](https://github.com/ELMOURABEA/MEGAGENT/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ELMOURABEA/MEGAGENT/discussions)
