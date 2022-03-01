import os

# from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_DIR= os.path.join(BASE_DIR, 'etc')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$p@g%4@631idmhi(z-x_%8#3vz8c#y6x#l23g+-ki=qk+6ap6m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

APP_NAME = 'traineeproject_dashboard'

SITE_ID = 1

# Reviewer site ID
REVIEWER_SITE_ID = 0

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'edc_timepoint.apps.AppConfig',
    'edc_protocol.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_navbar.apps.AppConfig',
    'edc_action_item.apps.AppConfig',
    'edc_lab.apps.AppConfig',
    'edc_lab_dashboard.apps.AppConfig',
    'edc_locator.apps.AppConfig',
    'edc_identifier.apps.AppConfig',
    'edc_data_manager.apps.AppConfig',
    'edc_model_wrapper.apps.AppConfig',
    'traineeproject_dashboard.apps.AppConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edc_subject_dashboard.middleware.DashboardMiddleware',
    'edc_dashboard.middleware.DashboardMiddleware',
    'edc_lab_dashboard.middleware.DashboardMiddleware',
]

ROOT_URLCONF = 'traineeproject_dashboard.urls'

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

WSGI_APPLICATION = 'traineeproject_dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

DASHBOARD_URL_NAMES = {
    'screening_listboard_url': 'traineeproject_dashboard:screening_listboard_url',
    'subject_listboard_url': 'traineeproject_dashboard:subject_listboard_url',
    'subject_dashboard_url': 'traineeproject_dashboard:subject_dashboard_url',
    'data_manager_listboard_url': 'edc_data_manager:data_manager_listboard_url',
    

}

DASHBOARD_BASE_TEMPLATES = {
    'listboard_base_template': 'traineeproject/base.html',
    'dashboard_base_template': 'traineeproject/base.html',
    'subject_dashboard_template': 'traineeproject_dashboard/subject/dashboard.html',
    'screening_listboard_template': 'traineeproject_dashboard/screening/listboard.html',
    'subject_listboard_template': 'traineeproject_dashboard/subject/listboard.html',
    'data_manager_listboard_template': 'edc_data_manager/listboard.html',

}