"""
Agile Sprint Management Models & Velocity Tracking.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class SprintStatus(models.TextChoices):
    PLANNING = 'PLANNING', 'Planning'
    ACTIVE = 'ACTIVE', 'Active'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Sprint(TenantScopedModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='sprints')
    name = models.CharField(max_length=150) # e.g. "Sprint 24: Core Auth & Payment Gateway"
    goal = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=SprintStatus.choices, default=SprintStatus.PLANNING)
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    total_story_points = models.IntegerField(default=0)
    completed_story_points = models.IntegerField(default=0)
    velocity = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.key} - {self.name} ({self.status})"
