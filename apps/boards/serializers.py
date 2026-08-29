"""
Kanban Board & Column Serializers.
"""
from rest_framework import serializers
from .models import Board, BoardColumn

class BoardColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardColumn
        fields = ['id', 'board', 'title', 'status_mapping', 'order', 'wip_limit', 'color']

class BoardSerializer(serializers.ModelSerializer):
    columns = BoardColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'project', 'name', 'description', 'is_default', 'columns', 'created_at']
