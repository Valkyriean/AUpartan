from tweepy import StreamingClient, Tweet, StreamRule

import secret

bearer_token = secret.BEARER_TOKEN


class TweetListener(StreamingClient):

    def on_tweet(self, tweet: Tweet):
        print(tweet.__repr__())
        
    def on_request_error(self, status_code):
        print(status_code)
    
    def on_connection_error(self):
        self.disconnect
        
client = TweetListener(bearer_token)

rules = [
    StreamRule(value="Melbourne lang:en")
    # StreamRule(value=""),
    # StreamRule(value="bounding_box:[144.3896 -38.5084 145.5459 -37.3127]")
    
]


resp = client.get_rules()
if resp and resp.data:
    rule_ids = []
    for rule in resp.data:
        rule_ids.append(rule.id)
    client.delete_rules(rule_ids)
    
    
resp = client.add_rules(rules, dry_run= True)
if resp.errors:
    raise RuntimeError(resp.errors)

resp = client.add_rules(rules)
if resp.errors:
    raise RuntimeError(resp.errors)

print(client.get_rules())

try:
    client.filter()
except KeyboardInterrupt:
    client.disconnect()
"""
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
"""