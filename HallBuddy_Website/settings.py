"""
Django settings for HallBuddy_Website project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url  # Auto-configures PostgreSQL
DEBUG = os.getenv('DEBUG', 'False') == 'True'
BASEDIR = os.path.dirname(os.path.dirname(__file__))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6+l!%iddsiyll25a!+#2lq+6skifv+zy2+wxddew-s0(!0tt*1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Home.apps.HomeConfig',
    'authentication.apps.AuthenticationConfig',
    'guestroom.apps.GuestroomConfig',
    'Complaints.apps.ComplaintsConfig',
    'Cleaning.apps.CleaningConfig',
    'django_razorpay',
]

DJ_RAZORPAY = {
 "organization_name": "HallBuddy",
 "organization_email": "team12.cs253@gmail.com",  # Optional
 "organization_domain": "https://something.com",
 "organization_logo": "https://company.com/orlogo.png",  # Optional,
 "nav_links": [("Membership Fee", "/payments/membership-fee"),
               ("Transactions", "/payments/transactions"),
               ("Adhoc Pay", "/payments/adhoc"),
               ("Manual transaction", "/payments/manual-transaction")
               ],
 "RAZORPAY_VARIANTS": {
     "public_key": "rzp_test_6GvpLSAmWckaMk",
     "secret_key": "Vo9OgyOw1FqGufiqhlWu4Fy32kl",
     "currency": "inr"
 },
  "RAZORPAY_ENABLE_CONVENIENCE_FEE": True,     # You charge a convenience fee to your customer.
  "USE_PAYMENT_LINK": True                     # If enabled it will create payment link, will not use checkout page
}

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
  messages.DEBUG: 'alert-info',
  messages.INFO: 'alert-info',
  messages.SUCCESS: 'alert-success',
  messages.WARNING: 'alert-warning',
  messages.ERROR: 'alert-danger',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'HallBuddy_Website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASEDIR, 'templates/'),
                 os.path.join(BASEDIR, 'Home/templates/'),
                 os.path.join(BASEDIR, 'guestroom/templates/'),
                 os.path.join(BASEDIR, 'Complaints/templates/'),
                 os.path.join(BASEDIR, 'Cleaning/templates/'),
                 ],
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

WSGI_APPLICATION = 'HallBuddy_Website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_ROOT = os.path.join(BASEDIR , 'static_files')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASEDIR, 'templates/'),
    os.path.join(BASEDIR, 'templates/static'),
    BASE_DIR / 'authentication/static/',
    BASE_DIR / 'Home/static/',
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'team12.cs253@gmail.com'         # put gmail id (in the quotes)
EMAIL_HOST_PASSWORD = 'mzsh xvjh auol ssbn '                           #   put app password for the gmail (in the quotes)

AUTH_USER_MODEL = 'authentication.User_class'