"""
Kanban Board & Board Column Models.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class Board(TenantScopedModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='boards')
    name = models.CharField(max_length=150, default='Main Kanban Board')
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

class BoardColumn(TenantScopedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=100) # e.g. Backlog, To Do, In Progress, Code Review, QA, Done
    status_mapping = models.CharField(max_length=30, default='TODO')
    order = models.PositiveIntegerField(default=0)
    wip_limit = models.PositiveIntegerField(default=0) # 0 means unlimited
    color = models.CharField(max_length=20, default='#64748B')

    class Meta:
        ordering = ['order']
        unique_together = ('board', 'order')

    def __str__(self):
        return f"{self.board.name} - {self.title} (Pos: {self.order})"
