import unittest
from sentiment_analyzer import base


class TestBase(unittest.TestCase):

    def setUp(self):
        self.client = base.Base()
        self.twitter_creds = self.client.load_config("Twitter")
        self.twitter_auth = self.client.authenticate(self.twitter_creds)

    def test_load_twitter_config(self):
        credentials = self.twitter_creds
        self.assertIsNotNone(credentials["key"])
        self.assertIsNotNone(credentials["secret"])
        self.assertIsNotNone(credentials["token"])
        self.assertIsNotNone(credentials["token_secret"])

    def test_load_yelp_config(self):
        credentials = self.client.load_config("Yelp")
        self.assertIsNotNone(credentials["access_token"])

    def test_load_no_config(self):
        empty_credentials = self.client.load_config()
        self.assertIsNone(empty_credentials)

    def test_authenticate(self):
        creds = self.twitter_creds
        self.assertIsNotNone(self.client.authenticate(creds))

    def test_fetch_twitter_feed_no_max_id(self):
        consumer = self.twitter_auth
        geocode = "32.776664,-96.796988"
        tweets = base.fetch_twitter_feed(consumer, geocode)
        self.assertIsNotNone(tweets)
        self.assertEquals(len(tweets), 100)

    def test_fetch_twitter_feed_with_max_id(self):
        consumer = self.twitter_auth
        geocode = "32.776664,-96.796988"
        tweets = base.fetch_twitter_feed(consumer=consumer, geocode=geocode, max_id="791286833623601152")
        self.assertIsNotNone(tweets)
        self.assertEquals(len(tweets), 100)

    def test_fetch_twitter_feed_empty(self):
        consumer = self.twitter_auth
        geocode = "32.776664,-96.796988"
        gibberish = "aosuhdosuahsaogiru13hbo1"
        tweets = base.fetch_twitter_feed(consumer, geocode, query=gibberish)
        self.assertIsNone(tweets)


    def test_fetch_yelp_feed(self):
        yelp_resp = base.fetch_yelp_feed(business_id="at-and-t-dallas-13")
        self.assertIsNotNone(yelp_resp)
        reviews = yelp_resp["reviews"]
        self.assertEquals(len(reviews), 3)
