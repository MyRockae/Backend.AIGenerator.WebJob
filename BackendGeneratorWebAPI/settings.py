from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_KEY = config('SUPABASE_KEY')

MINIO_URL = config('MINIO_URL')
MINIO_ACCESS_KEY = config('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = config('MINIO_SECRET_KEY')

SECRET_KEY = config('SECRET_KEY')

GENERATOR_API_KEY = config('GENERATOR_API_KEY')


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

GOOGLE_GENERATIVE_LANGUAGE_API_KEY = config('GOOGLE_GENERATIVE_LANGUAGE_API_KEY')
MAX_FREE_AI_QUESTIONS_PER_QUIZ = config('MAX_FREE_AI_QUESTIONS_PER_QUIZ')
MAX_FREE_AI_NOTES_PER_QUIZ = config('MAX_FREE_AI_NOTES_PER_QUIZ')

DEBUG = config('DEBUG', default=False, cast=bool)

# Get the database URL from environment variable
DATABASE_URL = config('DATABASE_URL')  # Ensure DATABASE_URL is set in .env or environment

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
}

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Added for DRF
    'rest_framework_simplejwt',  # Added for JWT authentication
    'apps.account',
    'apps.flashcard',
    'apps.quiz',   
    'apps.subscription',
    'apps.generator',
    'apps.utility',
    'apps.worker',
    'drf_spectacular',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://rockae.com",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.rockae\.com$",
]

#CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'BackendGeneratorWebAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add template directories here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'BackendGeneratorWebAPI.wsgi.application'



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=200),  # Set to 15 minutes, for example
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # 7 days for the refresh token
    # Other settings...
}

# Use a custom user model for the accounts app
AUTH_USER_MODEL = 'account.User'  # Ensure your custom user model is in the 'accounts' app

# Password validation
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
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# REST framework configuration for JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'BackendGeneratorWebAPI.utils.custom_exception_handler',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Backend.Generator.WebAPI',
    'DESCRIPTION': 'Asynchronous backend service for processing file uploads, extracting text, and interfacing with third-party LLM APIs.',
    'VERSION': '1.0.0',
    
    # Add a URL to be displayed on Swagger
    'SERVERS': [
        {'url': 'http://127.0.0.1:8000/', 'description': 'Local Development Server'},
        {'url': 'https://web-production-a0312.up.railway.app/', 'description': 'Production Server'}  
    ],

    # Contact Information
    'CONTACT': {
        'name': 'Rockae Support',
        'email': 'support@rockae.com',
        'url': 'https://rockae.com/contact'
    },

    # License Information
    'LICENSE': {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT'
    },

    # Schema Path Prefix (if your API has a specific prefix, e.g., /api/v1/)
    'SCHEMA_PATH_PREFIX': '/api/v1',

    # Documentation customization options
    'SCHEMA_PATH_PREFIX_TRIM': False,  # Keep full path in schema
    'SERVE_INCLUDE_SCHEMA': True,  # Ensure OpenAPI schema is included

    'COMPONENT_SPLIT_REQUEST': True,  # This ensures that the components are split for request and response.
    'SECURITY': [{'BasicAuth': []}],  # Adjust according to your authentication method
    'SERVE_INCLUDE_SCHEMA': False,   # Optional: Can control if schema should be served as a view
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

