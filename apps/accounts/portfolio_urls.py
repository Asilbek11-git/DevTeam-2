"""
URL patterns for Portfolio Management & Public Showcase in DevTeam.
"""
from django.urls import path
from .portfolio_views import (
    public_portfolio_list_view, public_portfolio_detail_view,
    portfolio_manage_list_view, portfolio_create_view,
    portfolio_edit_view, portfolio_delete_view
)

urlpatterns = [
    # Public Showcase
    path('', public_portfolio_list_view, name='public-portfolio'),
    
    # Private Management
    path('manage/', portfolio_manage_list_view, name='portfolio-manage'),
    path('manage/create/', portfolio_create_view, name='portfolio-create'),
    path('manage/<int:id>/edit/', portfolio_edit_view, name='portfolio-edit'),
    path('manage/<int:id>/delete/', portfolio_delete_view, name='portfolio-delete'),
    
    # Public Detail (keep at end to avoid slug collisions with manage)
    path('<slug:slug>/', public_portfolio_detail_view, name='public-portfolio-detail'),
]
