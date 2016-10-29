import csv
import sys
import requests
import json
import os, glob
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

def find_product(text):
    pass

def find_service(text):
    pass

def process_file(file_input):
    firstline = True
    try:
        f_in = open(file_input, 'rt')
        new_file = f_in.name.split('.')[0] + '_processed.csv'
        f_out = open(new_file, 'w')
        print "File being processed %s" % (new_file)
        reader = csv.reader(f_in)
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

def main():
    try:
        for filename in glob.glob(os.path.join(path, '*.csv')):
            if not os.path.isdir(filename):
                process_file(filename)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
