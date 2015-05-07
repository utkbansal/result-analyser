"""
Django settings for result_analyzer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*tzvfr!%*hzt#xu$^rvffe04ktop5^1t&6mh&%++4iqklz4@1j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scraper',
    'crispy_forms',
    'django.contrib.webdesign',
    'analyzer',
    'jsonify',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'result_analyzer.urls'

WSGI_APPLICATION = 'result_analyzer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'result_analyzer',
        'HOST': '',
        'PORT': '',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Set the default login url
LOGIN_URL = '/'


URLS = {
    # New url
    1: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frmBte'
       'ch1uplko2015dghdjhg.aspx',
    2: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frm'
       'Btech3uplko2015fhfdhfdhy.aspx',
    3: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frm'
       'Btech5uplko2015lkjdfg.aspx',
    4: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frm'
       'Btech7uplko2015yykkll.aspx'
}