import unittest
import json

import logging

logger = logging.getLogger(__name__)

class MockResponse:
    def __init__(self, value):
        self.value = value

    @property
    def text(self):
        logger.debug("Returning Mock Value")
        return self.value

class Mockery:
    def __init__(self, fixturePath):
        with open(fixturePath, 'r') as handle:
            self.FIXTURES = json.load(handle)

    def mockPost(self, *args, **kwargs):
        logger.debug("MockPost")
        return MockResponse("other things andvqd=7&more stuff")

    def mockGet(self, *args, **kwargs):
        logger.debug("MockGet")

        return MockResponse(self._getFixture())

    def _getFixture(self):
        return self.FIXTURES.pop()