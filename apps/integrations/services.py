"""
VCS Integration Adapters & Webhook Processor.
Processes GitHub / GitLab / Bitbucket webhooks:
- Commits mentioning [PROJECT-KEY] link to Task
- Pull Request opened -> moves Task to CODE_REVIEW
- Pull Request merged -> moves Task to QA
"""
import re
from django.utils import timezone
from apps.tasks.models import Task, TaskStatus
from apps.activity.models import ActivityLog
from .models import RepositoryIntegration, GitCommit, GitPullRequest

class VCSWebhookService:
    @staticmethod
    def extract_task_keys(text):
        """Extracts task keys like DEV-12, API-45 from commit messages or PR titles."""
        return re.findall(r'\[?([A-Z]{2,10}-\d+)\]?', text)

    @classmethod
    def process_github_webhook(cls, integration, event_type, payload):
        workspace = integration.workspace
        
        if event_type == 'push':
            commits = payload.get('commits', [])
            for c in commits:
                msg = c.get('message', '')
                keys = cls.extract_task_keys(msg)
                
                for key in keys:
                    task = Task.objects.filter(workspace=workspace, key=key).first()
                    if task:
                        GitCommit.objects.create(
                            workspace=workspace,
                            integration=integration,
                            task=task,
                            commit_hash=c.get('id', '')[:40],
                            author_name=c.get('author', {}).get('name', 'Developer'),
                            author_email=c.get('author', {}).get('email', 'dev@example.com'),
                            message=msg,
                            url=c.get('url', ''),
                            committed_at=timezone.now()
                        )
                        ActivityLog.objects.create(
                            workspace=workspace,
                            action=ActivityLog.ActionType.INTEGRATION_SYNC,
                            entity_type='Task',
                            entity_id=str(task.id),
                            description=f"GitHub commit {c.get('id', '')[:7]} linked to task {task.key}: {msg[:60]}"
                        )

        elif event_type == 'pull_request':
            action = payload.get('action')
            pr_data = payload.get('pull_request', {})
            title = pr_data.get('title', '')
            keys = cls.extract_task_keys(title) + cls.extract_task_keys(pr_data.get('head', {}).get('ref', ''))
            
            for key in set(keys):
                task = Task.objects.filter(workspace=workspace, key=key).first()
                if task:
                    is_merged = pr_data.get('merged', False)
                    state = GitPullRequest.State.MERGED if is_merged else (
                        GitPullRequest.State.CLOSED if action == 'closed' else GitPullRequest.State.OPEN
                    )

                    GitPullRequest.objects.update_or_create(
                        workspace=workspace,
                        integration=integration,
                        pr_number=pr_data.get('number', 1),
                        defaults={
                            'task': task,
                            'title': title,
                            'source_branch': pr_data.get('head', {}).get('ref', 'feature'),
                            'target_branch': pr_data.get('base', {}).get('ref', 'main'),
                            'state': state,
                            'author': pr_data.get('user', {}).get('login', 'developer'),
                            'url': pr_data.get('html_url', ''),
                        }
                    )

                    # Automated status transitions based on PR lifecycle
                    if action in ['opened', 'reopened'] and task.status != TaskStatus.CODE_REVIEW:
                        task.status = TaskStatus.CODE_REVIEW
                        task.save(update_fields=['status', 'updated_at'])
                    elif is_merged and task.status != TaskStatus.QA:
                        task.status = TaskStatus.QA
                        task.save(update_fields=['status', 'updated_at'])
                        ActivityLog.objects.create(
                            workspace=workspace,
                            action=ActivityLog.ActionType.INTEGRATION_SYNC,
                            entity_type='Task',
                            entity_id=str(task.id),
                            description=f"Pull Request #{pr_data.get('number')} merged! Moved task {task.key} to QA."
                        )
