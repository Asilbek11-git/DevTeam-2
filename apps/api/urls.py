"""
Unified REST API v1 Routing Configuration for DevTeam SaaS.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from apps.core.responses import success_response
from apps.reports.services import ReportService
from apps.ai.services import AIService
from drf_spectacular.utils import extend_schema

from apps.accounts.views import (
    RegisterView, LoginView, ProfileView, ChangePasswordView, ActiveSessionsView
)
from apps.workspaces.views import WorkspaceViewSet
from apps.projects.views import ProjectViewSet, MilestoneViewSet
from apps.tasks.views import TaskViewSet
from apps.sprints.views import SprintViewSet
from apps.boards.views import BoardViewSet
from apps.billing.views import PlanViewSet, SubscriptionViewSet

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(tags=['Health & System'])
    def get(self, request):
        return success_response(
            data={"status": "healthy", "service": "DevTeam SaaS", "version": "1.0.0"},
            message="DevTeam service is operational"
        )

class AIHelperView(APIView):
    @extend_schema(tags=['AI Features'])
    def post(self, request):
        action = request.data.get('action', 'generate_task_description')
        title = request.data.get('title', '')
        context = request.data.get('context', '')
        
        if action == 'estimate_complexity':
            data = AIService.estimate_complexity(title, context)
        else:
            description = AIService.generate_task_description(title, context, request.user, getattr(request, 'current_workspace', None))
            data = {"description": description}

        return success_response(data=data, message="AI generation completed")

class AnalyticsSummaryView(APIView):
    @extend_schema(tags=['Reports & Analytics'])
    def get(self, request):
        workspace = getattr(request, 'current_workspace', None)
        if workspace:
            data = ReportService.get_workspace_dashboard_metrics(workspace)
        else:
            data = ReportService.get_superadmin_saas_metrics()
        return success_response(data=data, message="Metrics retrieved")

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='api-workspaces')
router.register(r'projects', ProjectViewSet, basename='api-projects')
router.register(r'milestones', MilestoneViewSet, basename='api-milestones')
router.register(r'tasks', TaskViewSet, basename='api-tasks')
router.register(r'sprints', SprintViewSet, basename='api-sprints')
router.register(r'boards', BoardViewSet, basename='api-boards')
router.register(r'plans', PlanViewSet, basename='api-plans')
router.register(r'subscriptions', SubscriptionViewSet, basename='api-subscriptions')

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='api-health'),
    path('ai/generate/', AIHelperView.as_view(), name='api-ai-generate'),
    path('analytics/summary/', AnalyticsSummaryView.as_view(), name='api-analytics'),
    
    # Authentication Endpoints
    path('auth/register/', RegisterView.as_view(), name='api-auth-register'),
    path('auth/login/', LoginView.as_view(), name='api-auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('auth/profile/', ProfileView.as_view(), name='api-auth-profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='api-change-password'),
    path('auth/sessions/', ActiveSessionsView.as_view(), name='api-active-sessions'),
] + router.urls

