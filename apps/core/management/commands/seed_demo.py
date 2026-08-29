"""
Management command to seed realistic commercial SaaS demo data for DevTeam.
Usage: python manage.py seed_demo
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import uuid

class Command(BaseCommand):
    help = 'Seeds realistic SaaS demo data for DevTeam platform'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting DevTeam demo data seeder..."))
        
        from apps.accounts.models import User
        from apps.workspaces.models import Workspace, WorkspaceMember, WorkspaceRole
        from apps.billing.models import Plan, PlanTier, Subscription, Invoice, Coupon
        from apps.projects.models import Project, Milestone
        from apps.boards.models import Board, BoardColumn
        from apps.sprints.models import Sprint, SprintStatus
        from apps.tasks.models import Task, TaskStatus, TaskPriority, TimeLog, TaskDependency
        from apps.integrations.models import RepositoryIntegration, GitPullRequest, GitCommit
        from apps.automation.models import AutomationRule, AutomationTrigger, AutomationAction
        from apps.notifications.models import Notification, NotificationType

        # 1. Create Subscription Plans
        plans_data = [
            {
                'name': 'Free Starter',
                'tier': PlanTier.FREE,
                'monthly_price': 0.00,
                'yearly_price': 0.00,
                'max_members': 3,
                'max_projects': 2,
                'max_storage_mb': 500,
                'max_ai_generations_per_month': 20,
                'has_git_integrations': False,
                'has_advanced_reports': False,
            },
            {
                'name': 'Professional',
                'tier': PlanTier.PRO,
                'monthly_price': 29.00,
                'yearly_price': 279.00,
                'max_members': 10,
                'max_projects': 0, # unlimited
                'max_storage_mb': 10000,
                'max_ai_generations_per_month': 250,
                'has_git_integrations': True,
                'has_advanced_reports': True,
                'is_popular': True
            },
            {
                'name': 'Business & Growth',
                'tier': PlanTier.BUSINESS,
                'monthly_price': 79.00,
                'yearly_price': 759.00,
                'max_members': 50,
                'max_projects': 0,
                'max_storage_mb': 50000,
                'max_ai_generations_per_month': 1000,
                'has_git_integrations': True,
                'has_advanced_reports': True,
                'has_white_label': True
            },
            {
                'name': 'Enterprise',
                'tier': PlanTier.ENTERPRISE,
                'monthly_price': 199.00,
                'yearly_price': 1990.00,
                'max_members': 0,
                'max_projects': 0,
                'max_storage_mb': 500000,
                'max_ai_generations_per_month': 5000,
                'has_git_integrations': True,
                'has_advanced_reports': True,
                'has_white_label': True,
                'has_sso': True,
                'has_priority_support': True
            }
        ]

        created_plans = {}
        for p in plans_data:
            plan_obj, _ = Plan.objects.update_or_create(tier=p['tier'], defaults=p)
            created_plans[p['tier']] = plan_obj
        self.stdout.write(f"✓ Seeded {len(created_plans)} subscription plans.")

        # 2. Create Users
        admin_user, _ = User.objects.get_or_create(
            email='admin@devteam.io',
            defaults={
                'username': 'admin',
                'first_name': 'Alex',
                'last_name': 'Vance',
                'job_title': 'Chief Architect & SuperAdmin',
                'role': 'SUPERADMIN',
                'is_staff': True,
                'is_superuser': True,
                'referral_code': 'ALEX2026'
            }
        )
        admin_user.set_password('AdminSecure2026!')
        admin_user.save()

        lead_dev, _ = User.objects.get_or_create(
            email='sarah.lead@devteam.io',
            defaults={
                'username': 'sarah_dev',
                'first_name': 'Sarah',
                'last_name': 'Chen',
                'job_title': 'Lead Full-Stack Developer',
                'github_username': 'sarahchen-dev',
                'referral_code': 'SARAHDEV'
            }
        )
        lead_dev.set_password('DevTeam2026!')
        lead_dev.save()

        backend_dev, _ = User.objects.get_or_create(
            email='dmitry.py@devteam.io',
            defaults={
                'username': 'dmitry_be',
                'first_name': 'Dmitry',
                'last_name': 'Ivanov',
                'job_title': 'Senior Python/Django Engineer',
                'github_username': 'dmitry-py'
            }
        )
        backend_dev.set_password('DevTeam2026!')
        backend_dev.save()

        pm_user, _ = User.objects.get_or_create(
            email='elena.pm@devteam.io',
            defaults={
                'username': 'elena_pm',
                'first_name': 'Elena',
                'last_name': 'Rostova',
                'job_title': 'Senior Agile Project Manager'
            }
        )
        pm_user.set_password('DevTeam2026!')
        pm_user.save()

        # 3. Create Workspaces
        workspace, _ = Workspace.objects.get_or_create(
            slug='nexustech-solutions',
            defaults={
                'name': 'NexusTech Solutions Inc.',
                'description': 'High-growth fintech & cloud software development agency.',
                'owner': admin_user,
                'timezone': 'America/New_York',
                'brand_color': '#2563EB'
            }
        )

        WorkspaceMember.objects.get_or_create(workspace=workspace, user=admin_user, defaults={'role': WorkspaceRole.OWNER})
        WorkspaceMember.objects.get_or_create(workspace=workspace, user=pm_user, defaults={'role': WorkspaceRole.PROJECT_MANAGER})
        WorkspaceMember.objects.get_or_create(workspace=workspace, user=lead_dev, defaults={'role': WorkspaceRole.LEAD_DEVELOPER})
        WorkspaceMember.objects.get_or_create(workspace=workspace, user=backend_dev, defaults={'role': WorkspaceRole.DEVELOPER})

        # 4. Create Active Subscription & Invoices
        sub, _ = Subscription.objects.get_or_create(
            workspace=workspace,
            defaults={
                'plan': created_plans[PlanTier.PRO],
                'status': Subscription.Status.ACTIVE,
                'billing_cycle': Subscription.BillingCycle.MONTHLY,
                'start_date': timezone.now() - timedelta(days=45),
                'end_date': timezone.now() + timedelta(days=15),
                'payment_gateway': 'stripe'
            }
        )

        Invoice.objects.get_or_create(
            invoice_number='INV-2026-00918',
            defaults={
                'workspace': workspace,
                'subscription': sub,
                'amount': 29.00,
                'status': Invoice.Status.PAID,
                'payment_method': 'Credit Card (Stripe)',
                'paid_at': timezone.now() - timedelta(days=15)
            }
        )

        # 5. Create Projects
        fintech_project, _ = Project.objects.get_or_create(
            workspace=workspace,
            key='PAY',
            defaults={
                'name': 'NextGen Crypto & Fiat Checkout Gateway',
                'description': 'Multi-currency payment orchestrator with Stripe, Payme, and Click webhooks.',
                'status': 'ACTIVE',
                'health': 'ON_TRACK',
                'start_date': timezone.now().date() - timedelta(days=30),
                'deadline': timezone.now().date() + timedelta(days=60),
                'owner': pm_user,
                'lead': lead_dev,
                'tech_stack': ['Python 3.12', 'Django 5', 'PostgreSQL', 'Redis', 'Celery', 'Docker'],
                'repository_url': 'https://github.com/nexustech/payment-core',
                'budget': 24000.00,
                'spent_budget': 11400.00,
                'tags': ['fintech', 'backend', 'payments', 'critical']
            }
        )

        ai_project, _ = Project.objects.get_or_create(
            workspace=workspace,
            key='AIX',
            defaults={
                'name': 'AI Workflow & Code Review Automation Engine',
                'description': 'Automated pull request analysis, code quality grading, and Jira sync.',
                'status': 'ACTIVE',
                'health': 'ON_TRACK',
                'start_date': timezone.now().date() - timedelta(days=14),
                'deadline': timezone.now().date() + timedelta(days=45),
                'owner': pm_user,
                'lead': lead_dev,
                'tech_stack': ['Python', 'Gemini API', 'FastAPI', 'Redis', 'Docker'],
                'repository_url': 'https://github.com/nexustech/ai-reviewer',
                'budget': 18000.00,
                'spent_budget': 5200.00,
                'tags': ['ai', 'automation', 'llm']
            }
        )

        # 6. Create Milestones
        m1, _ = Milestone.objects.get_or_create(
            workspace=workspace,
            project=fintech_project,
            name='Milestone 1: Webhook Signature Verification & Idempotency',
            defaults={'deadline': timezone.now().date() + timedelta(days=10), 'status': 'IN_PROGRESS'}
        )

        # 7. Create Kanban Board & Columns
        board, _ = Board.objects.get_or_create(workspace=workspace, project=fintech_project, defaults={'name': 'Sprint Board'})
        columns_data = [
            ('Backlog', 'BACKLOG', 0, 0, '#64748B'),
            ('To Do', 'TODO', 1, 10, '#3B82F6'),
            ('In Progress', 'IN_PROGRESS', 2, 4, '#F59E0B'),
            ('Code Review', 'CODE_REVIEW', 3, 3, '#8B5CF6'),
            ('QA & Test', 'QA', 4, 3, '#EC4899'),
            ('Done', 'DONE', 5, 0, '#10B981'),
        ]
        col_objs = {}
        for title, status_val, order, wip, color in columns_data:
            col, _ = BoardColumn.objects.get_or_create(
                workspace=workspace, board=board, order=order,
                defaults={'title': title, 'status_mapping': status_val, 'wip_limit': wip, 'color': color}
            )
            col_objs[status_val] = col

        # 8. Create Sprints
        sprint, _ = Sprint.objects.get_or_create(
            workspace=workspace,
            project=fintech_project,
            name='Sprint 14: Payment Gateway & Webhook Hardening',
            defaults={
                'goal': 'Finalize Payme & Click signature verification, idempotency keys, and automated QA pipeline.',
                'status': SprintStatus.ACTIVE,
                'start_date': timezone.now().date() - timedelta(days=5),
                'end_date': timezone.now().date() + timedelta(days=9),
                'total_story_points': 24,
                'completed_story_points': 11,
                'velocity': 18.5
            }
        )

        # 9. Create Tasks
        tasks_seed = [
            {
                'key': 'PAY-101',
                'title': 'Implement Payme & Click Webhook Signature Verifier',
                'description': 'Ensure all incoming HMAC signatures are validated with merchant secrets before processing state changes.',
                'status': TaskStatus.IN_PROGRESS,
                'priority': TaskPriority.CRITICAL,
                'assignee': backend_dev,
                'reporter': lead_dev,
                'story_points': 5,
                'estimated_hours': 12.0,
                'actual_hours': 7.5,
                'due_date': timezone.now().date() + timedelta(days=2),
                'tags': ['security', 'payments', 'backend']
            },
            {
                'key': 'PAY-102',
                'title': 'Implement Idempotency Key Storage with Redis TTL',
                'description': 'Store processed transaction IDs in Redis with 24-hour expiration to prevent double-charging on network retries.',
                'status': TaskStatus.CODE_REVIEW,
                'priority': TaskPriority.HIGH,
                'assignee': lead_dev,
                'reporter': pm_user,
                'story_points': 3,
                'estimated_hours': 6.0,
                'actual_hours': 5.0,
                'due_date': timezone.now().date() + timedelta(days=1),
                'tags': ['redis', 'caching', 'payments']
            },
            {
                'key': 'PAY-103',
                'title': 'Docker Compose Cluster & Celery Worker Setup',
                'description': 'Containerize Django 5, PostgreSQL 16, Redis 7, and Celery beat scheduler for single-command deployment.',
                'status': TaskStatus.DONE,
                'priority': TaskPriority.HIGH,
                'assignee': backend_dev,
                'reporter': admin_user,
                'story_points': 5,
                'estimated_hours': 10.0,
                'actual_hours': 9.5,
                'due_date': timezone.now().date() - timedelta(days=2),
                'tags': ['devops', 'docker', 'infrastructure']
            },
            {
                'key': 'PAY-104',
                'title': 'Build Automated Unit Tests for Payment Gateway Interfaces',
                'description': 'Write pytest test suite covering Stripe, Payme, and Click gateway fallback flows and refund handlers.',
                'status': TaskStatus.TODO,
                'priority': TaskPriority.MEDIUM,
                'assignee': backend_dev,
                'reporter': lead_dev,
                'story_points': 3,
                'estimated_hours': 8.0,
                'actual_hours': 0.0,
                'due_date': timezone.now().date() + timedelta(days=4),
                'tags': ['testing', 'qa']
            },
            {
                'key': 'PAY-105',
                'title': 'Integrate drf-spectacular OpenAPI 3.0 & Swagger UI Docs',
                'description': 'Generate interactive OpenAPI schema and serve Swagger / ReDoc endpoints with token authentication.',
                'status': TaskStatus.DONE,
                'priority': TaskPriority.MEDIUM,
                'assignee': lead_dev,
                'reporter': admin_user,
                'story_points': 3,
                'estimated_hours': 4.0,
                'actual_hours': 3.5,
                'due_date': timezone.now().date() - timedelta(days=3),
                'tags': ['api', 'docs', 'swagger']
            }
        ]

        task_objs = {}
        for t in tasks_seed:
            task, _ = Task.objects.get_or_create(
                workspace=workspace,
                project=fintech_project,
                key=t['key'],
                defaults={
                    'title': t['title'],
                    'description': t['description'],
                    'status': t['status'],
                    'priority': t['priority'],
                    'assignee': t['assignee'],
                    'reporter': t['reporter'],
                    'sprint': sprint,
                    'board_column': col_objs.get(t['status']),
                    'milestone': m1,
                    'story_points': t['story_points'],
                    'estimated_hours': t['estimated_hours'],
                    'actual_hours': t['actual_hours'],
                    'due_date': t['due_date'],
                    'tags': t['tags']
                }
            )
            task_objs[t['key']] = task

        # 10. Create Task Dependencies (PAY-101 is blocked by PAY-102)
        if 'PAY-101' in task_objs and 'PAY-102' in task_objs:
            TaskDependency.objects.get_or_create(
                workspace=workspace,
                predecessor=task_objs['PAY-102'],
                successor=task_objs['PAY-101'],
                defaults={'dependency_type': TaskDependency.DependencyType.BLOCKS}
            )

        # 11. Create Time Logs
        if 'PAY-101' in task_objs:
            TimeLog.objects.get_or_create(
                workspace=workspace,
                task=task_objs['PAY-101'],
                user=backend_dev,
                defaults={
                    'description': 'Implemented HMAC-SHA256 signature verification algorithms',
                    'start_time': timezone.now() - timedelta(hours=4),
                    'duration_minutes': 240,
                    'is_billable': True
                }
            )

        # 12. Create GitHub Webhook & PR Simulator
        repo_int, _ = RepositoryIntegration.objects.get_or_create(
            workspace=workspace,
            project=fintech_project,
            repo_name='nexustech/payment-core',
            defaults={
                'provider': 'GITHUB',
                'repo_url': 'https://github.com/nexustech/payment-core',
                'is_active': True,
                'last_synced_at': timezone.now()
            }
        )

        GitPullRequest.objects.get_or_create(
            workspace=workspace,
            integration=repo_int,
            pr_number=42,
            defaults={
                'task': task_objs.get('PAY-102'),
                'title': '[PAY-102] Implement Redis Idempotency Key Lock',
                'source_branch': 'feat/redis-idempotency',
                'target_branch': 'main',
                'state': 'OPEN',
                'author': 'sarahchen-dev',
                'url': 'https://github.com/nexustech/payment-core/pull/42'
            }
        )

        # 13. Create Automation Rule
        AutomationRule.objects.get_or_create(
            workspace=workspace,
            name='Move to QA on Pull Request Merge',
            defaults={
                'trigger': AutomationTrigger.PR_MERGED,
                'action': AutomationAction.MOVE_TASK_TO,
                'action_config': {'target_status': 'QA'},
                'is_active': True,
                'execution_count': 14
            }
        )

        # 14. Create Promotional Coupon
        Coupon.objects.get_or_create(
            code='LAUNCH2026',
            defaults={
                'discount_type': Coupon.DiscountType.PERCENTAGE,
                'discount_value': 25.00,
                'max_uses': 500,
                'used_count': 42,
                'is_active': True
            }
        )

        # 15. Notification
        Notification.objects.get_or_create(
            workspace=workspace,
            recipient=backend_dev,
            title='Assigned to PAY-101: Payme & Click Webhook Signature Verifier',
            defaults={
                'notification_type': NotificationType.TASK_ASSIGNED,
                'message': 'Sarah Chen assigned you to critical payment security task PAY-101.',
                'action_url': '/tasks/',
                'is_read': False
            }
        )

        self.stdout.write(self.style.SUCCESS("✓ DevTeam SaaS demo data successfully seeded!"))
