from django.contrib import admin
from .models import ReferralReward

@admin.register(ReferralReward)
class ReferralRewardAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'reward_amount', 'is_paid', 'paid_at', 'created_at')
    list_filter = ('is_paid',)
    search_fields = ('referrer__email', 'referred_user__email')
