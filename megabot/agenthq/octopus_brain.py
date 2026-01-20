"""
🐙 Octopus Brain - Central Intelligence Hub for Agent HQ
The brain coordinates all tentacles (agents) for unified decision-making
"""
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class TentacleStatus(Enum):
    """Status of each tentacle (agent)"""
    ACTIVE = "active"
    READY = "ready"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    DISCONNECTED = "disconnected"


class OctopusBrain:
    """
    🧠 The central brain of the Octopus Agent System
    
    Coordinates all tentacles (agents) with intelligent decision-making,
    load balancing, and task distribution.
    """
    
    def __init__(self, logger=None):
        """
        Initialize the Octopus Brain
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger
        self.tentacles: Dict[str, Dict[str, Any]] = {}
        self.task_queue: List[Dict[str, Any]] = []
        self.memory: Dict[str, Any] = {
            "short_term": {},  # Recent operations
            "long_term": {},   # Persistent knowledge
            "working": {}      # Current task context
        }
        self.decision_history: List[Dict[str, Any]] = []
        
        if self.logger:
            self.logger.info("🧠 Octopus Brain initialized")
    
    def register_tentacle(self, name: str, capabilities: List[str],
                         provider: str, specialty: str) -> None:
        """
        Register a new tentacle (agent) with the brain
        
        Args:
            name: Tentacle name
            capabilities: List of capabilities
            provider: Provider/company
            specialty: Main specialty area
        """
        self.tentacles[name] = {
            "name": name,
            "capabilities": capabilities,
            "provider": provider,
            "specialty": specialty,
            "status": TentacleStatus.READY,
            "tasks_completed": 0,
            "success_rate": 1.0,
            "average_response_time": 0.0,
            "current_load": 0,
            "registered_at": datetime.now()
        }
        
        if self.logger:
            self.logger.info(f"🦾 Registered tentacle: {name} ({provider})")
    
    def think(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Central thinking process - analyze and make decisions
        
        Args:
            context: Current context and information
            
        Returns:
            Decision result with reasoning
        """
        thought_process = {
            "timestamp": datetime.now().isoformat(),
            "context_analyzed": True,
            "available_tentacles": len([t for t in self.tentacles.values() 
                                       if t["status"] in [TentacleStatus.READY, TentacleStatus.IDLE]]),
            "decision": None,
            "reasoning": [],
            "confidence": 0.0
        }
        
        # Analyze task complexity
        task = context.get("task", "")
        complexity = self._assess_complexity(task)
        thought_process["reasoning"].append(f"Task complexity: {complexity}")
        
        # Select best tentacles for task
        best_tentacles = self._select_tentacles(context)
        thought_process["decision"] = {
            "selected_tentacles": best_tentacles,
            "strategy": "parallel" if len(best_tentacles) > 1 else "single",
            "estimated_time": self._estimate_time(best_tentacles)
        }
        
        # Calculate confidence
        if best_tentacles:
            avg_success = sum(self.tentacles[t]["success_rate"] 
                            for t in best_tentacles) / len(best_tentacles)
            thought_process["confidence"] = avg_success
        
        # Store in decision history
        self.decision_history.append(thought_process)
        
        if self.logger:
            self.logger.debug(f"🧠 Thought process: {len(best_tentacles)} tentacles selected")
        
        return thought_process
    
    def _assess_complexity(self, task: str) -> str:
        """Assess task complexity"""
        if len(task) < 50:
            return "simple"
        elif len(task) < 200:
            return "medium"
        else:
            return "complex"
    
    def _select_tentacles(self, context: Dict[str, Any]) -> List[str]:
        """
        Intelligently select the best tentacles for a task
        
        Args:
            context: Task context
            
        Returns:
            List of selected tentacle names
        """
        task = context.get("task", "").lower()
        required_capabilities = context.get("capabilities", [])
        max_tentacles = context.get("max_tentacles", 3)
        
        # Score each tentacle
        scores = {}
        for name, tentacle in self.tentacles.items():
            if tentacle["status"] not in [TentacleStatus.READY, TentacleStatus.IDLE]:
                continue
            
            score = 0.0
            
            # Capability match
            if required_capabilities:
                matching_caps = len(set(tentacle["capabilities"]) & set(required_capabilities))
                score += matching_caps * 10
            
            # Specialty relevance
            if tentacle["specialty"].lower() in task:
                score += 20
            
            # Success rate
            score += tentacle["success_rate"] * 15
            
            # Current load (lower is better)
            score -= tentacle["current_load"] * 5
            
            # Provider diversity bonus (don't over-rely on one provider)
            provider_count = sum(1 for t in scores.values() 
                               if self.tentacles[list(scores.keys())[0]]["provider"] == tentacle["provider"])
            if provider_count == 0:
                score += 5
            
            scores[name] = score
        
        # Select top tentacles
        sorted_tentacles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected = [name for name, score in sorted_tentacles[:max_tentacles] if score > 0]
        
        return selected
    
    def _estimate_time(self, tentacles: List[str]) -> float:
        """Estimate completion time"""
        if not tentacles:
            return 0.0
        
        avg_time = sum(self.tentacles[t]["average_response_time"] 
                      for t in tentacles) / len(tentacles)
        return max(avg_time, 1.0)  # Minimum 1 second
    
    async def coordinate(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Coordinate execution of a task across tentacles
        
        Args:
            task: Task description
            context: Additional context
            
        Returns:
            Coordination results
        """
        if context is None:
            context = {}
        context["task"] = task
        
        # Think about the task
        decision = self.think(context)
        
        # Update working memory
        self.memory["working"]["current_task"] = task
        self.memory["working"]["decision"] = decision
        
        # Prepare results
        results = {
            "task": task,
            "decision": decision,
            "tentacle_results": [],
            "success": True,
            "coordination_time": 0.0
        }
        
        start_time = datetime.now()
        selected_tentacles = decision["decision"]["selected_tentacles"]
        
        if not selected_tentacles:
            results["success"] = False
            results["error"] = "No suitable tentacles available"
            return results
        
        # Mark tentacles as busy
        for tentacle_name in selected_tentacles:
            self.tentacles[tentacle_name]["status"] = TentacleStatus.BUSY
            self.tentacles[tentacle_name]["current_load"] += 1
        
        # Execute (simulated for now - will be replaced with actual execution)
        for tentacle_name in selected_tentacles:
            tentacle_result = {
                "tentacle": tentacle_name,
                "status": "completed",
                "output": f"Processed by {tentacle_name}: {task[:50]}..."
            }
            results["tentacle_results"].append(tentacle_result)
            
            # Update tentacle stats
            self.tentacles[tentacle_name]["tasks_completed"] += 1
            self.tentacles[tentacle_name]["status"] = TentacleStatus.IDLE
            self.tentacles[tentacle_name]["current_load"] -= 1
        
        results["coordination_time"] = (datetime.now() - start_time).total_seconds()
        
        # Update short-term memory
        self.memory["short_term"][datetime.now().isoformat()] = {
            "task": task,
            "tentacles_used": selected_tentacles,
            "success": results["success"]
        }
        
        if self.logger:
            self.logger.info(f"🧠 Coordinated task across {len(selected_tentacles)} tentacles")
        
        return results
    
    def learn(self, task: str, result: Dict[str, Any]) -> None:
        """
        Learn from task execution results
        
        Args:
            task: Completed task
            result: Execution result
        """
        # Update tentacle success rates
        for tentacle_result in result.get("tentacle_results", []):
            tentacle_name = tentacle_result["tentacle"]
            if tentacle_name in self.tentacles:
                tentacle = self.tentacles[tentacle_name]
                
                # Update success rate (moving average)
                success = tentacle_result["status"] == "completed"
                current_rate = tentacle["success_rate"]
                tentacle["success_rate"] = (current_rate * 0.9) + (1.0 if success else 0.0) * 0.1
        
        # Store learning in long-term memory
        task_type = self._categorize_task(task)
        if task_type not in self.memory["long_term"]:
            self.memory["long_term"][task_type] = []
        
        self.memory["long_term"][task_type].append({
            "task": task,
            "success": result.get("success", False),
            "tentacles_used": [r["tentacle"] for r in result.get("tentacle_results", [])],
            "timestamp": datetime.now().isoformat()
        })
        
        if self.logger:
            self.logger.debug(f"🧠 Learned from task execution")
    
    def _categorize_task(self, task: str) -> str:
        """Categorize task for learning"""
        task_lower = task.lower()
        if any(word in task_lower for word in ["code", "function", "program", "script"]):
            return "coding"
        elif any(word in task_lower for word in ["analyze", "explain", "understand"]):
            return "analysis"
        elif any(word in task_lower for word in ["write", "create", "generate", "compose"]):
            return "generation"
        elif any(word in task_lower for word in ["search", "find", "lookup", "research"]):
            return "research"
        else:
            return "general"
    
    def get_brain_status(self) -> Dict[str, Any]:
        """
        Get current brain status
        
        Returns:
            Status information
        """
        return {
            "tentacles": {
                "total": len(self.tentacles),
                "active": len([t for t in self.tentacles.values() 
                             if t["status"] == TentacleStatus.ACTIVE]),
                "ready": len([t for t in self.tentacles.values() 
                            if t["status"] == TentacleStatus.READY]),
                "busy": len([t for t in self.tentacles.values() 
                           if t["status"] == TentacleStatus.BUSY]),
                "idle": len([t for t in self.tentacles.values() 
                           if t["status"] == TentacleStatus.IDLE])
            },
            "memory": {
                "short_term_items": len(self.memory["short_term"]),
                "long_term_categories": len(self.memory["long_term"]),
                "working_context": bool(self.memory["working"])
            },
            "decision_history": len(self.decision_history),
            "total_tasks_processed": sum(t["tasks_completed"] for t in self.tentacles.values())
        }
    
    def get_tentacle_status(self, name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific tentacle"""
        tentacle = self.tentacles.get(name)
        if not tentacle:
            return None
        
        return {
            "name": tentacle["name"],
            "provider": tentacle["provider"],
            "specialty": tentacle["specialty"],
            "status": tentacle["status"].value,
            "capabilities": tentacle["capabilities"],
            "performance": {
                "tasks_completed": tentacle["tasks_completed"],
                "success_rate": f"{tentacle['success_rate']:.2%}",
                "current_load": tentacle["current_load"]
            }
        }
    
    def get_all_tentacles(self) -> List[Dict[str, Any]]:
        """Get status of all tentacles"""
        return [self.get_tentacle_status(name) for name in self.tentacles.keys()]
    
    def recall_memory(self, memory_type: str = "short_term", 
                     limit: int = 10) -> List[Dict[str, Any]]:
        """
        Recall memories from brain
        
        Args:
            memory_type: Type of memory (short_term, long_term, working)
            limit: Maximum number of memories to return
            
        Returns:
            List of memories
        """
        if memory_type == "short_term":
            items = list(self.memory["short_term"].items())[-limit:]
            return [{"timestamp": k, **v} for k, v in items]
        elif memory_type == "long_term":
            all_memories = []
            for category, memories in self.memory["long_term"].items():
                for memory in memories[-limit:]:
                    memory["category"] = category
                    all_memories.append(memory)
            return all_memories[-limit:]
        elif memory_type == "working":
            return [self.memory["working"]] if self.memory["working"] else []
        else:
            return []
