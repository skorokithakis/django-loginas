DEBUG = True

ROOT_URLCONF = 'loginas.tests.urls'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'loginas',
    'loginas.tests',
)
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3"}
}
SECRET_KEY = 'insecure'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

LOGIN_REDIRECT_URL = "/login-redirect"


import django
if django.VERSION[:2] >= (1, 7):
    MIDDLEWARE_CLASSES.append(
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware'
    )
