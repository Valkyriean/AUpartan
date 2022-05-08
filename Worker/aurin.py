import json
#from flask import Blueprint
from app import couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, ListField
from couchdb.design import ViewDefinition

receive_level = "sa3"
receive_keyword = "payroll"

# Design document for extracting SA3 / City Aurin Data
def extractSA3Data(design_doc, request, db):
    requestSA3 = ViewDefinition(design_doc, request,'''\
        function(doc){
            emit(doc._id, doc.'''+ request +''');
        }''')
    requestSA3.sync(db)
    return requestSA3

def extractCityData(design_doc, request, db):
    requestCity = ViewDefinition(design_doc, request,'''\
        function(doc){
            emit(doc.city, doc.'''+ request +''');
        }''')
    requestCity.sync(db)
    return requestCity

# Create database for storing target raw data
db_name = receive_level + "_" + receive_keyword
try:
    dbw = couch[db_name]
except:
    dbw = couch.create(db_name)

# Call database with selected region's scale
if (receive_level == "sa3"):
    dbraw = couch["aurin_sa3"]
    viewData = extractSA3Data('aurin', receive_keyword, dbraw)
else:
    dbraw = couch["aurin_city"]
    viewData = extractCityData('aurin', receive_keyword, dbraw)

def store_target(viewData, db):

    line = {}

    viewData_result = viewData(db)

    for row in viewData_result:
        line[row.key] = row.value
    
    print(line)

    # Return the mean value of the selected feature in a json format
    return ("test")

store_target(viewData, dbraw)