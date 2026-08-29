"""
URL patterns for Services Catalog in DevTeam.
"""
from django.urls import path
from .service_views import (
    service_list_view, service_create_view, service_edit_view,
    service_toggle_active_view, service_delete_view
)

urlpatterns = [
    path('', service_list_view, name='service-list'),
    path('create/', service_create_view, name='service-create'),
    path('<int:id>/edit/', service_edit_view, name='service-edit'),
    path('<int:id>/toggle/', service_toggle_active_view, name='service-toggle-active'),
    path('<int:id>/delete/', service_delete_view, name='service-delete'),
]
