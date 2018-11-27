import requests;
import re;
import json;
import time;
import logging;

logging.basicConfig(level=logging.DEBUG);
logger = logging.getLogger(__name__)

def search(keywords, max_results=None):
    url = 'https://duckduckgo.com/';
    params = {
    	'q': keywords
    };

    logger.debug("Hitting DuckDuckGo for Token");

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I);

    if not searchObj:
        logger.error("Token Parsing Failed !");
        return -1;

    logger.debug("Obtained Token");

    headers = {
        'dnt': '1',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'x-requested-with': 'XMLHttpRequest',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6,ms;q=0.4',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://duckduckgo.com/',
        'authority': 'duckduckgo.com',
    }

    params = (
    ('l', 'wt-wt'),
    ('o', 'json'),
    ('q', keywords),
    ('vqd', searchObj.group(1)),
    ('f', ',,,'),
    ('p', '2')
    )

    requestUrl = url + "i.js";

    logger.debug("Hitting Url : %s", requestUrl);

    while True:
        while True:
            try:
                res = requests.get(requestUrl, headers=headers, params=params);
                data = json.loads(res.text);
                break;
            except ValueError as e:
                logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl);
                time.sleep(5);
                continue;

        logger.debug("Hitting Url Success : %s", requestUrl);
        printJson(data["results"]);

        if "next" not in data:
            logger.debug("No Next Page - Exiting");
            exit(0);

        requestUrl = url + data["next"];

def printJson(objs):
    for obj in objs:
        print "Width {0}, Height {1}".format(obj["width"], obj["height"]);
        print "Thumbnail {0}".format(obj["thumbnail"]);
        print "Url {0}".format(obj["url"]);
        print "Title {0}".format(obj["title"].encode('utf-8'));
        print "Image {0}".format(obj["image"]);
        print "__________";

#  search("audi q6");
