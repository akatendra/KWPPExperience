import datetime

import os

from bs4 import BeautifulSoup

# Set up logging
import logging.config

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

blogpost_list = []
post_count = 0


def prettify_html(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.prettify()


def remove_file(file):
    if os.path.isfile(file):
        # os.remove() function to remove the file
        os.remove(file)
        # Printing the confirmation message of deletion
        print("File Deleted successfully")
    else:
        print("File does not exist")


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def save_file(data, filename):
    with open(filename, 'a') as file:
        file.write(data)


def parse(data):
    soup = BeautifulSoup(data, 'lxml')

    persons = soup.select('div[class="col s12 m6 l4"]')
    logger.debug(f'persons: {len(persons)}')
    # logger.debug(f'persons: {persons}')
    data_out = []
    for person in persons:
        logger.debug(f'person: {person}')
        name_raw = person.select_one('h3').text.strip().split()
        name = name_raw[0] + ' ' + name_raw[1]
        logger.debug(f'name: {name}')

        phone_raw = person.select_one('a[href*="tel:"]')
        phone = None
        if phone_raw:
            phone = phone_raw.text.strip()
        logger.debug(f'phone: {phone}')

        email_raw = person.select_one('a[href*="mailto:"]')
        email = None
        if email_raw:
            email = email_raw['href'].replace('mailto:', '')
        logger.debug(f'email: {email}')

        website_raw = person.select_one('a[href*="http"]')
        website = None
        if website_raw:
            website = website_raw['href']
        logger.debug(f'website: {website}')

        person_out = {'name': name,
                      'phone': phone,
                      'email': email,
                      'website': website

        }
        data_out.append(person_out)
    return data_out
