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
    path('<int:id>/', client_detail_view, name='client-detail'),
    path('<int:id>/edit/', client_edit_view, name='client-edit'),
    path('<int:id>/archive/', client_archive_view, name='client-archive'),
    path('<int:id>/restore/', client_restore_view, name='client-restore'),
]
