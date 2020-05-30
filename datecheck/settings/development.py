from .base import *
print("Using development settings")
DEBUG = True
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datechecker',
        'USER': 'datechecker',
        'PASSWORD': 'sup3rSECR3T!@#',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
