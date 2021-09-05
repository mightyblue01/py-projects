import glob
import json
import os
from geo_api import find_distance
from housing_logger import logger

base_dir = r"/mnt/c/Users/basan/Documents/root/src/data/domain_listing/14aug"
geodata_file = r"/mnt/c/Users/basan/Documents/root/src/data/domain_listing/14aug/geo_data/australian_postcodes.json"
results_dir = os.path.join(base_dir, "results/")

"""
Looks up geo data from australian postcodes dataset
"""
def read_geo_data():
    all_geo_suburbs = {}
    with open(geodata_file) as fgeo:
        geo_contents = json.load(fgeo)
        for item in geo_contents:
            # for now, only checking Victorian suburbs
            if item["state"].lower() == "vic":
                geoconfig = {}
                sub_name = {}
                geoconfig["lat"] = str(item["Lat_precise"])
                geoconfig["long"] = str(item["Long_precise"])
                #geoconfig["state"] = item["state"]
                sub_name[item["locality"].lower()] = geoconfig
                all_geo_suburbs.update(sub_name)

    return all_geo_suburbs


def spit_suburbs_list(records):
    suburbs = set()
    key = "listing"
    count = 1
    for rec in records:
        count += 1
        if key in rec:
            suburbs.add(rec[key]["propertyDetails"]["suburb"])
        else:
            print(f'key missing for record {count}')

    counter = 1
    with open(results_dir+"suburbs.txt","w") as f:
        for x in suburbs:
            f.write(str(counter)+" "+x+"\n")
            counter += 1

    return suburbs


def parse_json_contents(records):
    # first, give us list of suburbs
    records = spit_suburbs_list(records)

    return records


def filter_required_suburbs(suburbs, geo_data):
    suburbs_list = {}
    #print(f'total geo {(geo_data.keys())}')
    for item in suburbs:
        if item.lower() in geo_data.keys():
            suburbs_list[item.lower()] = geo_data[item.lower()]

    with open(results_dir + "suburb_latlong.json", "w") as f:
        json.dump(suburbs_list, f)

    return suburbs_list

"""
One time function to calculate distances from the capital
city. Uses distancematrix geoapi (one week trial version)
"""
def calculate_distance_from_capital(suburbs_list):
    distance_list = {}
    # lat, long of capital city - Melbourne
    # <Melbourne> dest = {"lat":"-37.8152065","long":"144.96393"}
    # <Geelong> dest = {"lat":"-38.1499181","long":"144.3617186"}
    # <Ballarat> dest = {"lat": "-37.5691087", "long": "143.8563224"}
    # <Bendigo> dest = {"lat": "-36.7570157", "long": "144.2793906"}
    # <Mildura> dest = {"lat": "-34.2151229", "long": "142.1169401"}
    # <Shepparton> dest = {"lat": "-36.383333", "long": "145.4"}
    # <Pakenham> dest = {"lat": "-38.073568", "long": "145.4851308"}
    # <Wodonga> dest = {"lat": "-36.1240938", "long": "146.8817639"}
    dest = {"lat": "-38.3686779", "long": "142.4982086"}
    counter = 1
    for item in suburbs_list:
        src = suburbs_list[item]
        logger.info(f'rest call for {item} latlong {src}')
        distance_list[item] = find_distance(src, dest)
        logger.info(f'suburb {item} distance {distance_list[item]}')
        print(f'suburb {item} distance {distance_list[item]}')
        print(f'record number # {counter}')
        #with open(results_dir + "suburb_distance_Geelong.json", "w") as f:
        #    json.dump(distance_list, f)
        counter += 1
    with open(results_dir+"suburb_distance_Warrnambool.json","w") as f:
        json.dump(distance_list, f)

    return distance_list

def run():
    contents = []
    final_list = []
    json_pattern = os.path.join(base_dir, '*.json')
    file_list = glob.glob(json_pattern)
    for file in file_list:
        with open(file) as f:
            contents.append(json.load(f))
    for outer in contents:
        for inner in outer:
            final_list.append(inner)
    suburbs = parse_json_contents(final_list)
    geo_data = read_geo_data()
    logger.info(f'total records {len(suburbs)}')
    #print(f'total geo records {(geo_data)}')
    suburbs_data = filter_required_suburbs(suburbs, geo_data)
    # now calculate distance of suburbs from capital city(Melbourne)
    #calculate_distance_from_capital(suburbs_data)


if __name__=="__main__":
    #run()
    run()