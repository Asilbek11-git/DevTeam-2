from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserSession, OwnerProfile, PortfolioItem

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'role', 'is_verified', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_verified')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'job_title', 'bio', 'avatar')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Integrations & 2FA', {'fields': ('github_username', 'gitlab_username', 'two_factor_enabled', 'referral_code', 'referred_by')}),
        ('Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'device', 'location', 'is_active', 'last_activity')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'ip_address', 'user_agent')

@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'professional_title', 'availability_status', 'hourly_rate', 'years_of_experience', 'updated_at')
    list_filter = ('availability_status', 'created_at')
    search_fields = ('full_name', 'user__email', 'professional_title', 'skills')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Account Link', {'fields': ('user', 'full_name', 'professional_title', 'username', 'profile_photo')}),
        ('Contact & Links', {'fields': ('email', 'phone', 'location', 'website_url', 'github_url', 'gitlab_url', 'linkedin_url', 'telegram_url')}),
        ('Professional Bio & Status', {'fields': ('bio', 'professional_status', 'availability_status', 'hourly_rate', 'years_of_experience')}),
        ('Technical Stack (JSON)', {'fields': ('skills', 'programming_languages', 'frameworks', 'databases', 'tools')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'client_type', 'is_featured', 'is_published', 'completion_date', 'project_value')
    list_filter = ('is_featured', 'is_published', 'completion_date')
    search_fields = ('title', 'short_description', 'description', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'completion_date'
    ordering = ('-is_featured', '-completion_date')

