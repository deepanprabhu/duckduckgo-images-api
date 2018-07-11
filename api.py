import requests
import re
import json
import time

def search(keyword, max_results = 50, refreshes=10):
    url = 'https://duckduckgo.com/';
    params = {
    	'q': keyword
    };
    
    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=(\d+)\&', res.text, re.M|re.I)
    
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
        ('q', keyword),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '2')
        )
    
    requestUrl = url + "i.js";

    image_urls = []
    
    for result in range(refreshes):
        res = requests.get(requestUrl, headers=headers, params=params)
        
        try:
            data = json.loads(res.text)
        except:
            print("there was a problem pulling from DuckDuckgo")
            print(res)
            print("----")
            break
        
        #scroll through the images on this page and pull out their urls
        for image in data['results']:
            
            im_url = image['image']
            
            #check the url has not been found once already
            if im_url not in image_urls:
                image_urls.append(im_url)
                
            else:
                print("Double found, %s"%im_url)
                
        #if we now have more images than we need we can simply return the
        #number of urls we wanted
        if len(image_urls) >= max_results:
            return image_urls[0:max_results]
          
          
        #if theres no next page we've run out of results and need to stop
        if "next" not in data:
            break
        requestUrl = url + data["next"]
        
        print("having a sleep to prevent rate limiting")
        time.sleep(1)
    
    return image_urls
