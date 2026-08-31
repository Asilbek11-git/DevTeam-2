"""
URL patterns for DevTeam Core templates and views.
"""
from django.urls import path
from . import views
from apps.accounts.profile_views import profile_dispatch_view, owner_profile_view, user_profile_view, client_profile_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('owner/dashboard/', views.owner_dashboard_view, name='owner-dashboard'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('team/', views.team_view, name='team'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/', profile_dispatch_view, name='profile'),
    path('settings/profile/', profile_dispatch_view, name='owner-profile'),
    path('profile/owner/', owner_profile_view, name='owner-profile-direct'),
    path('profile/developer/', user_profile_view, name='developer-profile'),
    path('profile/client/', client_profile_view, name='client-profile'),
    path('superadmin/', views.superadmin_view, name='superadmin'),
    path('ai-studio/', views.ai_studio_view, name='ai-studio'),
    path('ai/studio/', views.ai_studio_view, name='ai-studio-nested'),
    path('affiliates/', views.affiliates_view, name='affiliates'),
]


