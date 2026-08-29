from django.contrib import admin
from .models import RepositoryIntegration, GitCommit, GitPullRequest

@admin.register(RepositoryIntegration)
class RepositoryIntegrationAdmin(admin.ModelAdmin):
    list_display = ('repo_name', 'provider', 'project', 'workspace', 'is_active', 'last_synced_at')
    list_filter = ('provider', 'is_active', 'workspace')
    search_fields = ('repo_name', 'repo_url')

@admin.register(GitCommit)
class GitCommitAdmin(admin.ModelAdmin):
    list_display = ('commit_hash', 'integration', 'author_name', 'task', 'committed_at')
    search_fields = ('commit_hash', 'message', 'author_name', 'task__key')

@admin.register(GitPullRequest)
class GitPullRequestAdmin(admin.ModelAdmin):
    list_display = ('pr_number', 'title', 'integration', 'state', 'task', 'author')
    list_filter = ('state',)
    search_fields = ('title', 'task__key', 'author')
