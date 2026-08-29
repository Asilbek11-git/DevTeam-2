"""
Asynchronous Celery Tasks for Email, Push, and Webhook Notifications.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger('devteam.celery')

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_async_email_notification(self, recipient_email, subject, message_body):
    """Dispatches transactional emails in the background via Celery."""
    try:
        send_mail(
            subject=subject,
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {recipient_email}: {exc}")
        raise self.retry(exc=exc)

@shared_task
def send_daily_deadline_reminders():
    """Periodic Celery Beat task to notify assignees of upcoming deadlines."""
    from django.utils import timezone
    from datetime import timedelta
    from apps.tasks.models import Task
    from apps.notifications.models import Notification, NotificationType

    tomorrow = timezone.now().date() + timedelta(days=1)
    impending_tasks = Task.objects.filter(
        due_date=tomorrow,
        status__in=['TODO', 'IN_PROGRESS', 'CODE_REVIEW', 'QA'],
        assignee__isnull=False
    ).select_related('assignee', 'workspace', 'project')

    for task in impending_tasks:
        Notification.objects.create(
            workspace=task.workspace,
            recipient=task.assignee,
            notification_type=NotificationType.DEADLINE_APPROACHING,
            title=f"Deadline Tomorrow: [{task.key}] {task.title}",
            message=f"Task [{task.key}] is due tomorrow ({task.due_date}). Please review your progress.",
            action_url=f"/tasks/{task.id}/"
        )
    return f"Processed {impending_tasks.count()} deadline reminders."
