import unittest
import json
import os
import sys

import logging

from duckduckgo_images_api import search
import duckduckgo_images_api

from duckduckgo_images_api.mockery import Mockery

class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.setUpMockery()

    def setUpMockery(self):
        mockery = Mockery(os.path.join('duckduckgo_images_api','fixtures.json'))
        duckduckgo_images_api.api.requests.post = mockery.mockPost
        duckduckgo_images_api.api.requests.get = mockery.mockGet

    def tearDown(self):
        pass

    def test_search(self):
        results = search("fake search term")
        fullResults = list(results)

        self.assertEqual(len(fullResults), 193)

    def test_search_limit(self):
        with self.assertLogs(level="DEBUG") as cm:
            results = search("fake search term", query_limit=2)
            fullResults = list(results)

        self.assertEqual(len([d for d in cm.output if d.count("MockGet") > 0]), 2)

        self.assertEqual(len(fullResults), 97)

        self.setUpMockery()

        with self.assertLogs(level="DEBUG") as cm:
            results = search("fake search term", query_limit=1)
            fullResults = list(results)

        self.assertEqual(len([d for d in cm.output if d.count("MockGet") > 0]), 1)

        self.assertEqual(len(fullResults), 48)

        # I really just care that search can handle a zero limit
        self.setUpMockery()
        results = search("fake search term", query_limit=0)
        fullResults = list(results)
        
        self.assertEqual(len(fullResults), 193)

if __name__ == '__main__':
    unittest.main()