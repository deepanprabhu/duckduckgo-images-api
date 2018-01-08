=====================
Duckduckgo-Images-Api
=====================

Python Scraper - Scraping `DuckDuckGo`_ image search resutls with simple source code.

First request pulls a much needed token.
From 2nd request, we pull search results for FREE !!

---------------
Getting Started
---------------

Installation
============

.. code:: bash

  git clone https://github.com/rachmadaniHaryono/duckduckgo-images-api
  cd ./duckduckgo-images-api
  pip install .
  # to install package needed for server
  pip install .[server]

or using pip to install it directly from github

.. code:: bash

  pip install git+https://github.com/rachmadaniHaryono/duckduckgo-images-api.git

-----
Usage
-----

When running the following command, the program will run server with threaded and reloader mode on port 500 with database file `ddg.db`

.. code:: bash

  duckduckgo-images-api-server run --threaded --port 5003 --reloader --db-path ddg.db

With above configuration, it can be used as hydrus booru with below booru setting:

.. code:: yaml

  !Booru
  _advance_by_page_num: true
  _image_data: original image url
  _image_id: null
  _name: ddg booru
  _search_separator: +
  _search_url: http://127.0.0.1:5003/?query=%tags%&p_value=-1&page=%index%
  _tag_classnames_to_namespaces: {tag-type-query: ddg query, tag-type-title: ddg title,
    tag-type-url: ddg url}
  _thumb_classname: thumb

-----------------
Running the tests
-----------------

Install the required package:

.. code:: bash

  pip install -r requirements-dev.txt

and run the test with following command:

.. code:: bash

  python -m pytest .

------------
Contributing
------------

If you would like to contribute changes, Feel free to do SO !

Please read `CONTRIBUTING.md`_ for details on our code of conduct, and the process for submitting pull requests to us.

----------
Versioning
----------

We use `SemVer`_ for versioning.

-------
Authors
-------

- `Deepan Prabhu Babu`_ - *Initial works* - `duckduckgo-images-api`_
- `Rachmadani Haryono`_ - Maintainer

-------
License
-------

See the LICENSE.md file for details

---------------
Acknowledgments
---------------

- Thanks to `thibauts`_, for `his duckduckgo program`_

.. _DuckDuckGo: https://duckduckgo.com
.. _thibauts: https://github.com/thibauts
.. _his duckduckgo program: https://github.com/thibauts/duckduckgo
.. _duckduckgo-go-images-api: https://github.com/deepanprabhu/duckduckgo-images-api
.. _Deepan Prabhu Babu: https://github.com/deepanprabhu/duckduckgo-images-api
.. _Rachmadani Haryono: https://github.com/rachmadaniHaryono
.. _SemVer: http://semver.org/
.. _CONTRIBUTING.md: CONTRIBUTING.md
