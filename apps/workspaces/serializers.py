"""
Serializers for Workspaces, Members, and Invitations.
"""
from rest_framework import serializers
from .models import Workspace, WorkspaceMember, WorkspaceInvitation, WorkspaceRole
from apps.accounts.serializers import UserSerializer

class WorkspaceMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = WorkspaceMember
        fields = ['id', 'workspace', 'user', 'user_id', 'role', 'is_active', 'joined_at']
        read_only_fields = ['id', 'workspace', 'joined_at']

class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Workspace
        fields = [
            'id', 'name', 'slug', 'logo', 'description', 'owner',
            'timezone', 'language', 'custom_domain', 'brand_color',
            'is_active', 'members_count', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'owner', 'created_at']

class WorkspaceInvitationSerializer(serializers.ModelSerializer):
    invited_by = UserSerializer(read_only=True)

    class Meta:
        model = WorkspaceInvitation
        fields = ['id', 'workspace', 'email', 'role', 'invited_by', 'token', 'status', 'expires_at', 'created_at']
        read_only_fields = ['id', 'token', 'invited_by', 'status', 'created_at']
