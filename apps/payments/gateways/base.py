"""
Abstract Base Payment Gateway Interface.
Ensures uniform interface across all payment providers (Stripe, Payme, Click, etc.)
"""
from abc import ABC, abstractmethod

class BasePaymentGateway(ABC):
    @abstractmethod
    def create_checkout_session(self, workspace, plan, billing_cycle, success_url, cancel_url):
        """Initializes a checkout transaction with the provider."""
        pass

    @abstractmethod
    def verify_webhook_signature(self, request_payload, signature_header):
        """Verifies incoming webhook payload cryptographically."""
        pass

    @abstractmethod
    def handle_webhook_event(self, payload):
        """Processes event data and synchronizes billing subscriptions/invoices."""
        pass

    @abstractmethod
    def cancel_subscription(self, external_subscription_id):
        """Terminates an active subscription on the remote payment gateway."""
        pass
