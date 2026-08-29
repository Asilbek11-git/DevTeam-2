from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, ProfileView, ChangePasswordView, ActiveSessionsView,
    login_template_view, register_template_view, logout_template_view
)
from .profile_views import owner_profile_view

urlpatterns = [
    # Web Authentication Routes (Django Templates)
    path('login/', login_template_view, name='login'),
    path('register/', register_template_view, name='register'),
    path('logout/', logout_template_view, name='logout'),
    path('profile/', owner_profile_view, name='user-profile'),
    path('profile/owner/', owner_profile_view, name='owner-profile-direct'),


    # REST API Token & Profile Endpoints
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', ProfileView.as_view(), name='api-profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='api-change-password'),
    path('api/sessions/', ActiveSessionsView.as_view(), name='api-sessions'),
]
