"""
Configuration management for MEGA-Bot
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Manages configuration for MEGA-Bot"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to configuration file (JSON)
        """
        self.config_path = config_path or os.getenv("MEGABOT_CONFIG", "config.json")
        self.config: Dict[str, Any] = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        default_config = {
            "api_keys": {
                "copilot": os.getenv("COPILOT_API_KEY", ""),
                "gemini": os.getenv("GEMINI_API_KEY", ""),
                "chatgpt": os.getenv("CHATGPT_API_KEY", ""),
                "grok": os.getenv("GROK_API_KEY", "")
            },
            "database": {
                "type": "sqlite",
                "path": "megabot.db",
                "research_cache_enabled": True
            },
            "workflow": {
                "max_concurrent_tasks": 10,
                "auto_update_interval": 3600,
                "permission_level": "full"
            },
            "features": {
                "deep_research": True,
                "multi_tasking": True,
                "auto_update": True,
                "document_sync": True
            },
            "monetization": {
                "enabled": True,
                "tier": os.getenv("MEGABOT_TIER", "free"),
                "advertising_enabled": True
            },
            "advertising": {
                "app_id": os.getenv("ADMOB_APP_ID", ""),
                "banner_id": os.getenv("ADMOB_BANNER_ID", ""),
                "interstitial_id": os.getenv("ADMOB_INTERSTITIAL_ID", ""),
                "rewarded_id": os.getenv("ADMOB_REWARDED_ID", "")
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
        
        return default_config
    
    def save(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
