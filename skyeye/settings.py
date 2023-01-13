"""
Django settings for skyeye project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django_eventstream.utils import have_channels

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6ahgf-e=y(09gh3!gr2)hvmaphf$7nf8j@&^qg+ij!051m&yet"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
AUTH_USER_MODEL = 'accounts.User'

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.AllowAllUsersModelBackend',
#     'accounts.backends.CaseInsensitiveModelBackend',
# )

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

if have_channels():
    INSTALLED_APPS.append('channels')  # pip install channels

INSTALLED_APPS.extend([
    # local app
    'sse',
    'accounts',
    'winch',
    'mission_device',
    # 3rd party app
    'drf_yasg',  # pip install drf_yasg
    'rest_framework',  # pip install djangorestframework
    'rest_framework.authtoken',
    'django_eventstream',  # pip install django_eventstream
    # 'bootstrap4',  # pip install django-bootstrap4
])

MIDDLEWARE = [
    'django_grip.GripMiddleware',  # add
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 인증된 요청에 대해서만 view 호출
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',  # 비인증 요청에 대해서는 읽기만 허용
    ]
}

ROOT_URLCONF = "skyeye.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# # 로그인 성공후 이동하는 URL
# LOGIN_REDIRECT_URL = '/redoc'
# # 로그아웃시 이동하는 URL
# LOGOUT_REDIRECT_URL = '/users/login'

WSGI_APPLICATION = "skyeye.wsgi.application"
ASGI_APPLICATION = "skyeye.asgi.application"

EVENTSTREAM_STORAGE_CLASS = 'django_eventstream.storage.DjangoModelStorage'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',  # Database 이름
        'USER': 'skysys',  # 데이터베이스에서 사용할 계정
        'PASSWORD': 'tmzkdl11@!',  # 계정의 비밀번호
        'HOST': '192.168.88.6',  # 데이테베이스 주소
        'PORT': '3306',  # 데이터베이스 포트, mysql 디폴트값은 3306
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR.joinpath('static')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
