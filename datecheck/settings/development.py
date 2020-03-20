from .base import *
print("Using development settings")
DEBUG = True
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'local': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datecheck',
        'USER': 'datecheck',
        'PASSWORD': 'sup3rSECR3T!@#',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
