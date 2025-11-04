"""
Deep research engine for database queries and analysis
"""
import asyncio
from typing import Dict, Any, List, Optional
from ..integrations.base import AIIntegration
from .storage import DatabaseStorage


class ResearchEngine:
    """Deep research engine for comprehensive database analysis"""
    
    def __init__(self, integrations: List[AIIntegration], storage: DatabaseStorage):
        """
        Initialize research engine
        
        Args:
            integrations: List of AI platform integrations
            storage: Database storage instance
        """
        self.integrations = integrations
        self.storage = storage
        self.active_integrations = [i for i in integrations if i.is_available()]
    
    async def deep_research(self, topic: str, depth: str = "deep", use_cache: bool = True) -> Dict[str, Any]:
        """
        Perform deep research across all platforms
        
        Args:
            topic: Topic to research
            depth: Research depth (shallow, medium, deep)
            use_cache: Whether to use cached results
            
        Returns:
            Dict containing aggregated research from all platforms
        """
        results = {
            "topic": topic,
            "depth": depth,
            "platforms_used": [],
            "findings": {},
            "aggregated_sources": [],
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Collect research from all available platforms
        tasks = []
        for integration in self.active_integrations:
            # Check cache first if enabled
            if use_cache:
                cached = self.storage.get_cached_research(topic, integration.platform_name, depth)
                if cached:
                    results["platforms_used"].append(integration.platform_name)
                    results["findings"][integration.platform_name] = cached
                    continue
            
            # Perform fresh research
            tasks.append(self._research_with_platform(integration, topic, depth))
        
        # Execute all research tasks concurrently
        if tasks:
            platform_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in platform_results:
                if isinstance(result, Exception):
                    continue
                if result and "platform" in result:
                    platform_name = result["platform"]
                    results["platforms_used"].append(platform_name)
                    results["findings"][platform_name] = result
                    
                    # Cache the results
                    self.storage.cache_research(topic, platform_name, depth, result)
                    
                    # Collect unique sources
                    if "sources" in result:
                        for source in result["sources"]:
                            if source not in results["aggregated_sources"]:
                                results["aggregated_sources"].append(source)
        
        # Generate synthesis
        results["synthesis"] = self._synthesize_findings(results["findings"])
        
        return results
    
    async def _research_with_platform(self, integration: AIIntegration, topic: str, depth: str) -> Dict[str, Any]:
        """Perform research with a specific platform"""
        try:
            result = await integration.research(topic, depth)
            return result
        except Exception as e:
            return {"error": str(e), "platform": integration.platform_name}
    
    def _synthesize_findings(self, findings: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize findings from multiple platforms"""
        if not findings:
            return {"summary": "No findings available"}
        
        synthesis = {
            "summary": f"Research completed across {len(findings)} platforms",
            "key_insights": [],
            "common_themes": [],
            "unique_perspectives": {}
        }
        
        # Extract key insights from each platform
        for platform, data in findings.items():
            if "findings" in data and data["findings"]:
                # Add first finding as key insight
                if data["findings"]:
                    synthesis["key_insights"].append({
                        "platform": platform,
                        "insight": data["findings"][0]
                    })
                
                # Track unique perspectives
                synthesis["unique_perspectives"][platform] = len(data["findings"])
        
        # Identify common themes (simplified)
        all_findings = []
        for data in findings.values():
            if "findings" in data:
                all_findings.extend(data["findings"])
        
        if all_findings:
            synthesis["total_findings"] = len(all_findings)
            synthesis["common_themes"] = ["Comprehensive coverage", "Multi-perspective analysis", "Deep insights"]
        
        return synthesis
    
    async def query_all_platforms(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query all available platforms simultaneously
        
        Args:
            prompt: Query prompt
            context: Optional context
            
        Returns:
            Dict containing responses from all platforms
        """
        results = {
            "prompt": prompt,
            "responses": {},
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Query all platforms concurrently
        tasks = []
        for integration in self.active_integrations:
            tasks.append(self._query_platform(integration, prompt, context))
        
        if tasks:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            for response in responses:
                if isinstance(response, Exception):
                    continue
                if response and "platform" in response:
                    platform_name = response["platform"]
                    results["responses"][platform_name] = response
                    
                    # Save to query history
                    self.storage.save_query(
                        prompt,
                        platform_name,
                        str(response.get("response", ""))
                    )
        
        return results
    
    async def _query_platform(self, integration: AIIntegration, prompt: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Query a specific platform"""
        try:
            result = await integration.query(prompt, context)
            return result
        except Exception as e:
            return {"error": str(e), "platform": integration.platform_name}
    
    def get_research_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get research history from database"""
        return self.storage.get_query_history(limit)
