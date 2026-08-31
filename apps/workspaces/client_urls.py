"""
URL patterns for Client CRM in DevTeam.
"""
from django.urls import path
from .crm_views import (
    client_list_view, client_create_view, client_detail_view,
    client_edit_view, client_archive_view, client_restore_view
)

urlpatterns = [
    path('', client_list_view, name='client-list'),
    path('create/', client_create_view, name='client-create'),
    path('<str:id>/', client_detail_view, name='client-detail'),
    path('<str:id>/edit/', client_edit_view, name='client-edit'),
    path('<str:id>/archive/', client_archive_view, name='client-archive'),
    path('<str:id>/restore/', client_restore_view, name='client-restore'),
]
