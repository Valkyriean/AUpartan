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
receive_level = "sa3"
receive_keyword = "crime"
dbraw = couch["historic_raw"]

# Setup raw database for storing target keyword related tweets
db_name = "historic_" + receive_level + "_" + receive_keyword
try:
    dbrt = couch[db_name]
except:
    dbrt = couch.create(db_name)

# Design document for extracting related tweet from preserved historic database
def KeyData(design_doc, request, db):
    requestSA3 = ViewDefinition(design_doc, request, '''function(doc){\
        if (doc.tweet_text.includes("''' + request + '''")){
            emit(doc.sa3_id, doc.tweet_text);
        }
    }''')
    requestSA3.sync(db)
    return requestSA3

requestSA3 = KeyData("historic", receive_keyword, dbraw)

# Function for collecting target data from Aurin preserved database
def store_target(viewData, rawdb, targetdb):

    viewData_result = viewData(rawdb)
    list_row = {}
    for row in viewData_result:
        list_row[row.key] = row.value
    
    print(list_row)
    # Return the mean value of the selected feature in a json format
    return ("Collect Successful")

# Activate the harvester of Aurin for the target value in a specified region scale
store_target(requestSA3, dbraw, dbrt)