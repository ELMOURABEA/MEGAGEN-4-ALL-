"""
Tests for MEGA-Bot
"""
import pytest
import asyncio
from megabot import MegaBot, Config
from megabot.integrations import CopilotIntegration, GeminiIntegration


class TestConfig:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test creating a config object"""
        config = Config()
        assert config is not None
        assert config.config is not None
    
    def test_config_get(self):
        """Test getting config values"""
        config = Config()
        assert config.get("features.deep_research") is not None
        assert config.get("workflow.max_concurrent_tasks") is not None
    
    def test_config_set(self):
        """Test setting config values"""
        config = Config()
        config.set("test.value", "test_data")
        assert config.get("test.value") == "test_data"


class TestIntegrations:
    """Test AI platform integrations"""
    
    @pytest.mark.asyncio
    async def test_copilot_query(self):
        """Test Copilot integration query"""
        integration = CopilotIntegration("test-key", {})
        result = await integration.query("Test prompt")
        
        assert result is not None
        assert "platform" in result
        assert "response" in result
        assert result["platform"] == "GitHub Copilot"
    
    @pytest.mark.asyncio
    async def test_copilot_research(self):
        """Test Copilot integration research"""
        integration = CopilotIntegration("test-key", {})
        result = await integration.research("test topic", "medium")
        
        assert result is not None
        assert "topic" in result
        assert "findings" in result
        assert "sources" in result
    
    @pytest.mark.asyncio
    async def test_gemini_query(self):
        """Test Gemini integration query"""
        integration = GeminiIntegration("test-key", {})
        result = await integration.query("Test prompt")
        
        assert result is not None
        assert result["platform"] == "Gemini 2.5 Pro"
    
    def test_integration_capabilities(self):
        """Test getting integration capabilities"""
        integration = CopilotIntegration("test-key", {})
        capabilities = integration.get_capabilities()
        
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0


class TestMegaBot:
    """Test MEGA-Bot core functionality"""
    
    @pytest.mark.asyncio
    async def test_megabot_creation(self):
        """Test creating a MegaBot instance"""
        bot = MegaBot()
        assert bot is not None
        assert bot.config is not None
        assert bot.storage is not None
    
    @pytest.mark.asyncio
    async def test_megabot_start_stop(self):
        """Test starting and stopping MegaBot"""
        bot = MegaBot()
        
        await bot.start()
        assert bot.running is True
        
        await bot.stop()
        assert bot.running is False
    
    @pytest.mark.asyncio
    async def test_megabot_query(self):
        """Test querying MegaBot"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.query("Test query")
        
        assert result is not None
        assert "responses" in result
        assert "synthesis" in result
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_megabot_research(self):
        """Test research functionality"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.research("test topic", "medium")
        
        assert result is not None
        assert "topic" in result
        assert "depth" in result
        assert "platforms_used" in result
        assert "synthesis" in result
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_megabot_status(self):
        """Test getting bot status"""
        bot = MegaBot()
        await bot.start()
        
        status = bot.get_status()
        
        assert status is not None
        assert "running" in status
        assert "integrations" in status
        assert "permissions" in status
        assert "features" in status
        
        await bot.stop()
    
    @pytest.mark.asyncio
    async def test_megabot_capabilities(self):
        """Test getting bot capabilities"""
        bot = MegaBot()
        capabilities = bot.get_capabilities()
        
        assert isinstance(capabilities, list)
        # Capabilities list will be empty if no API keys configured
        # This is expected behavior
        assert capabilities is not None
    
    @pytest.mark.asyncio
    async def test_megabot_workflow(self):
        """Test workflow execution"""
        bot = MegaBot()
        await bot.start()
        
        result = await bot.execute_workflow(
            "comprehensive_analysis",
            topic="test"
        )
        
        assert result is not None
        assert "research" in result
        assert "queries" in result
        assert "final_analysis" in result
        
        await bot.stop()


class TestDatabase:
    """Test database functionality"""
    
    def test_database_creation(self):
        """Test creating database"""
        from megabot.database import DatabaseStorage
        
        db = DatabaseStorage(":memory:")
        assert db is not None
    
    def test_research_caching(self):
        """Test research caching"""
        from megabot.database import DatabaseStorage
        import tempfile
        import os
        
        # Create a temp file for the database
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        try:
            db = DatabaseStorage(path)
            
            # Cache some research
            db.cache_research("test", "platform", "deep", {"data": "test"})
            
            # Retrieve it
            result = db.get_cached_research("test", "platform", "deep")
            assert result is not None
            assert result["data"] == "test"
        finally:
            # Clean up
            if os.path.exists(path):
                os.unlink(path)
    
    def test_query_history(self):
        """Test query history"""
        from megabot.database import DatabaseStorage
        import tempfile
        import os
        
        # Create a temp file for the database
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        try:
            db = DatabaseStorage(path)
            
            # Save query
            db.save_query("test query", "test platform", "test response")
            
            # Get history
            history = db.get_query_history()
            assert len(history) > 0
            assert history[0]["query"] == "test query"
        finally:
            # Clean up
            if os.path.exists(path):
                os.unlink(path)


class TestWorkflow:
    """Test workflow components"""
    
    def test_permission_manager(self):
        """Test permission manager"""
        from megabot.workflow import PermissionManager
        
        pm = PermissionManager("full")
        assert pm.check_database_access() is True
        assert pm.check_api_access() is True
    
    def test_permission_grant_revoke(self):
        """Test granting and revoking permissions"""
        from megabot.workflow import PermissionManager
        
        pm = PermissionManager("read")
        
        # Initially should not have write
        assert pm.has_permission("database", "write") is False
        
        # Grant write
        pm.grant_permission("database", "write")
        assert pm.has_permission("database", "write") is True
        
        # Revoke write
        pm.revoke_permission("database", "write")
        assert pm.has_permission("database", "write") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
