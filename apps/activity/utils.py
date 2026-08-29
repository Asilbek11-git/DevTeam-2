"""
Audit Logging Utilities for DevTeam SaaS.
Logs user actions and business events for compliance, security, and activity history.
"""
import logging
from apps.activity.models import ActivityLog

logger = logging.getLogger('devteam.activity')

def log_activity(workspace, actor, action, entity_type, entity_id, description, changes=None, request=None):
    """
    Safely record an activity log entry scoped to a tenant workspace.
    """
    if not workspace:
        return None

    ip_address = None
    if request:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR')

    try:
        log_entry = ActivityLog.objects.create(
            workspace=workspace,
            actor=actor if (actor and actor.is_authenticated) else None,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id is not None else '',
            description=description,
            changes=changes or {},
            ip_address=ip_address or None
        )
        return log_entry
    except Exception as e:
        logger.warning(f"Failed to log activity '{action}' for {entity_type} #{entity_id}: {e}")
        return None
