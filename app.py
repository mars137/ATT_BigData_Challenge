from base import Base


# Parse the feed

def main():
    client = Base()

    # Example of reading twitter feed
    # client.load_config("Twitter")
    # query = {"q":"att"}
    # tweets = client.fetch_twitter_feed(params=query)
    # print(tweets)
    # att%20OR%20attcares%20OR%20uverse%20%40att%20OR%20%40attcares%20OR%20%40uverse%20near%3A"Dallas%2C%20TX"%20within%3A15mi%20since%3A2014-01-01%20until%3A2016-01-01&src=typd

    # Example of reading yelp reviews
    # client.load_config("Yelp")
    # print(client.fetch_yelp_feed(business_id="north-india-restaurant-san-francisco"))

if __name__ == '__main__':
    main()
