import unittest
import json
import os

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from duckduckgo_images_api import search
import duckduckgo_images_api

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

duckduckgo_images_api.api.requests.post = MockPost
duckduckgo_images_api.api.requests.get = MockGet

class TestApi(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search(self):
        results = search("fake search term")

        fullResults = list(results)

        self.assertEqual(len(fullResults), 193)

        #self.assertIn(task_name, task.keys())
        
if __name__ == '__main__':
    unittest.main()