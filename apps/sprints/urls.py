from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SprintViewSet, sprint_list_template_view

router = DefaultRouter()
router.register(r'api', SprintViewSet, basename='sprints-api')

urlpatterns = [
    path('', sprint_list_template_view, name='sprints-list'),
] + router.urls
