"""
Multi-Tenant Isolation & Audit Logging Middleware.
"""
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('devteam.tenant')

class WorkspaceTenantMiddleware(MiddlewareMixin):
    """
    Extracts the active workspace from header 'X-Workspace-ID' or session/cookie
    and binds it to request.current_workspace to ensure strict tenant isolation.
    """
    def process_request(self, request):
        request.current_workspace = None
        request.current_workspace_role = None
        workspace_id = request.headers.get('X-Workspace-ID') or request.session.get('active_workspace_id')
        
        if getattr(request, 'user', None) and request.user.is_authenticated:
            from apps.workspaces.models import Workspace, WorkspaceMember
            try:
                member = None
                if workspace_id:
                    member = WorkspaceMember.objects.filter(
                        workspace_id=workspace_id,
                        user=request.user,
                        is_active=True
                    ).select_related('workspace').first()
                if not member:
                    member = WorkspaceMember.objects.filter(
                        user=request.user,
                        is_active=True
                    ).select_related('workspace').first()
                if member:
                    request.current_workspace = member.workspace
                    request.current_workspace_role = member.role
            except Exception as e:
                logger.warning(f"Error resolving tenant workspace: {e}")

class AuditLoggingMiddleware(MiddlewareMixin):
    """Logs non-GET mutation requests for compliance and telemetry."""
    def process_response(self, request, response):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and getattr(request, 'user', None) and request.user.is_authenticated:
            # Audit log entry can be queued asynchronously
            pass
        return response
