import math
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Extract valid SA3 Code from AURIN dataset
melb_sa3 = []
income_level = "median_aud_2017_18"
file_income = "../Data/Aurin/income.json"
sa3 = "sa3_code"
income_list = {}
with open(file_income, 'r') as f:
    objects = json.load(f)

    for i in objects["features"]:
        instance = i["properties"]
        melb_sa3.append(str(instance["sa3_code"]))

# Collect SA3 code of all regions downloads from Aurin
sf = gpd.read_file("../Data/SA3_2021_AUST_SHP_GDA2020/SA3_2021_AUST_GDA2020.shp")
sf_len = len(sf["SA3_CODE21"])

SA3_codes = []
SA3_names = []
SA3_coords = []
SA3_radius = []
SA3_lon_range = []
SA3_lat_range = []
SA3_coorstr = []

for i in range(sf_len):
    sa3_info = (sf.iloc[[i]])
    sa3_code = (sa3_info["SA3_CODE21"].tolist())[0]

    if sa3_code in melb_sa3:
        SA3_codes.append(sa3_code)
    else:
        continue

    # Estimates radius of SA3 polygons for further usage for twitter search region
    sa3_a = math.sqrt(sa3_info["geometry"].area) * 100
    sa3_radius = round(sa3_a / 2, 5)

    # Record the SA3 names
    sa3_name = (sa3_info["SA3_NAME21"].tolist())[0]
    SA3_names.append(sa3_name)

    # Calculate bounding box of each polygon
    sa3_centroid = sa3_info["geometry"].centroid
    list_coor = Point(sa3_centroid.y, sa3_centroid.x)

    lat_up = round(list_coor.x + sa3_a / 222, 6)
    lat_down = round(list_coor.x - sa3_a / 222, 6)
    SA3_lat_range.append([lat_down, lat_up])

    lon_left = round(list_coor.y - sa3_a / (222 * math.cos(39)), 6)
    lon_right = round(list_coor.y + sa3_a / (222 * math.cos(39)), 6)
    SA3_lon_range.append([lon_left, lon_right])

    four_corner = [lon_left, lat_down, lon_right, lat_up]
    SA3_coords.append(four_corner)
    
    # Deliver coordinates and radius inforation for further usage of twitter harvesting
    coor_info = "[" + str(round(list_coor.x, 5)) + " " + str(round(list_coor.y, 5)) + " " + str(sa3_radius) + "km]"
    SA3_coorstr.append(coor_info)

# Save SA3 geo-information as csv for further usage
df = pd.DataFrame(list(zip(SA3_codes, SA3_names, SA3_lon_range, SA3_lat_range, SA3_coords, SA3_coorstr)),columns = ["SA3_CODE", "SA3_NAME", "SA3_LON", "SA3_LAT", "SA3_COORDS", "SA3_GEOINFO"])
df.to_csv("../Data/Geo/sa3_geoinfo.csv", index = False)