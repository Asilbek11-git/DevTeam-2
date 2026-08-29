"""
Project & Milestone Domain Models.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class ProjectStatus(models.TextChoices):
    PLANNING = 'PLANNING', 'Planning'
    ACTIVE = 'ACTIVE', 'Active'
    ON_HOLD = 'ON_HOLD', 'On Hold'
    COMPLETED = 'COMPLETED', 'Completed'
    ARCHIVED = 'ARCHIVED', 'Archived'

class ProjectHealth(models.TextChoices):
    ON_TRACK = 'ON_TRACK', 'On Track'
    AT_RISK = 'AT_RISK', 'At Risk'
    OFF_TRACK = 'OFF_TRACK', 'Off Track'

class Project(TenantScopedModel):
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=10, db_index=True)  # e.g., 'DEV', 'API'
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ACTIVE)
    health = models.CharField(max_length=20, choices=ProjectHealth.choices, default=ProjectHealth.ON_TRACK)
    
    start_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    
    owner = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='managed_projects')
    lead = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_projects')
    
    tech_stack = models.JSONField(default=list, blank=True)  # e.g. ["Python", "Django", "PostgreSQL", "Docker"]
    repository_url = models.URLField(blank=True)
    production_url = models.URLField(blank=True)
    staging_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='project_logos/', null=True, blank=True)
    
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    spent_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    tags = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ('workspace', 'key')
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.key}] {self.name}"

class Milestone(TenantScopedModel):
    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        DELAYED = 'DELAYED', 'Delayed'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)

    @property
    def progress(self):
        tasks = self.tasks.all()
        if not tasks.exists():
            return 0
        completed = tasks.filter(status='DONE').count()
        return int((completed / tasks.count()) * 100)

    def __str__(self):
        return f"{self.project.name} - {self.name}"
