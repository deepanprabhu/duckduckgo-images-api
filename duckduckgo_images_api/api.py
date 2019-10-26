import requests
import re
import json
import time
import logging

HEADERS = {
    'dnt': '1',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'x-requested-with': 'XMLHttpRequest',
    'accept-language': 'en-GB,en-USq=0.8,enq=0.6,msq=0.4',
    'user-agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'accept': 'application/json, text/javascript, */* q=0.01',
    'referer': 'https://duckduckgo.com/',
    'authority': 'duckduckgo.com',
}

BASE_URL = 'https://duckduckgo.com/'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def search(term, max_results=None):
    token = _get_token(term)

    params = _build_params(term, token)

    request_url = BASE_URL + "i.js"

    results_generator = _get_results(request_url, headers=HEADERS, params=params)

    for results in results_generator:
        for result in results:
            yield result

def _get_token(term, url = BASE_URL):
    params = {
        'q': term
    }

    logger.debug("Hitting DuckDuckGo for Token")

    #   Make a request to above URL, and parse out the 'vqd'
    response = requests.post(url, data=params)
    search_object = re.search(r'vqd=([\d-]+)\&', response.text, re.M|re.I)

    if search_object:
        logger.debug("Obtained Token")
        
        return search_object.group(1)
    else:
        logger.error("Token Parsing Failed !")
        raise Exception("Token Parsing Failed")

def _build_params(term, token):
    return (
        ('l', 'wt-wt'),
        ('o', 'json'),
        ('q', term),
        ('vqd', token),
        ('f', ',,,'),
        ('p', '2')
    )

def _get_results(request_url, headers, params):
    while request_url is not None:
        data = None

        while data is None:
            try:
                response = requests.get(request_url, headers=headers, params=params)
                data = json.loads(response.text)
            except ValueError as _e:
                logger.debug("Hitting Url Failure - Sleep and Retry: %s", request_url)
                time.sleep(5)

        logger.debug("Hitting Url Success : %s", request_url)

        if "next" in data:
            request_url = BASE_URL + data["next"]
        else:
            request_url = None
            logger.debug("No Next Page - Exiting")

        yield data["results"]