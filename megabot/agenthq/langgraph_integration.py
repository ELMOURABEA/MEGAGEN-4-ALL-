"""
LangGraph Integration for Agent HQ
Adds memory, branching, and feedback loops for intelligent AI workflows
"""
import asyncio
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    """Types of nodes in the graph"""
    START = "start"
    PROCESS = "process"
    DECISION = "decision"
    END = "end"
    FEEDBACK = "feedback"


@dataclass
class GraphNode:
    """Represents a node in the LangGraph"""
    name: str
    node_type: NodeType
    operation: Optional[Callable] = None
    condition: Optional[Callable] = None
    next_nodes: List[str] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.name)


class LangGraphOrchestrator:
    """
    LangGraph orchestrator for building intelligent AI workflows
    
    Features:
    - Memory management: Persistent state across workflow executions
    - Branching logic: Conditional paths based on context
    - Feedback loops: Iterative improvement and self-correction
    - Cyclic graphs: Support for complex workflow patterns
    """
    
    def __init__(self, integrations: List, logger=None):
        """
        Initialize LangGraph orchestrator
        
        Args:
            integrations: List of AI platform integrations
            logger: Optional logger instance
        """
        self.integrations = integrations
        self.logger = logger
        self.graphs: Dict[str, Dict[str, GraphNode]] = {}
        self.state: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []
        self.max_iterations = 10  # Prevent infinite loops
        
    def create_graph(self, name: str) -> None:
        """
        Create a new graph workflow
        
        Args:
            name: Graph name
        """
        self.graphs[name] = {}
        if self.logger:
            self.logger.info(f"Created graph: {name}")
    
    def add_node(self, graph_name: str, node: GraphNode) -> None:
        """
        Add a node to a graph
        
        Args:
            graph_name: Name of the graph
            node: GraphNode to add
        """
        if graph_name not in self.graphs:
            raise ValueError(f"Graph '{graph_name}' not found")
        
        self.graphs[graph_name][node.name] = node
        if self.logger:
            self.logger.debug(f"Added node '{node.name}' to graph '{graph_name}'")
    
    def connect_nodes(self, graph_name: str, from_node: str, to_node: str) -> None:
        """
        Connect two nodes in a graph
        
        Args:
            graph_name: Name of the graph
            from_node: Source node name
            to_node: Target node name
        """
        if graph_name not in self.graphs:
            raise ValueError(f"Graph '{graph_name}' not found")
        
        graph = self.graphs[graph_name]
        if from_node not in graph:
            raise ValueError(f"Node '{from_node}' not found in graph")
        
        graph[from_node].next_nodes.append(to_node)
        if self.logger:
            self.logger.debug(f"Connected {from_node} -> {to_node} in graph '{graph_name}'")
    
    async def execute_graph(self, graph_name: str, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a graph workflow
        
        Args:
            graph_name: Name of the graph to execute
            initial_state: Initial state for the workflow
            
        Returns:
            Final state after workflow execution
        """
        if graph_name not in self.graphs:
            raise ValueError(f"Graph '{graph_name}' not found")
        
        graph = self.graphs[graph_name]
        self.state = initial_state.copy()
        self.history = []
        
        # Find start node
        start_nodes = [node for node in graph.values() if node.node_type == NodeType.START]
        if not start_nodes:
            raise ValueError(f"No start node found in graph '{graph_name}'")
        
        current_node = start_nodes[0]
        iterations = 0
        
        if self.logger:
            self.logger.info(f"Starting graph execution: {graph_name}")
        
        while current_node and iterations < self.max_iterations:
            iterations += 1
            
            if self.logger:
                self.logger.debug(f"Executing node: {current_node.name} (iteration {iterations})")
            
            # Record history
            self.history.append({
                "node": current_node.name,
                "state": self.state.copy(),
                "iteration": iterations
            })
            
            # Check if we've reached an end node
            if current_node.node_type == NodeType.END:
                break
            
            # Execute node operation
            if current_node.operation:
                try:
                    result = await current_node.operation(self.state, self.integrations)
                    self.state.update(result)
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Error in node {current_node.name}: {e}")
                    self.state["error"] = str(e)
                    break
            
            # Determine next node
            next_node_name = await self._determine_next_node(current_node, graph)
            if not next_node_name:
                break
            
            current_node = graph.get(next_node_name)
        
        if iterations >= self.max_iterations:
            if self.logger:
                self.logger.warning(f"Max iterations ({self.max_iterations}) reached")
            self.state["max_iterations_reached"] = True
        
        return {
            "final_state": self.state,
            "history": self.history,
            "iterations": iterations
        }
    
    async def _determine_next_node(self, current_node: GraphNode, graph: Dict[str, GraphNode]) -> Optional[str]:
        """
        Determine the next node to execute
        
        Args:
            current_node: Current node being executed
            graph: Graph containing all nodes
            
        Returns:
            Name of next node or None
        """
        if not current_node.next_nodes:
            return None
        
        # If it's a decision node, use condition to choose path
        if current_node.node_type == NodeType.DECISION and current_node.condition:
            try:
                chosen_path = current_node.condition(self.state)
                if chosen_path in current_node.next_nodes:
                    return chosen_path
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in decision condition: {e}")
        
        # Default: return first next node
        return current_node.next_nodes[0]
    
    def create_feedback_loop(self, graph_name: str, nodes: List[str], condition: Callable) -> None:
        """
        Create a feedback loop in the graph
        
        Args:
            graph_name: Name of the graph
            nodes: List of node names in the loop
            condition: Function to determine if loop should continue
        """
        if graph_name not in self.graphs:
            raise ValueError(f"Graph '{graph_name}' not found")
        
        if len(nodes) < 2:
            raise ValueError("Feedback loop requires at least 2 nodes")
        
        graph = self.graphs[graph_name]
        
        # Create feedback node
        feedback_node = GraphNode(
            name=f"feedback_{nodes[0]}",
            node_type=NodeType.FEEDBACK,
            condition=condition,
            next_nodes=[nodes[0], nodes[-1]]  # Loop back or continue
        )
        
        self.add_node(graph_name, feedback_node)
        
        # Connect last node to feedback node
        if nodes[-1] in graph:
            graph[nodes[-1]].next_nodes.append(feedback_node.name)
        
        if self.logger:
            self.logger.info(f"Created feedback loop in '{graph_name}': {' -> '.join(nodes)}")
    
    def set_state(self, key: str, value: Any) -> None:
        """
        Set a value in the current state
        
        Args:
            key: State key
            value: Value to store
        """
        self.state[key] = value
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the current state
        
        Args:
            key: State key
            default: Default value if key not found
            
        Returns:
            State value or default
        """
        return self.state.get(key, default)
    
    def clear_state(self) -> None:
        """Clear the current state"""
        self.state.clear()
        if self.logger:
            self.logger.debug("State cleared")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get execution history
        
        Returns:
            List of historical states
        """
        return self.history.copy()
    
    async def create_simple_graph(self, 
                                   steps: List[Dict[str, Any]], 
                                   initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and execute a simple linear graph
        
        Args:
            steps: List of step definitions with 'name' and 'operation'
            initial_state: Initial state
            
        Returns:
            Execution results
        """
        graph_name = f"simple_graph_{id(steps)}"
        self.create_graph(graph_name)
        
        # Add start node
        start_node = GraphNode(name="start", node_type=NodeType.START)
        self.add_node(graph_name, start_node)
        
        prev_node = "start"
        
        # Add process nodes
        for step in steps:
            node = GraphNode(
                name=step["name"],
                node_type=NodeType.PROCESS,
                operation=step.get("operation")
            )
            self.add_node(graph_name, node)
            self.connect_nodes(graph_name, prev_node, step["name"])
            prev_node = step["name"]
        
        # Add end node
        end_node = GraphNode(name="end", node_type=NodeType.END)
        self.add_node(graph_name, end_node)
        self.connect_nodes(graph_name, prev_node, "end")
        
        return await self.execute_graph(graph_name, initial_state)
    
    def get_capabilities(self) -> List[str]:
        """
        Get list of LangGraph orchestrator capabilities
        
        Returns:
            List of capability names
        """
        return [
            "memory_management",
            "branching_logic",
            "feedback_loops",
            "cyclic_graphs",
            "state_tracking",
            "execution_history"
        ]
    
    def get_graph_info(self, graph_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific graph
        
        Args:
            graph_name: Name of the graph
            
        Returns:
            Dict with graph information or None if not found
        """
        if graph_name not in self.graphs:
            return None
        
        graph = self.graphs[graph_name]
        return {
            "name": graph_name,
            "nodes": len(graph),
            "node_names": list(graph.keys()),
            "node_types": {name: node.node_type.value for name, node in graph.items()}
        }
    
    def list_graphs(self) -> List[str]:
        """
        List all available graphs
        
        Returns:
            List of graph names
        """
        return list(self.graphs.keys())
    
    def visualize_graph(self, graph_name: str) -> str:
        """
        Create a text visualization of a graph
        
        Args:
            graph_name: Name of the graph
            
        Returns:
            String representation of the graph structure
        """
        if graph_name not in self.graphs:
            return f"Graph '{graph_name}' not found"
        
        graph = self.graphs[graph_name]
        lines = [f"Graph: {graph_name}", "=" * 40]
        
        for node_name, node in graph.items():
            lines.append(f"\n[{node.node_type.value}] {node_name}")
            if node.next_nodes:
                for next_node in node.next_nodes:
                    lines.append(f"  └─> {next_node}")
        
        return "\n".join(lines)
