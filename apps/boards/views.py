"""
Kanban Board views and template rendering.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.core.permissions import IsDeveloperOrHigher
from .models import Board, BoardColumn
from .serializers import BoardSerializer, BoardColumnSerializer
from apps.tasks.models import Task, TaskStatus

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsDeveloperOrHigher]

    def get_queryset(self):
        workspace = getattr(self.request, 'current_workspace', None)
        qs = Board.objects.filter(workspace__members__user=self.request.user)
        if workspace:
            qs = qs.filter(workspace=workspace)
        return qs.prefetch_related('columns').distinct()

    def perform_create(self, serializer):
        workspace = getattr(self.request, 'current_workspace', None)
        serializer.save(workspace=workspace)

@login_required(login_url='login')
def board_template_view(request, project_id=None):
    """Render interactive Kanban Board template."""
    workspace = getattr(request, 'current_workspace', None)
    tasks = []
    if workspace:
        tasks = Task.objects.filter(workspace=workspace).select_related('project', 'assignee')
        if project_id:
            tasks = tasks.filter(project_id=project_id)
            
    columns = [
        {'status': 'BACKLOG', 'title': 'Backlog', 'color': '#94A3B8'},
        {'status': 'TODO', 'title': 'To Do', 'color': '#3B82F6'},
        {'status': 'IN_PROGRESS', 'title': 'In Progress', 'color': '#EAB308'},
        {'status': 'CODE_REVIEW', 'title': 'Code Review', 'color': '#A855F7'},
        {'status': 'QA', 'title': 'QA & Testing', 'color': '#EC4899'},
        {'status': 'DONE', 'title': 'Done', 'color': '#10B981'},
    ]
    
    # Group tasks by column
    columns_with_tasks = []
    for col in columns:
        col_tasks = [t for t in tasks if t.status == col['status']]
        columns_with_tasks.append({
            **col,
            'tasks': col_tasks,
            'count': len(col_tasks)
        })

    return render(request, 'tasks/board.html', {
        'columns': columns_with_tasks,
        'page_title': 'Kanban Board'
    })
