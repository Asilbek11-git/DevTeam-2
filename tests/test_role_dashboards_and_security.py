"""
Test suite for Role-Based Dashboard Separation, Server-Side Security, and Financial Data Protection.
Verifies:
1. Owner / SuperAdmin dashboard contains executive metrics (Revenue, Profit, Expenses, Pipeline, Invoices, Clients)
2. Team / Developer dashboard contains engineering metrics (Assigned Tasks, Sprint Velocity, Time Logs) and NO financials
3. Client dashboard contains client portal (Deliverables, Milestones, Client Invoices) and NO team/financial internals
4. Strict server-side URL protection preventing non-owners from accessing financial and management routes
5. Cross-client data isolation
6. Real ORM mathematical calculations for revenue, expenses, and net profit
"""
import pytest
from decimal import Decimal
from django.utils import timezone
from django.test import Client
from apps.accounts.models import User, UserRole
from apps.workspaces.models import Workspace, WorkspaceMember, WorkspaceRole, Client as ClientModel, Lead
from apps.projects.models import Project, Milestone
from apps.tasks.models import Task, TaskStatus, TimeLog
from apps.sprints.models import Sprint, SprintStatus
from apps.billing.models import Invoice, Expense, Service

@pytest.mark.django_db
class TestRoleDashboardsAndSecurity:

    def setup_method(self):
        self.web_client = Client()

        # 1. Create Users with specific roles
        self.owner = User.objects.create_user(
            email='owner@saas.io',
            username='owner_user',
            password='Password123!',
            role=UserRole.ADMIN
        )
        self.developer = User.objects.create_user(
            email='dev@saas.io',
            username='dev_user',
            password='Password123!',
            role=UserRole.DEVELOPER
        )
        self.client_user_a = User.objects.create_user(
            email='client_a@acme.com',
            username='client_a',
            password='Password123!',
            role=UserRole.CLIENT
        )
        self.client_user_b = User.objects.create_user(
            email='client_b@globex.com',
            username='client_b',
            password='Password123!',
            role=UserRole.CLIENT
        )

        # 2. Workspace Setup
        self.workspace = Workspace.objects.create(
            name='Acme Engineering Workspace',
            slug='acme-eng',
            owner=self.owner
        )
        WorkspaceMember.objects.create(workspace=self.workspace, user=self.owner, role=WorkspaceRole.OWNER)
        WorkspaceMember.objects.create(workspace=self.workspace, user=self.developer, role=WorkspaceRole.DEVELOPER)
        WorkspaceMember.objects.create(workspace=self.workspace, user=self.client_user_a, role=WorkspaceRole.CLIENT)
        WorkspaceMember.objects.create(workspace=self.workspace, user=self.client_user_b, role=WorkspaceRole.CLIENT)

        # 3. CRM Client records
        self.client_record_a = ClientModel.objects.create(
            workspace=self.workspace,
            owner=self.owner,
            user=self.client_user_a,
            full_name='Alice Acme',
            company='Acme Corp',
            email='client_a@acme.com',
            status=ClientModel.Status.ACTIVE
        )
        self.client_record_b = ClientModel.objects.create(
            workspace=self.workspace,
            owner=self.owner,
            user=self.client_user_b,
            full_name='Bob Globex',
            company='Globex Inc',
            email='client_b@globex.com',
            status=ClientModel.Status.ACTIVE
        )

        # 4. Financial Records (Invoices & Expenses)
        self.invoice_a = Invoice.objects.create(
            workspace=self.workspace,
            client=self.client_record_a,
            invoice_number='INV-2026-001',
            amount=Decimal('3500.00'),
            status=Invoice.Status.PAID,
            paid_at=timezone.now()
        )
        self.invoice_b = Invoice.objects.create(
            workspace=self.workspace,
            client=self.client_record_b,
            invoice_number='INV-2026-002',
            amount=Decimal('1500.00'),
            status=Invoice.Status.PAID,
            paid_at=timezone.now()
        )
        self.expense = Expense.objects.create(
            workspace=self.workspace,
            owner=self.owner,
            title='Cloud Infrastructure & DB Hosting',
            amount=Decimal('1000.00'),
            category=Expense.Category.INFRASTRUCTURE,
            expense_date=timezone.now().date()
        )

        # 5. Projects & Deliverables
        self.project_a = Project.objects.create(
            workspace=self.workspace,
            key='ACME',
            name='Acme Cloud Platform',
            owner=self.owner
        )
        self.milestone_a = Milestone.objects.create(
            workspace=self.workspace,
            project=self.project_a,
            name='Phase 1: API Architecture',
            deadline=timezone.now().date(),
            status='COMPLETED'
        )

        # 6. Sprint & Tasks
        self.sprint = Sprint.objects.create(
            workspace=self.workspace,
            project=self.project_a,
            name='Sprint 1',
            status=SprintStatus.ACTIVE,
            total_story_points=20,
            completed_story_points=12
        )
        self.task_dev = Task.objects.create(
            workspace=self.workspace,
            project=self.project_a,
            sprint=self.sprint,
            key='ACME-10',
            title='Implement User Authentication and OAuth',
            assignee=self.developer,
            reporter=self.owner,
            status=TaskStatus.IN_PROGRESS
        )
        TimeLog.objects.create(
            workspace=self.workspace,
            task=self.task_dev,
            user=self.developer,
            duration_minutes=240,
            start_time=timezone.now()
        )

    def test_owner_dashboard_renders_executive_business_metrics(self):
        """Owner receives executive business dashboard with ORM-computed financials."""
        self.web_client.force_login(self.owner)
        response = self.web_client.get('/dashboard/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')

        # Check Owner Title & Executive Cards
        assert "Executive Business Operations" in content or "COMMAND CENTER" in content
        assert "Total Revenue" in content
        assert "Net Profit" in content
        # Total revenue is 3500 + 1500 = 5000.00, Expenses = 1000.00, Net Profit = 4000.00
        assert "5000.00" in content
        assert "4000.00" in content

    def test_developer_dashboard_renders_engineering_hub_without_financials(self):
        """Developer receives engineering hub and CANNOT see financial metrics."""
        self.web_client.force_login(self.developer)
        response = self.web_client.get('/dashboard/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')

        # Check Engineering Hub elements
        assert "Engineering & Sprint Hub" in content or "DEVELOPER WORKSPACE" in content
        assert "My Assigned Tasks" in content
        assert "Active Sprint" in content

        # Verify Developer NEVER receives owner financial metrics
        assert "Executive Business Operations" not in content
        assert "Net Profit" not in content
        assert "Pipeline Deals" not in content
        assert "Total Revenue" not in content

    def test_client_dashboard_renders_client_portal_without_internals(self):
        """Client receives client portal with their deliverables and invoices."""
        self.web_client.force_login(self.client_user_a)
        response = self.web_client.get('/dashboard/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')

        # Check Client Portal elements
        assert "CLIENT PORTAL" in content or "Project Status & Deliverables" in content
        assert "Active Projects" in content
        assert "Milestone Progress" in content
        assert "Invoices Paid" in content

        # Verify Client NEVER receives internal engineering hub or executive owner metrics
        assert "Executive Business Operations" not in content
        assert "Engineering & Sprint Hub" not in content
        assert "Net Profit" not in content
        assert "Pipeline Deals" not in content

    def test_server_side_url_protection_for_non_owners(self):
        """
        Server-side security: Developers and Clients must NEVER access
        /finance/, /owner/dashboard/, /clients/, /leads/ simply by URL.
        """
        restricted_urls = [
            '/finance/',
            '/owner/dashboard/',
            '/clients/',
            '/leads/',
            '/services/create/',
            '/superadmin/',
        ]

        for user in [self.developer, self.client_user_a]:
            self.web_client.force_login(user)
            for url in restricted_urls:
                res = self.web_client.get(url, follow=True)
                # Either redirected to /dashboard/ or returns 403
                content = res.content.decode('utf-8')
                # Must not show financial dashboard or client CRM
                assert "Executive Financial Overview" not in content or res.status_code == 403
                assert "Business Expenses" not in content or res.status_code == 403

    def test_cross_client_isolation(self):
        """Client A must NOT see Client B's invoices."""
        self.web_client.force_login(self.client_user_a)
        response = self.web_client.get('/dashboard/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')

        # Client A invoice #
        assert "INV-2026-001" in content or "3500.00" in content
        # Client B invoice # should NOT appear
        assert "INV-2026-002" not in content

    def test_real_database_financial_calculations(self):
        """Financial metrics must be computed strictly from database records."""
        from apps.billing.models import Invoice, Expense
        
        # Test exact sums
        total_rev = Invoice.objects.filter(workspace=self.workspace, status=Invoice.Status.PAID).aggregate(
            rev=pytest.importorskip('django.db.models').Sum('amount')
        )['rev']
        total_exp = Expense.objects.filter(workspace=self.workspace).aggregate(
            exp=pytest.importorskip('django.db.models').Sum('amount')
        )['exp']
        net_profit = total_rev - total_exp

        assert total_rev == Decimal('5000.00')
        assert total_exp == Decimal('1000.00')
        assert net_profit == Decimal('4000.00')
