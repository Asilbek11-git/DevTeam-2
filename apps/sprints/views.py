"""
Sprint views supporting both REST API and Django Templates.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from drf_spectacular.utils import extend_schema

from apps.core.responses import success_response
from apps.core.permissions import IsDeveloperOrHigher
from .models import Sprint
from .serializers import SprintSerializer

class SprintViewSet(viewsets.ModelViewSet):
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, IsDeveloperOrHigher]

    def get_queryset(self):
        workspace = getattr(self.request, 'current_workspace', None)
        qs = Sprint.objects.filter(workspace__members__user=self.request.user)
        if workspace:
            qs = qs.filter(workspace=workspace)
        return qs.select_related('project').distinct()

    def perform_create(self, serializer):
        workspace = getattr(self.request, 'current_workspace', None)
        serializer.save(workspace=workspace)

@login_required(login_url='login')
def sprint_list_template_view(request):
    """Render sprints list Django template."""
    workspace = getattr(request, 'current_workspace', None)
    sprints = []
    if workspace:
        sprints = Sprint.objects.filter(workspace=workspace).select_related('project')
    return render(request, 'sprints/list.html', {
        'sprints': sprints,
        'page_title': 'Agile Sprints & Velocity'
    })
