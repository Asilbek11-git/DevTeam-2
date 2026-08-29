from django.contrib import admin
from .models import Project, Milestone

class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'workspace', 'status', 'health', 'owner', 'lead', 'deadline')
    list_filter = ('status', 'health', 'workspace')
    search_fields = ('key', 'name', 'description')
    inlines = [MilestoneInline]

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'deadline', 'status')
    list_filter = ('status', 'project')
    search_fields = ('name', 'project__name')
