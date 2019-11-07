from .api import search
import sys

if __name__ == '__main__':
    print(sys.argv)
    if not len(sys.argv):
        print("Search term needed!")
    else:
        print(json.dumps(search(sys.argv[0])))