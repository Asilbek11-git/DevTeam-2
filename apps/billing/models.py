"""
SaaS Monetization, Subscription Tiers, Invoices & Coupon Models.
Plans are dynamic and database-driven (Free, Pro, Business, Enterprise).
"""
from django.db import models
from apps.core.models import TimeStampedModel, TenantScopedModel
from apps.core.exceptions import PlanLimitExceededException

class PlanTier(models.TextChoices):
    FREE = 'FREE', 'Free Starter'
    PRO = 'PRO', 'Professional'
    BUSINESS = 'BUSINESS', 'Business & Growth'
    ENTERPRISE = 'ENTERPRISE', 'Enterprise'

class Plan(TimeStampedModel):
    name = models.CharField(max_length=100) # e.g. "Professional"
    tier = models.CharField(max_length=20, choices=PlanTier.choices, default=PlanTier.FREE, unique=True)
    description = models.TextField(blank=True)
    
    # Pricing
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # e.g. with 20% discount
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    
    # Configurable limits
    max_members = models.PositiveIntegerField(default=3) # 0 = unlimited
    max_projects = models.PositiveIntegerField(default=2)
    max_storage_mb = models.PositiveIntegerField(default=500) # MB
    max_ai_generations_per_month = models.PositiveIntegerField(default=20)
    max_automation_rules = models.PositiveIntegerField(default=3)
    
    # Feature Flags
    has_git_integrations = models.BooleanField(default=False)
    has_advanced_reports = models.BooleanField(default=False)
    has_time_tracking = models.BooleanField(default=True)
    has_white_label = models.BooleanField(default=False)
    has_sso = models.BooleanField(default=False)
    has_priority_support = models.BooleanField(default=False)

    class Meta:
        ordering = ['monthly_price']

    def __str__(self):
        return f"{self.name} (${self.monthly_price}/mo)"

class Subscription(TenantScopedModel):
    class Status(models.TextChoices):
        TRIALING = 'TRIALING', 'Trialing'
        ACTIVE = 'ACTIVE', 'Active'
        PAST_DUE = 'PAST_DUE', 'Past Due'
        CANCELED = 'CANCELED', 'Canceled'
        EXPIRED = 'EXPIRED', 'Expired'

    class BillingCycle(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Monthly'
        YEARLY = 'YEARLY', 'Yearly'

    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TRIALING)
    billing_cycle = models.CharField(max_length=20, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    
    # Gateway payment references
    payment_gateway = models.CharField(max_length=30, blank=True, default='stripe')
    external_subscription_id = models.CharField(max_length=255, blank=True)
    external_customer_id = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.workspace.name} - {self.plan.name} ({self.status})"

    def check_project_limit(self):
        if self.plan.max_projects == 0:
            return True # Unlimited
        current_count = self.workspace.projects.count()
        if current_count >= self.plan.max_projects:
            raise PlanLimitExceededException(
                f"Your current {self.plan.name} plan has reached its limit of {self.plan.max_projects} projects. "
                "Upgrade your plan to create more projects."
            )
        return True

    def check_member_limit(self):
        if self.plan.max_members == 0:
            return True
        current_count = self.workspace.members.filter(is_active=True).count()
        if current_count >= self.plan.max_members:
            raise PlanLimitExceededException(
                f"Your current {self.plan.name} plan allows up to {self.plan.max_members} team members. "
                "Upgrade your plan to invite more developers."
            )
        return True

class Invoice(TenantScopedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    invoice_number = models.CharField(max_length=50, unique=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    client = models.ForeignKey('workspaces.Client', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PAID)
    
    payment_method = models.CharField(max_length=50, default='Credit Card (Stripe)')
    paid_at = models.DateTimeField(null=True, blank=True)
    pdf_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - ${self.amount} ({self.status})"

class Coupon(TimeStampedModel):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'PERCENTAGE', 'Percentage Discount'
        FIXED_AMOUNT = 'FIXED_AMOUNT', 'Fixed Amount Discount'

    code = models.CharField(max_length=50, unique=True) # e.g. "STARTUP50"
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices, default=DiscountType.PERCENTAGE)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2) # 50.00% or $50.00
    
    max_uses = models.PositiveIntegerField(default=100)
    used_count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_value}{'%' if self.discount_type == 'PERCENTAGE' else '$'})"

class Service(TimeStampedModel):
    """
    Freelance/business service offerings configurable by the owner.
    """
    workspace = models.ForeignKey(
        'workspaces.Workspace',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='services',
        verbose_name='Workspace'
    )
    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Service Provider / Owner'
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Service Name'
    )
    slug = models.SlugField(
        max_length=220,
        blank=True,
        verbose_name='URL Slug'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Service Description'
    )
    starting_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100.00,
        verbose_name='Starting Price ($)'
    )
    estimated_delivery_days = models.PositiveIntegerField(
        default=7,
        verbose_name='Estimated Delivery (Days)'
    )
    technologies = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Technologies & Stacks',
        help_text='List of tech stacks (e.g. Django, DRF, Celery, React)'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Active for Orders'
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order'
    )

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.name) or 'service'
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (from ${self.starting_price})"

class Expense(TimeStampedModel):
    """
    Operating business and freelance expense tracking.
    """
    class Category(models.TextChoices):
        INFRASTRUCTURE = 'INFRASTRUCTURE', 'Hosting, Servers & Cloud'
        SOFTWARE = 'SOFTWARE', 'Software & SaaS Licenses'
        MARKETING = 'MARKETING', 'Marketing & Advertising'
        CONTRACTOR = 'CONTRACTOR', 'Contractors & Freelancers'
        OFFICE = 'OFFICE', 'Hardware, Office & Equipment'
        OTHER = 'OTHER', 'Other Operating Expenses'

    workspace = models.ForeignKey(
        'workspaces.Workspace',
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Workspace'
    )
    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Logged By'
    )
    title = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Expense Title / Vendor'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description / Receipt Notes'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Amount ($)'
    )
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.INFRASTRUCTURE,
        db_index=True,
        verbose_name='Expense Category'
    )
    expense_date = models.DateField(
        verbose_name='Expense Date',
        db_index=True
    )

    class Meta:
        verbose_name = 'Business Expense'
        verbose_name_plural = 'Business Expenses'
        ordering = ['-expense_date', '-created_at']
        indexes = [
            models.Index(fields=['workspace', 'expense_date']),
            models.Index(fields=['workspace', 'category']),
        ]

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}: ${self.amount} ({self.expense_date})"

