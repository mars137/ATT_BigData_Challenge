from __future__ import print_function
from base import Base
import base
from Queue import Queue
import csv
import time
import json


class Tweet(object):
    def __init__(self, raw_tweet=None):
        self.tweet = raw_tweet
        self.tweet_as_row = []

    def parse_tweet(self):
        """
        @return: [id_str, text, created_at, source, latitude, longitude, user_id]
        """

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

    def get_location(self):
        if self.tweet_as_row is None:
            return None
        return self.tweet_as_row[4]

def get_last_marker():
    with open('tweet_marker.json', 'r') as f:
        data = json.load(f)
    return data["max_id"], data["page"]

def save_last_marker(max_id="", page=1):
    marker_data = {"max_id":max_id, "page":page}
    with open('tweet_marker.json', 'w') as f:
        json.dump(marker_data, f)

def main():
    try:
        client = Base()
        creds = client.load_config("Twitter")
        consumer = client.authenticate(creds)

        geocodes = ["32.776664,-96.796988",

                ]
        tweet_queue = Queue()
        max_id = ""
        filename_series = 'A'

        for loc in geocodes:
            # Loop through feed
            page = 1
            while page <= 30:
                twitter_resp = None
                if max_id == "":
                    twitter_resp = base.fetch_twitter_feed(consumer, loc)
                else:
                    twitter_resp = base.fetch_twitter_feed(consumer, loc, max_id)
                raw_tweets = twitter_resp["statuses"]

                if raw_tweets == 'statuses':
                    break

                for tweet in raw_tweets:
                    T = Tweet(tweet)
                    processed_tweet = T.parse_tweet()

                    # Skip the last processed tweet
                    if max_id == T.get_tweet_id():
                        continue

                    tweet_queue.put(processed_tweet)
                    max_id = T.get_tweet_id()

                filename ='tweet'+filename_series+str(page)+'.csv'
                f = open(filename, 'w')
                writer = csv.writer(f)

                # Set headers of the file (columns)
                writer.writerow(('TweetId', 'Text', 'CreatedAt', 'Source',
                                'Latitude', 'Longitude', 'UserId', 'StoreLocation'))

                # Open file and write line by line
                while not tweet_queue.empty():
                    current_tweet = tweet_queue.get()
                    writer.writerow((current_tweet[0], current_tweet[1],
                                    current_tweet[2], current_tweet[3],
                                    current_tweet[4], current_tweet[5],
                                    current_tweet[6], filename_series))

                f.close()

                # Save marker to file
                save_last_marker(max_id, page)

                print("Page %s processed for store %s" % (page, filename_series) )

                # Rate limit the calls to Twitter
                page += 1
                time.sleep(1)
            filename_series = chr(ord(filename_series)+1)


    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
