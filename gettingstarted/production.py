from .base import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['DEBUG'].lower() in ['true', 't', 'yes', 'y']:
	DEBUG = True
else:
	DEBUG = False

ALLOWED_HOSTS += ['.herokuapp.com']
CORS_ORIGIN_WHITELIST += ["*"]
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
	}
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER = 'goodneighborsubs@gmail.com' #this is a testing account
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_PORT = 587