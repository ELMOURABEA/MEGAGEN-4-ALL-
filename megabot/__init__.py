"""
MEGA-Bot - A unified AI agent integrating multiple platforms
"""

__version__ = "1.2.0"
__author__ = "MEGAGENT Team"

from .core import MegaBot
from .config import Config
from .utils import setup_logging, get_logger, validate_query, validate_topic
from .monetization import MonetizationManager, SubscriptionTier
from .advertising import AdvertisingCore, AdPlacement

__all__ = [
    "MegaBot", "Config", 
    "setup_logging", "get_logger", "validate_query", "validate_topic",
    "MonetizationManager", "SubscriptionTier",
    "AdvertisingCore", "AdPlacement"
]
