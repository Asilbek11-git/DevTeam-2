"""
Affiliate Partner Program Models & Commission Tracking.
"""
from django.db import models
from apps.core.models import TimeStampedModel
import uuid

class AffiliateProfile(TimeStampedModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='affiliate_profile')
    affiliate_code = models.CharField(max_length=30, unique=True, db_index=True)
    commission_rate_percent = models.DecimalField(max_digits=5, decimal_places=2, default=20.00) # 20% recurring
    
    total_clicks = models.PositiveIntegerField(default=0)
    total_registrations = models.PositiveIntegerField(default=0)
    total_paid_customers = models.PositiveIntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    is_approved = models.BooleanField(default=True)
    payout_email = models.EmailField(blank=True)

    def save(self, *args, **kwargs):
        if not self.affiliate_code:
            self.affiliate_code = f"AFF-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Affiliate {self.user.username} ({self.affiliate_code}) - {self.commission_rate_percent}%"
