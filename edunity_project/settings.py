# edunity_project/settings.py

"""
Django settings for edunity_project project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# In a real deployment, this key should be loaded from an environment variable.
SECRET_KEY = 'django-insecure-=+5!_a)l5i)y@399^x^s$v=i9#n*+8)e^!w(q@41*t1y_#+c5m'

# --- CRITICAL: Set to False before going live! ---
DEBUG = True 

# --- REQUIRED for deployment: Add your live website's domain name here ---
# Example: ALLOWED_HOSTS = ['roshan.pythonanywhere.com']
ALLOWED_HOSTS = []


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your Apps
    'core',
    'studymaterials',
    'forum',
    'lostandfound',
    'polls',
    'notices',
    'memes',
    'games',
    'leaderboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edunity_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.notification_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'edunity_project.wsgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES (For Production)
# ==============================================================================

STATIC_URL = 'static/'
# This is where your CSS and JS files are in development
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# --- THE FIX IS HERE ---
# This line tells 'collectstatic' where to put all the files for production.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
# This is where user-uploaded files (profile pics, etc.) are stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'