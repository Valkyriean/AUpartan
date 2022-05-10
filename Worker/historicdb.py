import json
import csv
import re
import ast
import os
import math
from emot.emo_unicode import UNICODE_EMOJI
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField

# Define function for converting emojis to text for further analysing
def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

# Setup couchd for storing raw data of historic database
def set_historic_cluster(couch):
    try:
        dbhr = couch['historic_raw']
    except:
        dbhr = couch.create('historic_raw')
    return dbhr

# Setup views and designed documents for storing and querying tweets
manager = CouchDBManager()
class HistoricRaw(Document):
    doc_type = 'historic_raw'
    _id = TextField()
    sa3_id = TextField()
    tweet_text = TextField()
manager.add_document(HistoricRaw)

#public_account:threshold for taking an account as public
def record_verify_hist(record_dict, public_account, language):
    if (record_dict["doc"]["coordinates"] == None): # Exclude the tweet without coordinates' information # Only analyse and collect the tweet sent in English
        return False
    if (record_dict["doc"]["user"]["followers_count"] > public_account): # Only include the tweet which is sent by the account with less than certain followers (exclude the Official Account)
        return False
    if (record_dict["doc"]["lang"] != language): # Only analyse and collect the tweet sent in English(or given language)
        return False
    if (record_dict["doc"]["retweeted"] == True): # Exclude the retweet# Only analyse and collect the tweet sent in English
       return False             
    return True

# Path: file path for historical data; public_account:threshold for taking an account as public;db:couchDB databaselanguage:language as target
def record_historic(csv_path, data_filepath, public_account, db, language):

    # Read in SA3 code and its geo-information for further usage
    sa3_list = []
    lon_list = []
    lat_list = []
    head = True

    # reading csv file
    with open(csv_path, 'r') as csvfile:
        
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
    file_size = os.path.getsize(data_filepath)
    read_end = math.ceil(file_size)
    current_pointer_index = 0

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

                if record_verify_hist(record_dict, public_account, language):
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

                    # Store historic data's information into couchdb as document without duplication
                    if tweet_id not in db:
                        new_historic = HistoricRaw(_id = tweet_id, sa3_id = sa3_num, tweet_text = text)
                        new_historic.store(db)

            except Exception as e:
                pass

    return ("Done")

def preserve_historic(couch):
    dbhr = set_historic_cluster(couch)
    record_historic("CCCA2/Data/Geo/sa3_geoinfo.csv", 'CCCA2/Data/Historic/twitter-melb.json', 3000, dbhr, 'en')
    return True