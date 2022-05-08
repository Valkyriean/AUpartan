import json
from app import couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField

try:
    dbsa3 = couch['aurin_sa3']
except:
    dbsa3 = couch.create('aurin_sa3')

try:
    dbcity = couch['aurin_city']
except:
    dbcity = couch.create('aurin_city')

manager = CouchDBManager()

class AurinSA3(Document):
    doc_type = 'AurinSA3'
    _id = TextField()
    income = FloatField()
    payroll = FloatField()
manager.add_document(AurinSA3)

class AurinCity(Document):
    doc_type = 'AurinCity'
    _id = TextField()
    city = TextField()
    immigration = FloatField()
manager.add_document(AurinCity)

#db should be return of setup_db function, file_payroll and file_income should be the path to the assigned json file(string)
def store_aurin_sa3(file_income, file_payroll, db):
       
    # Pre-store income information in each SA3 regions
    income_level = "median_aud_2017_18"
    sa3 = "sa3_code"
    income_list = {}
    with open(file_income, 'r') as f:
        income = json.load(f)

        for i in income["features"]:
            instance = i["properties"]
            if instance[sa3] not in income_list:
                income_list[str(instance[sa3])] = (float(instance[income_level]))

    # Read in payroll data and store income & payroll data in each SA3 regions into couchdb together
    payroll_level_later = "wk_end_2020_10_03"
    sa3_name = "sa3_code16"
    with open(file_payroll, 'r') as f:
        payroll = json.load(f)

        for i in payroll["features"]:
            instance = i["properties"]
            sa3_code = str(instance[sa3_name])
            
            # Store the wealth information in each SA3 regions into couch db
            if (sa3_code) not in db:
                new_wealth = AurinSA3(_id = sa3_code, income = income_list[sa3_code], payroll = instance[payroll_level_later])
                new_wealth.store(db)

    return ("Load Successful")

store_aurin_sa3("../Data/Aurin/SA3/income.json", "../Data/Aurin/SA3/payroll.json", dbsa3)

#db should be return of setup_db function, file_immi should assigned json file(string)
def store_aurin_city(file_immi, db):

    city_list = ["Melbourne", "Sydney", "Brisbane", "Adelaide", "Darwin", "Hobart", "Capital", "Perth"]

    with open(file_immi, 'r') as f:
        immiRecord = json.load(f)

        for element in immiRecord["features"]:
            for i in city_list:
                if (i in element["properties"]["gccsa_name_2016"]):
                    if i == "Capital":
                        if element["properties"]["gccsa_code_2016"] not in db:
                            new_immi = AurinCity(_id = element["properties"]["gccsa_code_2016"], city = "Canberra", immigration = element["properties"]["ctznshp_stts_prsns_brn_ovrss_cnss_astrln_ctzn_pc"])
                            new_immi.store(db)
                    else:
                        if element["properties"]["gccsa_code_2016"] not in db:
                            new_immi = AurinCity(_id = element["properties"]["gccsa_code_2016"], city = i, immigration = element["properties"]["ctznshp_stts_prsns_brn_ovrss_cnss_astrln_ctzn_pc"])
                            new_immi.store(db)

    return ("Load Successful")

store_aurin_city("../Data/Aurin/City/immirate.json", dbcity)