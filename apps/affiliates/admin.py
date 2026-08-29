from django.contrib import admin
from .models import AffiliateProfile

@admin.register(AffiliateProfile)
class AffiliateProfileAdmin(admin.ModelAdmin):
    list_display = ('affiliate_code', 'user', 'commission_rate_percent', 'total_paid_customers', 'total_earnings', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('affiliate_code', 'user__email', 'payout_email')
