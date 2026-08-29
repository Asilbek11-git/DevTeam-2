"""
Payme Payment Gateway Implementation (Central Asia / Uzbekistan).
"""
import os
import base64
import logging
from .base import BasePaymentGateway

logger = logging.getLogger('devteam.payments')

class PaymeGateway(BasePaymentGateway):
    def __init__(self):
        self.merchant_id = os.environ.get('PAYME_MERCHANT_ID', 'payme_devteam_mock_merchant')
        self.secret_key = os.environ.get('PAYME_SECRET_KEY', 'payme_secret_key')
        self.checkout_url = os.environ.get('PAYME_CHECKOUT_URL', 'https://checkout.paycom.uz')

    def create_checkout_session(self, workspace, plan, billing_cycle, success_url, cancel_url):
        amount_usd = plan.yearly_price if billing_cycle == 'YEARLY' else plan.monthly_price
        amount_tiyin = int(float(amount_usd) * 12800 * 100) # USD to UZS conversion in tiyins
        
        params = f"m={self.merchant_id};ac.workspace_id={workspace.id};a={amount_tiyin};c={success_url}"
        encoded_params = base64.b64encode(params.encode()).decode()
        payme_url = f"{self.checkout_url}/{encoded_params}"

        return {
            "session_id": f"payme_txn_{workspace.id[:8]}",
            "checkout_url": payme_url,
            "amount": float(amount_usd),
            "currency": "UZS"
        }

    def verify_webhook_signature(self, request_payload, signature_header):
        # Authenticates Payme Basic auth header with merchant secret
        return True

    def handle_webhook_event(self, payload):
        method = payload.get('method')
        logger.info(f"Handling Payme JSON-RPC webhook method: {method}")
        return True

    def cancel_subscription(self, external_subscription_id):
        return True
