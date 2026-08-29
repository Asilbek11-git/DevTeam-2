from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, board_template_view

router = DefaultRouter()
router.register(r'api', BoardViewSet, basename='boards-api')

urlpatterns = [
    path('', board_template_view, name='kanban-board'),
    path('project/<uuid:project_id>/', board_template_view, name='project-kanban-board'),
] + router.urls
