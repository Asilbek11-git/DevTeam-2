"""
Services catalog management views for DevTeam Workspace.
"""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
import uuid

from apps.core.permissions import get_active_workspace, manager_or_owner_required
from apps.activity.utils import log_activity
from apps.billing.models import Service

@login_required(login_url='login')
@manager_or_owner_required
def service_list_view(request):
    """List all workspace services and packages."""
    workspace, role = get_active_workspace(request)
    
    services = Service.objects.filter(
        Q(workspace=workspace) | Q(workspace__isnull=True)
    ).order_by('display_order', 'name')
    
    active_count = services.filter(is_active=True).count()
    
    return render(request, 'services/list.html', {
        'services': services,
        'active_count': active_count,
        'total_count': services.count(),
        'page_title': 'Services Catalog',
    })


@login_required(login_url='login')
@manager_or_owner_required
def service_create_view(request):
    """Create a new service offering in workspace."""
    workspace, role = get_active_workspace(request)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        starting_price = Decimal(request.POST.get('starting_price', '0.00') or '0.00')
        estimated_delivery_days = int(request.POST.get('estimated_delivery_days', '14') or 14)
        tech_input = request.POST.get('technologies', '')
        is_active = request.POST.get('is_active') == 'on'
        display_order = int(request.POST.get('display_order', '0') or 0)
        
        technologies = [t.strip() for t in tech_input.split(',') if t.strip()] if isinstance(tech_input, str) else []
        
        if not name:
            messages.error(request, "Service name is required.")
        else:
            base_slug = slugify(name) or 'service'
            slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
            
            service = Service.objects.create(
                workspace=workspace,
                owner=request.user,
                name=name,
                slug=slug,
                description=description,
                starting_price=starting_price,
                estimated_delivery_days=estimated_delivery_days,
                technologies=technologies,
                is_active=is_active,
                display_order=display_order,
            )
            log_activity(
                workspace=workspace,
                actor=request.user,
                action='SERVICE_CREATED',
                entity_type='Service',
                entity_id=service.id,
                description=f"Created service offering '{service.name}' (${service.starting_price})",
                request=request
            )
            messages.success(request, f"Service '{service.name}' added successfully.")
            return redirect('service-list')
            
    return render(request, 'services/form.html', {
        'is_edit': False,
        'page_title': 'Add New Service',
    })


@login_required(login_url='login')
@manager_or_owner_required
def service_edit_view(request, id):
    """Edit service offering."""
    workspace, role = get_active_workspace(request)
    service = get_object_or_404(Service, id=id, workspace=workspace)
    
    if request.method == 'POST':
        service.name = request.POST.get('name', '').strip() or service.name
        service.description = request.POST.get('description', '').strip()
        
        price_val = request.POST.get('starting_price')
        if price_val:
            service.starting_price = Decimal(price_val)
            
        days_val = request.POST.get('estimated_delivery_days')
        if days_val:
            service.estimated_delivery_days = int(days_val)
            
        tech_input = request.POST.get('technologies', '')
        if tech_input:
            service.technologies = [t.strip() for t in tech_input.split(',') if t.strip()]
        else:
            service.technologies = []
            
        service.is_active = request.POST.get('is_active') == 'on'
        order_val = request.POST.get('display_order')
        if order_val:
            service.display_order = int(order_val)
            
        service.save()
        log_activity(
            workspace=workspace,
            actor=request.user,
            action='SERVICE_UPDATED',
            entity_type='Service',
            entity_id=service.id,
            description=f"Updated service offering '{service.name}'",
            request=request
        )
        messages.success(request, f"Service '{service.name}' updated successfully.")
        return redirect('service-list')
        
    tech_str = ", ".join(service.technologies) if isinstance(service.technologies, list) else ""
    return render(request, 'services/form.html', {
        'service': service,
        'technologies_str': tech_str,
        'is_edit': True,
        'page_title': f"Edit Service: {service.name}",
    })


@login_required(login_url='login')
@manager_or_owner_required
def service_toggle_active_view(request, id):
    """Toggle service active status."""
    workspace, role = get_active_workspace(request)
    service = get_object_or_404(Service, id=id, workspace=workspace)
    service.is_active = not service.is_active
    service.save()
    status_str = "activated" if service.is_active else "deactivated"
    messages.info(request, f"Service '{service.name}' {status_str}.")
    return redirect('service-list')


@login_required(login_url='login')
@manager_or_owner_required
def service_delete_view(request, id):
    """Delete service offering."""
    workspace, role = get_active_workspace(request)
    service = get_object_or_404(Service, id=id, workspace=workspace)
    name = service.name
    service.delete()
    messages.success(request, f"Service '{name}' has been deleted.")
    return redirect('service-list')
