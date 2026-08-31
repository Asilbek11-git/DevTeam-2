"""
Task Management, Kanban Board Reordering, and Time Tracking API Views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.utils import timezone

from apps.core.responses import success_response, error_response
from apps.core.permissions import IsDeveloperOrHigher
from .models import Task, TaskDependency, TaskAttachment, TimeLog
from .serializers import (
    TaskSerializer, TaskDependencySerializer, TaskAttachmentSerializer,
    TimeLogSerializer
)
from .services import recalculate_task_actual_hours

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsDeveloperOrHigher]

    def get_queryset(self):
        workspace = getattr(self.request, 'current_workspace', None)
        qs = Task.objects.filter(
            workspace__members__user=self.request.user,
            parent_task__isnull=True # Top-level tasks
        )
        if workspace:
            qs = qs.filter(workspace=workspace)
        
        # Filtering by project, sprint, status, priority, assignee
        project_id = self.request.query_params.get('project')
        sprint_id = self.request.query_params.get('sprint')
        status_param = self.request.query_params.get('status')
        assignee_id = self.request.query_params.get('assignee')
        search_param = self.request.query_params.get('search')

        if project_id:
            qs = qs.filter(project_id=project_id)
        if sprint_id:
            qs = qs.filter(sprint_id=sprint_id)
        if status_param:
            qs = qs.filter(status=status_param)
        if assignee_id:
            qs = qs.filter(assignee_id=assignee_id)
        if search_param:
            qs = qs.filter(title__icontains=search_param)

        return qs.select_related('project', 'assignee', 'reporter', 'sprint').prefetch_related('subtasks', 'attachments').distinct()

    def perform_create(self, serializer):
        workspace = getattr(self.request, 'current_workspace', None)
        if not workspace:
            project = serializer.validated_data.get('project')
            workspace = project.workspace if project else None
        serializer.save(workspace=workspace, reporter=self.request.user)

    @extend_schema(tags=['Tasks'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(data=serializer.data, message="Task created successfully", status_code=status.HTTP_201_CREATED)

    @extend_schema(tags=['Tasks'])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(data=serializer.data, message="Task updated successfully")

    @extend_schema(tags=['Tasks'])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(data=None, message="Task deleted successfully", status_code=status.HTTP_204_NO_CONTENT)

    @extend_schema(tags=['Tasks'])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Tasks retrieved")

    @extend_schema(tags=['Tasks'])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Task details retrieved")

    @extend_schema(tags=['Tasks'])
    @action(detail=True, methods=['post'])
    def log_time(self, request, pk=None):
        task = self.get_object()
        duration_minutes = int(request.data.get('duration_minutes', 0))
        description = request.data.get('description', '')
        is_billable = request.data.get('is_billable', True)

        if duration_minutes <= 0:
            return error_response(message="Duration in minutes must be greater than 0")

        log = TimeLog.objects.create(
            workspace=task.workspace,
            task=task,
            user=request.user,
            start_time=timezone.now(),
            duration_minutes=duration_minutes,
            description=description,
            is_billable=is_billable
        )

        actual_hours = recalculate_task_actual_hours(task.id)

        return success_response(
            data={"time_log": TimeLogSerializer(log).data, "total_actual_hours": actual_hours},
            message=f"Logged {duration_minutes} minutes successfully",
            status_code=status.HTTP_201_CREATED
        )

    @extend_schema(tags=['Tasks'])
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        new_order = request.data.get('order', task.order)

        if new_status:
            task.status = new_status
        task.order = new_order
        task.save(update_fields=['status', 'order', 'updated_at'])

        # Trigger Automation Rules asynchronously
        from apps.automation.services import execute_task_automations
        execute_task_automations(task, event_type='status_changed')

        return success_response(
            data=TaskSerializer(task).data,
            message=f"Task status updated to {new_status}"
        )

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def task_list_template_view(request):
    """Render task table and list view."""
    workspace = getattr(request, 'current_workspace', None)
    tasks = []
    if workspace:
        tasks = Task.objects.filter(workspace=workspace).select_related('project', 'assignee', 'sprint')
    return render(request, 'tasks/list.html', {
        'tasks': tasks,
        'page_title': 'All Tasks'
    })

@login_required(login_url='login')
def task_detail_template_view(request, pk):
    """Render detailed view of a single task with subtasks, time logs, and comments."""
    workspace = getattr(request, 'current_workspace', None)
    task = get_object_or_404(Task, pk=pk, workspace=workspace)
    subtasks = task.subtasks.all()
    time_logs = task.time_logs.select_related('user').all()
    attachments = task.attachments.select_related('uploaded_by').all()
    return render(request, 'tasks/detail.html', {
        'task': task,
        'subtasks': subtasks,
        'time_logs': time_logs,
        'attachments': attachments,
        'page_title': f"{task.key} - {task.title}"
    })

