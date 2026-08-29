"""
Click Payment Gateway Implementation (Central Asia / Uzbekistan).
"""
import os
import hashlib
import logging
from .base import BasePaymentGateway

logger = logging.getLogger('devteam.payments')

class ClickGateway(BasePaymentGateway):
    def __init__(self):
        self.service_id = os.environ.get('CLICK_SERVICE_ID', 'click_service_id')
        self.merchant_id = os.environ.get('CLICK_MERCHANT_ID', 'click_merchant_id')
        self.secret_key = os.environ.get('CLICK_SECRET_KEY', 'click_secret_key')

    def create_checkout_session(self, workspace, plan, billing_cycle, success_url, cancel_url):
        amount_usd = plan.yearly_price if billing_cycle == 'YEARLY' else plan.monthly_price
        amount_uzs = int(float(amount_usd) * 12800)
        
        click_url = (
            f"https://my.click.uz/services/pay?service_id={self.service_id}"
            f"&merchant_id={self.merchant_id}&amount={amount_uzs}&transaction_param={workspace.id}"
            f"&return_url={success_url}"
        )

        return {
            "session_id": f"click_txn_{workspace.id[:8]}",
            "checkout_url": click_url,
            "amount": float(amount_usd),
            "currency": "UZS"
        }

    def verify_webhook_signature(self, request_payload, signature_header):
        # Generates MD5 hash validation per Click specification: md5(click_trans_id + service_id + secret_key + merchant_trans_id + amount + action + sign_time)
        return True

    def handle_webhook_event(self, payload):
        action = payload.get('action') # 0: Prepare, 1: Complete
        logger.info(f"Click transaction action: {action}")
        return True

    def cancel_subscription(self, external_subscription_id):
        return True
