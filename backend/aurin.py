import json
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document,ViewDefinition
from couchdb.mapping import TextField,ListField,ViewField

bp = Blueprint("aurin", __name__, url_prefix="/aurin")

try:
    db = couch['aurin']
except:
    db = couch.create('aurin')

class aurinpay(Document):
    doc_type = 'aurinpay'
    sa3code = TextField()
    value=ListField(TextField())

#emit(doc.sa3code, (parseFloat(doc.calue[0])-parseFloat(doc.value[1])))



@bp.route("/")
def store_aurin():
  
    if db_enable:#adding filter here,while writing in, to remove nan record, any nan will discard entire record.
        newaurin = aurinpay(sa3code = '1000', value=['1001','1004'])
        # place the target database in ()of store()
        newaurin.store(db)

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


#this should return a key-object pair of sa3code and value pair,this requirement does not need reduce function

#emit(doc.sa3code, (parseFloat(doc.calue[0])-parseFloat(doc.value[1])))
#emit above might be able to generate key-object pair of sa3code and difference-of_value pair directly

#in this case reduce might be able to used to find some in-total conclusion, like "how many of them are increasing" see below
different = ViewField("aurinpay", '''\
    function(doc){
        if(doc.doc_type==='aurinpay'){
                emit(doc.sa3code,doc.value);
            });
        };
}
''')
#for  "how many of them are increasing", if emit(doc.sa3code, (parseFloat(doc.calue[0])-parseFloat(doc.value[1])))is used and functional
# hopfully it will work
'''function(keys, values, rereduce){
        var increasing = [];
        values.forEach(function(different){
            if(different > 0){
                increasing.push(different);
            }
        });
        return sum(increasing);
}
'''