# Generated for DevTeam Phase 1 Foundation

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OwnerProfile",
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
                        blank=True,
                        help_text="Public or professional display name",
                        max_length=200,
                        verbose_name="Full Name",
                    ),
                ),
                (
                    "professional_title",
                    models.CharField(
                        blank=True,
                        default="Full Stack Software Architect & SaaS Developer",
                        max_length=200,
                        verbose_name="Professional Title",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Public Handle / Username",
                    ),
                ),
                (
                    "profile_photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="owner_profile/",
                        verbose_name="Profile Photo",
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        blank=True,
                        help_text="Detailed background, architectural philosophy, and engineering experience",
                        verbose_name="Biography / Overview",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Location"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name="Contact / Business Email",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Phone Number"
                    ),
                ),
                (
                    "github_url",
                    models.URLField(blank=True, verbose_name="GitHub Profile URL"),
                ),
                (
                    "gitlab_url",
                    models.URLField(blank=True, verbose_name="GitLab Profile URL"),
                ),
                (
                    "linkedin_url",
                    models.URLField(
                        blank=True, verbose_name="LinkedIn Profile URL"
                    ),
                ),
                (
                    "telegram_url",
                    models.URLField(
                        blank=True, verbose_name="Telegram Contact URL"
                    ),
                ),
                (
                    "website_url",
                    models.URLField(
                        blank=True, verbose_name="Personal / Company Website"
                    ),
                ),
                (
                    "skills",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of engineering capabilities and core competencies",
                        verbose_name="Core Skills",
                    ),
                ),
                (
                    "programming_languages",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of programming languages (e.g. Python, TypeScript, Go, SQL)",
                        verbose_name="Programming Languages",
                    ),
                ),
                (
                    "frameworks",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of frameworks (e.g. Django, DRF, React, FastAPI, Tailwind CSS)",
                        verbose_name="Frameworks & Libraries",
                    ),
                ),
                (
                    "databases",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of databases (e.g. PostgreSQL, Redis, ClickHouse, SQLite)",
                        verbose_name="Databases & Caches",
                    ),
                ),
                (
                    "tools",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of tools (e.g. Docker, Celery, Kubernetes, Nginx, Git, Linux)",
                        verbose_name="Tools & DevOps",
                    ),
                ),
                (
                    "years_of_experience",
                    models.PositiveIntegerField(
                        default=5, verbose_name="Years of Experience"
                    ),
                ),
                (
                    "availability_status",
                    models.CharField(
                        choices=[
                            ("AVAILABLE", "Available for Projects"),
                            ("BUSY", "Partially Available"),
                            ("UNAVAILABLE", "Unavailable / Fully Booked"),
                        ],
                        db_index=True,
                        default="AVAILABLE",
                        max_length=50,
                        verbose_name="Availability Status",
                    ),
                ),
                (
                    "professional_status",
                    models.CharField(
                        blank=True,
                        default="Accepting New Projects & Consulting",
                        max_length=150,
                        verbose_name="Professional Status Headline",
                    ),
                ),
                (
                    "hourly_rate",
                    models.DecimalField(
                        decimal_places=2,
                        default=50.0,
                        max_digits=10,
                        verbose_name="Hourly Rate ($)",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner_profile",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User Account",
                    ),
                ),
            ],
            options={
                "verbose_name": "Owner Profile",
                "verbose_name_plural": "Owner Profiles",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PortfolioItem",
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
                        db_index=True, max_length=255, verbose_name="Project Title"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=280,
                        unique=True,
                        verbose_name="URL Slug",
                    ),
                ),
                (
                    "short_description",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="Short Summary"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, verbose_name="Full Project Description"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="portfolio/",
                        verbose_name="Project Screenshot / Cover Image",
                    ),
                ),
                (
                    "technologies",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of tech stack items (e.g. Django, React, PostgreSQL)",
                        verbose_name="Technologies Used",
                    ),
                ),
                (
                    "github_url",
                    models.URLField(
                        blank=True, verbose_name="GitHub Repository URL"
                    ),
                ),
                (
                    "live_demo_url",
                    models.URLField(
                        blank=True, verbose_name="Live Demo / Production URL"
                    ),
                ),
                (
                    "client_type",
                    models.CharField(
                        blank=True,
                        default="SaaS / Freelance Client",
                        max_length=150,
                        verbose_name="Client / Project Type",
                    ),
                ),
                (
                    "completion_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Completion Date"
                    ),
                ),
                (
                    "project_value",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=12,
                        null=True,
                        verbose_name="Project Value ($)",
                    ),
                ),
                (
                    "results",
                    models.TextField(
                        blank=True,
                        help_text="Key impact metrics, performance outcomes or client feedback",
                        verbose_name="Key Results / Impact",
                    ),
                ),
                (
                    "is_featured",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        verbose_name="Featured on Homepage",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        verbose_name="Published Publicly",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="portfolio_items",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner / Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Portfolio Item",
                "verbose_name_plural": "Portfolio Items",
                "ordering": ["-is_featured", "-completion_date", "-created_at"],
            },
        ),
    ]
