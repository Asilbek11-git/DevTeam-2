"""
Task Serializers including Subtasks, Attachments, and TimeLogs.
"""
from rest_framework import serializers
from .models import Task, TaskDependency, TaskAttachment, TimeLog
from apps.accounts.serializers import UserSerializer
from .services import check_for_dependency_cycle, recalculate_task_actual_hours

class TimeLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TimeLog
        fields = ['id', 'workspace', 'task', 'user', 'description', 'start_time', 'end_time', 'duration_minutes', 'is_billable', 'created_at']
        read_only_fields = ['id', 'workspace', 'user', 'created_at']

class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = TaskAttachment
        fields = ['id', 'workspace', 'task', 'uploaded_by', 'file', 'filename', 'file_size_bytes', 'content_type', 'created_at']
        read_only_fields = ['id', 'workspace', 'uploaded_by', 'created_at']

class TaskDependencySerializer(serializers.ModelSerializer):
    predecessor_key = serializers.CharField(source='predecessor.key', read_only=True)
    successor_key = serializers.CharField(source='successor.key', read_only=True)

    class Meta:
        model = TaskDependency
        fields = ['id', 'workspace', 'predecessor', 'successor', 'predecessor_key', 'successor_key', 'dependency_type', 'created_at']
        read_only_fields = ['id', 'workspace', 'created_at']

    def validate(self, data):
        check_for_dependency_cycle(data['predecessor'].id, data['successor'].id)
        return data

class SubtaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'key', 'title', 'status', 'priority', 'assignee', 'estimated_hours', 'actual_hours']

class TaskSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    project_key = serializers.CharField(source='project.key', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    time_logs = TimeLogSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'workspace', 'project', 'project_key', 'project_name',
            'sprint', 'board_column', 'milestone', 'parent_task',
            'key', 'task_number', 'title', 'description',
            'status', 'priority', 'reporter', 'assignee', 'assignee_id',
            'due_date', 'estimated_hours', 'actual_hours', 'story_points',
            'tags', 'order', 'subtasks', 'attachments', 'time_logs', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'workspace', 'key', 'task_number', 'reporter', 'actual_hours', 'created_at', 'updated_at']
