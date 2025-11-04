"""
Auto-update manager for document synchronization
"""
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from ..integrations.base import AIIntegration
from ..database.storage import DatabaseStorage


class AutoUpdateManager:
    """Manages automatic updates from AI platforms"""
    
    def __init__(
        self,
        integrations: List[AIIntegration],
        storage: DatabaseStorage,
        update_interval: int = 3600
    ):
        """
        Initialize auto-update manager
        
        Args:
            integrations: List of AI platform integrations
            storage: Database storage instance
            update_interval: Update interval in seconds
        """
        self.integrations = integrations
        self.storage = storage
        self.update_interval = update_interval
        self.running = False
        self.last_update: Dict[str, float] = {}
    
    async def start(self):
        """Start auto-update service"""
        self.running = True
        
        # Run update loop
        while self.running:
            await self.update_all()
            await asyncio.sleep(self.update_interval)
    
    async def stop(self):
        """Stop auto-update service"""
        self.running = False
    
    async def update_all(self):
        """Update documents from all platforms"""
        update_tasks = []
        
        for integration in self.integrations:
            if integration.is_available():
                update_tasks.append(self._update_platform(integration))
        
        if update_tasks:
            await asyncio.gather(*update_tasks, return_exceptions=True)
    
    async def _update_platform(self, integration: AIIntegration):
        """Update documents from a specific platform"""
        try:
            updates = await integration.get_latest_updates()
            
            for update in updates:
                # Save to database
                self.storage.save_document_update(integration.platform_name, update)
            
            # Update timestamp
            self.last_update[integration.platform_name] = datetime.now().timestamp()
            
            return {
                "platform": integration.platform_name,
                "updates_count": len(updates),
                "timestamp": self.last_update[integration.platform_name]
            }
            
        except Exception as e:
            return {
                "platform": integration.platform_name,
                "error": str(e)
            }
    
    def get_last_update_time(self, platform: str) -> float:
        """Get timestamp of last update for a platform"""
        return self.last_update.get(platform, 0)
    
    def get_all_updates(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all stored updates"""
        return self.storage.get_latest_updates(limit=limit)
    
    def get_platform_updates(self, platform: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get updates for a specific platform"""
        return self.storage.get_latest_updates(platform=platform, limit=limit)
