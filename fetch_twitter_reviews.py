from __future__ import print_function
from base import Base
import base
from Queue import Queue
import csv
import time


class Tweet(object):
    def __init__(self, raw_tweet=None):
        self.tweet = raw_tweet
        self.tweet_as_row = []

    def parse_tweet(self):
        try:
            fields = ["id_str", "text", "created_at",
                        "source"]
            for f in fields:
                self.tweet_as_row.append(str(self.tweet[f].encode('utf-8')))

            latitude = None
            longitude = None
            if self.tweet["place"] is not None:
                elements = self.tweet["place"]["bounding_box"]["coordinates"][0][0]
                latitude = elements[0]
                longitude = elements[1]

            self.tweet_as_row.append(latitude)
            self.tweet_as_row.append(longitude)

            self.tweet_as_row.append(str(self.tweet["user"]["id_str"]))
            return self.tweet_as_row

        except UnicodeEncodeError as e:
            print(e, self.tweet[f])
    def get_tweet_id(self):
        if self.tweet_as_row is None:
            return None
        return self.tweet_as_row[0]

# class TweetList(object):
#     def __init__(self, raw_tweets=None):
#         self.tweets = raw_tweets
#         self.tweetlist = []
#
#         for raw_tweet in raw_tweets:
#             T = Tweet(raw_tweet)
#             self.tweetlist.append(T.parse_tweet())

def main():
    # try:
    client = Base()
    creds = client.load_config("Twitter")
    consumer = client.authenticate(creds)
    max_id = ""
    page = 1
    # Loop through feed
    while page <= 3:
        twitter_resp = None
        if max_id == "":
            twitter_resp = base.fetch_twitter_feed(consumer)
        else:
            twitter_resp = base.fetch_twitter_feed(consumer, max_id)
        raw_tweets = twitter_resp["statuses"]
        tweet_queue = Queue()

        for tweet in raw_tweets:
            T = Tweet(tweet)
            processed_tweet = T.parse_tweet()
            if max_id == T.get_tweet_id():
                continue
            tweet_queue.put(processed_tweet)
            max_id = T.get_tweet_id()

        filename ='tweet'+str(page)+'.csv'
        f = open(filename, 'w')
        writer = csv.writer(f)
        # Set headers of the file (columns)
        writer.writerow(('TweetId', 'Text', 'CreatedAt', 'Source', 'Coordinates', 'UserId'))

        # Open file and write line by line
        while not tweet_queue.empty():
            current_tweet = tweet_queue.get()
            writer.writerow((current_tweet[0], current_tweet[1],
                            current_tweet[2], current_tweet[3],
                            current_tweet[4], current_tweet[5]))

        f.close()

        # Save marker


        page += 1
        # time.sleep(1)

    # except Exception as e:
    #     print(e)



if __name__ == '__main__':
    main()
