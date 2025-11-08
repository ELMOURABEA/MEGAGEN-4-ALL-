"""
MEGA-Bot - A unified AI agent integrating multiple platforms
"""

__version__ = "1.1.0"
__author__ = "MEGAGENT Team"

from .core import MegaBot
from .config import Config
from .utils import setup_logging, get_logger, validate_query, validate_topic

__all__ = ["MegaBot", "Config", "setup_logging", "get_logger", "validate_query", "validate_topic"]
