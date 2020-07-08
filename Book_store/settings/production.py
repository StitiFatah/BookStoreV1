from .base import import *


DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = ["ip-address", "www.yourwebsite.com"]


# INTERNAL_IPS = [
#     '127.0.0.1',
# ]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'polls_db3',
        'USER': config("DB_NAME"),
        'PASSWORD': config("DB_PSWD"),
        'HOST': config("DB_HOST"),
        'PORT': '',
    }
}
