import tweepy
import json
import os

ACCESS_TOKEN = '931264431505358849-YzavFd1tCYRkkyrmbRuRkVAkmigYdWy'
ACCESS_TOKEN_SECRET = 'n4NFnvIsRN3aSoeHsUGs82CNcxJIV6B4zASDjkFxno65O'
CONSUMER_KEY = "K4leUSXBdJwHytayPXdFzEzJN"
CONSUMER_SECRET = "bpyL6MhIsNKRoWDrHj0ou9wHwib7tCm4ob5p3SZam51iDZyqv4"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

class MyListener(tweepy.Stream):
    def on_data(self, data):
        try:
            tweet_id = (json.loads(data.decode("utf-8"))["id"])
            text = api.get_status(tweet_id, tweet_mode = "extended")
            print(text)

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

stream = MyListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, max_retries=1)
stream.filter(languages = ["en"], track=["Melbourne Covid"], locations = [143.072686, -37.766864, 145.137758, -37.216227])
