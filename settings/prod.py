from .common import *


DEBUG = False

ALLOWED_HOSTS = ['15.164.13.163']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}