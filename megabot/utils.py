"""
Utility functions for MEGA-Bot
"""
import re
import logging
from typing import Optional


# Configure logging
def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Configure logging for MEGA-Bot
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("megabot")
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper()))
        
        # Console handler with formatting
        handler = logging.StreamHandler()
        handler.setLevel(getattr(logging, level.upper()))
        
        # Detailed format with timestamp
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Optional name for the logger (will be appended to 'megabot')
    
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"megabot.{name}")
    return logging.getLogger("megabot")


def validate_query(query: str, max_length: int = 10000) -> tuple[bool, Optional[str]]:
    """
    Validate user query for safety and correctness
    
    Args:
        query: The query string to validate
        max_length: Maximum allowed length for queries
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not query:
        return False, "Query cannot be empty"
    
    if not isinstance(query, str):
        return False, "Query must be a string"
    
    query = query.strip()
    
    if len(query) == 0:
        return False, "Query cannot be empty or whitespace only"
    
    if len(query) > max_length:
        return False, f"Query exceeds maximum length of {max_length} characters"
    
    # Check for potentially malicious patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',                 # JavaScript protocol
        r'on\w+\s*=',                   # Event handlers
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return False, "Query contains potentially unsafe content"
    
    return True, None


def validate_topic(topic: str, max_length: int = 500) -> tuple[bool, Optional[str]]:
    """
    Validate research topic
    
    Args:
        topic: The topic string to validate
        max_length: Maximum allowed length for topics
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not topic:
        return False, "Topic cannot be empty"
    
    if not isinstance(topic, str):
        return False, "Topic must be a string"
    
    topic = topic.strip()
    
    if len(topic) == 0:
        return False, "Topic cannot be empty or whitespace only"
    
    if len(topic) > max_length:
        return False, f"Topic exceeds maximum length of {max_length} characters"
    
    return True, None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially dangerous content
    
    Args:
        text: Input text to sanitize
    
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def format_error(error: Exception) -> str:
    """
    Format exception for user-friendly display
    
    Args:
        error: Exception to format
    
    Returns:
        Formatted error message
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    return f"{error_type}: {error_msg}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
