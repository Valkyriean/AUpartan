import tweepy
import os

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"

bearer_token = BEARER_TOKEN
token='931264431505358849-YzavFd1tCYRkkyrmbRuRkVAkmigYdWy'
token_secret='n4NFnvIsRN3aSoeHsUGs82CNcxJIV6B4zASDjkFxno65O'

stream = tweepy.Stream("K4leUSXBdJwHytayPXdFzEzJN", "bpyL6MhIsNKRoWDrHj0ou9wHwib7tCm4ob5p3SZam51iDZyqv4", token, token_secret)

test = stream.filter(languages = ["en"], track="Melbourne", locations=[144.852581, -37.83339, 145.044056, -37.782334])

print(test)


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