import unittest
from base import Base

class TestBase(unittest.TestCase):

    def setUp(self):
        self.client = Base()

    def test_load_twitter_config(self):
        credentials = self.client.load_config("Twitter")
        self.assertIsNotNone(credentials["key"])
        self.assertIsNotNone(credentials["secret"])
        self.assertIsNotNone(credentials["token"])
        self.assertIsNotNone(credentials["token_secret"])

    def test_load_yelp_config(self):
        credentials = self.client.load_config("Yelp")
        self.assertIsNotNone(credentials["key"])
        self.assertIsNotNone(credentials["secret"])
        self.assertIsNotNone(credentials["token"])
        self.assertIsNotNone(credentials["token_secret"])

    def test_load_no_config(self):
        empty_credentials = self.client.load_config()
        self.assertIsNone(empty_credentials)

    def test_authenticate(self):
        self.client.load_config("Twitter")
        self.assertIsNotNone(self.client.authenticate())
