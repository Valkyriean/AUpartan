# Qianjun Ding 1080391
# Zhiyuan Gao 1068184
# Jiachen Li 1068299
# Yanting Mu 1068314
# Chi Zhang 1067750

import json
import csv
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField, IntegerField
from couchdb.design import ViewDefinition


def set_aurin_cluster(couch):
    # Set up database for preserving aurin data
    try:
        dbsa3 = couch['aurin_sa3']
    except:
        dbsa3 = couch.create('aurin_sa3')
    try:
        dbcity = couch['aurin_city']
    except:
        dbcity = couch.create('aurin_city')
    return dbsa3, dbcity


manager = CouchDBManager()


class AurinSA3(Document):
    doc_type = 'AurinSA3'
    code = TextField()
    income = FloatField()
    payroll = FloatField()


manager.add_document(AurinSA3)


class AurinCity(Document):
    doc_type = 'AurinCity'
    code = TextField()
    city = TextField()
    immigration = FloatField()
    salary = IntegerField()


manager.add_document(AurinCity)

# db should be return of setup_db function, file_payroll and file_income should be the path to the assigned json file(string)


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
                income_list[str(instance[sa3])] = (
                    float(instance[income_level]))
    exist_list = []
    # duplicate check
    try:
        code_list = ViewDefinition('AurinSA3', 'code_list', '''\
            function(doc){
                emit(doc.code, 1 )

            }
        '''
                                   )
        code_list.sync(db)
        list_output = code_list(db)
        for row in list_output:
            exist_list.append(row.key)
    except:
        exist_list = []

    # Read in payroll data and store income & payroll data in each SA3 regions into couchdb together
    payroll_level_later = "wk_end_2020_10_03"
    sa3_name = "sa3_code16"
    with open(file_payroll, 'r') as f:
        payroll = json.load(f)
        for i in payroll["features"]:
            instance = i["properties"]
            sa3_code = str(instance[sa3_name])
            # Store the wealth information in each SA3 regions into couch db
            if (sa3_code) not in exist_list:  # (sa3_code) not in db:
                new_wealth = AurinSA3(
                    code=sa3_code, income=income_list[sa3_code], payroll=instance[payroll_level_later])
                new_wealth.store(db)
                exist_list.append(sa3_code)
    return ("Load Successful")

# db should be return of setup_db function, file_immi should assigned json file(string)


def store_aurin_city(file_immi, file_salary, db):
    city_list = ["Melbourne", "Sydney", "Brisbane",
                 "Adelaide", "Darwin", "Hobart", "Capital", "Perth"]
    city_salary = {}
    head = True
    exist_list = []
    try:
        code_list = ViewDefinition('AurinCity', 'code_list', '''\
            function(doc){
                emit(doc.code, 1 )
            }
        '''
                                   )
        code_list.sync(db)
        list_output = code_list(db)
        for row in list_output:
            exist_list.append(row.key)
    except:
        exist_list = []

    with open(file_salary, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if (head):
                head = False
                continue
            else:
                city_salary[row[0]] = int(row[1])
    with open(file_immi, 'r') as f:
        immiRecord = json.load(f)
        for element in immiRecord["features"]:
            for i in city_list:
                if (i in element["properties"]["gccsa_name_2016"]):
                    if i == "Capital":
                        # element["properties"]["gccsa_code_2016"] not in db:
                        if element["properties"]["gccsa_code_2016"] not in exist_list:
                            new_immi = AurinCity(code=element["properties"]["gccsa_code_2016"], city="Canberra", immigration=element["properties"]
                                                 ["ctznshp_stts_prsns_brn_ovrss_cnss_astrln_ctzn_pc"], salary=city_salary["Canberra"])
                            new_immi.store(db)
                            exist_list.append(
                                element["properties"]["gccsa_code_2016"])
                    else:
                        if element["properties"]["gccsa_code_2016"] not in exist_list:
                            new_immi = AurinCity(code=element["properties"]["gccsa_code_2016"], city=i, immigration=element["properties"]
                                                 ["ctznshp_stts_prsns_brn_ovrss_cnss_astrln_ctzn_pc"], salary=city_salary[i])
                            new_immi.store(db)
                            exist_list.append(
                                element["properties"]["gccsa_code_2016"])
    return ("Load Successful")


def preserve_aurin(couch):
    dbsa3, dbcity = set_aurin_cluster(couch)
    try:
        store_aurin_sa3("CCCA2/Data/Aurin/SA3/income.json",
                        "CCCA2/Data/Aurin/SA3/payroll.json", dbsa3)
        store_aurin_city("CCCA2/Data/Aurin/City/immirate.json",
                         "CCCA2/Data/Aurin/City/salary.csv", dbcity)
        return True
    except:
        return False
