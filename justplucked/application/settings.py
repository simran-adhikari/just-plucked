 
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4l7jl&@q@moow3+fq9aq(6*_ma!nosx7py8o_spdmzj_icuuds'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'whitenoise',
    'crispy_forms',
    'crispy_bootstrap5',
    'jazzmin',
    "django.contrib.humanize",
    'authapp',
    'blog',
    'chatbot',
    'farmer',
    'master',
    'order',
    'website',
    'products',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'chatterbot',
    'chatterbot.ext.django_chatterbot',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


MIDDLEWARE = [
     "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.example_context',
                'farmer.context_processors.farmer_dashboard_data'
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'check_same_thread': False,
        },
    }
    
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


 

STATIC_URL = 'static/'
 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"] 
STATIC_ROOT = BASE_DIR / "staticfiles"   

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

 
STRIPE_PUBLIC_KEY = 'pk_test_51RI4mmIHchYkQBZzCaZsPftC7gcmb6faO0Kv5nkSLzsxiusgS9cMp8jtplkHKpoeTLXwWzdCC2DclnuXutRaNO6r00SPuYRmjt'
STRIPE_SECRET_KEY = 'sk_test_51RI4mmIHchYkQBZznvLcrykRmttOGnA1ZRX2bhfuTLl4HuqCSawsQxK6pXTtrFrN1dXDkW5eyn13AAFXUnDpiGVa00dxP2bHml'
STRIPE_WEBHOOK_SECRET = 'your_webhook_secret'

# Currency
CURRENCY = 'USD'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'justplucked.vedanica.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'info@justplucked.vedanica.com'
EMAIL_HOST_PASSWORD = 'Balkot11@'  


CHATTERBOT = {
    'name': 'FarmersMarketplaceBot',
    'storage_adapter': 'chatterbot.storage.SQLStorageAdapter',
    'database_uri': None,  # Disable database
    'logic_adapters': [
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "Sorry, I couldn't understand. Please rephrase your question.",
            'maximum_similarity_threshold': 0.90
        }
    ],
    'preprocessors': [
        'chatterbot.preprocessors.clean_whitespace'
    ],
    'read_only': True,
}