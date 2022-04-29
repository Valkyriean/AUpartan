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

bp = Blueprint("hissummary", __name__, url_prefix="/hissummary")

if db_enable:
    try:
        db = couch['historic']
    except:
        db = couch.create('historic')

manager = CouchDBManager()

class HisSummary(Document):
    doc_type = 'HisSummary'
    _id = TextField()
    sa3_id = TextField()
    nlpvalue = ListField(FloatField())

manager.add_document(HisSummary)

emopos = ViewDefinition('HisSummary','positive','''\
    function(doc){
        emit(doc.sa3_id, doc.nlpvalue[0]);
    }''', '''function(keys, values, rereduce){
            return (sum(values) / values.length);
    }''', wrapper = Row, group = True)

emoneg = ViewDefinition('HisSummary','negative','''\
    function(doc){
        emit(doc.sa3_id, doc.nlpvalue[1]);
    }''', '''function(keys, values, rereduce){
            return (sum(values) / values.length);
    }''', wrapper = Row, group = True)

emo = ViewDefinition('HisSummary','emotion','''\
    function(doc){
        emit(doc.sa3_id, doc.nlpvalue[2]);
    }''', '''function(keys, values, rereduce){
            return (sum(values) / values.length);
    }''', wrapper = Row, group = True)

emocount = ViewDefinition('HisSummary','count','''\
    function(doc){
        emit(doc.sa3_id, 1);
    }''', '''function(keys, values, rereduce){
            return sum(values);
    }''', wrapper = Row, group = True)


# @synchronized
@bp.route("/")
def process_data():

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

    print(emopos_list)
    print(emoneg_list)
    print(emo_list)
    print(emocount_list)

    return ("test")