"""
Portfolio Management (Private) and Public Showcase Views for DevTeam.
Enforces secure file uploads, data privacy, and public SEO showcase.
"""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import uuid

from apps.core.validators import validate_image_file, sanitize_filename
from apps.core.permissions import get_active_workspace, owner_required
from apps.activity.utils import log_activity
from apps.accounts.models import PortfolioItem, OwnerProfile, User

# ==========================================
# PUBLIC PORTFOLIO SHOWCASE (ANONYMOUS ACCESSIBLE)
# ==========================================

def public_portfolio_list_view(request):
    """
    Public-facing portfolio showcase.
    Only shows is_published=True projects.
    """
    # Fetch owner profile for header display if available
    owner_profile = OwnerProfile.objects.first()
    
    tech_filter = request.GET.get('tech', '').strip()
    
    portfolio_items = PortfolioItem.objects.filter(is_published=True).order_by('-is_featured', '-completion_date', '-created_at')
    
    if tech_filter:
        portfolio_items = [p for p in portfolio_items if tech_filter.lower() in [t.lower() for t in p.technologies]]
        
    # Extract distinct list of technologies
    all_techs = set()
    for item in PortfolioItem.objects.filter(is_published=True):
        if isinstance(item.technologies, list):
            for t in item.technologies:
                all_techs.add(t.strip())
                
    return render(request, 'portfolio/public_list.html', {
        'portfolio_items': portfolio_items,
        'owner_profile': owner_profile,
        'all_technologies': sorted(list(all_techs)),
        'selected_tech': tech_filter,
        'page_title': f"{owner_profile.full_name if owner_profile else 'DevTeam'} — Portfolio & Case Studies",
    })


def public_portfolio_detail_view(request, slug):
    """
    Public single case study / project detail view.
    """
    item = get_object_or_404(PortfolioItem, slug=slug, is_published=True)
    owner_profile = OwnerProfile.objects.filter(user=item.owner).first() or OwnerProfile.objects.first()
    
    related_items = PortfolioItem.objects.filter(
        is_published=True
    ).exclude(id=item.id).order_by('-is_featured', '-created_at')[:3]
    
    return render(request, 'portfolio/public_detail.html', {
        'item': item,
        'owner_profile': owner_profile,
        'related_items': related_items,
        'page_title': f"{item.title} — Case Study",
    })


# ==========================================
# PRIVATE PORTFOLIO MANAGEMENT (AUTHENTICATED)
# ==========================================

@login_required(login_url='login')
def portfolio_manage_list_view(request):
    """Portfolio management table for Owner/Admin."""
    items = PortfolioItem.objects.filter(owner=request.user).order_by('-created_at')
    
    published_count = items.filter(is_published=True).count()
    featured_count = items.filter(is_featured=True).count()
    
    return render(request, 'portfolio/manage_list.html', {
        'items': items,
        'published_count': published_count,
        'featured_count': featured_count,
        'total_count': items.count(),
        'page_title': 'Manage Portfolio Projects',
    })


@login_required(login_url='login')
def portfolio_create_view(request):
    """Create a new portfolio item with cover image upload."""
    workspace, role = get_active_workspace(request)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        short_description = request.POST.get('short_description', '').strip()
        description = request.POST.get('description', '').strip()
        tech_input = request.POST.get('technologies', '')
        github_url = request.POST.get('github_url', '').strip()
        live_demo_url = request.POST.get('live_demo_url', '').strip()
        client_type = request.POST.get('client_type', '').strip()
        completion_date = request.POST.get('completion_date') or None
        project_val = request.POST.get('project_value')
        results = request.POST.get('results', '').strip()
        is_featured = request.POST.get('is_featured') == 'on'
        is_published = request.POST.get('is_published') == 'on'
        
        image_file = request.FILES.get('image')
        
        technologies = [t.strip() for t in tech_input.split(',') if t.strip()] if isinstance(tech_input, str) else []
        
        if not title:
            messages.error(request, "Project title is required.")
        else:
            try:
                if image_file:
                    validate_image_file(image_file)
                    
                base_slug = slugify(title) or 'project'
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
                
                project_value = Decimal(project_val) if project_val else None
                
                item = PortfolioItem.objects.create(
                    owner=request.user,
                    title=title,
                    slug=unique_slug,
                    short_description=short_description,
                    description=description,
                    image=image_file,
                    technologies=technologies,
                    github_url=github_url,
                    live_demo_url=live_demo_url,
                    client_type=client_type,
                    completion_date=completion_date,
                    project_value=project_value,
                    results=results,
                    is_featured=is_featured,
                    is_published=is_published,
                )
                
                if workspace:
                    log_activity(
                        workspace=workspace,
                        actor=request.user,
                        action='PORTFOLIO_CREATED',
                        entity_type='PortfolioItem',
                        entity_id=item.id,
                        description=f"Created portfolio project '{item.title}' (Published: {item.is_published})",
                        request=request
                    )
                    
                messages.success(request, f"Portfolio item '{item.title}' created successfully.")
                return redirect('portfolio-manage')
            except ValidationError as e:
                messages.error(request, f"File validation error: {e.message}")
            except Exception as e:
                messages.error(request, f"Failed to create project: {e}")
                
    return render(request, 'portfolio/form.html', {
        'is_edit': False,
        'page_title': 'Add Portfolio Project',
    })


@login_required(login_url='login')
def portfolio_edit_view(request, id):
    """Edit existing portfolio project."""
    workspace, role = get_active_workspace(request)
    item = get_object_or_404(PortfolioItem, id=id, owner=request.user)
    
    if request.method == 'POST':
        item.title = request.POST.get('title', '').strip() or item.title
        item.short_description = request.POST.get('short_description', '').strip()
        item.description = request.POST.get('description', '').strip()
        
        tech_input = request.POST.get('technologies', '')
        if tech_input:
            item.technologies = [t.strip() for t in tech_input.split(',') if t.strip()]
        else:
            item.technologies = []
            
        item.github_url = request.POST.get('github_url', '').strip()
        item.live_demo_url = request.POST.get('live_demo_url', '').strip()
        item.client_type = request.POST.get('client_type', '').strip()
        item.completion_date = request.POST.get('completion_date') or None
        
        project_val = request.POST.get('project_value')
        item.project_value = Decimal(project_val) if project_val else None
        
        item.results = request.POST.get('results', '').strip()
        item.is_featured = request.POST.get('is_featured') == 'on'
        item.is_published = request.POST.get('is_published') == 'on'
        
        new_image = request.FILES.get('image')
        if new_image:
            try:
                validate_image_file(new_image)
                item.image = new_image
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return redirect('portfolio-edit', id=item.id)
                
        item.save()
        
        if workspace:
            log_activity(
                workspace=workspace,
                actor=request.user,
                action='PORTFOLIO_UPDATED',
                entity_type='PortfolioItem',
                entity_id=item.id,
                description=f"Updated portfolio item '{item.title}'",
                request=request
            )
            
        messages.success(request, f"Portfolio item '{item.title}' updated successfully.")
        return redirect('portfolio-manage')
        
    tech_str = ", ".join(item.technologies) if isinstance(item.technologies, list) else ""
    return render(request, 'portfolio/form.html', {
        'item': item,
        'technologies_str': tech_str,
        'is_edit': True,
        'page_title': f"Edit Portfolio: {item.title}",
    })


@login_required(login_url='login')
def portfolio_delete_view(request, id):
    """Delete portfolio item."""
    item = get_object_or_404(PortfolioItem, id=id, owner=request.user)
    title = item.title
    item.delete()
    messages.success(request, f"Portfolio item '{title}' has been deleted.")
    return redirect('portfolio-manage')
