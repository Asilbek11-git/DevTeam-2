from django.contrib import admin
from .models import Task, TaskDependency, TimeLog, TaskAttachment

class TaskAttachmentInline(admin.TabularInline):
    model = TaskAttachment
    extra = 0

class TimeLogInline(admin.TabularInline):
    model = TimeLog
    extra = 0

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('key', 'title', 'project', 'workspace', 'status', 'priority', 'assignee', 'due_date', 'story_points')
    list_filter = ('status', 'priority', 'project', 'workspace')
    search_fields = ('key', 'title', 'description')
    inlines = [TaskAttachmentInline, TimeLogInline]

@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ('predecessor', 'dependency_type', 'successor', 'workspace')
    list_filter = ('dependency_type', 'workspace')
    search_fields = ('predecessor__key', 'successor__key')

@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'duration_minutes', 'is_billable', 'start_time', 'end_time')
    list_filter = ('is_billable', 'user')
    search_fields = ('task__key', 'user__email', 'description')

@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'task', 'uploaded_by', 'file_size_bytes', 'created_at')
    search_fields = ('filename', 'task__key', 'uploaded_by__email')
