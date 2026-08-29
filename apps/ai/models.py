"""
AI Usage Tracking & Prompt Analytics Models.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class AIUsageLog(TenantScopedModel):
    class ActionType(models.TextChoices):
        TASK_DESCRIPTION = 'TASK_DESCRIPTION', 'Task Description Generation'
        IMPROVE_DESCRIPTION = 'IMPROVE_DESCRIPTION', 'Improve Task Description'
        SUMMARIZE_PROJECT = 'SUMMARIZE_PROJECT', 'Project Summary'
        SUMMARIZE_SPRINT = 'SUMMARIZE_SPRINT', 'Sprint Summary & Retrospective'
        RELEASE_NOTES = 'RELEASE_NOTES', 'Release Notes Generation'
        ESTIMATE_COMPLEXITY = 'ESTIMATE_COMPLEXITY', 'Estimate Task Complexity'
        ANALYZE_OVERDUE = 'ANALYZE_OVERDUE', 'Analyze Overdue Tasks'

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='ai_usage_logs')
    action_type = models.CharField(max_length=40, choices=ActionType.choices)
    prompt_tokens = models.PositiveIntegerField(default=0)
    completion_tokens = models.PositiveIntegerField(default=0)
    model_name = models.CharField(max_length=50, default='gemini-2.5-flash')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.action_type} ({self.created_at.strftime('%Y-%m-%d')})"
