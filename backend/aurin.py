import json
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document
from couchdb.mapping import TextField

bp = Blueprint("aurin", __name__, url_prefix="/aurin")

try:
    db = couch['aurin']
except:
    db = couch.create('aurin')

class aurinpay(Document):
    doc_type = 'aurindata'
    sa3code = TextField()
    t1003 = TextField()
    t0104 = TextField()

@bp.route("/")
def store_aurin():
  
    if db_enable:
        newaurin = aurinpay(sa3code = '1000', t1003 = '1001', t0104 = '1004')
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