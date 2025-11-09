"""
Agent HQ Example - Demonstrating multi-agent orchestration
Shows LangChain, LangGraph, and Agent HQ capabilities
"""
import asyncio
from megabot import MegaBot


async def demonstrate_agent_hq():
    """Demonstrate Agent HQ features"""
    print("=" * 60)
    print("Agent HQ Demo - Orchestrate any agent, any time, anywhere")
    print("=" * 60)
    print()
    
    # Initialize MegaBot with Agent HQ
    bot = MegaBot()
    await bot.start()
    
    # 1. List all available agents
    print("\n1. Available Agents in Agent HQ")
    print("-" * 60)
    agents = bot.list_agents()
    print(f"Total agents: {len(agents)}")
    for agent in agents:
        print(f"  • {agent['name']:12} ({agent['provider']:15}) - {agent['status']:10}")
        print(f"    Capabilities: {', '.join(agent['capabilities'][:3])}")
    
    # 2. Get specific agent information
    print("\n2. Detailed Agent Information")
    print("-" * 60)
    copilot_info = bot.get_agent_info("copilot")
    print(f"Agent: {copilot_info['name']}")
    print(f"Platform: {copilot_info['platform']}")
    print(f"Capabilities: {', '.join(copilot_info['capabilities'])}")
    print(f"Status: {copilot_info['status']}")
    
    # 3. Sequential orchestration
    print("\n3. Sequential Agent Orchestration")
    print("-" * 60)
    print("Task: Analyze a Python function")
    result = await bot.orchestrate_agents(
        task="Write a Python function to calculate fibonacci numbers",
        agents=["copilot", "gpt"],
        mode="sequential"
    )
    print(f"Mode: {result['mode']}")
    print(f"Agents used: {', '.join(result['agents_used'])}")
    print(f"Responses received: {len(result['responses'])}")
    
    # 4. Parallel orchestration
    print("\n4. Parallel Agent Orchestration")
    print("-" * 60)
    print("Task: Explain machine learning")
    result = await bot.orchestrate_agents(
        task="Explain machine learning in simple terms",
        agents=["gpt", "gemini", "grok"],
        mode="parallel"
    )
    print(f"Mode: {result['mode']}")
    print(f"Agents used: {', '.join(result['agents_used'])}")
    print(f"Responses received: {len(result['responses'])}")
    
    # 5. Adaptive orchestration
    print("\n5. Adaptive Agent Orchestration")
    print("-" * 60)
    print("Task: Complex code analysis")
    result = await bot.orchestrate_agents(
        task="Analyze and optimize this sorting algorithm",
        mode="adaptive"
    )
    print(f"Mode: {result['mode']}")
    print(f"Execution info: {result.get('execution_info', {})}")
    
    # 6. LangChain demonstration
    print("\n6. LangChain Workflow")
    print("-" * 60)
    print("Creating a chain: Summarize -> Generate Title")
    steps = [
        "Summarize the following text in 2 sentences:",
        "Create a catchy title for this summary:"
    ]
    chain_result = await bot.create_langchain(
        steps=steps,
        initial_text="MEGAGENT is a unified AI platform that orchestrates multiple agents"
    )
    print(f"Chain steps executed: {len(chain_result['steps'])}")
    for i, step in enumerate(chain_result['steps'], 1):
        print(f"  Step {i}: {step['step_name']}")
    
    # 7. LangGraph demonstration
    print("\n7. LangGraph Workflow")
    print("-" * 60)
    print("Creating a graph with branching logic")
    
    async def analyze_step(state, integrations):
        print("  → Analyzing input...")
        return {"analyzed": True, "complexity": "medium"}
    
    async def process_step(state, integrations):
        print("  → Processing data...")
        return {"processed": True}
    
    graph_steps = [
        {"name": "analyze", "operation": analyze_step},
        {"name": "process", "operation": process_step}
    ]
    
    graph_result = await bot.create_langgraph(
        steps=graph_steps,
        initial_state={"input": "test data"}
    )
    print(f"Graph iterations: {graph_result['iterations']}")
    print(f"Final state keys: {list(graph_result['final_state'].keys())}")
    
    # 8. Self-update capability
    print("\n8. Agent HQ Self-Update")
    print("-" * 60)
    update_result = await bot.agent_hq_self_update()
    print(f"Last update: {update_result['timestamp']}")
    print(f"Updates found: {len(update_result['updates'])}")
    print(f"Agents before: {update_result['agents_before']}")
    print(f"Agents after: {update_result['agents_after']}")
    
    # 9. Self-build capability - Create custom workflow
    print("\n9. Agent HQ Self-Build")
    print("-" * 60)
    print("Building custom chain workflow...")
    build_result = await bot.agent_hq_self_build({
        "type": "chain",
        "name": "custom_analysis_chain",
        "steps": [
            {"name": "extract", "prompt": "Extract key information from {input}"},
            {"name": "analyze", "prompt": "Analyze the extracted data: {extract}"},
            {"name": "recommend", "prompt": "Provide recommendations based on: {analyze}"}
        ]
    })
    print(f"Workflows created: {len(build_result['created_workflows'])}")
    for workflow in build_result['created_workflows']:
        print(f"  • Type: {workflow['type']}, Name: {workflow['name']}, Steps: {workflow['steps']}")
    
    print("\n10. Building graph workflow...")
    build_result = await bot.agent_hq_self_build({
        "type": "graph",
        "name": "custom_decision_graph",
        "nodes": [
            {"name": "start", "type": "START"},
            {"name": "evaluate", "type": "PROCESS"},
            {"name": "decide", "type": "DECISION"},
            {"name": "end", "type": "END"}
        ]
    })
    print(f"Workflows created: {len(build_result['created_workflows'])}")
    for workflow in build_result['created_workflows']:
        print(f"  • Type: {workflow['type']}, Name: {workflow['name']}, Nodes: {workflow['nodes']}")
    
    # 10. Get Agent HQ status
    print("\n10. Agent HQ Status")
    print("-" * 60)
    status = bot.get_agent_hq_status()
    print(f"Enabled: {status['enabled']}")
    print(f"Total agents: {status['agents']['total']}")
    print(f"Active agents: {status['agents']['active']}")
    print(f"Available agents: {status['agents']['available']}")
    print(f"\nOrchestrators:")
    print(f"  LangChain - Chains: {status['orchestrators']['langchain']['chains']}")
    print(f"  LangChain - Templates: {status['orchestrators']['langchain']['templates']}")
    print(f"  LangGraph - Graphs: {status['orchestrators']['langgraph']['graphs']}")
    
    # 11. Agent HQ capabilities
    print("\n11. Agent HQ Capabilities")
    print("-" * 60)
    capabilities = bot.agent_hq.get_capabilities()
    print(f"Total capabilities: {len(capabilities)}")
    for cap in sorted(capabilities):
        print(f"  • {cap}")
    
    await bot.stop()
    
    print("\n" + "=" * 60)
    print("Agent HQ Demo Complete!")
    print("=" * 60)


async def demonstrate_langchain_advanced():
    """Demonstrate advanced LangChain features"""
    print("\n" + "=" * 60)
    print("Advanced LangChain Features")
    print("=" * 60)
    
    bot = MegaBot()
    await bot.start()
    
    langchain = bot.agent_hq.langchain
    
    # Create custom prompt templates
    print("\n1. Creating custom prompt templates...")
    langchain.create_prompt_template(
        "code_review",
        "Review this {language} code and suggest improvements:\n{code}"
    )
    langchain.create_prompt_template(
        "test_generation",
        "Generate unit tests for this function:\n{code}"
    )
    
    print(f"Templates created: {', '.join(langchain.list_templates())}")
    
    # Register custom tools
    print("\n2. Registering custom tools...")
    
    def code_formatter(text):
        """Simple code formatter"""
        return text.strip().replace("  ", "    ")
    
    def word_counter(text):
        """Count words in text"""
        return len(text.split())
    
    langchain.register_tool("format_code", code_formatter)
    langchain.register_tool("count_words", word_counter)
    
    print(f"Tools registered: {', '.join(langchain.list_tools())}")
    
    # Use memory across operations
    print("\n3. Using memory for context...")
    langchain.set_memory("project_type", "web_application")
    langchain.set_memory("language", "python")
    langchain.set_memory("framework", "django")
    
    print(f"Project type: {langchain.get_memory('project_type')}")
    print(f"Language: {langchain.get_memory('language')}")
    print(f"Framework: {langchain.get_memory('framework')}")
    
    await bot.stop()


async def demonstrate_langgraph_advanced():
    """Demonstrate advanced LangGraph features"""
    print("\n" + "=" * 60)
    print("Advanced LangGraph Features")
    print("=" * 60)
    
    bot = MegaBot()
    await bot.start()
    
    langgraph = bot.agent_hq.langgraph
    
    # Create a graph with decision nodes
    print("\n1. Creating graph with decision logic...")
    langgraph.create_graph("decision_workflow")
    
    from megabot.agenthq.langgraph_integration import GraphNode, NodeType
    
    # Add nodes
    start = GraphNode(name="start", node_type=NodeType.START)
    
    async def check_condition(state, integrations):
        state["score"] = 75
        return state
    
    check = GraphNode(
        name="check",
        node_type=NodeType.PROCESS,
        operation=check_condition
    )
    
    def decide_path(state):
        return "high_score" if state.get("score", 0) > 70 else "low_score"
    
    decision = GraphNode(
        name="decision",
        node_type=NodeType.DECISION,
        condition=decide_path
    )
    
    high_score = GraphNode(name="high_score", node_type=NodeType.END)
    low_score = GraphNode(name="low_score", node_type=NodeType.END)
    
    langgraph.add_node("decision_workflow", start)
    langgraph.add_node("decision_workflow", check)
    langgraph.add_node("decision_workflow", decision)
    langgraph.add_node("decision_workflow", high_score)
    langgraph.add_node("decision_workflow", low_score)
    
    langgraph.connect_nodes("decision_workflow", "start", "check")
    langgraph.connect_nodes("decision_workflow", "check", "decision")
    decision.next_nodes = ["high_score", "low_score"]
    
    # Execute graph
    result = await langgraph.execute_graph("decision_workflow", {"input": "test"})
    print(f"Graph executed with {result['iterations']} iterations")
    print(f"Final score: {result['final_state'].get('score')}")
    
    # Visualize graph
    print("\n2. Graph visualization:")
    print(langgraph.visualize_graph("decision_workflow"))
    
    # State management
    print("\n3. State management demonstration...")
    langgraph.set_state("session_id", "abc123")
    langgraph.set_state("user_preferences", {"theme": "dark", "language": "en"})
    
    print(f"Session ID: {langgraph.get_state('session_id')}")
    print(f"Preferences: {langgraph.get_state('user_preferences')}")
    
    await bot.stop()


async def main():
    """Run all demonstrations"""
    try:
        await demonstrate_agent_hq()
        await demonstrate_langchain_advanced()
        await demonstrate_langgraph_advanced()
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
