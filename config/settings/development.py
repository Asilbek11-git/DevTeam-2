"""Development settings for DevTeam."""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Optional database URL override for development
if os.environ.get('DB_HOST'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'devteam_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres_secure_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Fast password hasher for tests / local dev
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
