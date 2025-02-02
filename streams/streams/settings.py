from pathlib import Path
import os
# from google.oauth2 import service_account
from storages.backends.azure_storage import AzureStorage
from datetime import timedelta
# from google.cloud import storage

# INSTALLED_APPS += ["storages"]
azure_storage = AzureStorage()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to your GCS service account key file
# GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
#      os.path.join(BASE_DIR, 'streaming-449208-a827ccb1ac58.json')
#  )

# Azure Stack Storage settings

AZURE_ACCOUNT_NAME = 'geco2studios'
AZURE_CONTAINER = 'studios'

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-17q(99281&@#2jjx_!=&pf-kiuk%-u4(et61%w)7&ke7+4zgsf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['https://geco-games-streams-backend.onrender.com/', '*', '20.106.188.72' ]


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'users',
    'apis',
    'shows',
    'movies',
    
    'storages',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://192.168.1.122:8081',
    'https://geco-games-streams-backend.onrender.com'
    '20.106.188.72'
]

CSRF_TRUSTED_ORIGINS = [
    "https://geco-games-streams-backend.onrender.com"
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'streams.urls'

AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'streams.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# client = storage.Client()
# client._http.timeout = 6000 