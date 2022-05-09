from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField
from couchdb.design import ViewDefinition

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

def create_cluster(couch, receive_level, receive_keyword):
    # Create database for storing target summary data
    db_name = "aurin_" + receive_level + "_" + receive_keyword + "_summary"
    try:
        dbrt = couch[db_name]
    except:
        dbrt = couch.create(db_name)
    return dbrt

def import_view(couch, receive_level, receive_keyword):
    # Call database with selected region's scale
    if (receive_level == "sa3"):
        dbraw = couch["aurin_sa3"]
        viewData = extractSA3Data('aurin', receive_keyword, dbraw)
    else:
        dbraw = couch["aurin_city"]
        viewData = extractCityData('aurin', receive_keyword, dbraw)
    return dbraw, viewData

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
    return ("Mission Accomplished")

# Activate the harvester of Aurin for the target value in a specified region scale
def aurin_work(couch, receive_level, receive_keyword):
    dbrt = create_cluster(couch, receive_level, receive_keyword)
    dbraw, viewData = import_view(couch, receive_level, receive_keyword)
    store_target(viewData, dbraw, dbrt)
    return True