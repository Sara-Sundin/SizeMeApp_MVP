import os
from pathlib import Path
import dj_database_url
from decouple import config

# <!-- Define base directory for the project -->
BASE_DIR = Path(__file__).resolve().parent.parent

# <!-- Secret key and debug mode -->
SECRET_KEY = config('SECRET_KEY')
DEBUG = False

# <!-- Allowed hosts for the application -->
ALLOWED_HOSTS = [
    'sizemeapp-mvp-f444c8498547.herokuapp.com',
    'localhost',
    '127.0.0.1',
]

# <!-- Use database-backed session engine -->
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# <!-- Installed apps: project-specific, third-party, and Django default -->
INSTALLED_APPS = [
    # Project apps
    'accounts',
    'products',
    'sizemeapp',
    'home',
    'webshop',
    'bag',
    'checkout',

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',
    'django_countries',

    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# <!-- Middleware configuration -->
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # for static file serving in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# <!-- Crispy Forms config -->
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# <!-- Custom user model -->
AUTH_USER_MODEL = 'accounts.CustomUser'

# <!-- Login redirect and login URL -->
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'

# <!-- Root URLs -->
ROOT_URLCONF = 'config.urls'

# <!-- Templates and context processors -->
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.global_context',  # Custom context
                'bag.context_processors.bag_contents',     # Cart context
            ],
        },
    },
]

# <!-- WSGI config -->
WSGI_APPLICATION = 'config.wsgi.application'

# <!-- Database configuration -->
DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default="sqlite:///db.sqlite3")
    )
}

# <!-- Static files (CSS, JS) -->
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Used in production
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Local development
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# <!-- Media files via S3 -->
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='eu-north-1')
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

# <!-- Django Storages configuration for S3 -->
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": config('AWS_ACCESS_KEY_ID'),
            "secret_key": config('AWS_SECRET_ACCESS_KEY'),
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "object_parameters": {
                "CacheControl": "max-age=86400",
            },
            "querystring_auth": False,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# <!-- Password validation -->
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

# <!-- Email backend configuration -->
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mail.inleed.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# <!-- Stripe configuration -->
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_WH_SECRET = config('STRIPE_WH_SECRET')

# <!-- Localization -->
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# <!-- Default auto primary key field type -->
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
