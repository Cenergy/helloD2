"""
Django settings for helloD project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2r#q5_pw5@z)yntr)wr03#5+59lt2uex7u)f$n@88h0m9exjv*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]
AUTH_USER_MODEL = 'users.UserProfile'

# --------------------自定义认证后端-------------------------------------
AUTHENTICATION_BACKENDS = [
    'users.views.CustomBackend',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'courses.apps.CoursesConfig',
    'sources.apps.SourcesConfig',
    'wechat.apps.WechatConfig',
    'xadmin',
    'crispy_forms',
    'captcha',
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

ROOT_URLCONF = 'helloD2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'helloD2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST = "smtp.sina.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "helloaigis@sina.com"
EMAIL_HOST_PASSWORD = "Cenergy.0919"
EMAIL_USE_TLS = False
EMAIL_FROM = "helloaigis@sina.com"

# DEBUG = False
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, os.path.join('static'))
    ]
else:
    STATIC_ROOT = "static"

# ----------------------手机号码正则表达式-------------------------------
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
# 云片网apikey 配置
API_KEY = "09d6805265afbd0a779cfd9e16a0f4c5"

# DRF全局缓存时间设定
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3 * 3600
}

#百度识别# 定义常量
BAIDU_APP_ID = '14238582'
BAIDU_API_KEY = 'GLfcrhzmAepajd0WpEWTnpCV'
BAIDU_SECRET_KEY = 'gdAsgciejTyEtF6vyUPpwVeedSeSDTHu'

#图灵api
TURING_API_KEY='bf61c090a1bc4cfabc43e20e2d5b307b'
