"""
Payment Gateway Factory & Transaction Processing Orchestrator.
"""
from .gateways.stripe_gateway import StripeGateway
from .gateways.payme_gateway import PaymeGateway
from .gateways.click_gateway import ClickGateway
from apps.billing.models import Subscription, Invoice, Plan
from apps.notifications.models import Notification, NotificationType
from apps.activity.models import ActivityLog
from django.utils import timezone
from datetime import timedelta
import uuid

class PaymentService:
    @staticmethod
    def get_gateway(gateway_name='stripe'):
        gateways = {
            'stripe': StripeGateway(),
            'payme': PaymeGateway(),
            'click': ClickGateway(),
        }
        return gateways.get(gateway_name.lower(), StripeGateway())

    @classmethod
    def process_successful_payment(cls, workspace, plan, billing_cycle='MONTHLY', gateway='stripe', coupon_code=None):
        """Activates or upgrades workspace subscription and generates paid invoice."""
        days = 365 if billing_cycle == 'YEARLY' else 30
        now = timezone.now()
        
        # Calculate price with optional coupon
        price = plan.yearly_price if billing_cycle == 'YEARLY' else plan.monthly_price
        
        # Create or update subscription
        subscription, _ = Subscription.objects.update_or_create(
            workspace=workspace,
            defaults={
                'plan': plan,
                'status': Subscription.Status.ACTIVE,
                'billing_cycle': billing_cycle,
                'start_date': now,
                'end_date': now + timedelta(days=days),
                'payment_gateway': gateway,
                'cancel_at_period_end': False
            }
        )

        # Create paid Invoice
        invoice_num = f"INV-{now.strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
        invoice = Invoice.objects.create(
            workspace=workspace,
            subscription=subscription,
            invoice_number=invoice_num,
            amount=price,
            status=Invoice.Status.PAID,
            payment_method=f"{gateway.capitalize()} Gateway",
            paid_at=now
        )

        # Create notification for owner
        Notification.objects.create(
            workspace=workspace,
            recipient=workspace.owner,
            notification_type=NotificationType.PAYMENT_SUCCESS,
            title=f"Payment Received: {plan.name} Plan",
            message=f"Your subscription to {plan.name} ({billing_cycle.lower()}) has been activated. Invoice #{invoice_num} is available.",
            action_url="/billing/"
        )

        # Record activity
        ActivityLog.objects.create(
            workspace=workspace,
            action=ActivityLog.ActionType.PAYMENT_SUCCESS,
            entity_type='Subscription',
            entity_id=str(subscription.id),
            description=f"Workspace upgraded to {plan.name} (${price} via {gateway.upper()})."
        )

        return subscription, invoice
