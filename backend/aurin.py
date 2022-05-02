import json
#from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, ListField
from couchdb.design import ViewDefinition

#bp = Blueprint("aurin", __name__, url_prefix="/aurin")
# can import setup_db function in historic.py file when finally using
if db_enable:
    try:
        dbw = couch['aurin_wealth']
    except:
        dbw = couch.create('aurin_wealth')

if db_enable:
    try:
        dbi = couch['aurin_immi']
    except:
        dbi = couch.create('aurin_immi')

manager = CouchDBManager()
#afunction to generate document class and update it to the couchDB
def aurin_doc_update(manager):
    class Aurinwealth(Document):
        doc_type = 'Aurinwealth'
        _id = TextField()
        income_value = FloatField()
        payroll_value = ListField(FloatField())
    manager.add_document(Aurinwealth)
    class ImmiRate(Document):
        doc_type = 'ImmiRate'
        GCCSA_code = TextField()
        immi_rate = FloatField()
    manager.add_document(ImmiRate)


#@bp.route("/")
#db should be return of setup_db function, file_payroll and file_income should be the path to the assigned json file(string)
def store_aurin_wealth(file_income, file_payroll,db):
  
    if db_enable:
 
        # Wealth data in SA3 regions load into CouchDB
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

#db should be return of setup_db function, file_immi should assigned json file(string)
def store_aurin_immi(file_immi, db):
    #file_immi = "Data/Aurin/immirate.json"
    if db_enable:
        scenario = "immirate"
        record = {}
        with open(file_immi, 'r') as f:
            immiRecord = json.load(f)    
            for element in immiRecord:
                record[element['properties']['gccsa_code_2016']] = element['properties']['ctznshp_stts_prsns_brn_ovrss_cnss_astrln_ctzn_pc']
        
        for key in record.keys():
            new_immi = ImmiRate(GCCSA_code=key, immi_rate=record[key])
            new_immi.store(db)
    return ("Load Successful")

#this will return a viewResult data type. Access it should use result.row["col_name"]
def aurin_map(db, classname):
    aurin_view_wealth = ViewDefinition(classname, 'wealthCheck','''/
            function(doc){
                    emit()
            }
    ''')
    aurin_view_pay = ViewDefinition(classname, 'wealthCheck','''/
            function(doc){
                    emit()
            }
    ''')

    aurin_view_wealth.sync(db)
    aurin_view_pay.sync(db)
    wealth = aurin_view_wealth(db)
    payroll = aurin_view_pay(db)

    return wealth, payroll