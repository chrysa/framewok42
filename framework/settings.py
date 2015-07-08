#-*-coding:utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'umg@=!%oux#wouig$#_g^u+9)lo5=3ocqte106(oi$w$6805c%'
DEBUG = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'agreau@student.42.fr'
EMAIL_HOST_PASSWORD = 'mCKb0ss#123'
EMAIL_PORT = 468
EMAIL_USE_TLS = True
APPEND_SLASH = True

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

HIJACK_NOTIFY_ADMIN = True
HIJACK_NOTIFY_USER = True

LOGIN_PAGE = '/profil/login'
LOGIN_URL = '/profil/login'

HIJACK_LOGIN_REDIRECT_URL = "/"
REVERSE_HIJACK_LOGIN_REDIRECT_URL = "/admin/"

STATIC_URL = '/static/'
STATIC_ROOT = 'statics/'

ALLOWED_HOSTS = ['*']

APP_PERSO = (
    'contact',
    'core',
    'forum',
    'issues',
    'generate_logs',
    'profil',
)

ADDITIONALS_APPS = (
    'autoslug',
    'bootstrap3',
    'compat',
    'hijack',
    'jquery',
)

ADDITIONALS_MIDDLEWARE = (
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hijack.middleware.HijackRemoteUserMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
)

ADDITIONNALS_TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

LANGUAGES = (
    ('fr', u"français"),
    ('en', u"anglais"),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
) + ADDITIONALS_APPS + APP_PERSO

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
) + ADDITIONALS_MIDDLEWARE

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
) + ADDITIONNALS_TEMPLATE_CONTEXT_PROCESSORS

ROOT_URLCONF = 'framework.urls'

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

WSGI_APPLICATION = 'framework.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(levelname)s] [%(asctime)s][%(module)s:%(funcName)s:%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%m/%Y %H:%M:%S"
        },
        'simple': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file_critical': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/critical.log'),
            'formatter': 'verbose'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'formatter': 'verbose'
        },
        'file_warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/warning.log'),
            'formatter': 'verbose'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/info.log'),
            'formatter': 'simple'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'critical': {
            'handlers': ['file_critical'],
            'propagate': False,
            'level': 'CRITICAL',
        },
        'error': {
            'handlers': ['file_error'],
            'propagate': False,
            'level': 'ERROR',
        },
        'warning': {
            'handlers': ['file_warning'],
            'propagate': False,
            'level': 'WARNING',
        },
        'info': {
            'handlers': ['file_info'],
            'propagate': False,
            'level': 'INFO',
        },
        'debug': {
            'handlers': ['file_debug'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}

STATICFILES_DIRS = ()

for a in APP_PERSO:
    static = os.path.join(os.path.join(BASE_DIR, a),  'statics')
    template = os.path.join(os.path.join(BASE_DIR, a),  'templates')
    if os.path.isdir(static):
        STATICFILES_DIRS = STATICFILES_DIRS + (static,)
    if os.path.isdir(template):
        TEMPLATES[0]['DIRS'].append(template)
