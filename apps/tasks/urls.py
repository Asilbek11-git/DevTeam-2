from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, task_list_template_view, task_detail_template_view

router = DefaultRouter()
router.register(r'api', TaskViewSet, basename='tasks-api')

urlpatterns = [
    path('', task_list_template_view, name='task-list'),
    path('<uuid:pk>/', task_detail_template_view, name='task-detail'),
] + router.urls
