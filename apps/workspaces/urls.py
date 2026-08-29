from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet, workspace_list_template_view, switch_workspace_view

router = DefaultRouter()
router.register(r'api', WorkspaceViewSet, basename='workspaces-api')

urlpatterns = [
    path('', workspace_list_template_view, name='workspace-list'),
    path('switch/<uuid:workspace_id>/', switch_workspace_view, name='switch-workspace'),
] + router.urls
