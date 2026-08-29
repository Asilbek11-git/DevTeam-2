"""
Client & Lead CRM Views for DevTeam Workspace Owners & Managers.
Enforces strict workspace isolation and role-based permissions.
"""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden

from apps.core.permissions import get_active_workspace, manager_or_owner_required
from apps.activity.utils import log_activity
from apps.workspaces.models import Client, Lead, WorkspaceRole
from apps.billing.models import Service, Invoice
from apps.projects.models import Project

# ==========================================
# CLIENT MANAGEMENT VIEWS
# ==========================================

@login_required(login_url='login')
@manager_or_owner_required
def client_list_view(request):
    """List, search, filter, and paginate workspace clients."""
    workspace, role = get_active_workspace(request)
    
    status_filter = request.GET.get('status', 'ALL').upper()
    search_query = request.GET.get('q', '').strip()
    
    queryset = Client.objects.filter(workspace=workspace)
    
    if status_filter and status_filter != 'ALL':
        queryset = queryset.filter(status=status_filter)
        
    if search_query:
        queryset = queryset.filter(
            Q(full_name__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
        
    queryset = queryset.order_by('-created_at')
    
    # Aggregated metrics for header cards
    stats = {
        'total': Client.objects.filter(workspace=workspace).count(),
        'active': Client.objects.filter(workspace=workspace, status=Client.Status.ACTIVE).count(),
        'leads': Client.objects.filter(workspace=workspace, status=Client.Status.LEAD).count(),
        'archived': Client.objects.filter(workspace=workspace, status__in=[Client.Status.INACTIVE, Client.Status.ARCHIVED]).count(),
    }
    
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page', 1)
    clients_page = paginator.get_page(page_number)
    
    return render(request, 'clients/list.html', {
        'clients': clients_page,
        'stats': stats,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Client.Status.choices,
        'page_title': 'Clients CRM',
    })


@login_required(login_url='login')
@manager_or_owner_required
def client_create_view(request):
    """Create a new client in the active workspace."""
    workspace, role = get_active_workspace(request)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        company = request.POST.get('company', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        website = request.POST.get('website', '').strip()
        status = request.POST.get('status', Client.Status.ACTIVE)
        rating = int(request.POST.get('rating', 5) or 5)
        notes = request.POST.get('notes', '').strip()
        
        if not full_name:
            messages.error(request, "Client full name is required.")
        elif not email:
            messages.error(request, "Client email is required.")
        else:
            client = Client.objects.create(
                workspace=workspace,
                owner=request.user,
                full_name=full_name,
                company=company,
                email=email,
                phone=phone,
                website=website,
                status=status,
                rating=min(max(rating, 1), 5),
                notes=notes,
            )
            log_activity(
                workspace=workspace,
                actor=request.user,
                action='CLIENT_CREATED',
                entity_type='Client',
                entity_id=client.id,
                description=f"Created client '{client.full_name}' ({client.company or client.email})",
                request=request
            )
            messages.success(request, f"Client '{client.full_name}' created successfully.")
            return redirect('client-detail', id=client.id)
            
    return render(request, 'clients/create.html', {
        'status_choices': Client.Status.choices,
        'page_title': 'Add New Client',
    })


@login_required(login_url='login')
@manager_or_owner_required
def client_detail_view(request, id):
    """Client 360 view with projects, leads, invoices, notes, and activity."""
    workspace, role = get_active_workspace(request)
    client = get_object_or_404(Client, id=id, workspace=workspace)
    
    # Linked items within this workspace
    projects = Project.objects.filter(workspace=workspace).order_by('-created_at')[:5]
    leads = Lead.objects.filter(workspace=workspace, client=client).select_related('service').order_by('-created_at')
    invoices = Invoice.objects.filter(workspace=workspace).order_by('-created_at')[:5]
    services = Service.objects.filter(Q(workspace=workspace) | Q(workspace__isnull=True), is_active=True)
    
    total_deal_value = leads.aggregate(Sum('budget'))['budget__sum'] or Decimal('0.00')
    
    return render(request, 'clients/detail.html', {
        'client': client,
        'projects': projects,
        'leads': leads,
        'invoices': invoices,
        'services': services,
        'total_deal_value': total_deal_value,
        'page_title': f"Client: {client.full_name}",
    })


@login_required(login_url='login')
@manager_or_owner_required
def client_edit_view(request, id):
    """Update existing client information."""
    workspace, role = get_active_workspace(request)
    client = get_object_or_404(Client, id=id, workspace=workspace)
    
    if request.method == 'POST':
        client.full_name = request.POST.get('full_name', '').strip() or client.full_name
        client.company = request.POST.get('company', '').strip()
        client.email = request.POST.get('email', '').strip() or client.email
        client.phone = request.POST.get('phone', '').strip()
        client.website = request.POST.get('website', '').strip()
        client.status = request.POST.get('status', client.status)
        rating_val = request.POST.get('rating')
        if rating_val:
            client.rating = min(max(int(rating_val), 1), 5)
        client.notes = request.POST.get('notes', '').strip()
        client.save()
        
        log_activity(
            workspace=workspace,
            actor=request.user,
            action='CLIENT_UPDATED',
            entity_type='Client',
            entity_id=client.id,
            description=f"Updated profile for client '{client.full_name}'",
            request=request
        )
        messages.success(request, f"Client '{client.full_name}' updated successfully.")
        return redirect('client-detail', id=client.id)
        
    return render(request, 'clients/edit.html', {
        'client': client,
        'status_choices': Client.Status.choices,
        'page_title': f"Edit Client: {client.full_name}",
    })


@login_required(login_url='login')
@manager_or_owner_required
def client_archive_view(request, id):
    """Archive client."""
    workspace, role = get_active_workspace(request)
    client = get_object_or_404(Client, id=id, workspace=workspace)
    client.status = Client.Status.ARCHIVED
    client.save()
    messages.info(request, f"Client '{client.full_name}' has been archived.")
    return redirect('client-detail', id=client.id)


@login_required(login_url='login')
@manager_or_owner_required
def client_restore_view(request, id):
    """Restore archived client."""
    workspace, role = get_active_workspace(request)
    client = get_object_or_404(Client, id=id, workspace=workspace)
    client.status = Client.Status.ACTIVE
    client.save()
    messages.success(request, f"Client '{client.full_name}' has been restored to Active.")
    return redirect('client-detail', id=client.id)


# ==========================================
# LEAD CRM & PIPELINE VIEWS
# ==========================================

@login_required(login_url='login')
@manager_or_owner_required
def lead_list_view(request):
    """Lead pipeline with Kanban view and Table view."""
    workspace, role = get_active_workspace(request)
    
    view_mode = request.GET.get('view', 'kanban') # 'kanban' or 'table'
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'ALL')
    service_filter = request.GET.get('service', '')
    
    leads_qs = Lead.objects.filter(workspace=workspace).select_related('client', 'service')
    
    if search_query:
        leads_qs = leads_qs.filter(
            Q(title__icontains=search_query) |
            Q(client__full_name__icontains=search_query) |
            Q(client__company__icontains=search_query) |
            Q(source__icontains=search_query)
        )
        
    if status_filter and status_filter != 'ALL':
        leads_qs = leads_qs.filter(status=status_filter)
        
    if service_filter:
        leads_qs = leads_qs.filter(service_id=service_filter)
        
    leads_qs = leads_qs.order_by('-created_at')
    
    # Financial pipeline metrics
    total_leads_count = Lead.objects.filter(workspace=workspace).count()
    total_pipeline_val = Lead.objects.filter(workspace=workspace).aggregate(Sum('budget'))['budget__sum'] or Decimal('0.00')
    total_expected_rev = Lead.objects.filter(workspace=workspace).aggregate(Sum('expected_revenue'))['expected_revenue__sum'] or Decimal('0.00')
    won_leads_count = Lead.objects.filter(workspace=workspace, status__in=[Lead.Status.ACCEPTED, Lead.Status.IN_PROGRESS, Lead.Status.COMPLETED]).count()
    conversion_rate = (won_leads_count / total_leads_count * 100) if total_leads_count > 0 else 0.0

    # Group leads by stage for Kanban board
    kanban_stages = []
    for stage_code, stage_label in Lead.Status.choices:
        stage_leads = [lead for lead in leads_qs if lead.status == stage_code]
        stage_total = sum(lead.budget for lead in stage_leads)
        kanban_stages.append({
            'code': stage_code,
            'label': stage_label,
            'leads': stage_leads,
            'count': len(stage_leads),
            'total_value': stage_total,
        })
        
    services = Service.objects.filter(Q(workspace=workspace) | Q(workspace__isnull=True), is_active=True)
    
    paginator = Paginator(leads_qs, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    
    return render(request, 'leads/list.html', {
        'leads': page_obj,
        'kanban_stages': kanban_stages,
        'view_mode': view_mode,
        'search_query': search_query,
        'status_filter': status_filter,
        'service_filter': service_filter,
        'services': services,
        'status_choices': Lead.Status.choices,
        'stats': {
            'total_count': total_leads_count,
            'pipeline_value': total_pipeline_val,
            'expected_revenue': total_expected_rev,
            'won_count': won_leads_count,
            'conversion_rate': round(conversion_rate, 1),
        },
        'page_title': 'Lead & Order Pipeline',
    })


@login_required(login_url='login')
@manager_or_owner_required
def lead_create_view(request):
    """Create a new lead or deal inquiry."""
    workspace, role = get_active_workspace(request)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        client_id = request.POST.get('client_id')
        service_id = request.POST.get('service_id')
        budget = Decimal(request.POST.get('budget', '0.00') or '0.00')
        probability = int(request.POST.get('probability', '50') or 50)
        deadline = request.POST.get('deadline') or None
        status = request.POST.get('status', Lead.Status.NEW)
        source = request.POST.get('source', 'Direct Inquiry').strip()
        description = request.POST.get('description', '').strip()
        notes = request.POST.get('notes', '').strip()
        
        # Optional new client fields if creating inline
        new_client_name = request.POST.get('new_client_name', '').strip()
        new_client_email = request.POST.get('new_client_email', '').strip()
        new_client_company = request.POST.get('new_client_company', '').strip()
        
        if not title:
            messages.error(request, "Lead title is required.")
        else:
            client = None
            if client_id:
                client = Client.objects.filter(id=client_id, workspace=workspace).first()
            elif new_client_name and new_client_email:
                client = Client.objects.create(
                    workspace=workspace,
                    owner=request.user,
                    full_name=new_client_name,
                    email=new_client_email,
                    company=new_client_company,
                    status=Client.Status.LEAD
                )
                
            service = Service.objects.filter(id=service_id).first() if service_id else None
            
            lead = Lead.objects.create(
                workspace=workspace,
                client=client,
                service=service,
                title=title,
                budget=budget,
                probability=min(max(probability, 0), 100),
                deadline=deadline,
                status=status,
                source=source,
                description=description,
                notes=notes,
            )
            
            log_activity(
                workspace=workspace,
                actor=request.user,
                action='LEAD_CREATED',
                entity_type='Lead',
                entity_id=lead.id,
                description=f"Created deal/lead '{lead.title}' with budget ${lead.budget}",
                request=request
            )
            messages.success(request, f"Lead '{lead.title}' created successfully.")
            return redirect('lead-detail', id=lead.id)
            
    clients = Client.objects.filter(workspace=workspace).order_by('full_name')
    services = Service.objects.filter(Q(workspace=workspace) | Q(workspace__isnull=True), is_active=True)
    
    return render(request, 'leads/create.html', {
        'clients': clients,
        'services': services,
        'status_choices': Lead.Status.choices,
        'page_title': 'Add New Lead',
    })


@login_required(login_url='login')
@manager_or_owner_required
def lead_detail_view(request, id):
    """Lead detail view with stage transition actions and conversion workflow."""
    workspace, role = get_active_workspace(request)
    lead = get_object_or_404(Lead.objects.select_related('client', 'service'), id=id, workspace=workspace)
    clients = Client.objects.filter(workspace=workspace).order_by('full_name')
    services = Service.objects.filter(Q(workspace=workspace) | Q(workspace__isnull=True), is_active=True)
    
    return render(request, 'leads/detail.html', {
        'lead': lead,
        'clients': clients,
        'services': services,
        'status_choices': Lead.Status.choices,
        'page_title': f"Lead: {lead.title}",
    })


@login_required(login_url='login')
@manager_or_owner_required
def lead_edit_view(request, id):
    """Update existing lead details, status, probability, and budget."""
    workspace, role = get_active_workspace(request)
    lead = get_object_or_404(Lead, id=id, workspace=workspace)
    
    if request.method == 'POST':
        old_status = lead.status
        lead.title = request.POST.get('title', '').strip() or lead.title
        
        client_id = request.POST.get('client_id')
        if client_id:
            lead.client = Client.objects.filter(id=client_id, workspace=workspace).first()
        else:
            lead.client = None
            
        service_id = request.POST.get('service_id')
        lead.service = Service.objects.filter(id=service_id).first() if service_id else None
        
        budget_val = request.POST.get('budget')
        if budget_val:
            lead.budget = Decimal(budget_val)
            
        prob_val = request.POST.get('probability')
        if prob_val:
            lead.probability = min(max(int(prob_val), 0), 100)
            
        lead.deadline = request.POST.get('deadline') or None
        lead.status = request.POST.get('status', lead.status)
        lead.source = request.POST.get('source', lead.source).strip()
        lead.description = request.POST.get('description', '').strip()
        lead.notes = request.POST.get('notes', '').strip()
        lead.save()
        
        action_name = 'LEAD_STATUS_CHANGED' if old_status != lead.status else 'LEAD_UPDATED'
        log_activity(
            workspace=workspace,
            actor=request.user,
            action=action_name,
            entity_type='Lead',
            entity_id=lead.id,
            description=f"Updated lead '{lead.title}' (Stage: {lead.get_status_display()})",
            request=request
        )
        messages.success(request, f"Lead '{lead.title}' updated successfully.")
        return redirect('lead-detail', id=lead.id)
        
    clients = Client.objects.filter(workspace=workspace).order_by('full_name')
    services = Service.objects.filter(Q(workspace=workspace) | Q(workspace__isnull=True), is_active=True)
    
    return render(request, 'leads/edit.html', {
        'lead': lead,
        'clients': clients,
        'services': services,
        'status_choices': Lead.Status.choices,
        'page_title': f"Edit Lead: {lead.title}",
    })


@login_required(login_url='login')
@manager_or_owner_required
def lead_update_status_view(request, id):
    """Quickly update lead stage (e.g. via drag-and-drop or quick button)."""
    workspace, role = get_active_workspace(request)
    lead = get_object_or_404(Lead, id=id, workspace=workspace)
    
    new_status = request.POST.get('status') or request.GET.get('status')
    if new_status in dict(Lead.Status.choices):
        old_status = lead.status
        lead.status = new_status
        lead.save()
        log_activity(
            workspace=workspace,
            actor=request.user,
            action='LEAD_STATUS_CHANGED',
            entity_type='Lead',
            entity_id=lead.id,
            description=f"Changed stage of lead '{lead.title}' from {old_status} to {new_status}",
            request=request
        )
        messages.success(request, f"Lead stage changed to {lead.get_status_display()}.")
        
    return redirect('lead-detail', id=lead.id)


@login_required(login_url='login')
@manager_or_owner_required
def lead_convert_view(request, id):
    """
    Lead -> Client Conversion Workflow.
    Reuses existing client or creates new one, connects to workspace,
    and sets lead status to ACCEPTED atomically.
    """
    workspace, role = get_active_workspace(request)
    lead = get_object_or_404(Lead, id=id, workspace=workspace)
    
    if request.method == 'POST':
        client_option = request.POST.get('client_option', 'existing') # 'existing' or 'new'
        selected_client_id = request.POST.get('selected_client_id')
        
        new_name = request.POST.get('client_name', '').strip()
        new_company = request.POST.get('client_company', '').strip()
        new_email = request.POST.get('client_email', '').strip()
        new_phone = request.POST.get('client_phone', '').strip()
        
        with transaction.atomic():
            client = None
            if client_option == 'existing' and selected_client_id:
                client = Client.objects.filter(id=selected_client_id, workspace=workspace).first()
                if client:
                    client.status = Client.Status.ACTIVE
                    client.save()
            elif lead.client:
                client = lead.client
                client.status = Client.Status.ACTIVE
                client.save()
            else:
                # Create brand new Client
                if not new_name:
                    new_name = lead.title.replace("Inquiry", "").replace("Project", "").strip() or "Client Contact"
                if not new_email:
                    new_email = f"client-{lead.id}@deal.devteam"
                    
                client = Client.objects.create(
                    workspace=workspace,
                    owner=request.user,
                    full_name=new_name,
                    company=new_company,
                    email=new_email,
                    phone=new_phone,
                    status=Client.Status.ACTIVE,
                    notes=f"Converted from Lead #{lead.id}: {lead.title}\n{lead.notes}"
                )
                
            lead.client = client
            lead.status = Lead.Status.ACCEPTED
            lead.save()
            
            log_activity(
                workspace=workspace,
                actor=request.user,
                action='LEAD_CONVERTED',
                entity_type='Lead',
                entity_id=lead.id,
                description=f"Converted lead '{lead.title}' into active client '{client.full_name}'",
                request=request
            )
            
        messages.success(request, f"Lead successfully converted! Active Client '{client.full_name}' is linked.")
        return redirect('client-detail', id=client.id)
        
    clients = Client.objects.filter(workspace=workspace).order_by('full_name')
    return render(request, 'leads/convert_modal.html', {
        'lead': lead,
        'clients': clients,
        'page_title': f"Convert Lead: {lead.title}",
    })
