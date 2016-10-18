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

def fetch_twitter_feed(consumer, geocode, max_id=""):
    """
    Fetches dict of tweets based on keyword
    @param params: dict of parameters
    @return: list of tweets
    """
    twitter_base_url = "https://api.twitter.com/1.1/search/tweets.json"
    query_url = ' att%20OR%20attcares%20OR%20uverse%20lang%3Aen%20%40att%20OR%20%40attcares%20OR%20%40uverse&geocode='+ geocode +',3mi&result_type=recent&count=100'
    request_url = twitter_base_url + "?q=" + query_url
    if max_id != "":
        request_url = twitter_base_url + "?q=" + query_url + "&max_id=" + max_id
    resp, content = consumer.request(request_url,"GET")
    return json.loads(content)

def fetch_yelp_feed(self, business_id=None):
    yelp_base_url = "https://api.yelp.com/v3/businesses/"
    creds = self.load_config("Yelp")
    access_token = 'Bearer '+creds["access_token"]
    headers = {'Authorization': access_token}
    request_url = self.yelp_base_url + business_id + '/reviews'
    resp = requests.get(url=request_url, headers=headers)
    return json.loads(resp.text)
