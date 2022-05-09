from flaskext.couchdb import Row
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
from couchdb.mapping import TextField, FloatField, IntegerField
from couchdb.design import ViewDefinition

def create_cluster(couch, receive_keyword):
    # Setup raw database for storing target keyword related tweets (dbrt stands for database raw target)
    db_name = "historic_" + receive_keyword
    try:
        dbrt = couch[db_name]
    except:
        dbrt = couch.create(db_name)
    return dbrt

def KeyData(design_doc, request, db):
    if request != 'all':
        requestText = ViewDefinition(design_doc, request, '''function(doc){\
            if (doc.tweet_text.includes("''' + request + '''")){
            emit(doc._id, doc.tweet_text);
            }
            }''')
        requestText.sync(db)

        request_sa3 = request + "_sa3"
        requestSA3 = ViewDefinition(design_doc, request_sa3, '''function(doc){\
            if (doc.tweet_text.includes("''' + request + '''")){
                emit(doc._id, doc.sa3_id);
            }
        }''')
        requestSA3.sync(db)
    else:
        requestText = ViewDefinition(design_doc, request, '''\
            function(doc){
                emit(doc._id, doc.tweet_text);
            }''')
        requestText.sync(db)

        request_sa3 = request + "_sa3"
        requestSA3 = ViewDefinition(design_doc, request_sa3, '''\
            function(doc){
                emit(doc._id, doc.sa3_id);
            }''')
        requestSA3.sync(db)

    return requestText, requestSA3

# Setup class for collecting target historicu information into historic raw database
manager = CouchDBManager()
class Historic(Document):
    doc_type = 'historic'
    _id = TextField()
    sa3_id = TextField()
    nlppos = FloatField()
    nlpneg = FloatField()
    nlpemo = FloatField()
manager.add_document(Historic)

# Function for collecting target data from Aurin preserved database
def store_target(viewData, viewSA3, rawdb, targetdb):

    viewSA3_result = viewSA3(rawdb)
    viewData_result = viewData(rawdb)
    list_row = {}

    for row in viewData_result:
        list_row[row.key] = [sia.polarity_scores(row.value)["pos"], sia.polarity_scores(row.value)["neg"], sia.polarity_scores(row.value)["compound"]]
    
    for row in viewSA3_result:
        if row.key not in targetdb:
            newHistoric = Historic(_id = row.key, sa3_id = row.value, nlppos = list_row[row.key][0], nlpneg = list_row[row.key][1], nlpemo = list_row[row.key][2])
            newHistoric.store(targetdb)

    # Return the finished status to Gateway
    return ("Collect Successful")

# Create summarised database of the target information harvested from the historical dataset
def summaryView(design_doc, request, db):

    sa3_count = ViewDefinition(design_doc, request, '''\
        function(doc){
            emit(doc.sa3_id, 1);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    sa3_count.sync(db)

    request_sa3 = request + "pos"
    sa3_pos = ViewDefinition(design_doc, request_sa3, '''\
        function(doc){
            emit(doc.sa3_id, doc.nlppos);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    sa3_pos.sync(db)

    request_sa3 = request + "neg"
    sa3_neg = ViewDefinition(design_doc, request_sa3, '''\
        function(doc){
            emit(doc.sa3_id, doc.nlpneg);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    sa3_neg.sync(db)

    request_sa3 = request + "emo"
    sa3_emo = ViewDefinition(design_doc, request_sa3, '''\
        function(doc){
            emit(doc.sa3_id, doc.nlpemo);
        }''','''function(keys, values, rereduce){
              return sum(values);
        }''', wrapper = Row, group = True)
    sa3_emo.sync(db)

    return sa3_count, sa3_pos, sa3_neg, sa3_emo

def create_summary_cluster(couch, receive_keyword):
    # Create summarised database (dbsh stands for database summary historic)
    db_name = "historic_" + receive_keyword + "_summary"
    try:
        dbsh = couch[db_name]
    except:
        dbsh = couch.create(db_name)
    return dbsh

# Create class for generating objects of summaried data
manager = CouchDBManager()
class HistoricSummary(Document):
    doc_type = 'summary'
    _id = TextField()
    tweet_count = IntegerField()
    nlppos = FloatField()
    nlpneg = FloatField()
    nlpemo = FloatField()
manager.add_document(HistoricSummary)

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
            new_summary = HistoricSummary(_id = i, tweet_count = list_count[i], nlppos = list_pos[i] / list_count[i],
            nlpneg = list_neg[i] / list_count[i], nlpemo = list_emo[i] / list_count[i])
            new_summary.store(summarydb)

    # Return the mean value of the selected feature in a json format
    return ("Mission Accomplished")

# Activate the harvester of Aurin for the target value in a specified region scale

def historic_work(couch, receive_keyword):
    dbrt =  create_cluster(couch, receive_keyword)
    dbraw = couch["historic_raw"]
    requestText, requestSA3 = KeyData("historic", receive_keyword, dbraw)
    store_target(requestText, requestSA3, dbraw, dbrt)
    sa3_count, sa3_pos, sa3_neg, sa3_emo = summaryView('summary', receive_keyword, dbrt)
    dbsh = create_summary_cluster(couch, receive_keyword)
    summary_target(sa3_count, sa3_pos, sa3_neg, sa3_emo, dbrt, dbsh)
    return True