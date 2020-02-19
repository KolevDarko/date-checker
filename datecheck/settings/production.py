from .base import *
DEBUG = False
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
