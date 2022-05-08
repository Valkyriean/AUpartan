from app import couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField
from couchdb.design import ViewDefinition

# Region scale and keywrods collect from Gateway's task
receive_level = "city"
receive_keyword = "immigration"

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
    dbrt = couch[db_name]
except:
    dbrt = couch.create(db_name)

# Call database with selected region's scale
if (receive_level == "sa3"):
    dbraw = couch["aurin_sa3"]
    viewData = extractSA3Data('aurin', receive_keyword, dbraw)
else:
    dbraw = couch["aurin_city"]
    viewData = extractCityData('aurin', receive_keyword, dbraw)

# Store summarised target aurin data for further calling from the Gateway node and render it onto UI
manager = CouchDBManager()
class AurinTarget(Document):
    doc_type = 'aurintarget'
    _id = TextField()
    target_value = FloatField()
manager.add_document(AurinTarget)

# Function for collecting target data from Aurin preserved database
def store_target(viewData, rawdb, targetdb):

    viewData_result = viewData(rawdb)

    for row in viewData_result:
        if (row.key not in targetdb):
            newAurinTarget = AurinTarget(_id = row.key, target_value = row.value)
            newAurinTarget.store(targetdb)
    
    # Return the mean value of the selected feature in a json format
    return ("Collect Successful")

# Activate the harvester of Aurin for the target value in a specified region scale
store_target(viewData, dbraw, dbrt)