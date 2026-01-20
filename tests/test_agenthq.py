"""
Tests for Agent HQ functionality
"""
import pytest
import asyncio
from megabot import MegaBot, AgentHQCoordinator, LangChainOrchestrator, LangGraphOrchestrator
from megabot.agenthq.langgraph_integration import GraphNode, NodeType
from megabot.agenthq.langchain_integration import ChainStep


class TestLangChain:
    """Test LangChain orchestrator"""
    
    @pytest.mark.asyncio
    async def test_langchain_creation(self):
        """Test LangChain orchestrator creation"""
        bot = MegaBot()
        await bot.start()
        
        assert bot.agent_hq is not None
        assert bot.agent_hq.langchain is not None
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_prompt_template_creation(self):
        """Test creating prompt templates"""
        bot = MegaBot()
        await bot.start()
        
        langchain = bot.agent_hq.langchain
        langchain.create_prompt_template("test_template", "Summarize: {text}")
        
        assert "test_template" in langchain.prompt_templates
        formatted = langchain.format_prompt("test_template", text="Hello World")
        assert "Hello World" in formatted
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_chain_creation(self):
        """Test creating and executing chains"""
        bot = MegaBot()
        await bot.start()
        
        langchain = bot.agent_hq.langchain
        
        steps = [
            ChainStep(name="summarize", prompt_template="Summarize: {text}"),
            ChainStep(name="title", prompt_template="Create title for: {summarize}")
        ]
        
        langchain.create_chain("test_chain", steps)
        assert "test_chain" in langchain.chains
        
        result = await langchain.execute_chain("test_chain", {"text": "Test content"})
        assert "steps" in result
        assert len(result["steps"]) == 2
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_simple_chain(self):
        """Test simple chain execution"""
        bot = MegaBot()
        await bot.start()
        
        steps = [
            "Summarize the following text:",
            "Create a title for this summary:"
        ]
        
        result = await bot.create_langchain(steps, "LangChain helps build AI apps")
        
        assert "steps" in result
        assert len(result["steps"]) == 2
        
        await bot.stop()
    
    def test_memory_operations(self):
        """Test memory management"""
        bot = MegaBot()
        
        langchain = bot.agent_hq.langchain
        langchain.set_memory("key1", "value1")
        
        assert langchain.get_memory("key1") == "value1"
        assert langchain.get_memory("key2", "default") == "default"
        
        langchain.clear_memory()
        assert langchain.get_memory("key1") is None
    
    def test_tool_registration(self):
        """Test tool registration"""
        bot = MegaBot()
        
        langchain = bot.agent_hq.langchain
        
        def test_tool(text):
            return text.upper()
        
        langchain.register_tool("uppercase", test_tool)
        assert "uppercase" in langchain.tools
        assert langchain.tools["uppercase"]("hello") == "HELLO"
    
    def test_capabilities(self):
        """Test getting LangChain capabilities"""
        bot = MegaBot()
        
        capabilities = bot.agent_hq.langchain.get_capabilities()
        
        assert "chain_building" in capabilities
        assert "prompt_templates" in capabilities
        assert "tool_integration" in capabilities
        assert "memory_management" in capabilities


class TestLangGraph:
    """Test LangGraph orchestrator"""
    
    @pytest.mark.asyncio
    async def test_langgraph_creation(self):
        """Test LangGraph orchestrator creation"""
        bot = MegaBot()
        await bot.start()
        
        assert bot.agent_hq is not None
        assert bot.agent_hq.langgraph is not None
        
        await bot.stop()
    
    def test_graph_creation(self):
        """Test creating graphs"""
        bot = MegaBot()
        
        langgraph = bot.agent_hq.langgraph
        langgraph.create_graph("test_graph")
        
        assert "test_graph" in langgraph.graphs
    
    def test_node_addition(self):
        """Test adding nodes to graphs"""
        bot = MegaBot()
        
        langgraph = bot.agent_hq.langgraph
        langgraph.create_graph("test_graph")
        
        node = GraphNode(name="start", node_type=NodeType.START)
        langgraph.add_node("test_graph", node)
        
        assert "start" in langgraph.graphs["test_graph"]
    
    def test_node_connection(self):
        """Test connecting nodes"""
        bot = MegaBot()
        
        langgraph = bot.agent_hq.langgraph
        langgraph.create_graph("test_graph")
        
        node1 = GraphNode(name="node1", node_type=NodeType.START)
        node2 = GraphNode(name="node2", node_type=NodeType.END)
        
        langgraph.add_node("test_graph", node1)
        langgraph.add_node("test_graph", node2)
        langgraph.connect_nodes("test_graph", "node1", "node2")
        
        assert "node2" in langgraph.graphs["test_graph"]["node1"].next_nodes
    
    @pytest.mark.asyncio
    async def test_graph_execution(self):
        """Test executing graphs"""
        bot = MegaBot()
        await bot.start()
        
        langgraph = bot.agent_hq.langgraph
        langgraph.create_graph("test_graph")
        
        # Create simple graph
        start_node = GraphNode(name="start", node_type=NodeType.START)
        end_node = GraphNode(name="end", node_type=NodeType.END)
        
        langgraph.add_node("test_graph", start_node)
        langgraph.add_node("test_graph", end_node)
        langgraph.connect_nodes("test_graph", "start", "end")
        
        result = await langgraph.execute_graph("test_graph", {"initial": "state"})
        
        assert "final_state" in result
        assert "history" in result
        assert result["iterations"] >= 1
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_simple_graph(self):
        """Test simple graph execution"""
        bot = MegaBot()
        await bot.start()
        
        async def step_operation(state, integrations):
            return {"processed": True}
        
        steps = [
            {"name": "step1", "operation": step_operation},
            {"name": "step2", "operation": step_operation}
        ]
        
        result = await bot.create_langgraph(steps, {"input": "test"})
        
        assert "final_state" in result
        assert "history" in result
        
        await bot.stop()
    
    def test_state_management(self):
        """Test state management"""
        bot = MegaBot()
        
        langgraph = bot.agent_hq.langgraph
        langgraph.set_state("key1", "value1")
        
        assert langgraph.get_state("key1") == "value1"
        assert langgraph.get_state("key2", "default") == "default"
        
        langgraph.clear_state()
        assert langgraph.get_state("key1") is None
    
    def test_capabilities(self):
        """Test getting LangGraph capabilities"""
        bot = MegaBot()
        
        capabilities = bot.agent_hq.langgraph.get_capabilities()
        
        assert "memory_management" in capabilities
        assert "branching_logic" in capabilities
        assert "feedback_loops" in capabilities
        assert "cyclic_graphs" in capabilities
    
    def test_graph_visualization(self):
        """Test graph visualization"""
        bot = MegaBot()
        
        langgraph = bot.agent_hq.langgraph
        langgraph.create_graph("test_graph")
        
        node1 = GraphNode(name="start", node_type=NodeType.START)
        node2 = GraphNode(name="end", node_type=NodeType.END)
        
        langgraph.add_node("test_graph", node1)
        langgraph.add_node("test_graph", node2)
        langgraph.connect_nodes("test_graph", "start", "end")
        
        viz = langgraph.visualize_graph("test_graph")
        
        assert "test_graph" in viz
        assert "start" in viz
        assert "end" in viz


class TestAgentHQ:
    """Test Agent HQ coordinator"""
    
    @pytest.mark.asyncio
    async def test_coordinator_creation(self):
        """Test Agent HQ coordinator creation"""
        bot = MegaBot()
        await bot.start()
        
        assert bot.agent_hq is not None
        assert isinstance(bot.agent_hq, AgentHQCoordinator)
        
        await bot.stop()
    
    def test_agent_registration(self):
        """Test agent registration"""
        bot = MegaBot()
        
        coordinator = bot.agent_hq
        
        # Default agents should be registered
        agents = coordinator.list_agents()
        assert len(agents) > 0
        
        # Check for specific agents
        agent_names = [a["name"] for a in agents]
        assert "copilot" in agent_names
        assert "claude" in agent_names
        assert "gpt" in agent_names
        assert "gemini" in agent_names
        assert "grok" in agent_names
        assert "devin" in agent_names
        assert "jules" in agent_names
        assert "deepseek" in agent_names
        assert "perplexity" in agent_names
        assert "comet" in agent_names
    
    def test_list_agents_by_status(self):
        """Test listing agents by status"""
        bot = MegaBot()
        
        all_agents = bot.list_agents()
        active_agents = bot.list_agents(status="active")
        available_agents = bot.list_agents(status="available")
        
        assert len(all_agents) >= len(active_agents)
        assert len(all_agents) >= len(available_agents)
    
    def test_get_agent_info(self):
        """Test getting agent information"""
        bot = MegaBot()
        
        agent_info = bot.get_agent_info("copilot")
        
        assert agent_info is not None
        assert agent_info["name"] == "copilot"
        assert "platform" in agent_info
        assert "capabilities" in agent_info
        assert "status" in agent_info
    
    @pytest.mark.asyncio
    async def test_orchestrate_sequential(self):
        """Test sequential orchestration"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.orchestrate_agents(
            "Write a simple Python function",
            agents=["copilot", "gpt"],
            mode="sequential"
        )
        
        assert "task" in result
        assert "responses" in result
        assert "mode" in result
        assert result["mode"] == "sequential"
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_orchestrate_parallel(self):
        """Test parallel orchestration"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.orchestrate_agents(
            "Explain quantum computing",
            agents=["gpt", "gemini"],
            mode="parallel"
        )
        
        assert "task" in result
        assert "responses" in result
        assert result["mode"] == "parallel"
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_orchestrate_adaptive(self):
        """Test adaptive orchestration"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.orchestrate_agents(
            "Analyze this code and suggest improvements",
            mode="adaptive"
        )
        
        assert "task" in result
        assert "mode" in result
        assert result["mode"] == "adaptive"
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_self_update(self):
        """Test self-update capability"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.agent_hq_self_update()
        
        assert "timestamp" in result
        assert "updates" in result
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_self_build_chain(self):
        """Test self-build with chain"""
        bot = MegaBot()
        await bot.start()
        
        requirements = {
            "type": "chain",
            "name": "auto_chain_test",
            "steps": [
                {"name": "step1", "prompt": "Process {input}"},
                {"name": "step2", "prompt": "Refine {step1}"}
            ]
        }
        
        result = await bot.agent_hq_self_build(requirements)
        
        assert "created_workflows" in result
        assert len(result["created_workflows"]) > 0
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_self_build_graph(self):
        """Test self-build with graph"""
        bot = MegaBot()
        await bot.start()
        
        requirements = {
            "type": "graph",
            "name": "auto_graph_test",
            "nodes": [
                {"name": "start", "type": "START"},
                {"name": "process", "type": "PROCESS"},
                {"name": "end", "type": "END"}
            ]
        }
        
        result = await bot.agent_hq_self_build(requirements)
        
        assert "created_workflows" in result
        assert len(result["created_workflows"]) > 0
        
        await bot.stop()
    
    def test_get_status(self):
        """Test getting Agent HQ status"""
        bot = MegaBot()
        
        status = bot.get_agent_hq_status()
        
        assert status["enabled"] is True
        assert "agents" in status
        assert "orchestrators" in status
        assert "last_update" in status
    
    def test_get_capabilities(self):
        """Test getting Agent HQ capabilities"""
        bot = MegaBot()
        
        capabilities = bot.agent_hq.get_capabilities()
        
        assert "multi_agent_orchestration" in capabilities
        assert "self_update" in capabilities
        assert "self_build" in capabilities
        assert "native_github_integration" in capabilities


class TestMegaBotIntegration:
    """Test Agent HQ integration with MegaBot"""
    
    @pytest.mark.asyncio
    async def test_megabot_with_agent_hq(self):
        """Test MegaBot includes Agent HQ"""
        bot = MegaBot()
        await bot.start()
        
        status = bot.get_status()
        
        assert "agent_hq" in status
        assert status["agent_hq"]["enabled"] is True
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_megabot_agent_methods(self):
        """Test MegaBot agent methods"""
        bot = MegaBot()
        await bot.start()
        
        # Test list_agents
        agents = bot.list_agents()
        assert len(agents) > 0
        
        # Test get_agent_info
        agent_info = bot.get_agent_info("copilot")
        assert agent_info is not None
        
        # Test orchestrate_agents
        result = await bot.orchestrate_agents("Test task", mode="sequential")
        assert "responses" in result
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_langchain_integration(self):
        """Test LangChain integration through MegaBot"""
        bot = MegaBot()
        await bot.start()
        
        steps = ["Analyze this:", "Summarize the analysis:"]
        result = await bot.create_langchain(steps, "Test input")
        
        assert "steps" in result
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_langgraph_integration(self):
        """Test LangGraph integration through MegaBot"""
        bot = MegaBot()
        await bot.start()
        
        async def process(state, integrations):
            return {"processed": True}
        
        steps = [{"name": "step1", "operation": process}]
        result = await bot.create_langgraph(steps, {"input": "test"})
        
        assert "final_state" in result
        
        await bot.stop()


class TestOctopusBrain:
    """Test Octopus Brain functionality"""
    
    def test_octopus_brain_initialization(self):
        """Test Octopus Brain initialization"""
        bot = MegaBot()
        
        assert bot.agent_hq is not None
        assert bot.agent_hq.octopus_brain is not None
    
    def test_tentacle_registration(self):
        """Test tentacles are registered in brain"""
        bot = MegaBot()
        
        tentacles = bot.get_all_tentacles()
        
        assert len(tentacles) == 10  # All 10 agents
        assert any(t["name"] == "copilot" for t in tentacles)
        assert any(t["name"] == "deepseek" for t in tentacles)
        assert any(t["name"] == "perplexity" for t in tentacles)
        assert any(t["name"] == "comet" for t in tentacles)
    
    def test_get_tentacle_status(self):
        """Test getting individual tentacle status"""
        bot = MegaBot()
        
        tentacle_status = bot.get_tentacle_status("copilot")
        
        assert tentacle_status is not None
        assert tentacle_status["name"] == "copilot"
        assert "performance" in tentacle_status
        assert "capabilities" in tentacle_status
    
    def test_brain_status(self):
        """Test getting brain status"""
        bot = MegaBot()
        
        status = bot.get_octopus_brain_status()
        
        assert "tentacles" in status
        assert status["tentacles"]["total"] == 10
        assert "memory" in status
    
    @pytest.mark.asyncio
    async def test_octopus_coordination(self):
        """Test octopus brain coordination"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.octopus_coordinate(
            "Write a Python function",
            context={"capabilities": ["code_generation"]}
        )
        
        assert "decision" in result
        assert "tentacle_results" in result
        
        await bot.stop()


class TestCloudOctopus:
    """Test Cloud Octopus functionality"""
    
    @pytest.mark.asyncio
    async def test_cloud_deployment(self):
        """Test cloud deployment"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.deploy_to_cloud(
            provider="aws",
            regions=["us-east-1", "eu-west-1"]
        )
        
        assert result["provider"] == "aws"
        assert len(result["regions"]) == 2
        assert result["status"] == "deployed"
        assert len(result["endpoints"]) > 0
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_cloud_storage_provisioning(self):
        """Test big space cloud storage provisioning"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.provision_cloud_storage({
            "object_storage": True,
            "database": True,
            "cache": True,
            "data_warehouse": True
        })
        
        assert result["status"] == "provisioned"
        assert len(result["storage_provisioned"]) == 4
        
        await bot.stop()
    
    def test_cloud_status(self):
        """Test getting cloud status"""
        bot = MegaBot()
        
        status = bot.get_cloud_status()
        
        assert "deployment" in status
        assert "storage" in status
        assert "tentacles" in status
        assert "auto_scaling" in status


class TestEnterpriseOctogent:
    """Test Enterprise Cloud Octogent"""
    
    @pytest.mark.asyncio
    async def test_enterprise_deployment(self):
        """Test enterprise cloud deployment"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.deploy_to_enterprise_cloud({
            "domain": "octogent.mycompany.com",
            "regions": ["datacenter-1", "datacenter-2"]
        })
        
        assert result["deployment_type"] == "enterprise"
        assert result["status"] == "deployed"
        assert len(result["components_deployed"]) > 0
        assert len(result["endpoints"]) > 0
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_enterprise_infrastructure_config(self):
        """Test enterprise infrastructure configuration"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.configure_enterprise_infrastructure({
            "networking": {
                "vpc": "10.0.0.0/16",
                "subnets": ["10.0.1.0/24", "10.0.2.0/24"]
            },
            "security": {
                "firewall": "enabled",
                "encryption": "AES-256"
            }
        })
        
        assert len(result["applied_settings"]) == 2
        
        await bot.stop()
    
    def test_enterprise_octogent_status(self):
        """Test enterprise octogent status"""
        bot = MegaBot()
        
        status = bot.get_enterprise_octogent_status()
        
        assert "octogent" in status
        assert status["octogent"]["name"] == "🐙 Big Octogent"
        assert "enterprise_cloud" in status
        assert "tentacles" in status
        assert "brain" in status
    
    def test_enterprise_capacity(self):
        """Test enterprise capacity information"""
        bot = MegaBot()
        
        capacity = bot.get_enterprise_capacity()
        
        assert "compute" in capacity
        assert "storage" in capacity
        assert "network" in capacity
        assert "scaling" in capacity
    
    def test_enterprise_cost_estimate(self):
        """Test enterprise cost estimation"""
        bot = MegaBot()
        
        costs = bot.estimate_enterprise_costs()
        
        assert "monthly_costs" in costs
        assert "total_monthly" in costs
        assert "savings_opportunities" in costs
