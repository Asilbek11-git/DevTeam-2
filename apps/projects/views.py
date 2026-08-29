"""
Project Management Views with Multi-Tenant Scoping.
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from apps.core.responses import success_response, error_response
from apps.core.permissions import IsDeveloperOrHigher, IsProjectManagerOrHigher
from .models import Project, Milestone
from .serializers import ProjectSerializer, MilestoneSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsDeveloperOrHigher]

    def get_queryset(self):
        # Tenant isolation
        workspace = getattr(self.request, 'current_workspace', None)
        qs = Project.objects.filter(
            workspace__members__user=self.request.user,
            workspace__members__is_active=True
        )
        if workspace:
            qs = qs.filter(workspace=workspace)
        return qs.select_related('owner', 'lead', 'workspace').distinct()

    def perform_create(self, serializer):
        workspace = getattr(self.request, 'current_workspace', None)
        if not workspace:
            from apps.workspaces.models import WorkspaceMember
            membership = WorkspaceMember.objects.filter(user=self.request.user, is_active=True).first()
            if not membership:
                raise ValueError("No active workspace found")
            workspace = membership.workspace
        serializer.save(workspace=workspace, owner=self.request.user)

    @extend_schema(tags=['Projects'])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Projects retrieved")

    @extend_schema(tags=['Projects'])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Project details retrieved")

class MilestoneViewSet(viewsets.ModelViewSet):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated, IsProjectManagerOrHigher]

    def get_queryset(self):
        workspace = getattr(self.request, 'current_workspace', None)
        qs = Milestone.objects.filter(
            workspace__members__user=self.request.user
        )
        if workspace:
            qs = qs.filter(workspace=workspace)
        return qs.distinct()

    def perform_create(self, serializer):
        workspace = getattr(self.request, 'current_workspace', None)
        serializer.save(workspace=workspace)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def project_list_template_view(request):
    """Render projects list template."""
    workspace = getattr(request, 'current_workspace', None)
    projects = []
    if workspace:
        projects = Project.objects.filter(workspace=workspace).select_related('lead', 'owner')
    return render(request, 'projects/list.html', {
        'projects': projects,
        'page_title': 'Projects'
    })

@login_required(login_url='login')
def project_detail_template_view(request, pk):
    """Render single project detail view with milestones and tasks."""
    workspace = getattr(request, 'current_workspace', None)
    project = get_object_or_404(Project, pk=pk, workspace=workspace)
    milestones = project.milestones.all()
    tasks = project.tasks.select_related('assignee', 'sprint').all()[:20]
    return render(request, 'projects/detail.html', {
        'project': project,
        'milestones': milestones,
        'tasks': tasks,
        'page_title': f"{project.name} ({project.key})"
    })

