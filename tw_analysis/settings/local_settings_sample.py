import os
import tweepy

# DJANGO SETTING SECTION

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Twitter SECTION

# communication api
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Fetch data api
consumer_key_data = ""
consumer_secret_data = ""
access_token_data = ""
access_token_secret_data = ""

auth = tweepy.OAuthHandler(consumer_key_data, consumer_secret_data)
auth.set_access_token(access_token_data, access_token_secret_data)

api_data = tweepy.API(auth)

# admin twitter account for sending direct message
ADMIN_TW_ACCOUNT = ''

# DATABASE SECTION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# MongoDB
mongodb_authentication_source = ''
mongodb_username = ''
mongodb_password = ''
mongodb_host = ''
mongodb_port = ''
STATIC_ROOT = '/home/imanoel/Projects/twitter-analysis/static'
REDIS = ''
# PROXY SETTINGS
# http proxy
# proxy = ''
# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy
