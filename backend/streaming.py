from tweepy import StreamingClient, Tweet, StreamRule

import os

bearer_token = os.environ.get('BEARER_TOKEN', None)


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