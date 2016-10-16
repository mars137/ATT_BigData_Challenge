from base import Base


# Parse the feed

def main():
    client = Base()

    # Example of reading twitter feed
    # client.load_config("Twitter")
    # query = {"q":"att"}
    # tweets = client.fetch_twitter_feed(params=query)
    # print(tweets)

    # Example of reading yelp reviews
    # client.load_config("Yelp")
    # print(client.fetch_yelp_feed(business_id="north-india-restaurant-san-francisco"))

if __name__ == '__main__':
    main()
