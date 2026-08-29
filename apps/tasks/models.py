"""
Task, Subtask, Dependency Graph, Attachment & Time Tracking Models.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class TaskStatus(models.TextChoices):
    BACKLOG = 'BACKLOG', 'Backlog'
    TODO = 'TODO', 'To Do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    CODE_REVIEW = 'CODE_REVIEW', 'Code Review'
    QA = 'QA', 'QA'
    DONE = 'DONE', 'Done'
    CANCELLED = 'CANCELLED', 'Cancelled'

class TaskPriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'

class Task(TenantScopedModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    sprint = models.ForeignKey('sprints.Sprint', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    board_column = models.ForeignKey('boards.BoardColumn', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    milestone = models.ForeignKey('projects.Milestone', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')

    task_number = models.PositiveIntegerField(default=1)
    key = models.CharField(max_length=20, db_index=True) # e.g. "DEV-101"
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.TODO, db_index=True)
    priority = models.CharField(max_length=20, choices=TaskPriority.choices, default=TaskPriority.MEDIUM, db_index=True)

    reporter = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='reported_tasks')
    assignee = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    story_points = models.PositiveIntegerField(default=1)
    
    tags = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['workspace', 'project', 'status']),
            models.Index(fields=['key']),
        ]

    def save(self, *args, **kwargs):
        if not self.key and self.project:
            last_num = Task.objects.filter(project=self.project).count() + 1
            self.task_number = last_num
            self.key = f"{self.project.key}-{last_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.key}] {self.title}"

class TaskDependency(TenantScopedModel):
    class DependencyType(models.TextChoices):
        BLOCKS = 'BLOCKS', 'Blocks'
        RELATES_TO = 'RELATES_TO', 'Relates to'

    predecessor = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='outgoing_dependencies')
    successor = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='incoming_dependencies')
    dependency_type = models.CharField(max_length=20, choices=DependencyType.choices, default=DependencyType.BLOCKS)

    class Meta:
        unique_together = ('predecessor', 'successor')

    def __str__(self):
        return f"{self.predecessor.key} {self.dependency_type} {self.successor.key}"

class TimeLog(TenantScopedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_logs')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='time_logs')
    description = models.CharField(max_length=255, blank=True)
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    is_billable = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user.username} logged {self.duration_minutes}m on {self.task.key}"

class TaskAttachment(TenantScopedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size_bytes = models.PositiveBigIntegerField(default=0)
    content_type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.filename} ({self.task.key})"
