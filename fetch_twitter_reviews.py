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
        @return: [created_at, text,
                  sentiment, rating, source]
        """

        try:

            fields = ["created_at", "text"]
            for f in fields:
                self.tweet_as_row.append(str(self.tweet[f].encode('utf-8')))

            self.tweet_as_row.append("") # Sentiment
            self.tweet_as_row.append("") # Rating
            self.tweet_as_row.append("Twitter") # Source

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
    return data

def save_last_marker(max_id="", page=1, store_key=None):
    marker_data = {"max_id":max_id, "page":page, "store_key":store_key}
    with open('tweet_marker.json', 'w') as f:
        json.dump(marker_data, f)

def main():
    # try:
    client = Base()
    creds = client.load_config("Twitter")
    consumer = client.authenticate(creds)

    stores = {
    "Dallas1":["32.776664","-96.796988", "208 S Akard Street, Ste 110, Dallas, TX 75202"],
    "Dallas2":["32.8111091","-96.8092962","3329 Oak Lawn Avenue Dallas TX 75219"],
    "Dallas3":["32.8293128","-96.8272358","5616 Lemmon Ave Dallas TX 75209"],
    "Dallas4":["32.8685017","-96.7757012","8687 N Central Expressway Suite 2340"],
    "Dallas5":["32.8342578","-96.7045404","1152 North Buckner Blvd"],
    "Dallas6":["32.8740567","-96.771404","9100 N Central Expressway Suite 105"],
    "Dallas7":["32.8957338","-96.8079243","5959 Royal Lane Dallas TX 7523"],
    "Dallas8":["32.913273","-96.958064","7800 N. Macarthur Boulevard Suite 150"],
    "Dallas9":["33.009892","-96.709061","701 N Central Expy Plano, TX 75075"],
    "Dallas10":["32.953929","-96.821254","5100 Beltline Road Ste. 1032"],
    "Dallas11":["32.934372","-96.820672","13710 Dallas Parkway Suite I"]
    }
    store_processed = []
    store_record = set()
    page = 1
    tweet_queue = Queue()
    last_result = get_last_marker()

    max_id, page = last_result["max_id"], last_result["page"]
    store_processed = last_result["store_key"]

    for store_key, store_value in stores.items():

        if store_key in store_processed[:-1]:
            continue

        # Loop through feed

        while page <= 116:
            twitter_resp = None
            loc = store_value[0] + ',' + store_value[1]
            if max_id == "":
                twitter_resp = base.fetch_twitter_feed(consumer, loc)
            else:
                twitter_resp = base.fetch_twitter_feed(consumer, loc, max_id)

            if "statuses" in twitter_resp.keys():
                raw_tweets = twitter_resp["statuses"]
            else:
                break

            for tweet in raw_tweets:
                T = Tweet(tweet)
                processed_tweet = T.parse_tweet()

                # Skip the last processed tweet
                if max_id == T.get_tweet_id():
                    continue

                tweet_queue.put(processed_tweet)
                max_id = T.get_tweet_id()

            filename = store_key+'_twitter_'+str(page)+'.csv'
            f = open(filename, 'w')
            writer = csv.writer(f)

            # Set headers of the file (columns)
            writer.writerow(('Store', 'Latitude', 'Longitude',
                             'Address', 'CreatedAt', 'Text',
                             'Senti', 'Rating', 'Source'))

            # Open file and write line by line
            while not tweet_queue.empty():
                current_tweet = tweet_queue.get()
                writer.writerow((store_key, store_value[0],
                                store_value[1], store_value[2],
                                current_tweet[0], current_tweet[1],
                                current_tweet[2], current_tweet[3],
                                current_tweet[4]))

            f.close()
            store_record.add(store_key)
            store_processed = list(store_record)

            # Save marker to file
            save_last_marker(max_id, page, store_processed)

            print("Page %s processed for store %s" % (page, store_key) )

            # Rate limit the calls to Twitter
            page += 1
            time.sleep(2)

        page = 1

    # except Exception as e:
    #     print(e)


if __name__ == '__main__':
    main()
