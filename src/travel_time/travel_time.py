from geopy.geocoders import Nominatim
import ssl
import simplejson, urllib
import datetime
import sys
from traveltime_logger import logger


def calculate_travel_time(origin, destination, apikey):
   try:
        context = ssl._create_unverified_context()
        traffic = "best_guess"
        # best_guess, pesimistic, optimistic
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&traffic_model=" + traffic + "&departure_time=now&origins=" + origin + "&destinations=" + destination + "&mode=driving&language=en-EN&sensor=false&key=" + apikey
        result = simplejson.load(urllib.request.urlopen(url, context=context))
        logger.info(result)
        driving_time = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        driving_distance = result['rows'][0]['elements'][0]['distance']['text']
        logger.info('Driving time from -\n')
        logger.info('{} TO {}\n'.format(src_address,dest_address))
        now = datetime.datetime.now()
        logger.info(' {} , Distance {}. Time now {}'.format(driving_time, driving_distance,
                                                           now.strftime("%Y-%m-%d %H:%M:%S")))
   except Exception as e:
       logger.exception('Exception in calculate_travel_time method {}'.format(e))

def return_latlong(address):
    try:
        geolocator = Nominatim(user_agent="api21311")
        #logger.info('geo cord {}'.format(geolocator.geocode(address).raw))
        return geolocator.geocode(address)
    except Exception as e:
        logger.exception('exception is {}'.format(e))

def process_travel_time_request(src_address, dest_address, api_key):
    src_location = return_latlong(src_address)
    dest_location = return_latlong(dest_address)

    logger.info('source location {} '.format(src_location.address))
    logger.info('source lat {} and long {}'.format(src_location.latitude, src_location.longitude))
    logger.info('destination location {} '.format(dest_location.address))
    logger.info('destination lat {} and long {}'.format(dest_location.latitude, dest_location.longitude))

    src_latlong = str(src_location.latitude)+','+str(src_location.longitude)
    dest_latlong = str(dest_location.latitude)+','+str(dest_location.longitude)
    calculate_travel_time(src_latlong, dest_latlong, api_key)

if __name__=='__main__':
    #src_address = 'Levi's Stadium'
    #dest_address = 'Santa Cruz, California, USA'
    src_address = sys.argv[1]
    dest_address = sys.argv[2]
    api_key = sys.argv[3]
    process_travel_time_request(src_address, dest_address, api_key)