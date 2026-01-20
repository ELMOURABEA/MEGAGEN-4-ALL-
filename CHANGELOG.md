# Changelog

All notable changes to MEGA-Bot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-08

### Added
- **Monetization System**: Complete subscription tier management
  - Free tier: 10 queries/day, 5 research/day, shallow research only
  - Pro tier: Unlimited queries and research, all depths
  - Full Energy tier: Pro + 20 concurrent tasks + priority support
- **Advertising Core**: Google AdMob integration
  - Banner ads with configurable placement
  - Interstitial ads
  - Rewarded ads for bonus features
  - Partnership and sponsorship management
  - Ad rental slots
- AdMob integration configured via environment variables for security
- Usage tracking with daily reset
- Tier-based feature restrictions
- 11 new tests for monetization and advertising (total: 39 tests)
- `get_subscription_tiers()` - View all available tiers
- `get_tier_info()` - View current tier and usage
- `show_banner_ad()` - Display banner advertisements
- `show_rewarded_ad()` - Display rewarded ads with bonuses

### Changed
- Version bumped from 1.1.0 to 1.2.0
- Core module now checks monetization limits before queries and research
- TaskScheduler now uses tier-based concurrent task limits
- Configuration expanded with monetization and advertising sections
- Status endpoint now includes monetization and advertising info

### Security
- All monetization features follow existing validation patterns
- **AdMob IDs moved to environment variables**: Hardcoded AdMob IDs removed from source code and now loaded securely from environment variables (ADMOB_APP_ID, ADMOB_BANNER_ID, ADMOB_INTERSTITIAL_ID, ADMOB_REWARDED_ID)
- Ad IDs properly configured and validated

## [1.1.0] - 2025-11-08

### Added
- Comprehensive logging system for better debugging and monitoring
- Input validation utilities for secure query handling
- Enhanced error handling across all modules with try-catch blocks
- Changelog file to track project evolution
- Version display in CLI interface (demo and interactive modes)
- Utility module (`megabot/utils.py`) with common functions
- CONTRIBUTING.md with contribution guidelines
- `.gitattributes` for consistent line endings
- New validation example (`examples/validation_example.py`)
- Version command in interactive mode
- 9 new tests for utility functions (total: 28 tests)

### Changed
- Improved demo output formatting with version display
- Enhanced error messages with more context
- Updated documentation with logging and validation information
- Updated README with security features and test coverage
- Updated examples README with new validation example
- Core module now uses validation and logging throughout

### Security
- Added input sanitization to prevent injection attacks
- Implemented query length limits (10,000 chars) for safety
- Added validation for topic and prompt parameters
- Detection and blocking of dangerous patterns (scripts, JavaScript)
- Automatic HTML tag removal from inputs
- Comprehensive validation before any API processing

## [1.0.0] - 2024

### Added
- Initial release of MEGA-Bot
- Multi-platform AI integration (Copilot, Gemini, ChatGPT, Grok)
- Deep research engine with caching
- Database storage with SQLite
- Workflow system with task scheduler
- Permission management system
- Auto-update manager
- Comprehensive test suite (19 tests)
- Documentation and examples
- Interactive CLI mode
