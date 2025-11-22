"""
Debug mode utilities for MEGA-Bot development and troubleshooting
"""
import os
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class DebugMode:
    """
    Debug mode manager for MEGA-Bot
    
    Provides enhanced logging, diagnostics, and development utilities
    when DEBUG mode is enabled.
    """
    
    def __init__(self, enabled: Optional[bool] = None):
        """
        Initialize debug mode
        
        Args:
            enabled: Whether debug mode is enabled (defaults to DEBUG env var)
        """
        if enabled is None:
            enabled = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
        
        self.enabled = enabled
        self.debug_dir = Path("debug_logs")
        
        if self.enabled:
            self.debug_dir.mkdir(exist_ok=True)
            self._setup_debug_logging()
    
    def _setup_debug_logging(self):
        """Setup enhanced logging for debug mode"""
        log_file = self.debug_dir / f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Configure root logger for debug
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logging.info(f"Debug mode enabled. Logging to: {log_file}")
    
    def log(self, message: str, level: str = "INFO"):
        """
        Log a debug message
        
        Args:
            message: Message to log
            level: Log level (DEBUG, INFO, WARNING, ERROR)
        """
        if not self.enabled:
            return
        
        logger = logging.getLogger("megabot.debug")
        getattr(logger, level.lower())(message)
    
    def log_api_call(self, platform: str, endpoint: str, payload: Dict[str, Any], response: Any):
        """
        Log API call details for debugging
        
        Args:
            platform: Platform name (e.g., 'copilot', 'gemini')
            endpoint: API endpoint called
            payload: Request payload
            response: API response
        """
        if not self.enabled:
            return
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "endpoint": endpoint,
            "payload": payload,
            "response": str(response)[:500]  # Truncate long responses
        }
        
        log_file = self.debug_dir / f"api_calls_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        self.log(f"API call to {platform}/{endpoint}", "DEBUG")
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """
        Log error details with context
        
        Args:
            error: Exception that occurred
            context: Additional context about the error
        """
        if not self.enabled:
            return
        
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        }
        
        log_file = self.debug_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(error_entry) + "\n")
        
        logging.error(f"Error: {error}", exc_info=True)
    
    def dump_state(self, state: Dict[str, Any], name: str = "state"):
        """
        Dump current state to file for inspection
        
        Args:
            state: State dictionary to dump
            name: Name for the state dump file
        """
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        state_file = self.debug_dir / f"{name}_{timestamp}.json"
        
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2, default=str)
        
        self.log(f"State dumped to: {state_file}", "DEBUG")
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """
        Get system diagnostics information
        
        Returns:
            Dictionary with diagnostic information
        """
        return {
            "debug_enabled": self.enabled,
            "debug_dir": str(self.debug_dir),
            "python_version": os.sys.version,
            "platform": os.sys.platform,
            "environment": {
                k: v for k, v in os.environ.items()
                if k.startswith("MEGABOT_") or k.startswith("DEBUG")
            }
        }
    
    def measure_performance(self, operation: str, duration: float):
        """
        Log performance metrics
        
        Args:
            operation: Name of operation measured
            duration: Duration in seconds
        """
        if not self.enabled:
            return
        
        perf_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_seconds": duration
        }
        
        log_file = self.debug_dir / f"performance_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(perf_entry) + "\n")
        
        self.log(f"Performance: {operation} took {duration:.3f}s", "DEBUG")
    
    def clear_logs(self, older_than_days: int = 7):
        """
        Clear old debug logs
        
        Args:
            older_than_days: Delete logs older than this many days
        """
        if not self.enabled or not self.debug_dir.exists():
            return
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        
        for log_file in self.debug_dir.glob("*"):
            if log_file.is_file():
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_time < cutoff_date:
                    log_file.unlink()
                    self.log(f"Deleted old log: {log_file}", "INFO")


# Global debug instance
_debug_instance = None


def get_debug() -> DebugMode:
    """Get or create global debug instance"""
    global _debug_instance
    if _debug_instance is None:
        _debug_instance = DebugMode()
    return _debug_instance


def is_debug_enabled() -> bool:
    """Check if debug mode is enabled"""
    return get_debug().enabled
