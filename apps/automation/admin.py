from django.contrib import admin
from .models import AutomationRule

@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'workspace', 'trigger', 'action', 'is_active', 'execution_count')
    list_filter = ('trigger', 'action', 'is_active', 'workspace')
    search_fields = ('name', 'description')
