import json
import math
import geopandas as gpd 
from shapely.geometry import Point
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
from couchdb.design import ViewDefinition

bp = Blueprint("geosa3", __name__, url_prefix="/geosa3")

# Setup database in couchdb for stroing tweet information
try:
    db = couch['geodata']
except:
    db = couch.create('geodata')

manager = CouchDBManager()

# Setup views and designed documents for storing and querying SA3 geo-information
view = ViewDefinition("tweet", 'value', '''
    function(doc){
        if (doc.doc_type == 'tweet'){
            emit(doc.id, doc.text);
        };
    }''')

class sa3geo(Document):
    doc_type = 'sa3geo'
    _id = TextField()
    sa3_name = TextField()
    coor_info = TextField()

manager.add_document(sa3geo)

# Collect SA3 code of all regions downloads from Aurin
sf = gpd.read_file("../Data/SA3_2021_AUST_SHP_GDA2020/SA3_2021_AUST_GDA2020.shp")
SA3_group = []
for i in (sf["SA3_CODE21"]):
    SA3_group.append(i)

# Extract SA3 information in Greater Melbourne and Store them into couchdb
@bp.route("/")
def store_sa3geo():
    filename = "../Data/Aurin/payroll.json"
    with open(filename, 'r') as f:
        objects = json.load(f)

        for i in objects["features"]:

            # Extract instance from json
            instance = i["properties"]

            # Find out corresponding SA3 regions
            sa3_code = str(instance["sa3_code16"])
            sa3_data_row = sf.iloc[[SA3_group.index(sa3_code)]]

            # Estimates radius of SA3 polygons for further usage for twitter search region
            sa3_radius = round(math.sqrt(sa3_data_row["geometry"].area) * 100 / 2, 5)

            # Record the SA3 names
            sa3_name = (sa3_data_row["SA3_NAME21"].tolist())[0]

            # Calculate centroid of each polygon
            sa3_centroid = sa3_data_row["geometry"].centroid
            list_coor = Point(sa3_centroid.y, sa3_centroid.x)
            
            # Deliver coordinates and radius inforation for further usage of twitter harvesting
            coor_info = str(round(list_coor.x, 5)) + "," + str(round(list_coor.y, 5)) + "," + str(sa3_radius) + "km"

            # Store the SA3 information into couchdb without duplication
            if (db_enable):
                if (sa3_code) not in db:
                    new_sa3geo = sa3geo(_id = sa3_code, sa3_name = sa3_name, coor_info = coor_info)
                    new_sa3geo.store(db)
    
    return ("done")