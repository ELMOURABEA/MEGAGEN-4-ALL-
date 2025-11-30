"""
MEGA-Bot API module for web and system integrations
"""
from .client import APIClient
from .flask_app import create_app

__all__ = ["create_app", "APIClient"]
