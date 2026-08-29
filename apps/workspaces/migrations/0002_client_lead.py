# Generated for DevTeam Phase 1 Foundation

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0002_service_expense"),
        ("workspaces", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "full_name",
                    models.CharField(
                        db_index=True,
                        max_length=200,
                        verbose_name="Contact Full Name",
                    ),
                ),
                (
                    "company",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name="Company / Organization",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True,
                        max_length=254,
                        verbose_name="Contact Email",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Phone Number"
                    ),
                ),
                (
                    "website",
                    models.URLField(blank=True, verbose_name="Company Website"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("LEAD", "Lead"),
                            ("ACTIVE", "Active Client"),
                            ("INACTIVE", "Inactive Client"),
                            ("ARCHIVED", "Archived"),
                        ],
                        db_index=True,
                        default="ACTIVE",
                        max_length=20,
                        verbose_name="Client Status",
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        default=5,
                        help_text="Internal client score from 1 to 5",
                        verbose_name="Client Rating (1-5)",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, verbose_name="Internal Notes & History"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="managed_clients",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Account Owner / Manager",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        help_text="Optional registered user account for client portal access",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="client_profiles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Client Portal User",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clients",
                        to="workspaces.workspace",
                        verbose_name="Workspace",
                    ),
                ),
            ],
            options={
                "verbose_name": "Client",
                "verbose_name_plural": "Clients",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Lead",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        verbose_name="Lead / Deal Title",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, verbose_name="Scope & Requirements"
                    ),
                ),
                (
                    "budget",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        verbose_name="Estimated Budget ($)",
                    ),
                ),
                (
                    "deadline",
                    models.DateField(
                        blank=True, null=True, verbose_name="Target Deadline"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "New Lead"),
                            ("CONTACTED", "Contacted"),
                            ("NEGOTIATION", "In Negotiation"),
                            ("ACCEPTED", "Accepted / Won"),
                            ("IN_PROGRESS", "In Progress"),
                            ("COMPLETED", "Completed"),
                            ("CANCELLED", "Cancelled / Lost"),
                        ],
                        db_index=True,
                        default="NEW",
                        max_length=30,
                        verbose_name="Pipeline Stage",
                    ),
                ),
                (
                    "probability",
                    models.PositiveSmallIntegerField(
                        default=50,
                        help_text="Estimated close probability percentage (0-100)",
                        verbose_name="Win Probability (%)",
                    ),
                ),
                (
                    "expected_revenue",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        verbose_name="Expected Revenue ($)",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        default="Direct Inquiry",
                        help_text="e.g. Upwork, LinkedIn, Telegram, Referral, Organic",
                        max_length=100,
                        verbose_name="Lead Source",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, verbose_name="Negotiation Notes"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="leads",
                        to="workspaces.client",
                        verbose_name="Associated Client",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="leads",
                        to="billing.service",
                        verbose_name="Requested Service",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leads",
                        to="workspaces.workspace",
                        verbose_name="Workspace",
                    ),
                ),
            ],
            options={
                "verbose_name": "Lead / Order",
                "verbose_name_plural": "Leads & Orders",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="client",
            index=models.Index(
                fields=["workspace", "status"],
                name="workspaces__workspa_202868_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="client",
            index=models.Index(
                fields=["workspace", "email"],
                name="workspaces__workspa_5ff250_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="lead",
            index=models.Index(
                fields=["workspace", "status"],
                name="workspaces__workspa_78d8a7_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="lead",
            index=models.Index(
                fields=["workspace", "deadline"],
                name="workspaces__workspa_2eaee3_idx",
            ),
        ),
    ]
