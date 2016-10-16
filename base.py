from __future__ import print_function
import oauth2
import ConfigParser

class Base(object):

    def __init__(self):
        self.creds = {}
        self.key = None
        self.secret = None
        self.token = None
        self.token_secret = None

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

        self.creds = creds
        return creds if creds != {} else None

    # Authenticate the client
    def authenticate(self):
        consumer = oauth2.Consumer(key=self.creds["key"], secret=self.creds["secret"])
        token = oauth2.Token(key=self.creds["token"], secret=self.creds["token_secret"])
        return oauth2.Client(consumer, token)

    # Fetch the feed
    def fetch_feed():
        pass

# Parse the feed

# Save to CSV
def save_to_csv():
    pass
