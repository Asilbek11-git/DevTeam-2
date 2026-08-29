"""
URL patterns for Finance & Expense Management in DevTeam.
"""
from django.urls import path
from .finance_views import (
    finance_dashboard_view, expense_list_view, expense_create_view,
    expense_edit_view, expense_delete_view
)

urlpatterns = [
    path('', finance_dashboard_view, name='finance-dashboard'),
    path('expenses/', expense_list_view, name='expense-list'),
    path('expenses/create/', expense_create_view, name='expense-create'),
    path('expenses/<int:id>/edit/', expense_edit_view, name='expense-edit'),
    path('expenses/<int:id>/delete/', expense_delete_view, name='expense-delete'),
]
