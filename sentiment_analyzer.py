import csv
import sys
import requests
import json
from nltk.tokenize import word_tokenize
import os, glob, re, itertools, HTMLParser
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

path = 'dataset_part2'

def get_sentiment(text):
    """
    # @param text: blob of text
    # @return list of (sentiment, score) -> ('pos', '0.33')
    """
    blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    sentiment = blob.sentiment.classification
    score = blob.sentiment.p_pos - blob.sentiment.p_neg
    return [sentiment, score]

def preprocess_text(tweet):
    text = tweet.lower()
    html_parser = HTMLParser.HTMLParser()
    html_parsed_text = html_parser.unescape(text)
    standardized_text = ''.join(''.join(s)[:2] for _,s in itertools.groupby(html_parsed_text))
    cleaned_text = ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",standardized_text).split())
    return word_tokenize(cleaned_text)

def find_product(tweet):
    tweet_text = set(preprocess_text(tweet))
    product_dict = {"uverse":"uverse","attfiber":"fiber",
                "fiber":"fiber","directv":"directv",
                "directvservice":"directv"}
    product_set = set(product_dict.keys())

    for word in tweet_text:
        if word in product_set:
            return product_dict[word]
    return "general"

def find_service(tweet):
    tweet_text = set(preprocess_text(tweet))
    service_dict = {"technician":"technician dispatch",
                "installer":"technician dispatch",
                "installation":"product installation",
                "install":"product installation",
                "installed":"product installation",
                "store":"store experience",
                "experience":"store experience",
                "satisfaction":"satisfaction",
                "satisfied":"satisfaction",
                "unsatisfied":"satisfaction",
                }
    service_set = set(service_dict.keys())

    for word in tweet_text:
        if word in service_set:
            return service_dict[word]
    return "general"



def process_file(file_input): # pragma: no cover
    firstline = True
    try:
        f_in = open(file_input, 'rt')
        new_file = f_in.name.split('.')[0] + '_processed.csv'
        f_out = open(new_file, 'w')
        print "File being processed %s" % (new_file)
        reader = csv.reader(f_in)
        # Reads file line-by-line
        for row in reader:
            # skip first line
            if firstline:
                firstline = False
                continue
            text = row[6]

            # Get sentiment for text blob
            sentiment, score = get_sentiment(text)
            row[7] = sentiment
            row.insert(8, score)

            # Find product from text
            product = find_product(text)
            row.append(product)

            # Find service from text
            service = find_service(text)

            writer = csv.writer(f_out)
            writer.writerow((row))

    finally:
        f_in.close()
        f_out.close()

def main(): # pragma: no cover
    try:
        for filename in glob.glob(os.path.join(path, '*.csv')):
            if not os.path.isdir(filename):
                process_file(filename)
    except Exception as e:
        print(e)

if __name__ == '__main__': # pragma: no cover
    main()
