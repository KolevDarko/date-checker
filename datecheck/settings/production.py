from .base import *
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datecheck',
        'USER': 'datecheck',
        'PASSWORD': 'sup3rSECR3T!@#',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
