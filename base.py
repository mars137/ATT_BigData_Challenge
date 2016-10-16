from __future__ import print_function
import oauth2
import ConfigParser


class Base(object):

    def __init__(self):
        self.twitter_base_url = "https://api.twitter.com/1.1/search/tweets.json"
        self.yelp_base_url = ""

    # Load the configuration
    def load_config(self, service=None):
        Config = ConfigParser.ConfigParser()
        Config.read("config.ini")
        creds = {}

        if service == "Twitter":
            creds["key"] = Config.get("TwitterAuth", "key")
            creds["secret"] = Config.get("TwitterAuth", "secret")
            creds["token"] = Config.get("TwitterAuth", "token")
            creds["token_secret"] = Config.get("TwitterAuth", "token_secret")
        elif service == "Yelp":
            creds["key"] = Config.get("YelpAuth", "key")
            creds["secret"] = Config.get("YelpAuth", "secret")
            creds["token"] = Config.get("YelpAuth", "token")
            creds["token_secret"] = Config.get("YelpAuth", "token_secret")

        return creds if creds != {} else None

    # Authenticate the client
    def authenticate(self, creds=None):
        """
        @params: dict of api credentials
        @return: authencated client for fetching requests
        """
        consumer = oauth2.Consumer(key=creds["key"], secret=creds["secret"])
        token = oauth2.Token(key=creds["token"], secret=creds["token_secret"])
        return oauth2.Client(consumer, token)

    # Fetch the feed
    def fetch_twitter_feed(self, params=None):
        """
        @params: dict of parameters
        @return: list of tweets
        """
        creds = self.load_config("Twitter")
        consumer = self.authenticate(creds)
        request_url = self.twitter_base_url + "?q=" + params["q"]
        resp, content = consumer.request(request_url,"GET")
        return content["statuses"]

    def fetch_yelp_feed(self, params=None):
        creds = self.load_config("Yelp")
        consumer = self.authenticate(creds)
        
