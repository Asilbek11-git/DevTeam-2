"""
Multi-Tenant Workspace Models, Membership & RBAC Roles.
"""
from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
import uuid

class Workspace(TimeStampedModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, db_index=True)
    logo = models.ImageField(upload_to='workspace_logos/', null=True, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='owned_workspaces')
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    
    # Custom Enterprise White-Label settings
    custom_domain = models.CharField(max_length=255, blank=True, null=True)
    brand_color = models.CharField(max_length=20, default='#3B82F6')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or 'workspace'
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.slug})"

    @property
    def projects(self):
        from apps.projects.models import Project
        return Project.objects.filter(workspace=self)

    @property
    def tasks(self):
        from apps.tasks.models import Task
        return Task.objects.filter(workspace=self)

    @property
    def sprints(self):
        from apps.sprints.models import Sprint
        return Sprint.objects.filter(workspace=self)

class WorkspaceRole(models.TextChoices):
    OWNER = 'OWNER', 'Workspace Owner'
    ADMIN = 'ADMIN', 'Administrator'
    PROJECT_MANAGER = 'PROJECT_MANAGER', 'Project Manager'
    LEAD_DEVELOPER = 'LEAD_DEVELOPER', 'Lead Developer'
    DEVELOPER = 'DEVELOPER', 'Developer'
    CLIENT = 'CLIENT', 'Client'
    VIEWER = 'VIEWER', 'Viewer'

class WorkspaceMember(TimeStampedModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='workspace_memberships')
    role = models.CharField(max_length=30, choices=WorkspaceRole.choices, default=WorkspaceRole.DEVELOPER)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('workspace', 'user')
        indexes = [
            models.Index(fields=['workspace', 'user']),
            models.Index(fields=['workspace', 'role']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.role} in {self.workspace.name}"

class WorkspaceInvitation(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        EXPIRED = 'EXPIRED', 'Expired'

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField(db_index=True)
    role = models.CharField(max_length=30, choices=WorkspaceRole.choices, default=WorkspaceRole.DEVELOPER)
    invited_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='sent_invitations')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Invite to {self.email} for {self.workspace.name} ({self.status})"

class Client(TimeStampedModel):
    """
    Client profile model for freelance and business management.
    """
    class Status(models.TextChoices):
        LEAD = 'LEAD', 'Lead'
        ACTIVE = 'ACTIVE', 'Active Client'
        INACTIVE = 'INACTIVE', 'Inactive Client'
        ARCHIVED = 'ARCHIVED', 'Archived'

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Workspace'
    )
    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='managed_clients',
        verbose_name='Account Owner / Manager'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_profiles',
        verbose_name='Client Portal User',
        help_text='Optional registered user account for client portal access'
    )
    full_name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Contact Full Name'
    )
    company = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Company / Organization'
    )
    email = models.EmailField(
        db_index=True,
        verbose_name='Contact Email'
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Phone Number'
    )
    website = models.URLField(
        blank=True,
        verbose_name='Company Website'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
        verbose_name='Client Status'
    )
    rating = models.PositiveSmallIntegerField(
        default=5,
        verbose_name='Client Rating (1-5)',
        help_text='Internal client score from 1 to 5'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Internal Notes & History'
    )

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['workspace', 'status']),
            models.Index(fields=['workspace', 'email']),
        ]

    def __str__(self):
        if self.company:
            return f"{self.full_name} ({self.company})"
        return f"{self.full_name} <{self.email}>"

class Lead(TimeStampedModel):
    """
    Freelance/business lead & order pipeline tracking model.
    """
    class Status(models.TextChoices):
        NEW = 'NEW', 'New Lead'
        CONTACTED = 'CONTACTED', 'Contacted'
        NEGOTIATION = 'NEGOTIATION', 'In Negotiation'
        ACCEPTED = 'ACCEPTED', 'Accepted / Won'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled / Lost'

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='leads',
        verbose_name='Workspace'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Associated Client'
    )
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Lead / Deal Title'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Scope & Requirements'
    )
    service = models.ForeignKey(
        'billing.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Requested Service'
    )
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Estimated Budget ($)'
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name='Target Deadline'
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
        verbose_name='Pipeline Stage'
    )
    probability = models.PositiveSmallIntegerField(
        default=50,
        verbose_name='Win Probability (%)',
        help_text='Estimated close probability percentage (0-100)'
    )
    expected_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Expected Revenue ($)'
    )
    source = models.CharField(
        max_length=100,
        blank=True,
        default='Direct Inquiry',
        verbose_name='Lead Source',
        help_text='e.g. Upwork, LinkedIn, Telegram, Referral, Organic'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Negotiation Notes'
    )

    class Meta:
        verbose_name = 'Lead / Order'
        verbose_name_plural = 'Leads & Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['workspace', 'status']),
            models.Index(fields=['workspace', 'deadline']),
        ]

    def save(self, *args, **kwargs):
        if self.budget and self.probability is not None:
            self.expected_revenue = (self.budget * self.probability) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title} (${self.budget})"

