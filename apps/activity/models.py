"""
Audit Log & Activity Timeline Records for Compliance and History.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class ActivityLog(TenantScopedModel):
    class ActionType(models.TextChoices):
        USER_LOGIN = 'USER_LOGIN', 'User Login'
        PROJECT_CREATED = 'PROJECT_CREATED', 'Project Created'
        PROJECT_UPDATED = 'PROJECT_UPDATED', 'Project Updated'
        TASK_CREATED = 'TASK_CREATED', 'Task Created'
        TASK_UPDATED = 'TASK_UPDATED', 'Task Updated'
        TASK_DELETED = 'TASK_DELETED', 'Task Deleted'
        MEMBER_ADDED = 'MEMBER_ADDED', 'Member Added'
        MEMBER_REMOVED = 'MEMBER_REMOVED', 'Member Removed'
        ROLE_CHANGED = 'ROLE_CHANGED', 'Role Changed'
        SUBSCRIPTION_UPGRADED = 'SUBSCRIPTION_UPGRADED', 'Subscription Upgraded'
        PAYMENT_SUCCESS = 'PAYMENT_SUCCESS', 'Payment Success'
        INTEGRATION_SYNC = 'INTEGRATION_SYNC', 'Integration Synced'
        AUTOMATION_TRIGGERED = 'AUTOMATION_TRIGGERED', 'Automation Rule Triggered'

    actor = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    action = models.CharField(max_length=40, choices=ActionType.choices, db_index=True)
    entity_type = models.CharField(max_length=50) # 'Task', 'Project', 'Subscription'
    entity_id = models.CharField(max_length=64, blank=True)
    description = models.TextField()
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.action}] {self.description}"
