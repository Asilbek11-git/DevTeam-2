"""
Core views handling both Django HTML template rendering and core web routes.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone

from apps.core.permissions import get_active_workspace, manager_or_owner_required
from apps.workspaces.models import Workspace, WorkspaceMember, WorkspaceRole, Client, Lead
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.sprints.models import Sprint
from apps.billing.models import Plan, Subscription, Invoice, Expense, Service
from apps.activity.models import ActivityLog
from apps.accounts.models import OwnerProfile, PortfolioItem

def home_view(request):
    """Public landing page or redirects to dashboard if authenticated."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    plans = Plan.objects.filter(is_active=True).order_by('monthly_price')
    return render(request, 'core/index.html', {'plans': plans})

@login_required(login_url='login')
def dashboard_view(request):
    """
    Main SaaS productivity, workspace, and owner command center dashboard.
    Calculates real PostgreSQL / Django ORM data with zero hardcoded metrics.
    """
    workspace, role = get_active_workspace(request)
    now = timezone.now()
    today = now.date()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    projects = []
    tasks = []
    active_sprint = None
    recent_activity = []
    
    # Initialize all stats
    stats = {
        # Clients
        'total_clients': 0,
        'active_clients': 0,
        'inactive_clients': 0,
        'new_clients_month': 0,
        
        # Leads
        'total_leads': 0,
        'new_leads': 0,
        'negotiation_leads': 0,
        'accepted_leads': 0,
        'conversion_rate': 0.0,
        'pipeline_value': Decimal('0.00'),
        'expected_revenue': Decimal('0.00'),
        
        # Projects
        'total_projects': 0,
        'active_projects': 0,
        'completed_projects': 0,
        'overdue_projects': 0,
        'avg_project_value': Decimal('0.00'),
        
        # Tasks
        'total_tasks': 0,
        'active_tasks': 0,
        'completed_tasks': 0,
        'in_progress_tasks': 0,
        'overdue_tasks': 0,
        
        # Finance
        'total_revenue': Decimal('0.00'),
        'month_revenue': Decimal('0.00'),
        'year_revenue': Decimal('0.00'),
        'pending_payments': Decimal('0.00'),
        'total_expenses': Decimal('0.00'),
        'net_profit': Decimal('0.00'),
        
        # Team
        'team_members': 1,
        'services_count': 0,
    }
    
    recent_leads = []
    recent_clients = []
    recent_invoices = []
    lead_stages = []
    monthly_chart_data = []

    if workspace:
        # Projects & Tasks
        projects = Project.objects.filter(workspace=workspace).select_related('lead').order_by('-created_at')[:6]
        tasks = Task.objects.filter(workspace=workspace).select_related('project', 'assignee').order_by('-created_at')[:10]
        active_sprint = Sprint.objects.filter(workspace=workspace, status='ACTIVE').first()
        
        stats['total_projects'] = Project.objects.filter(workspace=workspace).count()
        stats['active_projects'] = Project.objects.filter(workspace=workspace, status__in=['PLANNING', 'ACTIVE']).count()
        stats['completed_projects'] = Project.objects.filter(workspace=workspace, status='COMPLETED').count()
        stats['overdue_projects'] = Project.objects.filter(workspace=workspace, target_end_date__lt=today).exclude(status__in=['COMPLETED', 'ARCHIVED']).count()
        avg_budget = Project.objects.filter(workspace=workspace).exclude(budget=0).aggregate(Avg('budget'))['budget__avg']
        stats['avg_project_value'] = avg_budget or Decimal('0.00')

        stats['total_tasks'] = Task.objects.filter(workspace=workspace).count()
        stats['active_tasks'] = Task.objects.filter(workspace=workspace).exclude(status__in=['DONE', 'CANCELLED']).count()
        stats['completed_tasks'] = Task.objects.filter(workspace=workspace, status='DONE').count()
        stats['in_progress_tasks'] = Task.objects.filter(workspace=workspace, status='IN_PROGRESS').count()
        stats['overdue_tasks'] = Task.objects.filter(workspace=workspace, due_date__lt=today).exclude(status__in=['DONE', 'CANCELLED']).count()
        stats['team_members'] = WorkspaceMember.objects.filter(workspace=workspace, is_active=True).count()

        # Clients
        stats['total_clients'] = Client.objects.filter(workspace=workspace).count()
        stats['active_clients'] = Client.objects.filter(workspace=workspace, status=Client.Status.ACTIVE).count()
        stats['inactive_clients'] = Client.objects.filter(workspace=workspace, status__in=[Client.Status.INACTIVE, Client.Status.ARCHIVED]).count()
        stats['new_clients_month'] = Client.objects.filter(workspace=workspace, created_at__gte=start_of_month).count()
        recent_clients = Client.objects.filter(workspace=workspace).order_by('-created_at')[:5]

        # Leads
        leads_qs = Lead.objects.filter(workspace=workspace)
        stats['total_leads'] = leads_qs.count()
        stats['new_leads'] = leads_qs.filter(status=Lead.Status.NEW).count()
        stats['negotiation_leads'] = leads_qs.filter(status=Lead.Status.NEGOTIATION).count()
        stats['accepted_leads'] = leads_qs.filter(status__in=[Lead.Status.ACCEPTED, Lead.Status.IN_PROGRESS, Lead.Status.COMPLETED]).count()
        stats['conversion_rate'] = round((stats['accepted_leads'] / stats['total_leads'] * 100), 1) if stats['total_leads'] > 0 else 0.0
        stats['pipeline_value'] = leads_qs.aggregate(Sum('budget'))['budget__sum'] or Decimal('0.00')
        stats['expected_revenue'] = leads_qs.aggregate(Sum('expected_revenue'))['expected_revenue__sum'] or Decimal('0.00')
        recent_leads = leads_qs.select_related('client', 'service').order_by('-created_at')[:5]
        
        # Lead Pipeline Stages summary
        for code, label in Lead.Status.choices:
            count = leads_qs.filter(status=code).count()
            val = leads_qs.filter(status=code).aggregate(Sum('budget'))['budget__sum'] or Decimal('0.00')
            lead_stages.append({'code': code, 'label': label, 'count': count, 'value': val})

        # Finance
        paid_inv = Invoice.objects.filter(workspace=workspace, status=Invoice.Status.PAID)
        stats['total_revenue'] = paid_inv.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        stats['month_revenue'] = paid_inv.filter(paid_at__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        stats['year_revenue'] = paid_inv.filter(paid_at__gte=start_of_year).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        stats['pending_payments'] = Invoice.objects.filter(workspace=workspace, status=Invoice.Status.DRAFT).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        stats['total_expenses'] = Expense.objects.filter(workspace=workspace).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        stats['net_profit'] = stats['total_revenue'] - stats['total_expenses']
        stats['services_count'] = Service.objects.filter(Q(workspace=workspace) | Q(workspace__isnull=True), is_active=True).count()

        recent_invoices = Invoice.objects.filter(workspace=workspace).order_by('-created_at')[:5]
        recent_activity = ActivityLog.objects.filter(workspace=workspace).select_related('actor').order_by('-created_at')[:8]

        # 6-Month Trend Data for Financial Chart
        for i in range(5, -1, -1):
            m_start = (now.replace(day=1) - timedelta(days=i*30)).replace(day=1)
            m_end = (m_start + timedelta(days=32)).replace(day=1)
            rev = paid_inv.filter(paid_at__gte=m_start, paid_at__lt=m_end).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            exp = Expense.objects.filter(workspace=workspace, expense_date__gte=m_start.date(), expense_date__lt=m_end.date()).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            monthly_chart_data.append({
                'label': m_start.strftime('%b'),
                'revenue': float(rev),
                'expenses': float(exp),
                'profit': float(rev - exp)
            })

    is_owner_or_admin = (role in ['OWNER', 'ADMIN']) or request.user.is_superuser
    owner_profile = OwnerProfile.objects.filter(user=request.user).first()

    context = {
        'workspace': workspace,
        'role': role,
        'is_owner_or_admin': is_owner_or_admin,
        'owner_profile': owner_profile,
        'projects': projects,
        'tasks': tasks,
        'active_sprint': active_sprint,
        'stats': stats,
        'recent_leads': recent_leads,
        'recent_clients': recent_clients,
        'recent_invoices': recent_invoices,
        'recent_activity': recent_activity,
        'lead_stages': lead_stages,
        'monthly_chart_data': monthly_chart_data,
        'page_title': 'Owner Command Center' if is_owner_or_admin else 'Workspace Dashboard',
    }
    return render(request, 'core/dashboard.html', context)


@login_required(login_url='login')
@manager_or_owner_required
def owner_dashboard_view(request):
    """Dedicated route for Owner/SuperAdmin Business Command Center."""
    return dashboard_view(request)


@login_required(login_url='login')
def analytics_view(request):
    """Engineering metrics, velocity trends, and sprint burndown analytics."""
    return render(request, 'core/analytics.html', {'page_title': 'Analytics & Velocity'})

@login_required(login_url='login')
def team_view(request):
    """Workspace team members, roles, and invitation management."""
    workspace = getattr(request, 'current_workspace', None)
    members = []
    if workspace:
        members = WorkspaceMember.objects.filter(workspace=workspace).select_related('user')
    return render(request, 'core/team.html', {
        'members': members,
        'roles': WorkspaceRole.choices,
        'page_title': 'Team & Access Control'
    })

@login_required(login_url='login')
def settings_view(request):
    """Workspace configuration, branding, and integration settings."""
    return render(request, 'core/settings.html', {'page_title': 'Workspace Settings'})

@login_required(login_url='login')
def superadmin_view(request):
    """SuperAdmin multi-tenant monitoring and SaaS business metrics."""
    return render(request, 'core/superadmin.html', {'page_title': 'SuperAdmin Console'})

@login_required(login_url='login')
def ai_studio_view(request):
    """DevTeam Gemini AI Studio for automated task breakdown & estimation."""
    return render(request, 'ai/studio.html', {'page_title': 'AI Studio'})

@login_required(login_url='login')
def affiliates_view(request):
    """DevTeam Referral & Affiliate partner program."""
    return render(request, 'affiliates/index.html', {'page_title': 'Affiliate Program'})


def custom_bad_request_view(request, exception=None):
    if request.path.startswith('/api/'):
        return JsonResponse({"success": False, "message": "Bad request", "data": None, "errors": ["Invalid syntax or parameters"]}, status=400)
    return render(request, '404.html', {'error_code': '400', 'error_title': 'Bad Request', 'error_message': 'The request parameters were invalid.'}, status=400)


def custom_permission_denied_view(request, exception=None):
    if request.path.startswith('/api/'):
        return JsonResponse({"success": False, "message": "Permission denied", "data": None, "errors": ["You do not have permission to access this resource"]}, status=403)
    return render(request, '403.html', {'error_code': '403', 'error_title': 'Access Denied', 'error_message': 'You do not have permission to access this resource in this workspace.'}, status=403)


def custom_page_not_found_view(request, exception=None):
    if request.path.startswith('/api/'):
        return JsonResponse({"success": False, "message": "Resource not found", "data": None, "errors": ["The requested endpoint or object does not exist"]}, status=404)
    return render(request, '404.html', {'error_code': '404', 'error_title': 'Page Not Found', 'error_message': 'The requested page could not be located on DevTeam.'}, status=404)


def custom_server_error_view(request):
    if request.path.startswith('/api/'):
        return JsonResponse({"success": False, "message": "Internal server error", "data": None, "errors": ["An unexpected server error occurred. Our team has been notified."]}, status=500)
    return render(request, '500.html', {'error_code': '500', 'error_title': 'Server Error', 'error_message': 'An unexpected error occurred. Please try again shortly.'}, status=500)
