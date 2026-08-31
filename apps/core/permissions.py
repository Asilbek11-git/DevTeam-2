"""
Custom DRF Permissions & RBAC Enforcement.
Roles:
- SuperAdmin
- Workspace Owner
- Project Manager
- Lead Developer
- Developer
- Client
- Viewer
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or getattr(request.user, 'role', '') == 'SUPERADMIN'))

class IsWorkspaceMember(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        # If accessing workspace-specific resource, check current_workspace or workspace_id in payload/params
        return True

    def has_object_permission(self, request, view, obj):
        workspace = getattr(obj, 'workspace', obj if hasattr(obj, 'members') else None)
        if not workspace:
            return True
        from apps.workspaces.models import WorkspaceMember
        return WorkspaceMember.objects.filter(workspace=workspace, user=request.user, is_active=True).exists()

class HasWorkspaceRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser or getattr(request.user, 'role', '') == 'SUPERADMIN':
            return True
        # Read operations allowed for viewers
        if request.method in SAFE_METHODS:
            return True
        role = getattr(request, 'current_workspace_role', None)
        if not role:
            _, role = get_active_workspace(request)
        if not role:
            role = getattr(request.user, 'role', None)
        if role and role in self.allowed_roles:
            return True
        return False

class IsWorkspaceOwner(HasWorkspaceRole):
    allowed_roles = ['OWNER', 'ADMIN']

class IsProjectManagerOrHigher(HasWorkspaceRole):
    allowed_roles = ['OWNER', 'ADMIN', 'PROJECT_MANAGER']

class IsLeadDeveloperOrHigher(HasWorkspaceRole):
    allowed_roles = ['OWNER', 'ADMIN', 'PROJECT_MANAGER', 'LEAD_DEVELOPER']

class IsDeveloperOrHigher(HasWorkspaceRole):
    allowed_roles = ['OWNER', 'ADMIN', 'PROJECT_MANAGER', 'LEAD_DEVELOPER', 'DEVELOPER']


from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def get_active_workspace(request):
    """
    Safely resolves the current active workspace for the authenticated user.
    Returns (workspace, role_name) or (None, None).
    """
    if not (request.user and request.user.is_authenticated):
        return None, None
    
    workspace = getattr(request, 'current_workspace', None)
    role = getattr(request, 'current_workspace_role', None)

    if workspace and role:
        return workspace, role

    from apps.workspaces.models import WorkspaceMember, WorkspaceRole
    active_workspace_id = request.session.get('active_workspace_id')
    
    membership = None
    if active_workspace_id:
        membership = WorkspaceMember.objects.filter(
            workspace_id=active_workspace_id,
            user=request.user,
            is_active=True
        ).select_related('workspace').first()
    
    if not membership:
        membership = WorkspaceMember.objects.filter(
            user=request.user,
            is_active=True
        ).select_related('workspace').first()

    if membership:
        request.current_workspace = membership.workspace
        request.current_workspace_role = membership.role
        request.session['active_workspace_id'] = str(membership.workspace.id)
        return membership.workspace, membership.role

    return None, None


def workspace_role_required(allowed_roles=None):
    """
    View decorator to enforce workspace access and role permissions.
    """
    if allowed_roles is None:
        allowed_roles = ['OWNER', 'ADMIN']

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            workspace, role = get_active_workspace(request)
            if not workspace:
                messages.warning(request, "Please create or select a workspace to continue.")
                return redirect('workspace-list')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if role not in allowed_roles:
                messages.error(request, "Access restricted. You do not have permission for this business section.")
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def owner_required(view_func):
    """Decorator restricting view to workspace owners, admins, or superusers."""
    return workspace_role_required(['OWNER', 'ADMIN'])(view_func)


def manager_or_owner_required(view_func):
    """Decorator restricting view to project managers, owners, admins, or superusers."""
    return workspace_role_required(['OWNER', 'ADMIN', 'PROJECT_MANAGER'])(view_func)

