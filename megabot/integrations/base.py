"""
Base class for AI platform integrations
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class AIIntegration(ABC):
    """Base class for AI platform integrations"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        """
        Initialize AI integration
        
        Args:
            api_key: API key for the platform
            config: Configuration dictionary
        """
        self.api_key = api_key
        self.config = config
        self.name = self.__class__.__name__
        self.enabled = bool(api_key)
    
    @abstractmethod
    async def query(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query the AI platform
        
        Args:
            prompt: The query/prompt to send
            context: Optional context information
            
        Returns:
            Dict containing response and metadata
        """
        pass
    
    @abstractmethod
    async def research(self, topic: str, depth: str = "medium") -> Dict[str, Any]:
        """
        Perform deep research on a topic
        
        Args:
            topic: Topic to research
            depth: Research depth (shallow, medium, deep)
            
        Returns:
            Dict containing research results
        """
        pass
    
    async def get_latest_updates(self) -> List[Dict[str, Any]]:
        """
        Get latest updates and documentation from the platform
        
        Returns:
            List of updates
        """
        return []
    
    def is_available(self) -> bool:
        """Check if the integration is available and configured"""
        return self.enabled and bool(self.api_key)
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities supported by this integration"""
        return ["query", "research"]
