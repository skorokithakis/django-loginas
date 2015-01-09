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
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
