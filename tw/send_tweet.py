import os

import tweepy

proxy = 'http://localhost:8123'

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
consumer_key = "ZqgQ7a9vT4YX7C7PwoGdf0Evh"
consumer_secret = "SmkGKxKTZlmzGvchpdskP6xzaEJZbWcsAVMr79hcB29HuN0Cvm"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "388123055-84MCemwg3wUT8FhtuqLKRffUbmYbNdjme9HmDlue"
access_token_secret = "jeU0qs7d4EikhdADj41avID3FgyRzfr4ZsIoZykveaG6h"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
# api.update_status('Updating using OAuth authentication via Tweepy!')
# imagePath = "test.png"
# imagePath1 = "test.png"
# status = "تویت نمونه برای ارسال از طریف کد"
# api.update_with_media([imagePath,imagePath1], status)


# images = ('test.png', 'test.png')
filenames = ('test.png', 'test.png', 'test.png', 'test.png')
media_ids = []
for filename in filenames:
    res = api.media_upload(filename)
    media_ids.append(res.media_id)

# tweet with multiple images
api.update_status(status='many images!✨', media_ids=media_ids)
