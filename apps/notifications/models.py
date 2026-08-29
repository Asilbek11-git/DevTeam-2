"""
Notification Models supporting In-App, Email, and Webhook channels.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class NotificationType(models.TextChoices):
    TASK_ASSIGNED = 'TASK_ASSIGNED', 'Task Assigned'
    TASK_STATUS_CHANGED = 'TASK_STATUS_CHANGED', 'Task Status Changed'
    COMMENT_MENTION = 'COMMENT_MENTION', 'Mention in Comment'
    DEADLINE_APPROACHING = 'DEADLINE_APPROACHING', 'Deadline Approaching'
    DEADLINE_MISSED = 'DEADLINE_MISSED', 'Deadline Missed'
    SPRINT_STARTED = 'SPRINT_STARTED', 'Sprint Started'
    SPRINT_COMPLETED = 'SPRINT_COMPLETED', 'Sprint Completed'
    INVITATION = 'INVITATION', 'Workspace Invitation'
    PAYMENT_SUCCESS = 'PAYMENT_SUCCESS', 'Payment Successful'
    PAYMENT_FAILED = 'PAYMENT_FAILED', 'Payment Failed'
    SUBSCRIPTION_UPDATED = 'SUBSCRIPTION_UPDATED', 'Subscription Updated'

class Notification(TenantScopedModel):
    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='triggered_notifications')
    
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.TASK_ASSIGNED)
    title = models.CharField(max_length=200)
    message = models.TextField()
    action_url = models.CharField(max_length=255, blank=True)
    
    is_read = models.BooleanField(default=False, db_index=True)
    is_email_sent = models.BooleanField(default=False)
    
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.recipient.email}"
