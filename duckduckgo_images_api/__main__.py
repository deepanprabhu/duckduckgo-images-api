from .api import search
import sys
import json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Search term needed!")
        print("Usage: python -m duckduckgo_images_api TERM count(optional)")
    else:
        count = 40
        if (len(sys.argv) > 2):
            count = int(sys.argv[2])
        print(json.dumps(search(sys.argv[1], count)))