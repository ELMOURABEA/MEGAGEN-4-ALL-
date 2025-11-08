# GitHub Copilot Instructions for MEGAGENT

## Project Overview

**MEGAGENT (XXXL MEGA BOT)** is a unified AI agent integration system that combines multiple cutting-edge AI platforms (GitHub Copilot, Google Gemini 2.5 Pro, ChatGPT 5, and Grok 4 Super) to provide deep research capabilities, multi-tasking workflows, and comprehensive data analysis.

### Key Capabilities
- **Deep Research Engine**: Multi-platform concurrent research with intelligent caching
- **Multi-Platform Queries**: Aggregated responses from all integrated AI platforms
- **Workflow Automation**: Priority-based task scheduling with full permission management
- **Auto-Update System**: Automatic synchronization with platform documentation
- **Database Storage**: SQLite-based persistent storage for research, queries, and updates

## Project Structure

```
MEGAGENT/
├── megabot/                    # Main package (all code here)
│   ├── __init__.py            # Package exports
│   ├── core.py                # MegaBot class - main orchestration layer
│   ├── config.py              # Configuration management (JSON/env vars)
│   ├── integrations/          # AI platform integrations
│   │   ├── base.py           # BaseIntegration abstract class
│   │   ├── copilot.py        # GitHub Copilot integration
│   │   ├── gemini.py         # Gemini 2.5 Pro integration
│   │   ├── chatgpt.py        # ChatGPT 5 integration
│   │   └── grok.py           # Grok 4 Super integration
│   ├── database/              # Database & research engine
│   │   ├── storage.py        # DatabaseStorage (SQLite)
│   │   └── research_engine.py # ResearchEngine (query/research logic)
│   └── workflow/              # Workflow management
│       ├── scheduler.py      # TaskScheduler (priority queues, async workers)
│       ├── permissions.py    # PermissionManager (access control)
│       └── auto_update.py    # AutoUpdateManager (doc sync)
├── examples/                  # Usage examples
├── tests/                     # Test suite (pytest)
├── main.py                    # CLI entry point (demo & interactive modes)
├── setup.py                   # Package installation
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
└── config.example.json       # Configuration template
```

## Architecture & Design Patterns

### Core Architecture
1. **MegaBot Core** (`megabot/core.py`): Main orchestration layer that coordinates all subsystems
2. **Integration Layer**: Async interfaces to AI platforms (all extend `BaseIntegration`)
3. **Database Layer**: Research caching, query history, document storage
4. **Workflow Layer**: Task scheduling, permissions, auto-updates

### Key Design Patterns Used
- **Async/Await**: All I/O operations are non-blocking
- **Factory Pattern**: Integration creation through base class
- **Observer Pattern**: Auto-update manager for platform changes
- **Strategy Pattern**: Different research depths (shallow, medium, deep)
- **Singleton-like**: Database storage instance per path

### Data Flow
```
User Request → MegaBot.query()/research()
  → Check Cache
  → Query all integrations concurrently
  → Aggregate & synthesize results
  → Store in database
  → Return to user
```

## Code Style & Conventions

### Python Standards
- **Python Version**: 3.8+ (asyncio features required)
- **Style**: Follow PEP 8 conventions
- **Type Hints**: Use typing module for function signatures
- **Docstrings**: Google-style docstrings for all classes and public methods
- **Async**: All I/O operations use `async`/`await`

### Naming Conventions
- Classes: `PascalCase` (e.g., `MegaBot`, `ResearchEngine`)
- Functions/Methods: `snake_case` (e.g., `deep_research`, `query_all_platforms`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_CONCURRENT_TASKS`)
- Private methods: prefix with `_` (e.g., `_init_integrations`)

### File Organization
- Each module has a clear, single responsibility
- All imports at the top, grouped: standard library, third-party, local
- Use relative imports within the package (e.g., `from .config import Config`)

### Error Handling
- Use try/except blocks for I/O operations
- Graceful degradation: system continues with fewer integrations if some fail
- Log warnings instead of crashing on non-critical errors
- Return meaningful error messages to users

## Development Workflow

### Setting Up Development Environment
```bash
# Clone and enter directory
git clone https://github.com/ELMOURABEA/MEGAGENT.git
cd MEGAGENT

# Install dependencies
pip install -r requirements.txt

# Optional: Install as editable package
pip install -e .

# Set up environment (optional - system works without API keys)
cp .env.example .env
# Edit .env to add API keys if available
```

### Running the Project
```bash
# Demo mode (shows all features)
python main.py

# Interactive mode
python main.py --interactive

# Run examples
python examples/basic_usage.py
python examples/advanced_research.py
python examples/workflow_automation.py

# Run tests
pytest tests/ -v
```

### Testing Approach
- **Test Framework**: pytest with pytest-asyncio
- **Test Location**: `tests/test_megabot.py` (19 tests, all passing)
- **Coverage Areas**: Config, Integrations, Core, Database, Workflow
- **Async Testing**: Use `@pytest.mark.asyncio` decorator for async tests
- **Test Data**: Tests use simulated responses (no real API calls needed)

### Making Changes
1. **Before Changes**: Run tests to ensure baseline passes
2. **During Development**: 
   - Keep changes minimal and focused
   - Follow existing patterns in similar modules
   - Add/update docstrings for public APIs
3. **After Changes**: Run tests again to verify no regressions
4. **No API Keys Needed**: System works with simulated responses for development

## Key Components Deep Dive

### 1. MegaBot Core (`megabot/core.py`)
- **Purpose**: Main orchestration and unified API
- **Key Methods**:
  - `start()`: Initialize all services (auto-update, document sync)
  - `query(prompt, context)`: Query all platforms concurrently
  - `research(topic, depth)`: Perform deep research with synthesis
  - `execute_workflow(name, **kwargs)`: Run multi-step workflows
  - `get_status()`: System status and active integrations
  - `sync_documents()`: Manually trigger document synchronization
- **Initialization**: Auto-creates default config if none provided
- **Background Tasks**: Tracks async tasks for cleanup

### 2. Integrations (`megabot/integrations/`)
- **Base Class**: `BaseIntegration` in `base.py` - defines interface
- **Required Methods**:
  - `query(prompt, context)`: Single query to platform
  - `research(topic, depth)`: Deep research query
  - `get_latest_updates()`: Fetch platform documentation updates
  - `get_capabilities()`: List platform capabilities
- **Common Pattern**: Check `is_available()` before using
- **API Keys**: Stored in config, empty string if not available
- **Simulated Mode**: Returns mock data when API key is empty

### 3. Database Storage (`megabot/database/storage.py`)
- **Database**: SQLite (file-based, no server needed)
- **Tables**:
  - `research_cache`: Cached research results (topic, platform, results, timestamp)
  - `query_history`: All query records
  - `document_updates`: Platform documentation updates
  - `workflow_tasks`: Scheduled tasks and results
- **Cache TTL**: 1 hour for research results
- **Thread-Safe**: Uses SQLite's built-in thread safety

### 4. Research Engine (`megabot/database/research_engine.py`)
- **Purpose**: Coordinates multi-platform research and synthesis
- **Key Methods**:
  - `deep_research(topic, depth)`: Concurrent research across platforms
  - `query_all_platforms(prompt)`: Parallel queries with aggregation
- **Caching**: Checks cache before querying platforms
- **Synthesis**: Aggregates responses, calculates confidence scores

### 5. Workflow Components (`megabot/workflow/`)
- **TaskScheduler**: Priority-based async task queue, max 10 concurrent tasks
- **PermissionManager**: Five levels (read, write, execute, admin, full)
- **AutoUpdateManager**: Periodic updates (default 1 hour interval)

### 6. Configuration (`megabot/config.py`)
- **Sources**: JSON file (config.json) + environment variables
- **Priority**: Environment variables override JSON config
- **Access**: Dot notation (e.g., `config.get("database.path")`)
- **Default Config**: Created automatically if file doesn't exist

## Common Tasks & Patterns

### Adding a New AI Platform Integration
1. Create new file in `megabot/integrations/` (e.g., `new_platform.py`)
2. Extend `BaseIntegration` class
3. Implement required methods: `query()`, `research()`, `get_latest_updates()`, `get_capabilities()`
4. Set `platform_name` in constructor
5. Add to `__init__.py` exports
6. Update `MegaBot._init_integrations()` to include new integration
7. Add API key handling to `config.py` default config

### Adding New Database Tables
1. Add table creation in `DatabaseStorage.__init__()`
2. Follow pattern: `CREATE TABLE IF NOT EXISTS table_name (...)`
3. Add methods to interact with table (insert, query, update)
4. Use parameterized queries to prevent SQL injection
5. Use `self.conn.commit()` after writes

### Creating Custom Workflows
```python
async def custom_workflow(bot, **kwargs):
    # Step 1: Perform research
    research = await bot.research(kwargs['topic'])
    
    # Step 2: Query for analysis
    query = await bot.query(f"Analyze {kwargs['topic']}")
    
    # Step 3: Combine results
    return {
        'research': research,
        'analysis': query,
        'combined': process_results(research, query)
    }

# Execute workflow
result = await bot.execute_workflow("custom_workflow", topic="AI ethics")
```

### Testing New Features
```python
import pytest
from megabot import MegaBot

@pytest.mark.asyncio
async def test_new_feature():
    bot = MegaBot()
    await bot.start()
    
    # Test your feature
    result = await bot.new_feature()
    assert result is not None
    
    await bot.stop()
```

## Dependencies & External Libraries

### Required Dependencies
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support

### Standard Library Usage
- **asyncio**: All async operations
- **sqlite3**: Database operations
- **json**: Configuration files
- **os**: Environment variables and file paths
- **typing**: Type hints

### No External API Libraries
- Project uses **simulated responses** for development
- Real API integration can be added later with libraries like:
  - `openai` for ChatGPT
  - `google-generativeai` for Gemini
  - Custom HTTP clients for other platforms

## Troubleshooting & Common Issues

### Issue: "No platforms available"
- **Cause**: No API keys configured (this is normal for development)
- **Solution**: System works in simulated mode; add API keys to `.env` for real integrations

### Issue: "Database is locked"
- **Cause**: Multiple processes accessing same database file
- **Solution**: Ensure proper async handling; close connections with `await bot.stop()`

### Issue: Import errors
- **Cause**: Dependencies not installed
- **Solution**: Run `pip install -r requirements.txt`

### Issue: Tests failing
- **Cause**: Environment or code changes
- **Solution**: Check test output; most tests are independent and shouldn't fail

### Performance Considerations
- **Concurrent Limit**: Default 10 tasks; configurable in config
- **Cache TTL**: 1 hour default; adjust in `research_engine.py` if needed
- **Database Growth**: SQLite file grows with usage; implement cleanup if needed

## Best Practices for AI Coding Agents

### When Adding Features
1. **Study existing patterns first**: Look at similar components before creating new ones
2. **Maintain async consistency**: All I/O operations must be async
3. **Follow the architecture**: Don't bypass layers (e.g., access database through research engine)
4. **Update tests**: Add tests for new functionality
5. **Update documentation**: Keep README.md in sync with changes

### When Fixing Bugs
1. **Write a failing test first**: Reproduces the bug
2. **Make minimal changes**: Fix only what's broken
3. **Verify the fix**: Ensure test passes and no regressions
4. **Check related code**: Look for similar patterns that might have same bug

### When Refactoring
1. **Ensure tests pass first**: Know the baseline
2. **Make small, incremental changes**: One refactor at a time
3. **Run tests frequently**: After each change
4. **Preserve public APIs**: Don't break existing usage patterns

### Code Quality Checklist
- [ ] Follows existing code style and conventions
- [ ] Has docstrings for public APIs
- [ ] Uses type hints for function signatures
- [ ] Handles errors gracefully
- [ ] Works in async context
- [ ] Tests pass (run `pytest tests/`)
- [ ] No hardcoded values (use config)
- [ ] No breaking changes to public APIs

## Configuration Examples

### Minimal Setup (No API Keys)
```json
{
  "database": {
    "path": "megabot.db"
  },
  "workflow": {
    "max_concurrent_tasks": 10
  }
}
```

### Full Configuration
```json
{
  "api_keys": {
    "copilot": "your-key",
    "gemini": "your-key",
    "chatgpt": "your-key",
    "grok": "your-key"
  },
  "database": {
    "type": "sqlite",
    "path": "megabot.db",
    "research_cache_enabled": true
  },
  "workflow": {
    "max_concurrent_tasks": 10,
    "auto_update_interval": 3600,
    "permission_level": "full"
  },
  "features": {
    "deep_research": true,
    "multi_tasking": true,
    "auto_update": true,
    "document_sync": true
  }
}
```

## Important Notes for Coding Agents

1. **No Real APIs Required**: System works with simulated responses; perfect for development and testing
2. **Async Everywhere**: All public methods on MegaBot and integrations are async; always use `await`
3. **Self-Contained**: No external services needed; SQLite database is file-based
4. **Graceful Degradation**: System continues working even if some integrations are unavailable
5. **Configuration Flexibility**: Supports both JSON config files and environment variables
6. **Comprehensive Tests**: 19 passing tests cover all major components; run them before and after changes
7. **Clear Documentation**: README, ARCHITECTURE, DOCUMENTATION, and PROJECT_SUMMARY files provide detailed info
8. **Examples Directory**: Contains working examples for common use cases; great learning resource

## Quick Reference

### Start a MegaBot Instance
```python
from megabot import MegaBot
import asyncio

async def main():
    bot = MegaBot()
    await bot.start()
    # Use bot
    await bot.stop()

asyncio.run(main())
```

### Run Tests
```bash
pytest tests/ -v
```

### Common File Locations
- Main code: `megabot/`
- Entry point: `main.py`
- Tests: `tests/test_megabot.py`
- Config: `config.json` (or `.env`)
- Database: `megabot.db` (auto-created)
- Examples: `examples/`

### Key Classes to Know
- `MegaBot`: Main orchestrator (megabot/core.py)
- `Config`: Configuration manager (megabot/config.py)
- `BaseIntegration`: Integration interface (megabot/integrations/base.py)
- `ResearchEngine`: Multi-platform research (megabot/database/research_engine.py)
- `DatabaseStorage`: SQLite operations (megabot/database/storage.py)
- `TaskScheduler`: Workflow execution (megabot/workflow/scheduler.py)

## Summary

MEGAGENT is a well-structured, async-first Python project that integrates multiple AI platforms. It emphasizes:
- **Clean architecture** with clear separation of concerns
- **Async patterns** throughout for non-blocking operations
- **Graceful degradation** and error handling
- **Comprehensive testing** with 19 passing tests
- **Flexible configuration** supporting multiple sources
- **Development-friendly** with simulated mode (no API keys needed)

When working on this project, prioritize maintaining these qualities and following the established patterns. The codebase is designed to be extensible, so adding new features should feel natural if you follow the existing structure.
