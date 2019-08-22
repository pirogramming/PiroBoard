from LPB.settings.common import *


DEBUG = False

ALLOWED_HOSTS = ['15.164.114.238']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}