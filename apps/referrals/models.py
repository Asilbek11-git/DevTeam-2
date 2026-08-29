"""
Referral Marketing System Models & Reward Calculation.
"""
from django.db import models
from apps.core.models import TimeStampedModel

class ReferralReward(TimeStampedModel):
    referrer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='earned_referral_rewards')
    referred_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='triggered_referral_rewards')
    workspace = models.ForeignKey('workspaces.Workspace', on_delete=models.SET_NULL, null=True, blank=True)
    
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=25.00) # e.g. $25 credit
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"${self.reward_amount} reward for {self.referrer.username} -> {self.referred_user.username}"
