from pickle import TRUE
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, ListField, BooleanField
from couchdb.design import ViewDefinition

bp = Blueprint("aurin", __name__, url_prefix="/aurin")

try:
    db = couch['aurin']
except:
    db = couch.create('aurin')

manager = CouchDBManager()

class aurinpay(Document):
    doc_type = 'aurinpay'
    sa3code = TextField()
    value = ListField(TextField())
    active = BooleanField()

view = ViewDefinition("aurinpay", 'value', '''
    function(doc){
        if (doc.sa3code == '1000'){
            emit(doc.sa3code, doc.value);
        };
    }''')

manager.add_document(aurinpay)

@bp.route("/")
def store_aurin():
  
    if db_enable:#adding filter here,while writing in, to remove nan record, any nan will discard entire record.
        newaurin = aurinpay(sa3code = '1000', value=['1001','1004'], active = TRUE)
        newaurin_1 = aurinpay(sa3code = '1001', value=['1000','1004'], active = TRUE)
        # place the target database in ()of store()
        newaurin.store(db)
        newaurin_1.store(db)

    '''
    # Payroll data load in CouchDB
    scenario = "payroll_covid"
    timepoint_before = "wk_end_2020_01_04"
    timepoint_after = "wk_end_2020_10_03"
    filename = "../Data/Aurin/abs_weekly_payroll_jobs_pc_sa3_2020_oct-870542151270269027.json"

    with open(filename, 'r') as f:
        objects = json.load(f)

        for i in objects["features"]:
            instance = i["properties"]

            if db_enable:
                if str(instance["sa3_code16"]) not in db:
                    db.save({'_id': str(instance["sa3_code16"]), "payroll_scenario": scenario, timepoint_before: instance[timepoint_before], timepoint_after: instance[timepoint_after]})
    
    # Payroll data load in CouchDB
    scenario = "payroll_afterCovid"
    timepoint = "wk_end_2020_01_04"
    filename = "../Data/Aurin/2020-1.json"

    with open(filename, 'r') as f:
        objects = json.load(f)

        for i in objects["features"]:
            instance = i["properties"]

            if db_enable:
                db.save({'id_sa3': instance["sa3_code16"], "payroll_scenario": scenario, 'payroll': instance[timepoint]})'''
    
    return ("Load Successful")

@bp.route("/retrieve")
def retrieve_aurin():
    view.sync(db)
    for row in view(db):
        print(row.value)
    return ("docs")