import time
import datetime
import os

# Set up logging
import logging.config

import request
import scraper
import xlsx

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def spent_time():
    global start_time
    sec_all = time.time() - start_time
    if sec_all > 60:
        minutes = sec_all // 60
        sec = sec_all % 60
        time_str = f'| {int(minutes)} min {round(sec, 1)} sec'
    else:
        time_str = f'| {round(sec_all, 1)} sec'
    start_time = time.time()
    return time_str


def get_html(url):
    # html = request.get_request(url)
    html = request.get_request_proxy(url)
    # html = scraper.prettify_html(html)
    return html


def get_blogpost_links():
    url = 'https://www.svpg.com/articles/'
    for i in range(1, 28):
        url_cat = url + 'page/' + str(i) + '/'
        logger.debug(f'url_cat: {url_cat}')
        html = get_html(url_cat)
        # logger.debug(f'html: {html}')
        scraper.parse_blogpost_links(html)
    return scraper.save_blogpost_links()


def get_blogpost(url):
    html = get_html(url)
    return html


if __name__ == '__main__':
    time_begin = start_time = time.time()

    # # Get html from page and save into file
    # url = 'https://www.thekwppexperience.com/our-agents/'
    # html = get_html(url)
    # scraper.save_file(html, 'data.html')
    # logger.debug(f'html: {html}')

    html = scraper.read_file('data.html')
    # logger.debug(f'html: {html}')

    data = scraper.parse(html)
    for item in data:
        xlsx.append_xlsx_file(item, 'out.xlsx')




    logger.debug(f'{spent_time()}')
