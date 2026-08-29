"""
Workspace Management API Views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema

from apps.core.responses import success_response, error_response
from apps.core.permissions import IsWorkspaceOwner, IsWorkspaceMember
from .models import Workspace, WorkspaceMember, WorkspaceInvitation, WorkspaceRole
from .serializers import WorkspaceSerializer, WorkspaceMemberSerializer, WorkspaceInvitationSerializer

class WorkspaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Multi-tenant isolation: Only return workspaces user belongs to
        return Workspace.objects.filter(
            members__user=self.request.user,
            members__is_active=True
        ).distinct()

    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        # Automatically make creator the Workspace Owner
        WorkspaceMember.objects.create(
            workspace=workspace,
            user=self.request.user,
            role=WorkspaceRole.OWNER
        )

    @extend_schema(tags=['Workspaces'])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Workspaces retrieved")

    @extend_schema(tags=['Workspaces'])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Workspace details retrieved")

    @extend_schema(responses={200: WorkspaceMemberSerializer(many=True)}, tags=['Workspaces'])
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        workspace = self.get_object()
        members = workspace.members.filter(is_active=True).select_related('user')
        serializer = WorkspaceMemberSerializer(members, many=True)
        return success_response(data=serializer.data, message="Workspace members retrieved")

    @extend_schema(request=WorkspaceInvitationSerializer, responses={201: WorkspaceInvitationSerializer}, tags=['Workspaces'])
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsWorkspaceOwner])
    def invite(self, request, pk=None):
        workspace = self.get_object()
        email = request.data.get('email')
        role = request.data.get('role', WorkspaceRole.DEVELOPER)

        if not email:
            return error_response(message="Email address is required")

        # Create invitation
        invitation = WorkspaceInvitation.objects.create(
            workspace=workspace,
            email=email,
            role=role,
            invited_by=request.user,
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        return success_response(
            data=WorkspaceInvitationSerializer(invitation).data,
            message=f"Invitation sent to {email}",
            status_code=status.HTTP_201_CREATED
        )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def switch_workspace_view(request, workspace_id):
    """Switch active tenant workspace in user session."""
    membership = WorkspaceMember.objects.filter(
        workspace_id=workspace_id,
        user=request.user,
        is_active=True
    ).first()
    if membership:
        request.session['active_workspace_id'] = str(workspace_id)
        messages.success(request, f"Switched to workspace: {membership.workspace.name}")
    else:
        messages.error(request, "Workspace not found or unauthorized.")
    return redirect('dashboard')

@login_required(login_url='login')
def workspace_list_template_view(request):
    """List all workspaces user belongs to."""
    memberships = WorkspaceMember.objects.filter(user=request.user, is_active=True).select_related('workspace')
    return render(request, 'workspaces/list.html', {
        'memberships': memberships,
        'page_title': 'Workspaces'
    })

