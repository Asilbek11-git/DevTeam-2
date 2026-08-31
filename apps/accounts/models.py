"""
Custom User Model & Authentication Records.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from apps.core.models import TimeStampedModel

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'SUPERADMIN')
        return self.create_user(email, username, password, **extra_fields)

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrator'
    PROJECT_MANAGER = 'PROJECT_MANAGER', 'Project Manager'
    LEAD_DEVELOPER = 'LEAD_DEVELOPER', 'Lead Developer'
    DEVELOPER = 'DEVELOPER', 'Developer'
    CLIENT = 'CLIENT', 'Client'
    VIEWER = 'VIEWER', 'Viewer'
    MEMBER = 'MEMBER', 'Member'
    SUPERADMIN = 'SUPERADMIN', 'SuperAdmin'
    USER = 'USER', 'Standard User'

class User(AbstractUser, TimeStampedModel):
    class GlobalRole(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'SuperAdmin'
        USER = 'USER', 'Standard User'

    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=30, default=GlobalRole.USER)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    job_title = models.CharField(max_length=100, blank=True, default='Software Engineer')
    github_username = models.CharField(max_length=100, blank=True)
    gitlab_username = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    is_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=64, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"

class UserSession(TimeStampedModel):
    """Tracks active sessions and login audit history."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    device = models.CharField(max_length=100, blank=True, default='Desktop Browser')
    location = models.CharField(max_length=100, blank=True, default='Unknown')
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session for {self.user.email} from {self.ip_address}"

class OwnerProfile(TimeStampedModel):
    """
    Professional profile for the Owner / SuperAdmin.
    Configurable from Settings/Profile and public portfolio.
    """
    class Availability(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available for Projects'
        BUSY = 'BUSY', 'Partially Available'
        UNAVAILABLE = 'UNAVAILABLE', 'Unavailable / Fully Booked'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owner_profile',
        verbose_name='User Account'
    )
    full_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Full Name',
        help_text='Public or professional display name'
    )
    professional_title = models.CharField(
        max_length=200,
        blank=True,
        default='Full Stack Software Architect & SaaS Developer',
        verbose_name='Professional Title'
    )
    username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Public Handle / Username'
    )
    profile_photo = models.ImageField(
        upload_to='owner_profile/',
        null=True,
        blank=True,
        verbose_name='Profile Photo'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Biography / Overview',
        help_text='Detailed background, architectural philosophy, and engineering experience'
    )
    location = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Location'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Contact / Business Email'
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Phone Number'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='GitHub Profile URL'
    )
    gitlab_url = models.URLField(
        blank=True,
        verbose_name='GitLab Profile URL'
    )
    linkedin_url = models.URLField(
        blank=True,
        verbose_name='LinkedIn Profile URL'
    )
    telegram_url = models.URLField(
        blank=True,
        verbose_name='Telegram Contact URL'
    )
    website_url = models.URLField(
        blank=True,
        verbose_name='Personal / Company Website'
    )
    skills = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Core Skills',
        help_text='List of engineering capabilities and core competencies'
    )
    programming_languages = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Programming Languages',
        help_text='List of programming languages (e.g. Python, TypeScript, Go, SQL)'
    )
    frameworks = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Frameworks & Libraries',
        help_text='List of frameworks (e.g. Django, DRF, React, FastAPI, Tailwind CSS)'
    )
    databases = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Databases & Caches',
        help_text='List of databases (e.g. PostgreSQL, Redis, ClickHouse, SQLite)'
    )
    tools = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Tools & DevOps',
        help_text='List of tools (e.g. Docker, Celery, Kubernetes, Nginx, Git, Linux)'
    )
    years_of_experience = models.PositiveIntegerField(
        default=5,
        verbose_name='Years of Experience'
    )
    availability_status = models.CharField(
        max_length=50,
        default=Availability.AVAILABLE,
        choices=Availability.choices,
        verbose_name='Availability Status',
        db_index=True
    )
    professional_status = models.CharField(
        max_length=150,
        default='Accepting New Projects & Consulting',
        blank=True,
        verbose_name='Professional Status Headline'
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=50.00,
        verbose_name='Hourly Rate ($)'
    )

    class Meta:
        verbose_name = 'Owner Profile'
        verbose_name_plural = 'Owner Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"Owner Profile: {self.full_name or self.user.email}"

class PortfolioItem(TimeStampedModel):
    """
    Public and showcase portfolio project item.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='portfolio_items',
        verbose_name='Owner / Author'
    )
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Project Title'
    )
    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True,
        db_index=True,
        verbose_name='URL Slug'
    )
    short_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Short Summary'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Full Project Description'
    )
    image = models.ImageField(
        upload_to='portfolio/',
        null=True,
        blank=True,
        verbose_name='Project Screenshot / Cover Image'
    )
    technologies = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Technologies Used',
        help_text='List of tech stack items (e.g. Django, React, PostgreSQL)'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='GitHub Repository URL'
    )
    live_demo_url = models.URLField(
        blank=True,
        verbose_name='Live Demo / Production URL'
    )
    client_type = models.CharField(
        max_length=150,
        blank=True,
        default='SaaS / Freelance Client',
        verbose_name='Client / Project Type'
    )
    completion_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Completion Date'
    )
    project_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Project Value ($)'
    )
    results = models.TextField(
        blank=True,
        verbose_name='Key Results / Impact',
        help_text='Key impact metrics, performance outcomes or client feedback'
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Featured on Homepage'
    )
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Published Publicly'
    )

    class Meta:
        verbose_name = 'Portfolio Item'
        verbose_name_plural = 'Portfolio Items'
        ordering = ['-is_featured', '-completion_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.title) or 'project'
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({'Featured' if self.is_featured else 'Standard'})"

