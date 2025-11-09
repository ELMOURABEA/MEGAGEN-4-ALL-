"""
LangChain Integration for Agent HQ
Provides chains, prompts, and tools for building AI workflows
"""
import asyncio
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass


@dataclass
class ChainStep:
    """Represents a step in a LangChain workflow"""
    name: str
    prompt_template: str
    process_func: Optional[Callable] = None
    inputs: List[str] = None
    
    def __post_init__(self):
        if self.inputs is None:
            self.inputs = []


class LangChainOrchestrator:
    """
    LangChain orchestrator for building AI application sequences
    
    Features:
    - Chain building: Create sequences of AI operations
    - Prompt templates: Reusable prompt structures
    - Tool integration: Connect external tools and APIs
    - Memory management: Maintain context across chains
    """
    
    def __init__(self, integrations: List, logger=None):
        """
        Initialize LangChain orchestrator
        
        Args:
            integrations: List of AI platform integrations
            logger: Optional logger instance
        """
        self.integrations = integrations
        self.logger = logger
        self.chains: Dict[str, List[ChainStep]] = {}
        self.prompt_templates: Dict[str, str] = {}
        self.tools: Dict[str, Callable] = {}
        self.memory: Dict[str, Any] = {}
        
    def create_prompt_template(self, name: str, template: str) -> None:
        """
        Create a reusable prompt template
        
        Args:
            name: Template name
            template: Template string with placeholders like {variable}
        """
        self.prompt_templates[name] = template
        if self.logger:
            self.logger.debug(f"Created prompt template: {name}")
    
    def format_prompt(self, template_name: str, **kwargs) -> str:
        """
        Format a prompt template with provided variables
        
        Args:
            template_name: Name of the template
            **kwargs: Variables to fill in the template
            
        Returns:
            Formatted prompt string
        """
        if template_name not in self.prompt_templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.prompt_templates[template_name]
        return template.format(**kwargs)
    
    def create_chain(self, name: str, steps: List[ChainStep]) -> None:
        """
        Create a chain of operations
        
        Args:
            name: Chain name
            steps: List of ChainStep objects defining the workflow
        """
        self.chains[name] = steps
        if self.logger:
            self.logger.info(f"Created chain '{name}' with {len(steps)} steps")
    
    def register_tool(self, name: str, func: Callable) -> None:
        """
        Register a tool for use in chains
        
        Args:
            name: Tool name
            func: Function to execute when tool is called
        """
        self.tools[name] = func
        if self.logger:
            self.logger.debug(f"Registered tool: {name}")
    
    async def execute_chain(self, chain_name: str, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a chain with the given initial input
        
        Args:
            chain_name: Name of the chain to execute
            initial_input: Initial input data for the chain
            
        Returns:
            Dict containing results from all chain steps
        """
        if chain_name not in self.chains:
            raise ValueError(f"Chain '{chain_name}' not found")
        
        chain = self.chains[chain_name]
        results = {"steps": []}
        context = initial_input.copy()
        
        if self.logger:
            self.logger.info(f"Executing chain '{chain_name}' with {len(chain)} steps")
        
        for i, step in enumerate(chain):
            if self.logger:
                self.logger.debug(f"Executing step {i+1}/{len(chain)}: {step.name}")
            
            # Format prompt with current context
            prompt = step.prompt_template.format(**context)
            
            # Query available integrations
            step_result = await self._query_integrations(prompt)
            
            # Apply custom processing if provided
            if step.process_func:
                step_result = step.process_func(step_result, context)
            
            # Update context with step results
            context[step.name] = step_result
            
            results["steps"].append({
                "step_name": step.name,
                "prompt": prompt,
                "result": step_result
            })
        
        results["final_output"] = context
        return results
    
    async def _query_integrations(self, prompt: str) -> str:
        """
        Query available integrations with a prompt
        
        Args:
            prompt: Prompt to send to integrations
            
        Returns:
            Response from the first available integration
        """
        for integration in self.integrations:
            if integration.is_available():
                try:
                    result = await integration.query(prompt)
                    return result.get("response", "")
                except Exception as e:
                    if self.logger:
                        self.logger.warning(f"Integration {integration.name} failed: {e}")
                    continue
        
        # Fallback to simulated response
        return f"Simulated response for: {prompt[:50]}..."
    
    def set_memory(self, key: str, value: Any) -> None:
        """
        Store data in memory for cross-chain context
        
        Args:
            key: Memory key
            value: Value to store
        """
        self.memory[key] = value
        if self.logger:
            self.logger.debug(f"Stored in memory: {key}")
    
    def get_memory(self, key: str, default: Any = None) -> Any:
        """
        Retrieve data from memory
        
        Args:
            key: Memory key
            default: Default value if key not found
            
        Returns:
            Stored value or default
        """
        return self.memory.get(key, default)
    
    def clear_memory(self) -> None:
        """Clear all memory"""
        self.memory.clear()
        if self.logger:
            self.logger.debug("Memory cleared")
    
    async def create_simple_chain(self, steps: List[str], initial_text: str) -> Dict[str, Any]:
        """
        Create and execute a simple chain from a list of prompts
        
        Args:
            steps: List of prompt templates
            initial_text: Initial text to process
            
        Returns:
            Results from chain execution
        """
        chain_steps = []
        context_text = initial_text
        
        for i, step_prompt in enumerate(steps):
            step = ChainStep(
                name=f"step_{i+1}",
                prompt_template=step_prompt + " {text}",
                inputs=["text"]
            )
            chain_steps.append(step)
        
        chain_name = f"simple_chain_{id(steps)}"
        self.create_chain(chain_name, chain_steps)
        
        return await self.execute_chain(chain_name, {"text": initial_text})
    
    def get_capabilities(self) -> List[str]:
        """
        Get list of LangChain orchestrator capabilities
        
        Returns:
            List of capability names
        """
        return [
            "chain_building",
            "prompt_templates",
            "tool_integration",
            "memory_management",
            "multi_step_workflows"
        ]
    
    def get_chain_info(self, chain_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific chain
        
        Args:
            chain_name: Name of the chain
            
        Returns:
            Dict with chain information or None if not found
        """
        if chain_name not in self.chains:
            return None
        
        chain = self.chains[chain_name]
        return {
            "name": chain_name,
            "steps": len(chain),
            "step_names": [step.name for step in chain]
        }
    
    def list_chains(self) -> List[str]:
        """
        List all available chains
        
        Returns:
            List of chain names
        """
        return list(self.chains.keys())
    
    def list_templates(self) -> List[str]:
        """
        List all available prompt templates
        
        Returns:
            List of template names
        """
        return list(self.prompt_templates.keys())
    
    def list_tools(self) -> List[str]:
        """
        List all registered tools
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
