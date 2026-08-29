# Generated for DevTeam Phase 1 Foundation

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_initial"),
        ("workspaces", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
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
                    "name",
                    models.CharField(
                        db_index=True, max_length=200, verbose_name="Service Name"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=220, verbose_name="URL Slug"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, verbose_name="Service Description"
                    ),
                ),
                (
                    "starting_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=100.0,
                        max_digits=10,
                        verbose_name="Starting Price ($)",
                    ),
                ),
                (
                    "estimated_delivery_days",
                    models.PositiveIntegerField(
                        default=7, verbose_name="Estimated Delivery (Days)"
                    ),
                ),
                (
                    "technologies",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of tech stacks (e.g. Django, DRF, Celery, React)",
                        verbose_name="Technologies & Stacks",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        verbose_name="Active for Orders",
                    ),
                ),
                (
                    "display_order",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Display Order"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Service Provider / Owner",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="workspaces.workspace",
                        verbose_name="Workspace",
                    ),
                ),
            ],
            options={
                "verbose_name": "Service",
                "verbose_name_plural": "Services",
                "ordering": ["display_order", "name"],
            },
        ),
        migrations.CreateModel(
            name="Expense",
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
                        max_length=200,
                        verbose_name="Expense Title / Vendor",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        verbose_name="Description / Receipt Notes",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=12, verbose_name="Amount ($)"
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("INFRASTRUCTURE", "Hosting, Servers & Cloud"),
                            ("SOFTWARE", "Software & SaaS Licenses"),
                            ("MARKETING", "Marketing & Advertising"),
                            ("CONTRACTOR", "Contractors & Freelancers"),
                            ("OFFICE", "Hardware, Office & Equipment"),
                            ("OTHER", "Other Operating Expenses"),
                        ],
                        db_index=True,
                        default="INFRASTRUCTURE",
                        max_length=50,
                        verbose_name="Expense Category",
                    ),
                ),
                (
                    "expense_date",
                    models.DateField(
                        db_index=True, verbose_name="Expense Date"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expenses",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Logged By",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expenses",
                        to="workspaces.workspace",
                        verbose_name="Workspace",
                    ),
                ),
            ],
            options={
                "verbose_name": "Business Expense",
                "verbose_name_plural": "Business Expenses",
                "ordering": ["-expense_date", "-created_at"],
                "indexes": [
                    models.Index(
                        fields=["workspace", "expense_date"],
                        name="billing_exp_workspa_729481_idx",
                    ),
                    models.Index(
                        fields=["workspace", "category"],
                        name="billing_exp_workspa_18a22d_idx",
                    ),
                ],
            },
        ),
    ]
