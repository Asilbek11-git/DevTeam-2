"""
Authentication & Profile API Views.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.core.responses import success_response, error_response
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    ChangePasswordSerializer, UserSessionSerializer
)
from .models import User, UserSession

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: UserSerializer}, tags=['Authentication'])
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return success_response(
                data={
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                },
                message="Account successfully registered.",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(message="Registration validation failed", errors=serializer.errors)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: UserSerializer}, tags=['Authentication'])
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.filter(email=email).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    return error_response(message="Account is disabled", status_code=status.HTTP_403_FORBIDDEN)
                
                refresh = RefreshToken.for_user(user)
                
                # Record session log
                UserSession.objects.create(
                    user=user,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
                )
                
                return success_response(
                    data={
                        "user": UserSerializer(user).data,
                        "tokens": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    },
                    message="Login successful"
                )
            return error_response(message="Invalid email or password credentials", status_code=status.HTTP_401_UNAUTHORIZED)
        return error_response(message="Invalid input", errors=serializer.errors)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer}, tags=['Accounts'])
    def get(self, request):
        return success_response(data=UserSerializer(request.user).data, message="Profile retrieved")

    @extend_schema(request=UserSerializer, responses={200: UserSerializer}, tags=['Accounts'])
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Profile updated successfully")
        return error_response(message="Validation failed", errors=serializer.errors)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer, tags=['Accounts'])
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(serializer.validated_data['old_password']):
                return error_response(message="Current password is incorrect")
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return success_response(message="Password successfully changed")
        return error_response(errors=serializer.errors)

class ActiveSessionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSessionSerializer(many=True)}, tags=['Accounts'])
    def get(self, request):
        sessions = UserSession.objects.filter(user=request.user, is_active=True).order_by('-last_activity')
        return success_response(data=UserSessionSerializer(sessions, many=True).data)

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages

def login_template_view(request):
    """Render and handle web login form."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password) or User.objects.filter(email=email).first()
        if user and user.check_password(password):
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
        messages.error(request, "Invalid email or password credentials.")
    return render(request, 'auth/login.html')

def register_template_view(request):
    """Render and handle web register form."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip() or email.split('@')[0]
        password = request.POST.get('password', '')
        workspace_name = request.POST.get('workspace_name', 'My Workspace').strip()

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            from apps.workspaces.models import Workspace, WorkspaceMember, WorkspaceRole
            workspace = Workspace.objects.create(name=workspace_name, owner=user)
            WorkspaceMember.objects.create(workspace=workspace, user=user, role=WorkspaceRole.OWNER)
            auth_login(request, user)
            messages.success(request, f"Welcome to DevTeam! Your workspace '{workspace_name}' is ready.")
            return redirect('dashboard')
    return render(request, 'auth/register.html')

def logout_template_view(request):
    """Handle web logout."""
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

