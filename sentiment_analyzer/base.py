from __future__ import print_function
import oauth2
import ConfigParser
import requests, json



class Base(object):

    def load_config(self, service=None):
        """
        Reads the configuration from ini file
        @param service: service to which the API keys are required
        @return: dict of credentials for auth
        """
        Config = ConfigParser.ConfigParser()
        Config.read("config.ini")
        creds = {}

        if service == "Twitter":
            creds["key"] = Config.get("TwitterAuth", "key")
            creds["secret"] = Config.get("TwitterAuth", "secret")
            creds["token"] = Config.get("TwitterAuth", "token")
            creds["token_secret"] = Config.get("TwitterAuth", "token_secret")
        elif service == "Yelp":
            creds["access_token"] = Config.get("YelpAuth_v3", "access_token")
            # creds["key"] = Config.get("YelpAuth_v2", "key")
            # creds["secret"] = Config.get("YelpAuth_v2", "secret")
            # creds["token"] = Config.get("YelpAuth_v2", "token")
            # creds["token_secret"] = Config.get("YelpAuth_v2", "token_secret")

        return creds if creds != {} else None

    def authenticate(self, creds=None):
        """
        Authenticates the program using OAuth2
        @param creds: dict of api credentials
        @return: authencated client for fetching requests
        """
        consumer = oauth2.Consumer(key=creds["key"], secret=creds["secret"])
        token = oauth2.Token(key=creds["token"], secret=creds["token_secret"])
        return oauth2.Client(consumer, token)

def fetch_twitter_feed(consumer, geocode, max_id="", query=""):
    """
    Fetches dict of tweets based on keyword
    @param params: dict of parameters
    @return: list of tweets
    """
    twitter_base_url = "https://api.twitter.com/1.1/search/tweets.json"
    # query_url = 'att%20OR%20attcares%20OR%20uverse%20OR%20at%26t%20OR%20digital%20OR%20life%20OR%20attfiber%20OR%20directv%20OR%20directvservice%20%23att%20OR%20%23attcares%20OR%20%23uverse%20OR%20%23directv%20OR%20%23attfiber%20lang%3Aen%20%40att%20OR%20%40attcares%20OR%20%40uverse%20OR%20%40directv%20OR%20%40directvservice&geocode='+ geocode +',10mi&count=100'
    query_url ='att%20OR%20attcares%20OR%20uverse%20OR%20attfiber%20OR%20directv%20OR%20directvservice%20OR%40att%20OR%20%40attcares%20OR%20%40uverse%20OR%20%40directv%20OR%20%40directvservice&geocode='+geocode+',10mi&count=100'

    if query != "":
        query_url = query

    request_url = twitter_base_url + "?q=" + query_url

    if max_id != "":
        request_url += "&max_id=" + max_id

    resp, content = consumer.request(request_url,"GET")
    tweet_feed = json.loads(content)

    if 'statuses' not in tweet_feed.keys():
        return None

    return tweet_feed["statuses"] or None

def fetch_yelp_feed(business_id=None):
    client = Base()
    yelp_base_url = "https://api.yelp.com/v3/businesses/"
    creds = client.load_config("Yelp")
    access_token = 'Bearer '+creds["access_token"]
    headers = {'Authorization': access_token}
    request_url = yelp_base_url + business_id + '/reviews'
    resp = requests.get(url=request_url, headers=headers)
    return json.loads(resp.text)
