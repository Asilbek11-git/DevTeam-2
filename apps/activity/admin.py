from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'entity_type', 'actor', 'workspace', 'created_at')
    list_filter = ('action', 'entity_type', 'workspace')
    search_fields = ('description', 'actor__email', 'entity_id')
    readonly_fields = ('created_at', 'updated_at')
