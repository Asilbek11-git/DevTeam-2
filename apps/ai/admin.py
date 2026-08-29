from django.contrib import admin
from .models import AIUsageLog

@admin.register(AIUsageLog)
class AIUsageLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'workspace', 'action_type', 'model_name', 'prompt_tokens', 'completion_tokens', 'created_at')
    list_filter = ('action_type', 'model_name', 'workspace')
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)
