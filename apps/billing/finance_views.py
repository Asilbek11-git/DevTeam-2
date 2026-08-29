"""
Finance Analytics & Expense Management Views for DevTeam SaaS.
Calculates real revenue, expenses, net profit, and financial breakdown using Django ORM.
"""
from decimal import Decimal
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone

from apps.core.permissions import get_active_workspace, owner_required
from apps.activity.utils import log_activity
from apps.billing.models import Expense, Invoice, Subscription

@login_required(login_url='login')
@owner_required
def finance_dashboard_view(request):
    """
    Executive Financial Overview Dashboard.
    Real PostgreSQL/Django ORM data calculations.
    """
    workspace, role = get_active_workspace(request)
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Invoices (Revenue)
    paid_invoices = Invoice.objects.filter(workspace=workspace, status=Invoice.Status.PAID)
    pending_invoices = Invoice.objects.filter(workspace=workspace, status=Invoice.Status.DRAFT)
    
    total_revenue = paid_invoices.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    month_revenue = paid_invoices.filter(paid_at__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    year_revenue = paid_invoices.filter(paid_at__gte=start_of_year).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    pending_receivables = pending_invoices.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Expenses
    expenses_qs = Expense.objects.filter(workspace=workspace)
    total_expenses = expenses_qs.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    month_expenses = expenses_qs.filter(expense_date__gte=start_of_month.date()).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Net Profit
    net_profit = total_revenue - total_expenses
    month_net_profit = month_revenue - month_expenses
    profit_margin = ((net_profit / total_revenue) * 100) if total_revenue > 0 else Decimal('0.0')
    
    # Expenses by Category Breakdown
    category_totals = []
    for cat_code, cat_label in Expense.Category.choices:
        cat_sum = expenses_qs.filter(category=cat_code).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        percentage = (cat_sum / total_expenses * 100) if total_expenses > 0 else 0
        category_totals.append({
            'code': cat_code,
            'label': cat_label,
            'amount': cat_sum,
            'percentage': round(percentage, 1),
        })
        
    # Recent financial items
    recent_invoices = Invoice.objects.filter(workspace=workspace).order_by('-created_at')[:6]
    recent_expenses = expenses_qs.order_by('-expense_date', '-created_at')[:6]
    
    # Monthly history (last 6 months)
    monthly_history = []
    for i in range(5, -1, -1):
        target_month_date = (now.replace(day=1) - timedelta(days=i*30)).replace(day=1)
        next_month_date = (target_month_date + timedelta(days=32)).replace(day=1)
        
        m_rev = paid_invoices.filter(
            paid_at__gte=target_month_date,
            paid_at__lt=next_month_date
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        m_exp = expenses_qs.filter(
            expense_date__gte=target_month_date.date(),
            expense_date__lt=next_month_date.date()
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        monthly_history.append({
            'month_name': target_month_date.strftime('%b %Y'),
            'revenue': float(m_rev),
            'expense': float(m_exp),
            'profit': float(m_rev - m_exp)
        })
        
    return render(request, 'finance/dashboard.html', {
        'total_revenue': total_revenue,
        'month_revenue': month_revenue,
        'year_revenue': year_revenue,
        'pending_receivables': pending_receivables,
        'total_expenses': total_expenses,
        'month_expenses': month_expenses,
        'net_profit': net_profit,
        'month_net_profit': month_net_profit,
        'profit_margin': round(profit_margin, 1),
        'category_totals': category_totals,
        'recent_invoices': recent_invoices,
        'recent_expenses': recent_expenses,
        'monthly_history': monthly_history,
        'page_title': 'Financial Command Center',
    })


@login_required(login_url='login')
@owner_required
def expense_list_view(request):
    """List, search, filter, and paginate business expenses."""
    workspace, role = get_active_workspace(request)
    
    category_filter = request.GET.get('category', 'ALL')
    search_query = request.GET.get('q', '').strip()
    
    expenses_qs = Expense.objects.filter(workspace=workspace)
    
    if category_filter and category_filter != 'ALL':
        expenses_qs = expenses_qs.filter(category=category_filter)
        
    if search_query:
        expenses_qs = expenses_qs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        
    expenses_qs = expenses_qs.order_by('-expense_date', '-created_at')
    
    total_filtered_amount = expenses_qs.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_all_expenses = Expense.objects.filter(workspace=workspace).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    paginator = Paginator(expenses_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    
    return render(request, 'finance/expenses_list.html', {
        'expenses': page_obj,
        'total_filtered_amount': total_filtered_amount,
        'total_all_expenses': total_all_expenses,
        'category_filter': category_filter,
        'search_query': search_query,
        'category_choices': Expense.Category.choices,
        'page_title': 'Business Expenses',
    })


@login_required(login_url='login')
@owner_required
def expense_create_view(request):
    """Log a new business expense."""
    workspace, role = get_active_workspace(request)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        amount_val = request.POST.get('amount', '0.00')
        category = request.POST.get('category', Expense.Category.OTHER)
        expense_date = request.POST.get('expense_date') or timezone.now().date()
        description = request.POST.get('description', '').strip()
        
        if not title:
            messages.error(request, "Expense title is required.")
        elif not amount_val or Decimal(amount_val) <= 0:
            messages.error(request, "A valid positive amount is required.")
        else:
            expense = Expense.objects.create(
                workspace=workspace,
                owner=request.user,
                title=title,
                amount=Decimal(amount_val),
                category=category,
                expense_date=expense_date,
                description=description,
            )
            log_activity(
                workspace=workspace,
                actor=request.user,
                action='EXPENSE_CREATED',
                entity_type='Expense',
                entity_id=expense.id,
                description=f"Logged expense '{expense.title}' (${expense.amount}) in category {expense.get_category_display()}",
                request=request
            )
            messages.success(request, f"Expense '{expense.title}' (${expense.amount}) logged successfully.")
            return redirect('expense-list')
            
    return render(request, 'finance/expense_form.html', {
        'category_choices': Expense.Category.choices,
        'today_date': timezone.now().date().isoformat(),
        'is_edit': False,
        'page_title': 'Log Business Expense',
    })


@login_required(login_url='login')
@owner_required
def expense_edit_view(request, id):
    """Edit existing expense."""
    workspace, role = get_active_workspace(request)
    expense = get_object_or_404(Expense, id=id, workspace=workspace)
    
    if request.method == 'POST':
        expense.title = request.POST.get('title', '').strip() or expense.title
        amount_val = request.POST.get('amount')
        if amount_val and Decimal(amount_val) > 0:
            expense.amount = Decimal(amount_val)
        expense.category = request.POST.get('category', expense.category)
        date_val = request.POST.get('expense_date')
        if date_val:
            expense.expense_date = date_val
        expense.description = request.POST.get('description', '').strip()
        expense.save()
        
        log_activity(
            workspace=workspace,
            actor=request.user,
            action='EXPENSE_UPDATED',
            entity_type='Expense',
            entity_id=expense.id,
            description=f"Updated expense '{expense.title}' (${expense.amount})",
            request=request
        )
        messages.success(request, f"Expense '{expense.title}' updated successfully.")
        return redirect('expense-list')
        
    return render(request, 'finance/expense_form.html', {
        'expense': expense,
        'category_choices': Expense.Category.choices,
        'is_edit': True,
        'page_title': f"Edit Expense: {expense.title}",
    })


@login_required(login_url='login')
@owner_required
def expense_delete_view(request, id):
    """Delete expense."""
    workspace, role = get_active_workspace(request)
    expense = get_object_or_404(Expense, id=id, workspace=workspace)
    title = expense.title
    amount = expense.amount
    expense.delete()
    messages.success(request, f"Expense '{title}' (${amount}) has been removed.")
    return redirect('expense-list')
