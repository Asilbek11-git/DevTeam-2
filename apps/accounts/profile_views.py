"""
Owner & SuperAdmin Profile Settings View.
Allows the business owner to maintain their professional information, skills, rate, and links.
"""
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from apps.core.validators import validate_image_file
from apps.core.permissions import get_active_workspace
from apps.activity.utils import log_activity
from apps.accounts.models import OwnerProfile

def _split_list(input_str):
    if not input_str:
        return []
    if isinstance(input_str, list):
        return input_str
    return [item.strip() for item in input_str.split(',') if item.strip()]

@login_required(login_url='login')
def owner_profile_view(request):
    """
    View and edit Owner / SuperAdmin profile information.
    """
    workspace, role = get_active_workspace(request)
    
    profile, created = OwnerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'username': request.user.username,
            'email': request.user.email,
            'professional_title': 'Full-Stack Software Architect & SaaS Engineer',
        }
    )
    
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', '').strip() or profile.full_name
        profile.professional_title = request.POST.get('professional_title', '').strip()
        profile.username = request.POST.get('username', '').strip() or profile.username
        profile.bio = request.POST.get('bio', '').strip()
        profile.location = request.POST.get('location', '').strip()
        profile.email = request.POST.get('email', '').strip() or profile.email
        profile.phone = request.POST.get('phone', '').strip()
        
        # Links
        profile.github_url = request.POST.get('github_url', '').strip()
        profile.gitlab_url = request.POST.get('gitlab_url', '').strip()
        profile.linkedin_url = request.POST.get('linkedin_url', '').strip()
        profile.telegram_url = request.POST.get('telegram_url', '').strip()
        profile.website_url = request.POST.get('website_url', '').strip()
        
        # Professional details
        exp_val = request.POST.get('years_of_experience')
        if exp_val:
            profile.years_of_experience = max(int(exp_val), 0)
            
        rate_val = request.POST.get('hourly_rate')
        if rate_val:
            profile.hourly_rate = Decimal(rate_val)
            
        profile.availability_status = request.POST.get('availability_status', profile.availability_status)
        profile.professional_status = request.POST.get('professional_status', '').strip()
        
        # Skills and Tech Stacks
        profile.skills = _split_list(request.POST.get('skills', ''))
        profile.programming_languages = _split_list(request.POST.get('programming_languages', ''))
        profile.frameworks = _split_list(request.POST.get('frameworks', ''))
        profile.databases = _split_list(request.POST.get('databases', ''))
        profile.tools = _split_list(request.POST.get('tools', ''))
        
        # Photo upload
        photo_file = request.FILES.get('profile_photo')
        if photo_file:
            try:
                validate_image_file(photo_file)
                profile.profile_photo = photo_file
            except ValidationError as e:
                messages.error(request, f"Profile photo upload error: {e.message}")
                return redirect('owner-profile')
                
        profile.save()
        
        if workspace:
            log_activity(
                workspace=workspace,
                actor=request.user,
                action='PROFILE_UPDATED',
                entity_type='OwnerProfile',
                entity_id=profile.id,
                description=f"Updated owner professional profile: {profile.full_name}",
                request=request
            )
            
        messages.success(request, "Owner profile updated successfully.")
        return redirect('owner-profile')
        
    return render(request, 'accounts/owner_profile.html', {
        'profile': profile,
        'availability_choices': OwnerProfile.AvailabilityStatus.choices,
        'skills_str': ", ".join(profile.skills) if isinstance(profile.skills, list) else "",
        'languages_str': ", ".join(profile.programming_languages) if isinstance(profile.programming_languages, list) else "",
        'frameworks_str': ", ".join(profile.frameworks) if isinstance(profile.frameworks, list) else "",
        'databases_str': ", ".join(profile.databases) if isinstance(profile.databases, list) else "",
        'tools_str': ", ".join(profile.tools) if isinstance(profile.tools, list) else "",
        'page_title': 'Owner Profile & Professional Settings',
    })
