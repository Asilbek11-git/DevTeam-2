"""
URL patterns for Lead CRM & Pipeline in DevTeam.
"""
from django.urls import path
from .crm_views import (
    lead_list_view, lead_create_view, lead_detail_view,
    lead_edit_view, lead_update_status_view, lead_convert_view
)

urlpatterns = [
    path('', lead_list_view, name='lead-list'),
    path('create/', lead_create_view, name='lead-create'),
    path('<str:id>/', lead_detail_view, name='lead-detail'),
    path('<str:id>/edit/', lead_edit_view, name='lead-edit'),
    path('<str:id>/status/', lead_update_status_view, name='lead-update-status'),
    path('<str:id>/status-update/', lead_update_status_view, name='lead-status-update'),
    path('<str:id>/convert/', lead_convert_view, name='lead-convert'),
]
