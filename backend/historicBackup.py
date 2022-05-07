
"""
import os
import re
from tokenize import group
import tweepy
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, IntegerField, ListField, FloatField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row
import functools, threading

#bp = Blueprint("hissummary", __name__, url_prefix="/hissummary")

@bp.route("/")
def record_historic():

    # Read in SA3 code and its geo-information for further usage
    filename = "../Data/Geo/sa3_geoinfo.csv"
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
    data_filepath = '../Data/Historic/twitter-melb.json'
    file_size = os.path.getsize(data_filepath)
    read_end = math.ceil(file_size)
    current_pointer_index = 0
    public_account = 3000

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


                if ((record_dict["doc"]["coordinates"] != None) and # Exclude the tweet without coordinates' information # Only analyse and collect the tweet sent in English
                (record_dict["doc"]["user"]["followers_count"] <= public_account) and # Only include the tweet which is sent by the account with less than certain followers (exclude the Official Account)
                (record_dict["doc"]["lang"] == "en") and # Only analyse and collect the tweet sent in English
                (record_dict["doc"]["retweeted"] == False)):# Exclude the retweet# Only analyse and collect the tweet sent in English
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

manager = CouchDBManager()
class HisSummary(Document):
    doc_type = 'HisSummary'
    _id = TextField()
    sa3_id = TextField()
    nlpvalue = ListField(FloatField())
manager.add_document(HisSummary)


def set_emoview(design_doc):
    emopos = ViewDefinition(design_doc,'positive','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[0]);
        }''', '''function(keys, values, rereduce){
                return (sum(values) / values.length);
        }''', wrapper = Row, group = True)

    emoneg = ViewDefinition(design_doc,'negative','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[1]);
        }''', '''function(keys, values, rereduce){
                return (sum(values) / values.length);
        }''', wrapper = Row, group = True)

    emo = ViewDefinition(design_doc,'emotion','''\
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
    return emopos, emoneg, emo, emocount


# @synchronized
#@bp.route("/")
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
    """

'''function(doc){
    if (doc.text,includes("''' + request + '''")){
        emit(doc.key, doc.value);
    }
}
'''

