import tweepy
from emot.emo_unicode import UNICODE_EMOJI
import nltk
import re
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
from flaskext.couchdb import Row
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
from couchdb.mapping import TextField, FloatField, IntegerField
from couchdb.design import ViewDefinition

# Convert emojis to string for furter usage such as sentimental analysis with nlp package
def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

# Tweet API Streaming
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"
client = tweepy.Client(BEARER_TOKEN, wait_on_rate_limit=True)

def create_raw_cluster(couch, input_keyword):
    # Create raw database for storing tweets from search harvester
    rawdb_name = "search_" + input_keyword.lower()
    try:
        dbrcity = couch[rawdb_name]
    except:
        dbrcity = couch.create(rawdb_name)
    return dbrcity

# Construct query keyword string
def ruleGenerate(input_keyword, input_city):
    query_rule = input_keyword + " ("
    for i in range(len(input_city)):
        if (i >= len(input_city) - 1):
            query_rule += input_city[i]
        else:
            query_rule += input_city[i]
            query_rule += " OR "
    query_rule += ")"
    return query_rule

def nlpText(input_text, sia_tool):
    text = convert_emojis(input_text)
    text = re.sub('http://\S+|https://\S+', '', text)
    nlp_result = [sia_tool.polarity_scores(text)["pos"], sia_tool.polarity_scores(text)["neg"], sia_tool.polarity_scores(text)["compound"]]
    return text, nlp_result

manager = CouchDBManager()
class Search(Document):
    doc_type = 'search'
    _id = TextField()
    city_name = TextField()
    nlppos = FloatField()
    nlpneg = FloatField()
    nlpemo = FloatField()
manager.add_document(Search)

# Create summarised database of the target information harvested from the historical dataset
def summaryView(design_doc, request, db):

    city_count = ViewDefinition(design_doc, request, '''\
        function(doc){
            emit(doc.city_name, 1);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    city_count.sync(db)

    request_city = request + "pos"
    city_pos = ViewDefinition(design_doc, request_city, '''\
        function(doc){
            emit(doc.city_name, doc.nlppos);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    city_pos.sync(db)

    request_city = request + "neg"
    city_neg = ViewDefinition(design_doc, request_city, '''\
        function(doc){
            emit(doc.city_name, doc.nlpneg);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    city_neg.sync(db)

    request_city = request + "emo"
    city_emo = ViewDefinition(design_doc, request_city, '''\
        function(doc){
            emit(doc.city_name, doc.nlpemo);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    city_emo.sync(db)

    return city_count, city_pos, city_neg, city_emo

def writeDb(result, dbrcity, input_city):
    sia = SentimentIntensityAnalyzer()
    for i in result[0]:
        tweet_text, nlp_stat = nlpText(str(i), sia)
        for j in input_city:
            if j.lower() in tweet_text.lower():
                if (str(i.id) not in dbrcity):
                    new_search = Search(_id = str(i.id), city_name = j, nlppos = nlp_stat[0], nlpneg = nlp_stat[1], nlpemo = nlp_stat[2])
                    new_search.store(dbrcity)
                    break
    return ("Success")

def search_store(dbrcity, client, query_rule, city_set):
    result_finish = True #are these two essential as argument?
    state_start = True
    while result_finish:
        try:
            if (state_start):
                result = client.search_recent_tweets(query_rule, max_results = 100)
                writeDb(result, dbrcity, city_set)
                if "next_token" in result[3]:
                    state_start = False
                    next_page = result[3]["next_token"]
                else:
                    break
            else:
                result = client.search_recent_tweets(query_rule, max_results = 100, next_token = next_page)
                writeDb(result, dbrcity, city_set)
                if "next_token" in result[3]:
                    next_page = result[3]["next_token"]
                else:
                    break
        except Exception as e:
            pass
    return ('done')

def create_summary_cluster(couch, input_keyword):
    # Create summarised database (dbsh stands for database summary search)
    db_name = "search_" + input_keyword.lower() + "_summary"
    try:
        dbss = couch[db_name]
    except:
        dbss = couch.create(db_name)
    return dbss

# Create class for generating objects of summaried data
manager = CouchDBManager()
class SearchSummary(Document):
    doc_type = 'summary'
    _id = TextField()
    tweet_count = IntegerField()
    nlppos = FloatField()
    nlpneg = FloatField()
    nlpemo = FloatField()
manager.add_document(SearchSummary)

# Function for collecting target data from Aurin preserved database
def summary_target(viewCount, viewPos, viewNeg, viewEmo, rawtarget, summarydb):

    viewCount_result = viewCount(rawtarget)
    viewPos_result = viewPos(rawtarget)
    viewNeg_result = viewNeg(rawtarget)
    viewEmo_result = viewEmo(rawtarget)

    list_count = {}
    list_pos = {}
    list_neg = {}
    list_emo = {}

    for row in viewCount_result:
        list_count[row.key] = row.value

    for row in viewPos_result:
        list_pos[row.key] = row.value

    for row in viewNeg_result:
        list_neg[row.key] = row.value

    for row in viewEmo_result:
        list_emo[row.key] = row.value

    for i in list_count:
        if i not in summarydb:
            new_summary = SearchSummary(_id = i, tweet_count = list_count[i], nlppos = list_pos[i] / list_count[i],
            nlpneg = list_neg[i] / list_count[i], nlpemo = list_emo[i] / list_count[i])
            new_summary.store(summarydb)

    # Return the mean value of the selected feature in a json format
    return ("Mission Accomplished")

def search_work(couch, input_keyword):
    city_set = ["Canberra", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Hobart"]
    dbrcity = create_raw_cluster(couch, input_keyword)
    query_rule = ruleGenerate(input_keyword, city_set)
    city_count, city_pos, city_neg, city_emo = summaryView('summary', input_keyword, dbrcity)
    search_store(dbrcity, client, query_rule, city_set)
    dbss = create_summary_cluster(couch, input_keyword)
    summary_target(city_count, city_pos, city_neg, city_emo, dbrcity, dbss)
    return True