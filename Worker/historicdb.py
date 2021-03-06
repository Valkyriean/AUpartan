# Group 1 Melbourne
# Qianjun Ding 1080391
# Zhiyuan Gao 1068184
# Jiachen Li 1068299
# Yanting Mu 1068314
# Chi Zhang 1067750

import json
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField

# Setup couchd for storing raw data of historic database


def set_historic_cluster(couch):
    try:
        dbhr = couch['historic_raw']
    except:
        dbhr = couch.create('historic_raw')
    return dbhr


manager = CouchDBManager()


class HistoricRaw(Document):
    doc_type = 'historic_raw'
    _id = TextField()
    sa3_id = TextField()
    tweet_text = TextField()


manager.add_document(HistoricRaw)


def store_historic(data_filepath, db):

    with open(data_filepath, 'r', encoding="utf8") as map_file:

        line_record = map_file.readline()

        record_dict = json.loads(line_record)

        for i in record_dict:
            if i not in db:
                new_historic = HistoricRaw(
                    _id=i, sa3_id=record_dict[i]["sa3_id"], tweet_text=record_dict[i]["tweet_text"])
                new_historic.store(db)
    print("Historic Done")
    return ("Done")


def preserve_historic(couch):
    dbhr = set_historic_cluster(couch)
    try:
        store_historic('CCCA2/Data/Historic/preprocess_historic.json', dbhr)
        print('store finish')
        return True
    except:
        return False
