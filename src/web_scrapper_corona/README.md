# About
This application extracts Corona virus statistics in a given country/ies and
sends out an email with these numbers to recipients.
# Modules
    covid19_scrapper.py => process_scrapping_request
# Usage
Call the module with following parameters -

    process_scrapping_request(country_list, sender_email, receiver_email):        
# Dependencies
To allow sending emails from Gmail, following setting need to be enabled

    Google Account -> Security -> Less secure app access ON