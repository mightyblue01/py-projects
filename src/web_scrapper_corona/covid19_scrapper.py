import requests
from bs4 import BeautifulSoup
from covid19_logger import logger
from send_email import send_email
import datetime
import sys

COVID19_URL = 'https://www.worldometers.info/coronavirus/'

def extract_metadata(raw_data, input_country_list):
    try:
        country_list = {}
        data_section = raw_data.find(class_='main_table_countries_div')
        trs = data_section.findAll('tr')
        for tr in trs:
            tds = tr.findAll('td')
            for td in tds:
                country_url = td.find('a')
                if country_url != None:
                    country_data = 'total cases '+td.find_next_sibling("td").text + ', total deaths '+\
                                   td.find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").text
                    country_list[country_url.text]=country_data
        message = '\n\n'
        for k in country_list:
            if k in input_country_list:
                message += k+': '+country_list[k]+'\n'

        now = datetime.datetime.now()
        message += "\n\n Statistics as of {}".format(now.strftime("%Y-%m-%d %H:%M:%S"))
        return message
    except Exception as e:
        logger.exception('Exception occured in extract_metadata method {}'.format(e))

def scrape_url():
    logger.info('going to fetch url ')
    try:
        contents = requests.get(COVID19_URL)
        return BeautifulSoup(contents.text,'html.parser')
    except Exception as e:
        logger.exception('Error in scrape_url module {}'.fomat(e))

def process_scrapping_request(country_list, sender_email, receiver_email):
    raw_data = scrape_url()
    result_data = extract_metadata(raw_data, country_list)
    logger.info(result_data)
    send_email(result_data, sender_email, receiver_email)

if __name__ == '__main__':
    country_list = sys.argv[1]
    sender_email = sys.argv[2]
    receiver_email = sys.argv[3]

    result_data = process_scrapping_request(country_list, sender_email, receiver_email)

