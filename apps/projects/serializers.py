"""
Serializers for Projects and Milestones.
"""
from rest_framework import serializers
from .models import Project, Milestone
from apps.accounts.serializers import UserSerializer

class MilestoneSerializer(serializers.ModelSerializer):
    progress = serializers.IntegerField(read_only=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Milestone
        fields = ['id', 'workspace', 'project', 'name', 'description', 'deadline', 'status', 'progress', 'tasks_count', 'created_at']
        read_only_fields = ['id', 'workspace', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    lead = UserSerializer(read_only=True)
    lead_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)
    completed_tasks_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    milestones = MilestoneSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'workspace', 'name', 'key', 'description', 'status', 'health',
            'start_date', 'deadline', 'owner', 'lead', 'lead_id',
            'tech_stack', 'repository_url', 'production_url', 'staging_url',
            'logo', 'budget', 'spent_budget', 'tags', 'tasks_count',
            'completed_tasks_count', 'progress', 'milestones', 'created_at'
        ]
        read_only_fields = ['id', 'workspace', 'owner', 'created_at']

    def get_completed_tasks_count(self, obj):
        return obj.tasks.filter(status='DONE').count()

    def get_progress(self, obj):
        total = obj.tasks.count()
        if total == 0:
            return 0
        done = obj.tasks.filter(status='DONE').count()
        return int((done / total) * 100)
