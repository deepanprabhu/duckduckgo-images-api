import unittest
import json
import os

import logging

from duckduckgo_images_api import search
import duckduckgo_images_api

from duckduckgo_images_api.mockery import Mockery
logging.disable(logging.WARN)

class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mockery = Mockery(os.path.join('duckduckgo_images_api','fixtures.json'))
        duckduckgo_images_api.api.requests.post = mockery.mockPost
        duckduckgo_images_api.api.requests.get = mockery.mockGet

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search(self):
        results = search("fake search term")
        fullResults = list(results)

        self.assertEqual(len(fullResults), 193)

if __name__ == '__main__':
    unittest.main()