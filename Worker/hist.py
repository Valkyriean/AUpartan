from app import db
import json
import csv
import re
import ast
import os
import math
from emot.emo_unicode import UNICODE_EMOJI
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, ListField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Define function for converting emojis to text for further analysing
def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

# Setup views and designed documents for storing and querying tweets
manager = CouchDBManager()
class Historic(Document):
    doc_type = 'historic'
    _id = TextField()
    sa3_id = TextField()
    nlpvalue = ListField(FloatField())
manager.add_document(Historic)

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

# design-doc should be the doc-type of historic dat document, in string
def set_emoview(design_doc, db):
    emoposlinr = ViewDefinition(design_doc,'positivecount','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[0]);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emoposcount = ViewDefinition(design_doc,'positivenum','''\
        function(doc){
            emit(doc.sa3_id, 1);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emoneglinr = ViewDefinition(design_doc,'negativecount','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[1]);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emonegcount = ViewDefinition(design_doc,'negativenum','''\
        function(doc){
            emit(doc.sa3_id, 1);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emocount = ViewDefinition(design_doc,'count','''\
        function(doc){
            emit(doc.sa3_id, 1);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)

    emolinr = ViewDefinition(design_doc,'emotionnum','''\
        function(doc){
            emit(doc.sa3_id, doc.nlpvalue[2]);
        }''', '''function(keys, values, rereduce){
                return sum(values);
        }''', wrapper = Row, group = True)
    
    emoposlinr.sync(db)
    emoposcount.sync(db)
    emoneglinr.sync(db)
    emonegcount.sync(db)
    emocount.sync(db)
    emolinr.sync(db)
    
    return emoposcount, emoposlinr, emonegcount, emoneglinr, emocount, emolinr

# Load view definition / MapReduce into database for further usage
emoposcount, emoposlinr, emonegcount, emoneglinr, emocount, emolinr = set_emoview('historicnew', db)

# Path: file path for historical data; public_account:threshold for taking an account as public;db:couchDB databaselanguage:language as target
def record_historic(path, data_filepath, public_account, db, language):

    # Read in SA3 code and its geo-information for further usage
    sa3_list = []
    lon_list = []
    lat_list = []
    head = True

    # reading csv file
    with open(path, 'r') as csvfile:
        
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
                    nlp_result = [sia.polarity_scores(text)["pos"], sia.polarity_scores(text)["neg"], sia.polarity_scores(text)["compound"]]

                    # Store historic data's information into couchdb as document without duplication
                    if tweet_id not in db:
                        new_historic = Historic(_id = tweet_id, sa3_id = sa3_num, nlpvalue = nlp_result)
                        new_historic.store(db)

            except Exception as e:
                pass

    return ("Done")

# Load in historic data
record_historic("../Data/Geo/sa3_geoinfo.csv", '../Data/Historic/twitter-melb.json', 3000, db, 'en')

# Function to generate pre-cooked data, store it into new summary database and return it as a json file
def hist_average(viewCount, viewLine, db):

    # Store data into dictionary for further computational usage (generating summarised json)
    average_dict = {}
    count = {}
    line = {}

    # Query data with MapReduce function
    viewCount_result = viewCount(db)
    viewLine_result = viewLine(db)

    for row in viewCount_result:
        count[row.key] = row.value

    for row in viewLine_result:
        line[row.key] = row.value

    # Calcualte average value of each emotional statistic
    for key in count:
        try:
            average_dict[key] = count[key]/line[key]
        except Exception as e:
            average_dict[key] = "value error"
            pass
    
    print(average_dict)

    # Return the mean value of the selected feature in a json format
    return json.dumps(average_dict, indent = 4)

# Call the hist_average function to compute the average value of all sentimental statistic
pos_json = hist_average(emoposlinr, emoposcount, db)
neg_json = hist_average(emoneglinr, emonegcount, db)
emo_json = hist_average(emolinr, emocount, db)