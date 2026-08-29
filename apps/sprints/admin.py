from django.contrib import admin
from .models import Sprint

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'start_date', 'end_date', 'total_story_points', 'completed_story_points', 'velocity')
    list_filter = ('status', 'project', 'workspace')
    search_fields = ('name', 'goal', 'project__name')
