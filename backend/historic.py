# Import library
import json
import csv
import re
import ast
import os
import math
from emot.emo_unicode import UNICODE_EMOJI
#from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, ListField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row

# Install vader_lexicon for sentimental analysis of historic data
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Set up NLP analysis tools
sia = SentimentIntensityAnalyzer()

def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

#this should put in the name of your db in string, return couchdb,db object, needed for write in and view
def setup_db(db_name):
    if db_enable:
        try:
            db = couch[db_name]
        except:
            db = couch.create(db_name)
        return db
    else:
        print("db error")
        return None

# Setup database in couchdb for stroing historic tweet information
#bp = Blueprint("historic", __name__, url_prefix="/historic")

# Setup views and designed documents for storing and querying tweets
manager = CouchDBManager()

class Historic(Document):
    doc_type = 'historic'
    _id = TextField()
    sa3_id = TextField()
    nlpvalue = ListField(FloatField())
manager.add_document(Historic)


#public_account:threshold for taking an account as public
def record_verify_hist(record_dict,public_account, language):
    if (record_dict["doc"]["coordinates"] == None):# Exclude the tweet without coordinates' information # Only analyse and collect the tweet sent in English
        return False
    if (record_dict["doc"]["user"]["followers_count"] > public_account):# Only include the tweet which is sent by the account with less than certain followers (exclude the Official Account)
        return False
    if (record_dict["doc"]["lang"] != language): # Only analyse and collect the tweet sent in English(or given language)
        return False
    if (record_dict["doc"]["retweeted"] == True):# Exclude the retweet# Only analyse and collect the tweet sent in English
       return False             
    return True

#path:file path for historical data; public_account:threshold for taking an account as public;db:couchDB databaselanguage:language as target
def record_historic(path,data_filepath ,public_account,db,language):

    # Read in SA3 code and its geo-information for further usage
    #filename = "../Data/Geo/sa3_geoinfo.csv"
    filename = path
    sa3_list = []
    lon_list = []
    lat_list = []
    head = True

    # reading csv file
    with open(filename, 'r') as csvfile:
        
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # Store lat, lon range information of each SA3 area into lists
        for row in csvreader:
            if (head):
                head = False
                continue
            else:
                sa3_list.append(row[0])
                lon_list.append(ast.literal_eval(row[2]))
                lat_list.append(ast.literal_eval(row[3]))

    # Read in historic tweet data with json and process it with nltk package for sentimental analysing
    #data_filepath = '../Data/Historic/twitter-melb.json'
    file_size = os.path.getsize(data_filepath)
    read_end = math.ceil(file_size)
    current_pointer_index = 0
    #public_account = 3000

    with open(data_filepath, 'r', encoding = "utf8") as map_file:
            
        while current_pointer_index < read_end:

            line_record = map_file.readline()
            current_pointer_index = map_file.tell()

            # Preprocess before converting string to dict with json.loads
            new_line = line_record.rstrip("]}")
            new_line = new_line.rstrip("\n")
            new_line = new_line.rstrip("\r")
            new_line = new_line.rstrip(",")

            try:
                record_dict = json.loads(new_line)

                if record_verify_hist(record_dict,public_account, language):
                    # Allocate tweet into specific SA3 region with its coordinate
                    tweet_coor = record_dict["doc"]["coordinates"]["coordinates"]
                    for j in range(len(lon_list)):
                        if ((tweet_coor[0] > lon_list[j][0] and tweet_coor[0] < lon_list[j][1]) and
                        (tweet_coor[1] > lat_list[j][0] and tweet_coor[1] < lat_list[j][1])):
                            sa3_num = sa3_list[j]
                            break
                                
                    # Store tweet_id for duplication checking in couchdb
                    tweet_id = record_dict["doc"]["_id"]

                    # Store NLP sentimental score into couchdb
                    text = convert_emojis(record_dict["doc"]["text"])
                    text = re.sub('http://\S+|https://\S+', '', text)
                    nlp_result = [sia.polarity_scores(text)["neg"], sia.polarity_scores(text)["pos"], sia.polarity_scores(text)["compound"]]

                    # Store historic data's information into couchdb as document without duplication
                    if tweet_id not in db:
                        new_historic = Historic(_id = tweet_id, sa3_id = sa3_num, nlpvalue = nlp_result)
                        new_historic.store(db)

            except Exception as e:
                pass
    return ("Done")

#design-doc should be the doc-type of historic dat document, in string
def set_emoview(design_doc):
    emoposcount = ViewDefinition(design_doc,'positivecount','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[0]);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emoposlinr = ViewDefinition(design_doc,'positivenum','''\
        function(doc){
            emit(doc.sa3_id, 1);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emonegcount = ViewDefinition(design_doc,'negativecount','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[1]);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emoneglinr = ViewDefinition(design_doc,'negativenum','''\
        function(doc){
            emit(doc.sa3_id, 1);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emocounts = ViewDefinition(design_doc,'emotioncount','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[2]);
        }''', '''function(keys, values, rereduce){
                return (sum(values) / values.length);
        }''', wrapper = Row, group = True)
    
    emolinr = ViewDefinition(design_doc,'emotionnum','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[2]);
        }''', '''function(keys, values, rereduce){
                return (sum(values) / values.length);
        }''', wrapper = Row, group = True)

    emocount = ViewDefinition(design_doc,'count','''\
        function(doc){
            emit(doc.sa3_id, 1);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)
    return emoposcount, emonegcount,emoneglinr, emocounts, emolinr, emocount, emoposlinr

#db be the result of set_result function, others should be return of set_emoview function, be careful of the order
def process_data(db, emopos, emoneg, emo, emocount):

    emopos.sync(db)
    emoneg.sync(db)
    emo.sync(db)
    emocount.sync(db)

    emopos_list = []
    emoneg_list = []
    emo_list = []
    emocount_list = []

    emopos_dict = emopos(db)
    emoneg_dict = emoneg(db)
    emo_dict = emo(db)
    emocount_dict = emocount(db)

    for row in emopos_dict:
        emopos_list.append(row.value)
    for row in emoneg_dict:
        emoneg_list.append(row.value)
    for row in emo_dict:
        emo_list.append(row.value)
    for row in emocount_dict:
        emocount_list.append(row.value)

    #for row in emopo:
     #   emopos_list.append(row.value)
    #for row in emoneg(db):
     #   emoneg_list.append(row.value)
    #for row in emo(db):
     #   emo_list.append(row.value)
    #for row in emocount(db):
     #   emocount_list.append(row.value)

    #print(emopos_list)
    #print(emoneg_list)
    #print(emo_list)
    #print(emocount_list)

    return emopos_list, emoneg_list, emo_list, emocount_list

#a general version of function above, to reduce the probability of the overflow problem of above function
def run_single_request_hist(view, db):
    view.sync(db)
    view_dict = {}
    view_result = view(db)
    for row in view_result:
        view_dict[row.key] = row.value
    
    return json.dumps(view_dict, indent=4)

#a function that return average of each key, just in case there will be error for process_data()function
def hist_average(viewCount, viewLine, db):
    viewCount.sync(db)
    viewLine.sync(db)
    average_dict = {}
    count = {}
    line = {}
    viewCount_result = viewCount(db)
    viewLine_result = viewLine(db)
    for row in viewCount_result:
        count[row.key] = row.value
    for row in viewLine_result:
        line[row.key] = row.value
    for key in count:
        try:
            average_dict[key] = count[key]/line[key]
        except Exception as e:
            average_dict[key] = "value error"
            #pass
    
    return json.dumps(average_dict, indent=4)



#code to run above code
#save
dbh = setup_db("historic")
record_historic("../Data/Geo/sa3_geoinfo.csv", '../Data/Historic/twitter-melb.json', 3000, dbh, 'en')
#readwith map-reduce
emoposcount, emonegcount,emoneglinr, emocounts, emolinr, emocount, emoposlinr = set_emoview('historic')
#emopos_list, emoneg_list, emo_list, emocount_list = process_data(dbh, emopos, emoneg, emo, emocount)

