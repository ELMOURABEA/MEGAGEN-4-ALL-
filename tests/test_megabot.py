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
        # Create config with pro tier for testing
        config = Config()
        config.set("monetization.tier", "pro")
        bot = MegaBot(config)
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


class TestUtils:
    """Test utility functions"""
    
    def test_validate_query_valid(self):
        """Test validating a valid query"""
        from megabot.utils import validate_query
        
        is_valid, error = validate_query("What is AI?")
        assert is_valid is True
        assert error is None
    
    def test_validate_query_empty(self):
        """Test validating an empty query"""
        from megabot.utils import validate_query
        
        is_valid, error = validate_query("")
        assert is_valid is False
        assert error is not None
    
    def test_validate_query_too_long(self):
        """Test validating a query that's too long"""
        from megabot.utils import validate_query
        
        long_query = "a" * 10001
        is_valid, error = validate_query(long_query)
        assert is_valid is False
        assert "exceeds maximum length" in error
    
    def test_validate_query_dangerous(self):
        """Test validating a query with dangerous content"""
        from megabot.utils import validate_query
        
        is_valid, error = validate_query("Hello <script>alert('xss')</script>")
        assert is_valid is False
        assert "unsafe content" in error
    
    def test_validate_topic_valid(self):
        """Test validating a valid topic"""
        from megabot.utils import validate_topic
        
        is_valid, error = validate_topic("Machine Learning")
        assert is_valid is True
        assert error is None
    
    def test_validate_topic_empty(self):
        """Test validating an empty topic"""
        from megabot.utils import validate_topic
        
        is_valid, error = validate_topic("")
        assert is_valid is False
        assert error is not None
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        from megabot.utils import sanitize_input
        
        dirty = "Hello <script>alert('xss')</script> World"
        clean = sanitize_input(dirty)
        assert "<script>" not in clean
        assert "Hello" in clean
        assert "World" in clean
    
    def test_truncate_text(self):
        """Test text truncation"""
        from megabot.utils import truncate_text
        
        long_text = "a" * 200
        truncated = truncate_text(long_text, max_length=50)
        assert len(truncated) == 50
        assert truncated.endswith("...")
    
    def test_logging_setup(self):
        """Test logging setup"""
        from megabot.utils import setup_logging, get_logger
        
        logger = setup_logging("INFO")
        assert logger is not None
        
        logger2 = get_logger("test")
        assert logger2 is not None


class TestMonetization:
    """Test monetization features"""
    
    def test_monetization_manager_creation(self):
        """Test creating a monetization manager"""
        from megabot.monetization import MonetizationManager
        
        manager = MonetizationManager("free")
        assert manager is not None
        assert manager.tier.value == "free"
    
    def test_free_tier_query_limit(self):
        """Test free tier query limits"""
        from megabot.monetization import MonetizationManager
        
        manager = MonetizationManager("free")
        
        # Should allow first 10 queries
        for i in range(10):
            can_query, msg = manager.can_query()
            assert can_query is True
            manager.record_query()
        
        # 11th query should be blocked
        can_query, msg = manager.can_query()
        assert can_query is False
        assert "limit reached" in msg.lower()
    
    def test_pro_tier_unlimited(self):
        """Test pro tier has unlimited queries"""
        from megabot.monetization import MonetizationManager
        
        manager = MonetizationManager("pro")
        
        # Should allow many queries
        for i in range(20):
            can_query, msg = manager.can_query()
            assert can_query is True
            manager.record_query()
    
    def test_research_depth_restrictions(self):
        """Test research depth restrictions by tier"""
        from megabot.monetization import MonetizationManager
        
        free_manager = MonetizationManager("free")
        pro_manager = MonetizationManager("pro")
        
        # Free tier can only do shallow research
        can_shallow, _ = free_manager.can_research("shallow")
        assert can_shallow is True
        
        can_deep, msg = free_manager.can_research("deep")
        assert can_deep is False
        assert "not available" in msg.lower()
        
        # Pro tier can do all depths
        can_deep, _ = pro_manager.can_research("deep")
        assert can_deep is True
    
    def test_tier_info(self):
        """Test getting tier information"""
        from megabot.monetization import MonetizationManager
        
        manager = MonetizationManager("pro")
        info = manager.get_tier_info()
        
        assert "tier" in info
        assert "limits" in info
        assert "usage" in info
        assert info["tier"] == "pro"
    
    def test_get_all_tiers(self):
        """Test getting all tier information"""
        from megabot.monetization import MonetizationManager
        
        tiers = MonetizationManager.get_all_tiers()
        assert "free" in tiers
        assert "pro" in tiers
        assert "full_energy" in tiers


class TestAdvertising:
    """Test advertising features"""
    
    def test_advertising_core_creation(self):
        """Test creating advertising core"""
        from megabot.advertising import AdvertisingCore
        
        ad_core = AdvertisingCore()
        assert ad_core is not None
    
    def test_advertising_initialization(self):
        """Test advertising initialization"""
        from megabot.advertising import AdvertisingCore
        
        ad_core = AdvertisingCore()
        result = ad_core.initialize()
        assert result is True
    
    def test_show_banner(self):
        """Test showing banner ad"""
        from megabot.advertising import AdvertisingCore
        
        ad_core = AdvertisingCore()
        ad_core.initialize()
        
        result = ad_core.show_banner("bottom")
        assert result["status"] == "success"
        assert result["type"] == "banner"
    
    def test_show_rewarded(self):
        """Test showing rewarded ad"""
        from megabot.advertising import AdvertisingCore
        
        ad_core = AdvertisingCore({
            "rewarded_id": "test-rewarded-id"
        })
        ad_core.initialize()
        
        result = ad_core.show_rewarded("bonus_queries")
        assert result["status"] == "success"
        assert "reward" in result
    
    def test_ad_config(self):
        """Test getting ad configuration"""
        from megabot.advertising import AdvertisingCore
        
        ad_core = AdvertisingCore()
        ad_core.initialize()
        
        config = ad_core.get_config()
        assert config["initialized"] is True
        assert "app_id" in config
    
    def test_ad_ids_from_config(self):
        """Test that AdMob IDs are properly loaded from config"""
        from megabot.advertising import AdvertisingCore
        
        # Test with custom config
        custom_config = {
            "app_id": "ca-app-pub-test~1234567890",
            "banner_id": "ca-app-pub-test/1234567890",
            "interstitial_id": "ca-app-pub-test/0987654321",
            "rewarded_id": "ca-app-pub-test/1122334455"
        }
        ad_core = AdvertisingCore(custom_config)
        
        assert ad_core.app_id == "ca-app-pub-test~1234567890"
        assert ad_core.banner_id == "ca-app-pub-test/1234567890"
        assert ad_core.interstitial_id == "ca-app-pub-test/0987654321"
        assert ad_core.rewarded_id == "ca-app-pub-test/1122334455"
    
    def test_ad_ids_default_empty(self):
        """Test that AdMob IDs default to empty strings when not configured"""
        from megabot.advertising import AdvertisingCore
        
        # Test with no config
        ad_core = AdvertisingCore()
        
        # Without configuration, IDs should be empty strings (not hardcoded)
        assert ad_core.app_id == ""
        assert ad_core.banner_id == ""
        assert ad_core.interstitial_id == ""
        assert ad_core.rewarded_id == ""
    
    @pytest.fixture
    def admob_env_vars(self):
        """Fixture to set and cleanup AdMob environment variables"""
        import os
        old_app_id = os.environ.get("ADMOB_APP_ID")
        old_banner_id = os.environ.get("ADMOB_BANNER_ID")
        os.environ["ADMOB_APP_ID"] = "ca-app-pub-env~1234567890"
        os.environ["ADMOB_BANNER_ID"] = "ca-app-pub-env/1234567890"
        yield
        if old_app_id is not None:
            os.environ["ADMOB_APP_ID"] = old_app_id
        else:
            os.environ.pop("ADMOB_APP_ID", None)
        if old_banner_id is not None:
            os.environ["ADMOB_BANNER_ID"] = old_banner_id
        else:
            os.environ.pop("ADMOB_BANNER_ID", None)

    def test_config_loads_env_vars(self, admob_env_vars):
        """Test that Config properly loads AdMob IDs from environment variables"""
        from megabot.config import Config
        
        config = Config()
        
        assert config.get("advertising.app_id") == "ca-app-pub-env~1234567890"
        assert config.get("advertising.banner_id") == "ca-app-pub-env/1234567890"
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
