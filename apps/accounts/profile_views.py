"""
User Profile & Owner Professional Settings Views.
Handles role-specific profile management:
- Owner/SuperAdmin/Admin: Full OwnerProfile (21 fields, bio, portfolio, skills, hourly rate, links)
- Developer/Team Member: Engineering profile (name, username, email, job title, bio, github, gitlab, timezone, avatar)
- Client: Client portal profile (name, company, email, phone, website, address, avatar)
"""
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from apps.core.validators import validate_image_file
from apps.core.permissions import get_active_workspace
from apps.activity.utils import log_activity
from apps.accounts.models import OwnerProfile, User
from apps.workspaces.models import Client

def _split_list(input_str):
    if not input_str:
        return []
    if isinstance(input_str, list):
        return input_str
    return [item.strip() for item in input_str.split(',') if item.strip()]

@login_required(login_url='login')
def profile_dispatch_view(request):
    """
    Main profile router view.
    Dispatches to appropriate profile view based on the user's role:
    - Owner/SuperAdmin -> OwnerProfile view
    - Client -> ClientProfile view
    - Team Member -> UserProfile view
    """
    workspace, role = get_active_workspace(request)
    user = request.user
    
    if user.is_superuser or getattr(user, 'role', '') == 'SUPERADMIN' or role in ['OWNER', 'ADMIN']:
        return owner_profile_view(request)
    elif role == 'CLIENT' or getattr(user, 'role', '') == 'CLIENT':
        return client_profile_view(request)
    else:
        return user_profile_view(request)


@login_required(login_url='login')
def owner_profile_view(request):
    """
    View and edit Owner / SuperAdmin profile information.
    Includes all 21 approved fields for business, skills, rate, links, and avatar.
    """
    workspace, role = get_active_workspace(request)
    user = request.user
    
    # Safe get_or_create to guarantee profile always exists
    profile, created = OwnerProfile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'username': user.username,
            'email': user.email,
            'professional_title': 'Full-Stack Software Architect & SaaS Engineer',
            'professional_status': 'Available for New Projects & Consulting',
            'skills': ['Python', 'Django', 'TypeScript', 'React', 'Cloud Architecture'],
            'programming_languages': ['Python', 'TypeScript', 'SQL', 'Bash'],
            'frameworks': ['Django', 'React', 'FastAPI', 'Tailwind CSS'],
            'databases': ['PostgreSQL', 'Redis', 'SQLite'],
            'tools': ['Docker', 'Git', 'Linux', 'Celery', 'Nginx'],
            'years_of_experience': 5,
            'hourly_rate': Decimal('85.00'),
        }
    )
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        professional_title = request.POST.get('professional_title', '').strip()
        username = request.POST.get('username', '').strip()
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Links
        github_url = request.POST.get('github_url', '').strip()
        gitlab_url = request.POST.get('gitlab_url', '').strip()
        linkedin_url = request.POST.get('linkedin_url', '').strip()
        telegram_url = request.POST.get('telegram_url', '').strip()
        website_url = request.POST.get('website_url', '').strip()
        
        # Professional details
        exp_val = request.POST.get('years_of_experience')
        rate_val = request.POST.get('hourly_rate')
        availability_status = request.POST.get('availability_status', profile.availability_status)
        professional_status = request.POST.get('professional_status', '').strip()
        
        # Skills and Tech Stacks
        skills = _split_list(request.POST.get('skills', ''))
        programming_languages = _split_list(request.POST.get('programming_languages', ''))
        frameworks = _split_list(request.POST.get('frameworks', ''))
        databases = _split_list(request.POST.get('databases', ''))
        tools = _split_list(request.POST.get('tools', ''))
        
        # Validation and assignment
        profile.full_name = full_name or profile.full_name
        profile.professional_title = professional_title or profile.professional_title
        profile.username = username or profile.username
        profile.bio = bio
        profile.location = location
        profile.email = email or profile.email
        profile.phone = phone
        
        profile.github_url = github_url
        profile.gitlab_url = gitlab_url
        profile.linkedin_url = linkedin_url
        profile.telegram_url = telegram_url
        profile.website_url = website_url
        
        if exp_val:
            try:
                profile.years_of_experience = max(int(exp_val), 0)
            except ValueError:
                pass
                
        if rate_val:
            try:
                profile.hourly_rate = Decimal(rate_val)
            except Exception:
                pass
                
        if availability_status in dict(OwnerProfile.Availability.choices):
            profile.availability_status = availability_status
            
        profile.professional_status = professional_status
        
        profile.skills = skills
        profile.programming_languages = programming_languages
        profile.frameworks = frameworks
        profile.databases = databases
        profile.tools = tools
        
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
        
        # Keep user model synchronized
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        if email:
            user.email = email
        user.save()
        
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
        'availability_choices': OwnerProfile.Availability.choices,
        'skills_str': ", ".join(profile.skills) if isinstance(profile.skills, list) else "",
        'languages_str': ", ".join(profile.programming_languages) if isinstance(profile.programming_languages, list) else "",
        'frameworks_str': ", ".join(profile.frameworks) if isinstance(profile.frameworks, list) else "",
        'databases_str': ", ".join(profile.databases) if isinstance(profile.databases, list) else "",
        'tools_str': ", ".join(profile.tools) if isinstance(profile.tools, list) else "",
        'page_title': 'Owner Profile & Professional Settings',
        'is_owner_or_admin': True,
    })


@login_required(login_url='login')
def user_profile_view(request):
    """
    Team Member / Developer profile view and edit.
    Allows viewing/updating individual account details safely.
    """
    workspace, role = get_active_workspace(request)
    user = request.user
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        job_title = request.POST.get('job_title', '').strip()
        bio = request.POST.get('bio', '').strip()
        github_username = request.POST.get('github_username', '').strip()
        gitlab_username = request.POST.get('gitlab_username', '').strip()
        timezone_val = request.POST.get('timezone', 'UTC').strip()
        
        user.first_name = first_name
        user.last_name = last_name
        user.job_title = job_title
        user.bio = bio
        user.github_username = github_username
        user.gitlab_username = gitlab_username
        user.timezone = timezone_val
        
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            try:
                validate_image_file(avatar_file)
                user.avatar = avatar_file
            except ValidationError as e:
                messages.error(request, f"Avatar upload error: {e.message}")
                return redirect('user-profile')
                
        user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('user-profile')
        
    return render(request, 'accounts/user_profile.html', {
        'user_obj': user,
        'role': role or 'DEVELOPER',
        'page_title': 'Developer Profile & Settings',
        'is_owner_or_admin': False,
    })


@login_required(login_url='login')
def client_profile_view(request):
    """
    Client Portal profile view and edit.
    Allows client users to update their company and contact information.
    """
    workspace, role = get_active_workspace(request)
    user = request.user
    
    client_record = None
    if workspace:
        client_record = Client.objects.filter(
            user=user,
            workspace=workspace
        ).first() or Client.objects.filter(
            email__iexact=user.email,
            workspace=workspace
        ).first()
        
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        website = request.POST.get('website', '').strip()
        address = request.POST.get('address', '').strip()
        
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
                
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            try:
                validate_image_file(avatar_file)
                user.avatar = avatar_file
            except ValidationError as e:
                messages.error(request, f"Photo upload error: {e.message}")
                return redirect('user-profile')
                
        user.save()
        
        if client_record:
            client_record.full_name = full_name or client_record.full_name
            client_record.company_name = company_name
            client_record.phone = phone
            client_record.website = website
            client_record.address = address
            client_record.save()
            
        messages.success(request, "Client profile updated successfully.")
        return redirect('user-profile')
        
    return render(request, 'accounts/client_profile.html', {
        'user_obj': user,
        'client_record': client_record,
        'role': 'CLIENT',
        'page_title': 'Client Account & Company Profile',
        'is_owner_or_admin': False,
    })
