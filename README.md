# DuckDuckGo Image Search API

DuckDuckGo Image Search API is a python application for programmatically downloading DuckDuckGo Image Search Results. This is for educational purposes only !

## How it Works
Tested with Python 2.7.
This project has simple source code to extract image search results, check out api.py.

First request pulls a much needed token,
From 2nd request, we pull search results for FREE !!
We have some basic logic, to retry the search engine when no results are returned.

## Command-Line
```sh
Usage: ddg-image-search [OPTIONS] [KEYWORDS]...

Options:
  --max_results INTEGER
  --help Show this message and exit.
```

Example:
```sh
ddg-image-search blue bus --max_results=2 | jq .
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

If you implement support for python 3. please share.

## Credits
Thanks to,

1) https://github.com/thibauts/duckduckgo
2) https://github.com/rachmadaniHaryono

[Original Author - Deepan Prabhu Babu](https://github.com/deepanprabhu)

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Developer Connect
If you are a passionate developer looking to collaborate on interesting projects, feel free to connect through a PR in this project.