"""
Monetization and subscription management for MEGA-Bot
"""
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class SubscriptionTier(Enum):
    """Subscription tier levels"""
    FREE = "free"
    PRO = "pro"
    FULL_ENERGY = "full_energy"


class MonetizationManager:
    """
    Manages subscription tiers and feature access
    
    Tiers:
    - FREE: Limited features (10 queries/day, shallow research only)
    - PRO: Full features (unlimited queries, all research depths)
    - FULL_ENERGY: Pro + priority support + early access to new features
    """
    
    # Feature limits per tier
    TIER_LIMITS = {
        SubscriptionTier.FREE: {
            "max_queries_per_day": 10,
            "max_research_per_day": 5,
            "allowed_research_depths": ["shallow"],
            "concurrent_tasks": 2,
            "cache_enabled": True,
            "auto_update": False,
            "priority_support": False,
            "early_access": False
        },
        SubscriptionTier.PRO: {
            "max_queries_per_day": -1,  # unlimited
            "max_research_per_day": -1,  # unlimited
            "allowed_research_depths": ["shallow", "medium", "deep"],
            "concurrent_tasks": 10,
            "cache_enabled": True,
            "auto_update": True,
            "priority_support": False,
            "early_access": False
        },
        SubscriptionTier.FULL_ENERGY: {
            "max_queries_per_day": -1,  # unlimited
            "max_research_per_day": -1,  # unlimited
            "allowed_research_depths": ["shallow", "medium", "deep"],
            "concurrent_tasks": 20,
            "cache_enabled": True,
            "auto_update": True,
            "priority_support": True,
            "early_access": True
        }
    }
    
    def __init__(self, tier: str = "free"):
        """
        Initialize monetization manager
        
        Args:
            tier: Subscription tier (free, pro, full_energy)
        """
        try:
            self.tier = SubscriptionTier(tier.lower())
        except ValueError:
            self.tier = SubscriptionTier.FREE
        
        self.limits = self.TIER_LIMITS[self.tier]
        
        # Usage tracking
        self._reset_date = datetime.now().date()
        self._query_count = 0
        self._research_count = 0
    
    def _check_reset(self):
        """Reset daily counters if needed"""
        current_date = datetime.now().date()
        if current_date > self._reset_date:
            self._reset_date = current_date
            self._query_count = 0
            self._research_count = 0
    
    def can_query(self) -> tuple[bool, Optional[str]]:
        """
        Check if user can make a query
        
        Returns:
            Tuple of (allowed, reason_if_not_allowed)
        """
        self._check_reset()
        
        max_queries = self.limits["max_queries_per_day"]
        if max_queries == -1:  # unlimited
            return True, None
        
        if self._query_count >= max_queries:
            return False, f"Daily query limit reached ({max_queries}). Upgrade to Pro for unlimited queries."
        
        return True, None
    
    def can_research(self, depth: str = "shallow") -> tuple[bool, Optional[str]]:
        """
        Check if user can perform research at specified depth
        
        Args:
            depth: Research depth (shallow, medium, deep)
            
        Returns:
            Tuple of (allowed, reason_if_not_allowed)
        """
        self._check_reset()
        
        # Check depth permission
        allowed_depths = self.limits["allowed_research_depths"]
        if depth not in allowed_depths:
            return False, f"Research depth '{depth}' not available in {self.tier.value} tier. Upgrade to Pro for all research depths."
        
        # Check daily limit
        max_research = self.limits["max_research_per_day"]
        if max_research == -1:  # unlimited
            return True, None
        
        if self._research_count >= max_research:
            return False, f"Daily research limit reached ({max_research}). Upgrade to Pro for unlimited research."
        
        return True, None
    
    def record_query(self):
        """Record a query usage"""
        self._check_reset()
        self._query_count += 1
    
    def record_research(self):
        """Record a research usage"""
        self._check_reset()
        self._research_count += 1
    
    def get_tier_info(self) -> Dict[str, Any]:
        """Get current tier information"""
        self._check_reset()
        
        return {
            "tier": self.tier.value,
            "limits": self.limits,
            "usage": {
                "queries_today": self._query_count,
                "research_today": self._research_count,
                "reset_date": self._reset_date.isoformat()
            }
        }
    
    def get_max_concurrent_tasks(self) -> int:
        """Get maximum concurrent tasks for this tier"""
        return self.limits["concurrent_tasks"]
    
    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a feature is enabled for this tier
        
        Args:
            feature: Feature name (e.g., 'auto_update', 'priority_support')
        
        Returns:
            True if feature is enabled
        """
        return self.limits.get(feature, False)
    
    @staticmethod
    def get_all_tiers() -> Dict[str, Dict[str, Any]]:
        """Get information about all subscription tiers"""
        return {
            "free": {
                "name": "Free",
                "price": "$0/month",
                "features": [
                    "10 queries per day",
                    "5 research operations per day",
                    "Shallow research only",
                    "2 concurrent tasks",
                    "Basic caching"
                ]
            },
            "pro": {
                "name": "Pro",
                "price": "$9.99/month",
                "features": [
                    "Unlimited queries",
                    "Unlimited research",
                    "All research depths (shallow, medium, deep)",
                    "10 concurrent tasks",
                    "Advanced caching",
                    "Auto-updates"
                ]
            },
            "full_energy": {
                "name": "Full Energy",
                "price": "$29.99/month",
                "features": [
                    "Everything in Pro",
                    "20 concurrent tasks",
                    "Priority support",
                    "Early access to new features",
                    "Premium integrations"
                ]
            }
        }
