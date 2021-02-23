from .base import *
import dj_database_url
import django_heroku

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ['DEBUG'].lower() in ['true', 't', 'yes', 'y']:
	DEBUG = True
else:
	DEBUG = False

ALLOWED_HOSTS += ['.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'mydatabase',
		'USER': 'yxwcweadgrqons',
		'PASSWORD': 'a6db2dac0bf38934fa2f2a54b42b72378d159cff1799b9ab0026f4393dca93e3',
		'HOST': 'ec2-3-95-85-91.compute-1.amazonaws.com',
		'PORT': '5432'
	}
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

django_heroku.settings(locals())

# EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST_USER = 'goodneighborsubs@gmail.com' #this is a testing account
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
# EMAIL_PORT = 587