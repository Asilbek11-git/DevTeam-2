"""
VCS Integrations (GitHub, GitLab, Bitbucket) Models & Webhook Bindings.
"""
from django.db import models
from apps.core.models import TenantScopedModel

class VCSProvider(models.TextChoices):
    GITHUB = 'GITHUB', 'GitHub'
    GITLAB = 'GITLAB', 'GitLab'
    BITBUCKET = 'BITBUCKET', 'Bitbucket'

class RepositoryIntegration(TenantScopedModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='vcs_integrations')
    provider = models.CharField(max_length=20, choices=VCSProvider.choices, default=VCSProvider.GITHUB)
    repo_name = models.CharField(max_length=255) # e.g. "org/backend-api"
    repo_url = models.URLField()
    webhook_secret = models.CharField(max_length=128, blank=True)
    access_token = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.provider} ({self.repo_name}) -> {self.project.key}"

class GitCommit(TenantScopedModel):
    integration = models.ForeignKey(RepositoryIntegration, on_delete=models.CASCADE, related_name='commits')
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='git_commits')
    commit_hash = models.CharField(max_length=64, db_index=True)
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    message = models.TextField()
    url = models.URLField(blank=True)
    committed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.commit_hash[:7]} - {self.message[:50]}"

class GitPullRequest(TenantScopedModel):
    class State(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        MERGED = 'MERGED', 'Merged'
        CLOSED = 'CLOSED', 'Closed'

    integration = models.ForeignKey(RepositoryIntegration, on_delete=models.CASCADE, related_name='pull_requests')
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='git_pull_requests')
    pr_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    source_branch = models.CharField(max_length=150)
    target_branch = models.CharField(max_length=150)
    state = models.CharField(max_length=20, choices=State.choices, default=State.OPEN)
    author = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"PR #{self.pr_number}: {self.title} ({self.state})"
