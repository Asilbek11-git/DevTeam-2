"""
Task Comment & User Mentions Models.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class Comment(TenantScopedModel):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='task_comments')
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    mentions = models.ManyToManyField('accounts.User', blank=True, related_name='mentioned_in_comments')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.key}"
