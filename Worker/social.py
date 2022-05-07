from tweepy import StreamingClient, Tweet, StreamRule
import tweepy
import re
import json
from app import dbp
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row
from emot.emo_unicode import UNICODE_EMOJI
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Define function for converting emojis to text for further analysing
def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

manager = CouchDBManager()
class Social(Document):
    doc_type = 'social'
    _id = TextField()
    city = TextField()
    topic = TextField()
    tweet_text = TextField()
    tweet_emo = FloatField()
manager.add_document(Social)

topic = ["Election", "Labor", "Liberal"]
city = ["Melbourne", "Sydney", "Adelaide", "Hobart", "Perth", "Brisbane", "Darwin", "Canberra"]

# design-doc should be the doc-type of historic data document, in string
# Storing design document into database
def view_twitter_social(design_doc, db):

    countsocial = ViewDefinition(design_doc, 'totalsocial', '''\
        function(doc){
            emit(doc.city, 1)
        }''','''function(keys, values, rereduce){
                    return sum(values);
        }''', wrapper = Row, group = True)

    electionemo = ViewDefinition(design_doc, 'cityemo', '''\
        function(doc){
            emit(doc.city, doc.tweet_emo);
        }''','''function(keys, values, rereduce){
                return (sum(values));
        }''', wrapper = Row, group = True)
    
    labor = ViewDefinition(design_doc, 'laboremo', '''\
        function(doc){
            if (doc.topic == 'Labor'){
                emit(doc.city, doc.tweet_emo);
            }
        }''','''function(keys, values, rereduce){
                return (sum(values));
        }''', wrapper = Row, group = True)

    laborcount = ViewDefinition(design_doc, 'laborcount', '''\
        function(doc){
            if (doc.topic == 'Labor'){
                emit(doc.city, 1);
            }
        }''','''function(keys, values, rereduce){
                return (sum(values));
        }''', wrapper = Row, group = True)
    
    liberal = ViewDefinition(design_doc, 'liberalemo', '''\
        function(doc){
            if (doc.topic == 'Liberal'){
                emit(doc.city, doc.tweet_emo);
            }
        }''','''function(keys, values, rereduce){
                return (sum(values));
        }''', wrapper = Row, group = True)
    
    liberalcount = ViewDefinition(design_doc, 'liberalcount', '''\
        function(doc){
            if (doc.topic == 'Liberal'){
                emit(doc.city, 1);
            }
        }''','''function(keys, values, rereduce){
                return (sum(values));
        }''', wrapper = Row, group = True)

    countsocial.sync(db)
    electionemo.sync(db)
    labor.sync(db)
    laborcount.sync(db)
    liberal.sync(db)
    liberalcount.sync(db)

    return countsocial, electionemo, labor, laborcount, liberal, liberalcount

countsocial, electionemo, labor, laborcount, liberal, liberalcount = view_twitter_social("social", dbp)

# Tweet API Streaming
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"
CONSUMER_KEY = "K4leUSXBdJwHytayPXdFzEzJN"
CONSUMER_SECRET = "bpyL6MhIsNKRoWDrHj0ou9wHwib7tCm4ob5p3SZam51iDZyqv4"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def citylang(city_name, input_text, follower_limit, db, bearer_token, api, sia):
    
    class TweetListener(StreamingClient):

        def on_tweet(self, tweet: Tweet):

            try: 
                text = api.get_status(tweet.id, tweet_mode = "extended")

                if ((text.user.followers_count < follower_limit) and (text.lang != "und")):

                    text = convert_emojis(text.full_text)
                    text = re.sub('http://\S+|https://\S+', '', text)
                    nlp_result = sia.polarity_scores(text)["compound"]

                    if str(tweet.id) not in db:
                        new_historic = Social(_id = str(tweet.id), city = city_name, topic = input_text, tweet_text = text, tweet_emo = nlp_result)
                        new_historic.store(db)

            except Exception as e:
                pass
                
        def on_request_error(self, status_code):
            print(status_code)
            
        def on_connection_error(self):
            self.disconnect
                
    client = TweetListener(bearer_token)
    rules = [StreamRule(value = input_text, tag = city_name)]

    resp = client.get_rules()
    if resp and resp.data:
        rule_ids = []
        for rule in resp.data:
            rule_ids.append(rule.id)
        client.delete_rules(rule_ids)
            
    resp = client.add_rules(rules, dry_run=True)
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

    return ('Done')

citylang("Sydney", "Liberal", 3000, dbp, BEARER_TOKEN, api, sia)

# Function to generate pre-cooked data, store it into new summary database and return it as a json file
def view_twitter_stream(viewdef, db):

    language_stat = viewdef(db)

    rate_dict = {}
    for row in language_stat:
        rate_dict[row.key] = row.value
    
    print(rate_dict)
    return json.dumps(rate_dict, indent = 4)

# Call the view_twitter_stream function to compute the summarised data of all city language statistic
view_twitter_stream(countsocial, dbp) # 每个城市参与政治的Tweet量
view_twitter_stream(electionemo, dbp) # 每个城市参与政治的Tweet的加和emotional stat
view_twitter_stream(labor, dbp) # 每个城市发与Labor相关的tweet的加和emotional stat
view_twitter_stream(laborcount, dbp) # 每个城市发与Labor相关的tweet的数量
view_twitter_stream(liberal, dbp) # 每个城市发与Liberal相关的tweet的加和emotional stat
view_twitter_stream(liberalcount, dbp) # 每个城市发与Liberal相关的tweet的数量