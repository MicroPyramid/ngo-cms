from .settings import *

DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = ['127.0.0.1', '*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cjws',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}