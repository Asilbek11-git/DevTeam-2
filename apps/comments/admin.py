from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'workspace', 'is_edited', 'created_at')
    list_filter = ('is_edited', 'workspace')
    search_fields = ('content', 'task__key', 'author__email')
