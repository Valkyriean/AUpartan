import json
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, ListField

bp = Blueprint("aurin", __name__, url_prefix="/aurin")

if db_enable:
    try:
        db = couch['aurin']
    except:
        db = couch.create('aurin')

manager = CouchDBManager()

class aurinwealth(Document):
    doc_type = 'aurinwealth'
    _id = TextField()
    income_value = FloatField()
    payroll_value = ListField(FloatField())

manager.add_document(aurinwealth)

@bp.route("/")
def store_aurin():
  
    if db_enable:
 
        # Wealth data in SA3 regions load into CouchDB
        scenario = "wealth"
        
        # Pre-store income information in each SA3 regions
        income_level = "median_aud_2017_18"
        file_income = "../Data/Aurin/income.json"
        sa3 = "sa3_code"
        income_list = {}
        with open(file_income, 'r') as f:
            objects = json.load(f)

            for i in objects["features"]:
                instance = i["properties"]
                if instance[sa3] not in income_list:
                    income_list[str(instance[sa3])] = (float(instance[income_level]))

        # Read in payroll data and store income & payroll data in each SA3 regions into couchdb together
        file_payroll = "../Data/Aurin/payroll.json"
        payroll_level_before = "wk_end_2020_01_04"
        payroll_level_later = "wk_end_2020_10_03"
        sa3_name = "sa3_code16"
        with open(file_payroll, 'r') as f:
            objects = json.load(f)

            for i in objects["features"]:
                instance = i["properties"]
                sa3_code = str(instance[sa3_name])
                
                # Store the wealth information in each SA3 regions into couch db
                if (sa3_code) not in db:
                    new_wealth = aurinwealth(_id = sa3_code, income_value = income_list[sa3_code], payroll_value = [instance[payroll_level_before], instance[payroll_level_later]])
                    new_wealth.store(db)

    return ("Load Successful")