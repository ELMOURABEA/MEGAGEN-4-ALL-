"""
Payment processing integrations for MEGA-Bot
Supports multiple payment methods: Stripe, Bank Transfer, Bitcoin, Dogecoin
"""
from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime
import json


class PaymentMethod(Enum):
    """Supported payment methods"""
    STRIPE = "stripe"
    BANK_TRANSFER = "bank_transfer"
    BITCOIN = "bitcoin"
    DOGECOIN = "dogecoin"
    STRIPE_WALLET = "stripe_wallet"


class PaymentStatus(Enum):
    """Payment status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProcessor:
    """
    Payment processing manager for MEGA-Bot subscriptions
    
    Handles multiple payment methods:
    - Stripe (credit/debit cards)
    - Stripe Wallet
    - Bank Transfer
    - Bitcoin
    - Dogecoin
    """
    
    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize payment processor
        
        Args:
            config: Payment configuration dictionary
                - stripe_api_key: Stripe API key
                - stripe_webhook_secret: Stripe webhook secret
                - bitcoin_address: Bitcoin wallet address
                - dogecoin_address: Dogecoin wallet address
                - bank_account: Bank account details
        """
        self.config = config or {}
        
        # Stripe configuration
        self.stripe_api_key = self.config.get("stripe_api_key", "")
        self.stripe_webhook_secret = self.config.get("stripe_webhook_secret", "")
        
        # Cryptocurrency addresses
        self.bitcoin_address = self.config.get("bitcoin_address", "")
        self.dogecoin_address = self.config.get("dogecoin_address", "")
        
        # Bank transfer details
        self.bank_account = self.config.get("bank_account", {})
        
        # Transaction history
        self.transactions = []
    
    def create_payment_intent(
        self, 
        amount: float, 
        currency: str = "usd",
        method: PaymentMethod = PaymentMethod.STRIPE,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a payment intent
        
        Args:
            amount: Payment amount
            currency: Currency code (usd, btc, doge)
            method: Payment method
            metadata: Additional metadata (user_id, subscription_tier, etc.)
        
        Returns:
            Payment intent details
        """
        transaction_id = f"txn_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        payment_intent = {
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "method": method.value,
            "status": PaymentStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        # Add method-specific details
        if method == PaymentMethod.STRIPE or method == PaymentMethod.STRIPE_WALLET:
            payment_intent["stripe_intent_id"] = f"pi_{transaction_id}"
            payment_intent["payment_url"] = f"https://checkout.stripe.com/pay/{transaction_id}"
        
        elif method == PaymentMethod.BANK_TRANSFER:
            payment_intent["bank_details"] = {
                "account_number": self.bank_account.get("account_number", "XXXXXXXXXX"),
                "routing_number": self.bank_account.get("routing_number", "XXXXXXXXX"),
                "account_name": self.bank_account.get("account_name", "MEGAGENT LLC"),
                "bank_name": self.bank_account.get("bank_name", "Your Bank"),
                "reference": transaction_id
            }
        
        elif method == PaymentMethod.BITCOIN:
            payment_intent["crypto_address"] = self.bitcoin_address or "bc1qxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            payment_intent["amount_crypto"] = amount / 50000  # Approximate BTC conversion
            payment_intent["qr_code_url"] = f"https://api.qrserver.com/v1/create-qr-code/?data={payment_intent['crypto_address']}"
        
        elif method == PaymentMethod.DOGECOIN:
            payment_intent["crypto_address"] = self.dogecoin_address or "DXXXXXXXXXXXXXXXXXXXXXXXXXXXXx"
            payment_intent["amount_crypto"] = amount / 0.10  # Approximate DOGE conversion
            payment_intent["qr_code_url"] = f"https://api.qrserver.com/v1/create-qr-code/?data={payment_intent['crypto_address']}"
        
        self.transactions.append(payment_intent)
        return payment_intent
    
    def verify_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        Verify payment status
        
        Args:
            transaction_id: Transaction ID to verify
        
        Returns:
            Payment verification result
        """
        # Find transaction
        transaction = next(
            (t for t in self.transactions if t["transaction_id"] == transaction_id),
            None
        )
        
        if not transaction:
            return {
                "verified": False,
                "status": "not_found",
                "message": "Transaction not found"
            }
        
        # In a real implementation, this would verify with payment provider
        # For now, return pending status
        return {
            "verified": False,
            "status": transaction["status"],
            "message": "Payment verification requires integration with payment provider",
            "transaction": transaction
        }
    
    def process_webhook(self, payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """
        Process payment webhook (e.g., from Stripe)
        
        Args:
            payload: Webhook payload
            signature: Webhook signature for verification
        
        Returns:
            Processing result
        """
        # In a real implementation, verify signature and process event
        event_type = payload.get("type", "unknown")
        
        if event_type == "payment_intent.succeeded":
            transaction_id = payload.get("data", {}).get("object", {}).get("metadata", {}).get("transaction_id")
            if transaction_id:
                self._update_transaction_status(transaction_id, PaymentStatus.COMPLETED)
        
        return {
            "received": True,
            "event_type": event_type
        }
    
    def _update_transaction_status(self, transaction_id: str, status: PaymentStatus):
        """Update transaction status"""
        for transaction in self.transactions:
            if transaction["transaction_id"] == transaction_id:
                transaction["status"] = status.value
                transaction["updated_at"] = datetime.now().isoformat()
                break
    
    def get_payment_methods(self) -> Dict[str, Dict[str, Any]]:
        """
        Get available payment methods with configuration status
        
        Returns:
            Dictionary of payment methods and their availability
        """
        return {
            "stripe": {
                "enabled": bool(self.stripe_api_key),
                "name": "Credit/Debit Card (Stripe)",
                "description": "Pay with credit or debit card via Stripe",
                "currencies": ["usd", "eur", "gbp"]
            },
            "stripe_wallet": {
                "enabled": bool(self.stripe_api_key),
                "name": "Stripe Wallet",
                "description": "Pay with your Stripe wallet balance",
                "currencies": ["usd", "eur", "gbp"]
            },
            "bank_transfer": {
                "enabled": bool(self.bank_account),
                "name": "Bank Transfer",
                "description": "Direct bank transfer (ACH/Wire)",
                "currencies": ["usd"],
                "processing_time": "1-3 business days"
            },
            "bitcoin": {
                "enabled": bool(self.bitcoin_address),
                "name": "Bitcoin (BTC)",
                "description": "Pay with Bitcoin cryptocurrency",
                "currencies": ["btc"],
                "address": self.bitcoin_address if self.bitcoin_address else "Not configured"
            },
            "dogecoin": {
                "enabled": bool(self.dogecoin_address),
                "name": "Dogecoin (DOGE)",
                "description": "Pay with Dogecoin cryptocurrency",
                "currencies": ["doge"],
                "address": self.dogecoin_address if self.dogecoin_address else "Not configured"
            }
        }
    
    def get_transaction_history(self, user_id: Optional[str] = None) -> list:
        """
        Get transaction history
        
        Args:
            user_id: Optional user ID to filter transactions
        
        Returns:
            List of transactions
        """
        if user_id:
            return [
                t for t in self.transactions
                if t.get("metadata", {}).get("user_id") == user_id
            ]
        return self.transactions
    
    def refund_payment(self, transaction_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Process a refund
        
        Args:
            transaction_id: Transaction to refund
            amount: Amount to refund (None for full refund)
        
        Returns:
            Refund result
        """
        transaction = next(
            (t for t in self.transactions if t["transaction_id"] == transaction_id),
            None
        )
        
        if not transaction:
            return {
                "success": False,
                "message": "Transaction not found"
            }
        
        if transaction["status"] != PaymentStatus.COMPLETED.value:
            return {
                "success": False,
                "message": "Can only refund completed transactions"
            }
        
        refund_amount = amount or transaction["amount"]
        refund_id = f"ref_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self._update_transaction_status(transaction_id, PaymentStatus.REFUNDED)
        
        return {
            "success": True,
            "refund_id": refund_id,
            "amount": refund_amount,
            "transaction_id": transaction_id,
            "message": "Refund processed successfully"
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Get payment processor configuration (sanitized)"""
        return {
            "stripe_configured": bool(self.stripe_api_key),
            "bitcoin_configured": bool(self.bitcoin_address),
            "dogecoin_configured": bool(self.dogecoin_address),
            "bank_transfer_configured": bool(self.bank_account),
            "total_transactions": len(self.transactions),
            "payment_methods_available": len([m for m in self.get_payment_methods().values() if m["enabled"]])
        }
