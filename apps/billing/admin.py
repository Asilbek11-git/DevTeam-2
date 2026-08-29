from django.contrib import admin
from .models import Plan, Subscription, Invoice, Coupon, Service, Expense

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'monthly_price', 'yearly_price', 'max_members', 'max_projects', 'is_active', 'is_popular')
    list_filter = ('tier', 'is_active', 'is_popular')
    search_fields = ('name', 'description')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('workspace', 'plan', 'status', 'billing_cycle', 'start_date', 'end_date', 'cancel_at_period_end')
    list_filter = ('status', 'billing_cycle', 'plan')
    search_fields = ('workspace__name', 'external_subscription_id')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'workspace', 'amount', 'currency', 'status', 'payment_method', 'paid_at')
    list_filter = ('status', 'currency')
    search_fields = ('invoice_number', 'workspace__name')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'used_count', 'max_uses', 'is_active', 'expires_at')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting_price', 'estimated_delivery_days', 'is_active', 'display_order', 'owner')
    list_filter = ('is_active', 'workspace')
    search_fields = ('name', 'description', 'technologies')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('display_order', 'name')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'expense_date', 'workspace', 'owner')
    list_filter = ('category', 'workspace', 'expense_date')
    search_fields = ('title', 'description', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'expense_date'
    ordering = ('-expense_date',)

