from base import Base
import base


# Parse the feed
class Tweet(object):
    def __init__(self, raw_tweet=None):
        self.tweet = raw_tweet
        self.tweet_as_row = []

    def parse_tweet(self):
        fields = []
        for f in fields:
            self.tweet_as_row.append(raw_tweet[f])
        return self.tweet_as_row

def main():
    client = Base()
    creds = client.load_config("Twitter")
    consumer = client.authenticate(creds)
    twitter_resp = base.fetch_twitter_feed(consumer)
    raw_tweets = twitter_resp["statuses"]
    for tweet in raw_tweets:

    # Example of reading twitter feed
    print(len(tweets))

if __name__ == '__main__':
    main()
