"""
Automation Rules Execution Engine.
Evaluates triggers and executes corresponding actions automatically.
"""
from django.utils import timezone
from apps.notifications.models import Notification, NotificationType
from apps.activity.models import ActivityLog
from .models import AutomationRule, AutomationTrigger, AutomationAction

def execute_task_automations(task, event_type='status_changed'):
    """Finds active rules matching the event and executes them."""
    workspace = task.workspace
    rules = AutomationRule.objects.filter(
        workspace=workspace,
        is_active=True
    )
    if task.project:
        rules = rules.filter(models_project_filter(task.project))

    for rule in rules:
        matched = False
        
        # Status change trigger check
        if rule.trigger == AutomationTrigger.TASK_STATUS_CHANGED:
            target_trigger_status = rule.trigger_config.get('status')
            if not target_trigger_status or task.status == target_trigger_status:
                matched = True

        if matched:
            apply_automation_action(rule, task)
            rule.execution_count += 1
            rule.last_triggered_at = timezone.now()
            rule.save(update_fields=['execution_count', 'last_triggered_at'])

def apply_automation_action(rule, task):
    """Executes the specific action defined on the rule."""
    if rule.action == AutomationAction.MOVE_TASK_TO:
        target_status = rule.action_config.get('target_status')
        if target_status and task.status != target_status:
            task.status = target_status
            task.save(update_fields=['status', 'updated_at'])
            
    elif rule.action == AutomationAction.NOTIFY_ROLE:
        role_name = rule.action_config.get('notify_role', 'LEAD_DEVELOPER')
        from apps.workspaces.models import WorkspaceMember
        members = WorkspaceMember.objects.filter(
            workspace=task.workspace,
            role=role_name,
            is_active=True
        ).select_related('user')
        
        for m in members:
            Notification.objects.create(
                workspace=task.workspace,
                recipient=m.user,
                notification_type=NotificationType.TASK_STATUS_CHANGED,
                title=f"Automation Alert: [{task.key}] in {task.status}",
                message=f"Task [{task.key}] reached '{task.status}' matching rule '{rule.name}'.",
                action_url=f"/tasks/{task.id}/"
            )

    ActivityLog.objects.create(
        workspace=task.workspace,
        action=ActivityLog.ActionType.AUTOMATION_TRIGGERED,
        entity_type='Task',
        entity_id=str(task.id),
        description=f"Rule '{rule.name}' triggered on task {task.key} ({rule.get_action_display()})."
    )

def models_project_filter(project):
    from django.db.models import Q
    return Q(project=project) | Q(project__isnull=True)
