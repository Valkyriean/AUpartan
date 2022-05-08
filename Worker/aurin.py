import json
#from flask import Blueprint
from app import couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, ListField
from couchdb.design import ViewDefinition

receive_level = "SA3"
receive_keyword = "income"

# Create database for storing raw data
db_name = receive_level + "_" + receive_keyword
try:
    dbw = couch[db_name]
except:
    dbw = couch.create(db_name)

read_path = "../Data/Aurin/" + receive_level + "/" + receive_keyword + ".json"

manager = CouchDBManager()
class AurinData(Document):
    doc_type = 'AurinData'
    _id = TextField()
    income_value = FloatField()
    payroll_value = ListField(FloatField())
manager.add_document(AurinData)

def store_aurin(file_income, region, keyword, db):
   
    # Wealth data in SA3 regions load into CouchDB
    if region == "SA3":
        region_code = "sa3_code"
    else:
        region_code = ""
    scenario = "wealth"
    
    # Pre-store income information in each SA3 regions
    income_level = "median_aud_2017_18"
    #file_income = "../Data/Aurin/income.json"
    sa3 = "sa3_code"
    income_list = {}
    with open(file_income, 'r') as f:
        income = json.load(f)

        for i in income["features"]:
            instance = i["properties"]
            if instance[sa3] not in income_list:
                income_list[str(instance[sa3])] = (float(instance[income_level]))

    # Read in payroll data and store income & payroll data in each SA3 regions into couchdb together
    #file_payroll = "../Data/Aurin/payroll.json"
    payroll_level_before = "wk_end_2020_01_04"
    payroll_level_later = "wk_end_2020_10_03"
    sa3_name = "sa3_code16"
    with open(file_payroll, 'r') as f:
        payroll = json.load(f)

        for i in payroll["features"]:
            instance = i["properties"]
            sa3_code = str(instance[sa3_name])
            
            # Store the wealth information in each SA3 regions into couch db
            if (sa3_code) not in db:
                new_wealth = Aurinwealth(_id = sa3_code, income_value = income_list[sa3_code], payroll_value = [instance[payroll_level_before], instance[payroll_level_later]])
                new_wealth.store(db)

    return ("Load Successful")