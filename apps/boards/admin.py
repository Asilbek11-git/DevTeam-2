from django.contrib import admin
from .models import Board, BoardColumn

class BoardColumnInline(admin.TabularInline):
    model = BoardColumn
    extra = 1

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'workspace', 'is_default')
    list_filter = ('is_default', 'workspace')
    search_fields = ('name', 'project__name')
    inlines = [BoardColumnInline]

@admin.register(BoardColumn)
class BoardColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'status_mapping', 'order', 'wip_limit')
    list_filter = ('board',)
    ordering = ('board', 'order')
