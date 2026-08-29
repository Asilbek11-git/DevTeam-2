"""
Automation Rule Engine Models (WHEN / THEN workflows).
"""
from django.db import models
from apps.core.models import TenantScopedModel

class AutomationTrigger(models.TextChoices):
    TASK_STATUS_CHANGED = 'TASK_STATUS_CHANGED', 'When task status changes'
    TASK_CREATED = 'TASK_CREATED', 'When a new task is created'
    TASK_OVERDUE = 'TASK_OVERDUE', 'When a task becomes overdue'
    PR_OPENED = 'PR_OPENED', 'When a Pull Request is opened'
    PR_MERGED = 'PR_MERGED', 'When a Pull Request is merged'

class AutomationAction(models.TextChoices):
    MOVE_TASK_TO = 'MOVE_TASK_TO', 'Move task to status'
    ASSIGN_TO_USER = 'ASSIGN_TO_USER', 'Assign to user'
    NOTIFY_ROLE = 'NOTIFY_ROLE', 'Notify role (e.g. Lead Developer, PM)'
    SEND_WEBHOOK = 'SEND_WEBHOOK', 'Trigger external webhook'

class AutomationRule(TenantScopedModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True, related_name='automation_rules')
    name = models.CharField(max_length=200) # e.g. "Move to QA on PR Merge"
    description = models.TextField(blank=True)
    
    trigger = models.CharField(max_length=40, choices=AutomationTrigger.choices)
    trigger_config = models.JSONField(default=dict, blank=True) # e.g. {"status": "CODE_REVIEW"}
    
    action = models.CharField(max_length=40, choices=AutomationAction.choices)
    action_config = models.JSONField(default=dict, blank=True) # e.g. {"target_status": "QA", "notify_role": "LEAD_DEVELOPER"}
    
    is_active = models.BooleanField(default=True)
    execution_count = models.PositiveIntegerField(default=0)
    last_triggered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.trigger} -> {self.action})"
