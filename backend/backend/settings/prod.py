import os

# DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "football-team-simulation-production.up.railway.app"]

# os package will be inherited from base.py
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}