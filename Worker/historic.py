from sqlalchemy import Float
from app import couch
import json
import csv
import re
import ast
import os
import math
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
from couchdb.mapping import TextField, FloatField
from couchdb.design import ViewDefinition

# Region scale and keywrods collect from Gateway's task
receive_keyword = "all"
dbraw = couch["historic_raw"]

# Setup raw database for storing target keyword related tweets
db_name = "historic_" + receive_keyword
try:
    dbrt = couch[db_name]
except:
    dbrt = couch.create(db_name)

# Design document for extracting related tweet from preserved historic database
def KeyData(design_doc, request, db):

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

    return requestText, requestSA3
    
def KeyDataAll(design_doc, request, db):
    requestTextAll = ViewDefinition(design_doc, request, '''\
        function(doc){
            emit(doc._id, doc.tweet_text);
        }''')
    requestTextAll.sync(db)

    request_sa3 = request + "_sa3"
    requestSA3All = ViewDefinition(design_doc, request_sa3, '''\
        function(doc){
            emit(doc._id, doc.sa3_id);
        }''')
    requestSA3All.sync(db)

    return requestTextAll, requestSA3All

if receive_keyword != "all":
    requestText, requestSA3 = KeyData("historic", receive_keyword, dbraw)
else:
    requestText, requestSA3 = KeyDataAll("historicall", receive_keyword, dbraw)

到此为止是设计all和普通keyword的区别view def

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

# Activate the harvester of Aurin for the target value in a specified region scale
store_target(requestText, requestSA3, dbraw, dbrt)