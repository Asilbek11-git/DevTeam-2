from django.contrib import admin
from .models import Workspace, WorkspaceMember, WorkspaceInvitation, Client, Lead

class WorkspaceMemberInline(admin.TabularInline):
    model = WorkspaceMember
    extra = 1

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'owner__email')
    list_filter = ('is_active',)
    inlines = [WorkspaceMemberInline]

@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'workspace', 'role', 'is_active', 'joined_at')
    list_filter = ('role', 'is_active', 'workspace')
    search_fields = ('user__email', 'workspace__name')

@admin.register(WorkspaceInvitation)
class WorkspaceInvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'workspace', 'role', 'status', 'invited_by', 'expires_at')
    list_filter = ('status', 'role')
    search_fields = ('email', 'workspace__name')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'email', 'phone', 'workspace', 'status', 'rating', 'created_at')
    list_filter = ('status', 'rating', 'workspace', 'created_at')
    search_fields = ('full_name', 'company', 'email', 'phone', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'workspace', 'service', 'budget', 'status', 'probability', 'expected_revenue', 'deadline')
    list_filter = ('status', 'workspace', 'source', 'deadline')
    search_fields = ('title', 'description', 'client__full_name', 'client__company', 'notes')
    readonly_fields = ('expected_revenue', 'created_at', 'updated_at')
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)

