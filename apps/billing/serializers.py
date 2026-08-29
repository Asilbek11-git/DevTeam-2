"""
Billing, Subscription & Invoice Serializers.
"""
from rest_framework import serializers
from .models import Plan, Subscription, Invoice, Coupon

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'tier', 'description', 'monthly_price', 'yearly_price',
            'is_active', 'is_popular', 'max_members', 'max_projects', 'max_storage_mb',
            'max_ai_generations_per_month', 'max_automation_rules', 'has_git_integrations',
            'has_advanced_reports', 'has_time_tracking', 'has_white_label', 'has_sso', 'has_priority_support'
        ]

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'workspace', 'plan', 'status', 'billing_cycle',
            'start_date', 'end_date', 'trial_end', 'cancel_at_period_end'
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'amount', 'currency', 'status', 'payment_method', 'paid_at', 'pdf_url', 'created_at']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'is_active', 'expires_at']
