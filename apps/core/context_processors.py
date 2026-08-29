"""Global template context processors for DevTeam frontend."""
from django.conf import settings

def global_saas_context(request):
    context = {
        'APP_NAME': 'DevTeam',
        'APP_VERSION': '1.0.0',
        'DEBUG': settings.DEBUG,
        'current_workspace': getattr(request, 'current_workspace', None),
        'current_role': getattr(request, 'current_workspace_role', 'DEVELOPER'),
        'user_workspaces': [],
        'unread_notifications_count': 0,
    }

    if getattr(request, 'user', None) and request.user.is_authenticated:
        from apps.workspaces.models import WorkspaceMember
        from apps.notifications.models import Notification
        
        user_memberships = WorkspaceMember.objects.filter(
            user=request.user, is_active=True
        ).select_related('workspace')
        
        context['user_workspaces'] = [m.workspace for m in user_memberships]
        
        if not context['current_workspace'] and user_memberships.exists():
            context['current_workspace'] = user_memberships.first().workspace
            context['current_role'] = user_memberships.first().role

        context['unread_notifications_count'] = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()

    return context
