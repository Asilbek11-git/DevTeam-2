"""
Sprint domain serializers for REST API.
"""
from rest_framework import serializers
from .models import Sprint

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'id', 'project', 'name', 'goal', 'status',
            'start_date', 'end_date', 'total_story_points',
            'completed_story_points', 'velocity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
