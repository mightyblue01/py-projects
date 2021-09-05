import json
import time
from housing_logger import logger
import requests

API_TOKEN = 'AfJq6n35QdgThpK61EyFixmoGIdAd'
api_base_url = 'https://api.distancematrix.ai/maps/api/distancematrix/json?'

def find_distance(src, dest):
    body = 'origins='+src["lat"]+","+src["long"] \
            + '&destinations='+dest["lat"]+","+dest["long"] \
            + '&key='+ API_TOKEN
    full_url = api_base_url + body
    try:
        response = requests.get(full_url).json()
        print(response["rows"][0]["elements"][0]["distance"]["text"])

        time.sleep(3)
        return response["rows"][0]["elements"][0]["distance"]["text"]

    except Exception as e:
        print(f'Exception for src {src} error {e}')
        return "None"



if __name__=="__main__":
    #src = {"lat":"-37.7409649","long":"145.0683729"}
    #dest = {"lat":"-37.8152065","long":"144.96393"}
    #find_distance(src, dest)
    pass