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

LOGIN_PAGE = '/profil/sel_login'
LOGIN_URL = '/profil/sel_login'

ALLOWED_HOSTS = ['*']

APP_PERSO = (
    'contact',
    'core',
    'forum',
    'profil',
    'issues'
)

ADDITIONALS_APPS = (
    'bootstrap3',
    'autoslug',
    'jquery',
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
)

AUTHENTICATION_BACKENDS = (
    'django_python3_ldap.auth.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

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

STATIC_URL = '/static/'
STATIC_ROOT = '/statics/'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

for a in APP_PERSO:
    static = os.path.join(os.path.join(BASE_DIR, a),  'statics')
    template = os.path.join(os.path.join(BASE_DIR, a),  'templates')
    if os.path.isdir(static):
        STATICFILES_DIRS = STATICFILES_DIRS + (static,)
    if os.path.isdir(template):
        TEMPLATES[0]['DIRS'].append(template)
