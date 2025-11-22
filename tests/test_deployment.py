"""
Tests for deployment-related features (debug, payments)
"""
import pytest
import os
from pathlib import Path
from megabot import DebugMode, get_debug, is_debug_enabled
from megabot import PaymentProcessor, PaymentMethod, PaymentStatus


class TestDebugMode:
    """Test debug mode functionality"""
    
    def test_debug_mode_disabled_by_default(self):
        """Test debug mode is disabled by default"""
        debug = DebugMode(enabled=False)
        assert debug.enabled is False
    
    def test_debug_mode_enabled(self):
        """Test debug mode can be enabled"""
        debug = DebugMode(enabled=True)
        assert debug.enabled is True
        assert debug.debug_dir.exists()
    
    def test_debug_mode_from_env(self, monkeypatch):
        """Test debug mode reads from environment"""
        monkeypatch.setenv("DEBUG", "true")
        debug = DebugMode()
        assert debug.enabled is True
    
    def test_debug_log(self):
        """Test debug logging"""
        debug = DebugMode(enabled=True)
        # Should not raise
        debug.log("Test message", "INFO")
        debug.log("Debug message", "DEBUG")
    
    def test_debug_log_disabled(self):
        """Test debug logging when disabled"""
        debug = DebugMode(enabled=False)
        # Should not raise even when disabled
        debug.log("Test message", "INFO")
    
    def test_api_call_logging(self):
        """Test API call logging"""
        debug = DebugMode(enabled=True)
        debug.log_api_call(
            "test_platform",
            "/test/endpoint",
            {"query": "test"},
            {"result": "success"}
        )
    
    def test_error_logging(self):
        """Test error logging"""
        debug = DebugMode(enabled=True)
        error = ValueError("Test error")
        debug.log_error(error, {"context": "test"})
    
    def test_state_dump(self):
        """Test state dumping"""
        debug = DebugMode(enabled=True)
        state = {"key": "value", "number": 42}
        debug.dump_state(state, "test_state")
    
    def test_get_diagnostics(self):
        """Test diagnostics"""
        debug = DebugMode(enabled=True)
        diagnostics = debug.get_diagnostics()
        
        assert "debug_enabled" in diagnostics
        assert "python_version" in diagnostics
        assert "platform" in diagnostics
    
    def test_performance_measurement(self):
        """Test performance measurement"""
        debug = DebugMode(enabled=True)
        debug.measure_performance("test_operation", 0.123)
    
    def test_global_debug_instance(self):
        """Test global debug instance"""
        debug1 = get_debug()
        debug2 = get_debug()
        assert debug1 is debug2
    
    def test_is_debug_enabled(self):
        """Test is_debug_enabled helper"""
        enabled = is_debug_enabled()
        assert isinstance(enabled, bool)


class TestPaymentProcessor:
    """Test payment processing functionality"""
    
    def test_payment_processor_creation(self):
        """Test payment processor creation"""
        processor = PaymentProcessor()
        assert processor is not None
        assert processor.transactions == []
    
    def test_payment_processor_with_config(self):
        """Test payment processor with configuration"""
        config = {
            "stripe_api_key": "sk_test_123",
            "bitcoin_address": "bc1qtest123",
            "dogecoin_address": "Dtest123"
        }
        processor = PaymentProcessor(config)
        assert processor.stripe_api_key == "sk_test_123"
        assert processor.bitcoin_address == "bc1qtest123"
        assert processor.dogecoin_address == "Dtest123"
    
    def test_create_payment_intent_stripe(self):
        """Test creating Stripe payment intent"""
        processor = PaymentProcessor()
        intent = processor.create_payment_intent(
            9.99,
            "usd",
            PaymentMethod.STRIPE,
            {"user_id": "test123"}
        )
        
        assert intent["amount"] == 9.99
        assert intent["currency"] == "usd"
        assert intent["method"] == "stripe"
        assert intent["status"] == "pending"
        assert "transaction_id" in intent
        assert "stripe_intent_id" in intent
        assert "payment_url" in intent
    
    def test_create_payment_intent_bitcoin(self):
        """Test creating Bitcoin payment intent"""
        processor = PaymentProcessor()
        intent = processor.create_payment_intent(
            100.0,
            "usd",
            PaymentMethod.BITCOIN
        )
        
        assert intent["amount"] == 100.0
        assert intent["method"] == "bitcoin"
        assert "crypto_address" in intent
        assert "amount_crypto" in intent
        assert "qr_code_url" in intent
    
    def test_create_payment_intent_dogecoin(self):
        """Test creating Dogecoin payment intent"""
        processor = PaymentProcessor()
        intent = processor.create_payment_intent(
            50.0,
            "usd",
            PaymentMethod.DOGECOIN
        )
        
        assert intent["amount"] == 50.0
        assert intent["method"] == "dogecoin"
        assert "crypto_address" in intent
        assert "amount_crypto" in intent
    
    def test_create_payment_intent_bank_transfer(self):
        """Test creating bank transfer payment intent"""
        config = {
            "bank_account": {
                "account_number": "123456789",
                "routing_number": "987654321",
                "account_name": "MEGAGENT LLC"
            }
        }
        processor = PaymentProcessor(config)
        intent = processor.create_payment_intent(
            29.99,
            "usd",
            PaymentMethod.BANK_TRANSFER
        )
        
        assert intent["amount"] == 29.99
        assert intent["method"] == "bank_transfer"
        assert "bank_details" in intent
        assert intent["bank_details"]["account_number"] == "123456789"
    
    def test_verify_payment(self):
        """Test payment verification"""
        processor = PaymentProcessor()
        intent = processor.create_payment_intent(9.99, "usd", PaymentMethod.STRIPE)
        
        result = processor.verify_payment(intent["transaction_id"])
        assert result["verified"] is False
        assert result["status"] == "pending"
    
    def test_verify_payment_not_found(self):
        """Test verifying non-existent payment"""
        processor = PaymentProcessor()
        result = processor.verify_payment("nonexistent_id")
        
        assert result["verified"] is False
        assert result["status"] == "not_found"
    
    def test_get_payment_methods(self):
        """Test getting available payment methods"""
        processor = PaymentProcessor()
        methods = processor.get_payment_methods()
        
        assert "stripe" in methods
        assert "bitcoin" in methods
        assert "dogecoin" in methods
        assert "bank_transfer" in methods
        assert "stripe_wallet" in methods
        
        # All should be disabled without config
        assert methods["stripe"]["enabled"] is False
        assert methods["bitcoin"]["enabled"] is False
    
    def test_get_payment_methods_configured(self):
        """Test getting payment methods with configuration"""
        config = {
            "stripe_api_key": "sk_test_123",
            "bitcoin_address": "bc1qtest"
        }
        processor = PaymentProcessor(config)
        methods = processor.get_payment_methods()
        
        assert methods["stripe"]["enabled"] is True
        assert methods["bitcoin"]["enabled"] is True
        assert methods["dogecoin"]["enabled"] is False
    
    def test_transaction_history(self):
        """Test transaction history"""
        processor = PaymentProcessor()
        processor.create_payment_intent(9.99, "usd", PaymentMethod.STRIPE)
        processor.create_payment_intent(29.99, "usd", PaymentMethod.STRIPE)
        
        history = processor.get_transaction_history()
        assert len(history) == 2
    
    def test_transaction_history_filtered(self):
        """Test filtered transaction history"""
        processor = PaymentProcessor()
        processor.create_payment_intent(
            9.99, "usd", PaymentMethod.STRIPE,
            {"user_id": "user1"}
        )
        processor.create_payment_intent(
            29.99, "usd", PaymentMethod.STRIPE,
            {"user_id": "user2"}
        )
        
        history = processor.get_transaction_history("user1")
        assert len(history) == 1
        assert history[0]["metadata"]["user_id"] == "user1"
    
    def test_refund_payment(self):
        """Test refunding a payment"""
        processor = PaymentProcessor()
        intent = processor.create_payment_intent(9.99, "usd", PaymentMethod.STRIPE)
        
        # Manually mark as completed for testing
        processor._update_transaction_status(
            intent["transaction_id"],
            PaymentStatus.COMPLETED
        )
        
        result = processor.refund_payment(intent["transaction_id"])
        assert result["success"] is True
        assert "refund_id" in result
        assert result["amount"] == 9.99
    
    def test_refund_payment_not_completed(self):
        """Test refunding a non-completed payment"""
        processor = PaymentProcessor()
        intent = processor.create_payment_intent(9.99, "usd", PaymentMethod.STRIPE)
        
        result = processor.refund_payment(intent["transaction_id"])
        assert result["success"] is False
        assert "Can only refund completed" in result["message"]
    
    def test_refund_payment_not_found(self):
        """Test refunding non-existent payment"""
        processor = PaymentProcessor()
        result = processor.refund_payment("nonexistent_id")
        
        assert result["success"] is False
        assert "not found" in result["message"]
    
    def test_get_config(self):
        """Test getting payment processor config"""
        config = {
            "stripe_api_key": "sk_test_123",
            "bitcoin_address": "bc1qtest"
        }
        processor = PaymentProcessor(config)
        
        config_info = processor.get_config()
        assert config_info["stripe_configured"] is True
        assert config_info["bitcoin_configured"] is True
        assert config_info["dogecoin_configured"] is False
        assert config_info["total_transactions"] == 0
    
    def test_process_webhook(self):
        """Test processing payment webhook"""
        processor = PaymentProcessor()
        payload = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "metadata": {
                        "transaction_id": "txn_123"
                    }
                }
            }
        }
        
        result = processor.process_webhook(payload, "test_signature")
        assert result["received"] is True
        assert result["event_type"] == "payment_intent.succeeded"


class TestEnterpriseSubscription:
    """Test enterprise subscription tier"""
    
    def test_enterprise_tier_in_monetization(self):
        """Test that enterprise tier is available"""
        from megabot import MonetizationManager, SubscriptionTier
        
        manager = MonetizationManager("enterprise")
        assert manager.tier == SubscriptionTier.ENTERPRISE
    
    def test_enterprise_tier_unlimited(self):
        """Test enterprise tier has unlimited access"""
        from megabot import MonetizationManager
        
        manager = MonetizationManager("enterprise")
        can_query, reason = manager.can_query()
        assert can_query is True
        assert reason is None
        
        can_research, reason = manager.can_research("deep")
        assert can_research is True
        assert reason is None
    
    def test_enterprise_tier_info(self):
        """Test getting enterprise tier information"""
        from megabot import MonetizationManager
        
        all_tiers = MonetizationManager.get_all_tiers()
        assert "enterprise" in all_tiers
        assert all_tiers["enterprise"]["name"] == "Enterprise"
        assert "$29.99" in all_tiers["enterprise"]["price"]
