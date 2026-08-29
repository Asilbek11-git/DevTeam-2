from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, MilestoneViewSet, project_list_template_view, project_detail_template_view

router = DefaultRouter()
router.register(r'api/milestones', MilestoneViewSet, basename='milestones-api')
router.register(r'api', ProjectViewSet, basename='projects-api')

urlpatterns = [
    path('', project_list_template_view, name='project-list'),
    path('<uuid:pk>/', project_detail_template_view, name='project-detail'),
] + router.urls
