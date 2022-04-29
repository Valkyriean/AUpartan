import os
import re
import tweepy
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, IntegerField, ListField, FloatField
from couchdb.design import ViewDefinition
from aurin import aurinwealth

bp = Blueprint("hissummary", __name__, url_prefix="/hissummary")

if db_enable:
    try:
        db = couch['aurin']
    except:
        db = couch.create('aurin')

manager = CouchDBManager()

class HisSummary(Document):
    doc_type = 'HisSummary'
    _id = TextField()
    payroll_value = ListField(FloatField())

manager.add_document(HisSummary)

different = ViewDefinition('HisSummary','different','''\
    function(doc){
        emit(doc._id, (doc.payroll_value[0]-doc.payroll_value[1]));
    }''')


@bp.route("/")
def process_data():
    
    different.sync(db)

    for row in different(db):
        print(row.value)
    return ("done")


'''function(keys, values, rereduce){
            return (values);
    }
    '''

