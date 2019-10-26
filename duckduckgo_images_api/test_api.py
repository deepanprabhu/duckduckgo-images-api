import unittest
import json
import os

import logging

from duckduckgo_images_api import search
import duckduckgo_images_api

logging.disable(logging.WARN)
logger = logging.getLogger(__name__)

class MockResponse:
    def __init__(self, value):
        self.value = value

    @property
    def text(self):
        logger.debug("Returning Mock Value")
        return self.value

def MockPost(*args, **kwargs):
    logger.debug("MockPost")
    return MockResponse("other things andvqd=7&more stuff")

with open(os.path.join('duckduckgo_images_api','fixtures.json'), 'r') as handle:
    FIXTURES = json.load(handle)

def get_fixture():
    return FIXTURES.pop()

def MockGet(*args, **kwargs):
    logger.debug("MockGet")

    return MockResponse(get_fixture())

class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        duckduckgo_images_api.api.requests.post = MockPost
        duckduckgo_images_api.api.requests.get = MockGet

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search(self):
        # duckduckgo_images_api.api.logger
        # logging.getLogger(results.__name__)
        with self.assertLogs(logger=duckduckgo_images_api.api.logger, level='DEBUG') as cm:
            results = search("fake search term")
            fullResults = list(results)

        self.assertEqual(len(fullResults), 193)

if __name__ == '__main__':
    unittest.main()