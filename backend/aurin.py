import json
from flask import Blueprint
from flask import Flask
from app import db_enable, couch

bp = Blueprint("aurin", __name__, url_prefix="/aurin")

try:
    db = couch['aurin']
except:
    db = couch.create('aurin')

@bp.route("/")
def store_aurin():

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
    '''scenario = "payroll_afterCovid"
    timepoint = "wk_end_2020_01_04"
    filename = "../Data/Aurin/2020-1.json"

    with open(filename, 'r') as f:
        objects = json.load(f)

        for i in objects["features"]:
            instance = i["properties"]

            if db_enable:
                db.save({'id_sa3': instance["sa3_code16"], "payroll_scenario": scenario, 'payroll': instance[timepoint]})'''
    
    return ("Load Successful")


from flaskext.couchdb import Document
import uuid
# a data structue class for aurin data of payment
class aurinpay(Document):
    doc_type='aurindata'

    sa3code=TextField()
    t1003rate=TextField()
    t0104rate=TextField()       

newaurin = aurinpay(sa3code='1000', t1003rate=1001, t0104rate=1004)
newaurin.id = uuid.uuid4().hex
#place the target database in ()of store()
newaurin.store()

