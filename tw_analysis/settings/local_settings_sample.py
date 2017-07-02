import tweepy

consumer_key = ""
consumer_secret = ""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Fetch data api
consumer_key_data = ""
consumer_secret_data = ""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token_data = ""
access_token_secret_data = ""

auth = tweepy.OAuthHandler(consumer_key_data, consumer_secret_data)
auth.set_access_token(access_token_data, access_token_secret_data)

api_data = tweepy.API(auth)

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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# MongoDB
mongodb_authentication_source = ''
mongodb_username = ''
mongodb_password = '',
mongodb_host = ''
