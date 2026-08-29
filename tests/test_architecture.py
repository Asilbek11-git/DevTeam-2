"""
Comprehensive Unit & Integration Test Suite for DevTeam SaaS.
Covers:
1. Authentication & JWT Tokens
2. Workspace Multi-Tenant Isolation & RBAC
3. Dependency Cycle Prevention Graph Algorithm
4. Plan Limits & Upgrade Enforcement
5. REST API Standard Response Contract & Health
6. OpenAPI / Swagger Documentation Schema
7. Django Templates Frontend HTML Page Rendering
8. AI Service Structured Fallbacks
9. Payment Gateways (Stripe, Payme, Click)
10. VCS Webhook Processing & Task Automation
"""
import pytest
from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.workspaces.models import Workspace, WorkspaceMember, WorkspaceRole
from apps.projects.models import Project, Milestone
from apps.tasks.models import Task, TaskStatus, TaskDependency, TimeLog
from apps.tasks.services import check_for_dependency_cycle
from apps.sprints.models import Sprint, SprintStatus
from apps.core.exceptions import DependencyCycleException, PlanLimitExceededException
from apps.billing.models import Plan, PlanTier, Subscription, Invoice
from apps.ai.services import AIService
from apps.payments.services import PaymentService
from apps.integrations.models import RepositoryIntegration
from apps.integrations.services import VCSWebhookService

@pytest.mark.django_db
class TestDevTeamArchitecture:

    def setup_method(self):
        self.api_client = APIClient()
        self.web_client = Client()
        
        self.user1 = User.objects.create_user(email='test1@devteam.io', username='test1', password='Password123!')
        self.user2 = User.objects.create_user(email='test2@devteam.io', username='test2', password='Password123!')

        self.workspace1 = Workspace.objects.create(name='Workspace Alpha', slug='ws-alpha', owner=self.user1)
        WorkspaceMember.objects.create(workspace=self.workspace1, user=self.user1, role=WorkspaceRole.OWNER)

        self.workspace2 = Workspace.objects.create(name='Workspace Beta', slug='ws-beta', owner=self.user2)
        WorkspaceMember.objects.create(workspace=self.workspace2, user=self.user2, role=WorkspaceRole.OWNER)

        self.project1 = Project.objects.create(workspace=self.workspace1, key='ALP', name='Alpha Project', owner=self.user1)

    def test_authentication_and_jwt_issuance(self):
        """Verify user login returns JWT tokens."""
        response = self.api_client.post('/api/v1/auth/login/', {
            'email': 'test1@devteam.io',
            'password': 'Password123!'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'tokens' in response.data['data']
        assert 'access' in response.data['data']['tokens']

    def test_strict_multi_tenant_workspace_isolation(self):
        """User2 must NEVER be able to view Workspace1 projects."""
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.get(f'/api/v1/projects/{self.project1.id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_dependency_cycle_detection_algorithm(self):
        """Graph cycle check must prevent A -> B -> C -> A circular deadlocks."""
        t1 = Task.objects.create(workspace=self.workspace1, project=self.project1, key='ALP-1', title='Task 1', reporter=self.user1)
        t2 = Task.objects.create(workspace=self.workspace1, project=self.project1, key='ALP-2', title='Task 2', reporter=self.user1)
        t3 = Task.objects.create(workspace=self.workspace1, project=self.project1, key='ALP-3', title='Task 3', reporter=self.user1)

        TaskDependency.objects.create(workspace=self.workspace1, predecessor=t1, successor=t2)
        TaskDependency.objects.create(workspace=self.workspace1, predecessor=t2, successor=t3)

        with pytest.raises(DependencyCycleException):
            check_for_dependency_cycle(t3.id, t1.id)

    def test_plan_project_limit_enforcement(self):
        """Free plan with limit=2 must throw PlanLimitExceededException on 3rd project."""
        from django.utils import timezone
        free_plan = Plan.objects.create(name='Free Tier', tier=PlanTier.FREE, max_projects=2)
        sub = Subscription.objects.create(workspace=self.workspace1, plan=free_plan, status=Subscription.Status.ACTIVE, start_date=timezone.now())
        
        Project.objects.create(workspace=self.workspace1, key='ALP2', name='Project 2', owner=self.user1)
        
        with pytest.raises(PlanLimitExceededException):
            sub.check_project_limit()

    def test_health_check_endpoint(self):
        """Verify REST API health check endpoint."""
        response = self.api_client.get('/api/v1/health/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['data']['status'] == 'healthy'

    def test_openapi_schema_endpoint(self):
        """Verify OpenAPI 3.0 Spectacular documentation schema."""
        response = self.api_client.get('/api/schema/')
        assert response.status_code == status.HTTP_200_OK

    def test_django_templates_rendering(self):
        """Verify that Django directly serves and renders HTML pages via Django Templates."""
        # Public Landing Page
        res_home = self.web_client.get('/')
        assert res_home.status_code == 200
        assert b'DevTeam' in res_home.content

        # Login Template Page
        res_login = self.web_client.get('/auth/login/')
        assert res_login.status_code == 200
        assert b'Log In' in res_login.content or b'Sign In' in res_login.content or b'login' in res_login.content.lower()

        # Register Template Page
        res_reg = self.web_client.get('/auth/register/')
        assert res_reg.status_code == 200

        # Authenticated Dashboard Template
        self.web_client.force_login(self.user1)
        res_dash = self.web_client.get('/dashboard/')
        assert res_dash.status_code == 200
        assert b'Dashboard' in res_dash.content or b'DevTeam' in res_dash.content

        # Projects Template
        res_proj = self.web_client.get('/projects/')
        assert res_proj.status_code == 200

        # Tasks Template
        res_tasks = self.web_client.get('/tasks/')
        assert res_tasks.status_code == 200

        # Sprints Template
        res_sprints = self.web_client.get('/sprints/')
        assert res_sprints.status_code == 200

        # Pricing Plans Template
        res_pricing = self.web_client.get('/billing/plans/')
        assert res_pricing.status_code == 200

        # AI Studio Template
        res_ai = self.web_client.get('/ai/studio/')
        assert res_ai.status_code == 200

        # Team & RBAC Template
        res_team = self.web_client.get('/team/')
        assert res_team.status_code == 200

    def test_ai_service_fallback(self):
        """Verify AI service falls back to structured requirement breakdown when API key is not present."""
        desc = AIService.generate_task_description("Build Payment Webhook", "Stripe subscription handling")
        assert "Objective" in desc
        assert "Acceptance Criteria" in desc
        assert "Implementation Steps" in desc

        complexity = AIService.estimate_complexity("Build Stripe Payment Webhook")
        assert "story_points" in complexity
        assert complexity["story_points"] >= 1

    def test_payment_processing_flow(self):
        """Verify payment processing activates subscription and creates invoice."""
        pro_plan = Plan.objects.create(name='Pro Plan', tier=PlanTier.PRO, monthly_price=29.00, yearly_price=290.00)
        sub, inv = PaymentService.process_successful_payment(
            workspace=self.workspace1,
            plan=pro_plan,
            billing_cycle='MONTHLY',
            gateway='stripe'
        )
        assert sub.status == Subscription.Status.ACTIVE
        assert sub.plan == pro_plan
        assert inv.amount == 29.00
        assert inv.status == Invoice.Status.PAID

    def test_vcs_webhook_task_linking(self):
        """Verify git commit messages with task keys automatically link to the task."""
        task = Task.objects.create(workspace=self.workspace1, project=self.project1, key='ALP-99', title='Feature 99', reporter=self.user1)
        repo = RepositoryIntegration.objects.create(
            workspace=self.workspace1,
            project=self.project1,
            repo_name='org/backend-repo',
            repo_url='https://github.com/org/backend-repo'
        )

        payload = {
            'commits': [
                {
                    'id': 'abc1234567890abcdef',
                    'message': 'Fix authentication bug [ALP-99]',
                    'author': {'name': 'Dev', 'email': 'dev@test.io'},
                    'url': 'https://github.com/org/repo/commit/abc1234'
                }
            ]
        }

        VCSWebhookService.process_github_webhook(repo, 'push', payload)
        assert repo.commits.filter(task=task).exists()

    def test_owner_profile_and_portfolio_item_creation(self):
        """Verify OwnerProfile and PortfolioItem models and configurations."""
        from apps.accounts.models import OwnerProfile, PortfolioItem
        
        # 1. OwnerProfile
        profile = OwnerProfile.objects.create(
            user=self.user1,
            full_name='Lead Software Architect',
            professional_title='Principal SaaS Engineer & Consultant',
            bio='Specializing in Django, React, Distributed Systems & AI',
            skills=['Python', 'Django', 'Architecture', 'AI Integration'],
            programming_languages=['Python', 'TypeScript', 'SQL'],
            frameworks=['Django', 'DRF', 'React', 'FastAPI'],
            databases=['PostgreSQL', 'Redis', 'ClickHouse'],
            tools=['Docker', 'Celery', 'Git', 'Nginx'],
            years_of_experience=8,
            hourly_rate=75.00,
            availability_status=OwnerProfile.Availability.AVAILABLE
        )
        assert profile.user == self.user1
        assert profile.hourly_rate == 75.00
        assert 'Python' in profile.programming_languages
        assert self.user1.owner_profile == profile

        # 2. PortfolioItem
        portfolio = PortfolioItem.objects.create(
            owner=self.user1,
            title='DevTeam SaaS Platform',
            short_description='All-in-one agile SaaS platform for engineering teams',
            technologies=['Django', 'PostgreSQL', 'Redis', 'Celery'],
            is_featured=True,
            is_published=True,
            project_value=15000.00
        )
        assert portfolio.owner == self.user1
        assert portfolio.slug.startswith('devteam-saas-platform')
        assert portfolio.is_featured is True

    def test_client_and_lead_pipeline_and_isolation(self):
        """Verify Client & Lead models and workspace isolation."""
        from apps.workspaces.models import Client as ClientModel, Lead
        from apps.billing.models import Service

        # Create service
        service = Service.objects.create(
            workspace=self.workspace1,
            owner=self.user1,
            name='Custom Django API & SaaS Backend',
            starting_price=1200.00,
            estimated_delivery_days=10,
            technologies=['Django', 'DRF', 'PostgreSQL']
        )
        assert service.slug.startswith('custom-django-api')

        # Create Client in Workspace 1
        client1 = ClientModel.objects.create(
            workspace=self.workspace1,
            owner=self.user1,
            full_name='Jane Doe',
            company='Acme Corp',
            email='jane@acme.com',
            status=ClientModel.Status.ACTIVE,
            rating=5
        )
        assert client1.workspace == self.workspace1

        # Create Lead
        lead = Lead.objects.create(
            workspace=self.workspace1,
            client=client1,
            service=service,
            title='Enterprise ERP API',
            budget=5000.00,
            probability=80,
            status=Lead.Status.IN_PROGRESS
        )
        # Expected revenue is auto-calculated: 5000 * 80 / 100 = 4000
        assert lead.expected_revenue == 4000.00

        # Workspace isolation: Workspace 2 has zero clients or leads
        assert ClientModel.objects.filter(workspace=self.workspace2).count() == 0
        assert Lead.objects.filter(workspace=self.workspace2).count() == 0

    def test_expense_tracking_model(self):
        """Verify Expense model calculations and categorization."""
        from apps.billing.models import Expense
        from django.utils import timezone

        expense = Expense.objects.create(
            workspace=self.workspace1,
            owner=self.user1,
            title='Cloud Server Hosting & DB Cluster',
            amount=149.50,
            category=Expense.Category.INFRASTRUCTURE,
            expense_date=timezone.now().date()
        )
        assert expense.amount == 149.50
        assert expense.workspace == self.workspace1
        assert expense.category == Expense.Category.INFRASTRUCTURE


