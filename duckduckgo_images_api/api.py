#!/usr/bin/python3
import re
import json
import time

import requests
import structlog

log = structlog.getLogger(__name__)


def search(keywords, max_results=None, **args):
    """search images."""
    url = 'https://duckduckgo.com/'
    vqd = args.get('vqd', None)
    requestUrl = args.get('request_url', None)
    if vqd is None:
        params = {
            'q': keywords
        }

        # First make a request to above URL, and parse out the 'vqd'
        # This is a special token,
        # which should be used in the subsequent request
        res = requests.post(url, data=params)
        searchObj = re.search(r'vqd=(\d+)\&', res.text, re.M | re.I)
        vqd = searchObj.group(1)

    headers = {
        'dnt': '1',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'x-requested-with': 'XMLHttpRequest',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6,ms;q=0.4',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',  # NOQA
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://duckduckgo.com/',
        'authority': 'duckduckgo.com',
    }

    params = (
        ('l', 'wt-wt'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', vqd),
        ('f', ',,,'),
        ('p', '2')
    )

    if requestUrl is None:
        requestUrl = url + "i.js"

    while True:
        if requestUrl is None:
            break
        log.debug('request url', v=requestUrl)
        res = requests.get(requestUrl, headers=headers, params=params)
        data = json.loads(res.text)
        if "next" not in data:
            requestUrl = None
        else:
            requestUrl = url + data["next"]
        yield {
            'json_data': data,
            'next_request_url': requestUrl,
            'vqd': vqd,
        }
        time.sleep(5)


def print_json(objs):
    for obj in objs:
        print("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        print("Thumbnail {0}".format(obj["thumbnail"]))
        print("Url {0}".format(obj["url"]))
        print("Title {0}".format(obj["title"].encode('utf-8')))
        print("Image {0}".format(obj["image"]))
        print("__________")


if __name__ == '__main__':
    search("dora coloring pages")
