from .base import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE" : "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3")

    }
}


#Settings for sending out emails

EMAIL_HOST_USER = 'goodneighborsubs@gmail.com' #this is a testing account
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com' # Wha is this
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_PORT = 587
