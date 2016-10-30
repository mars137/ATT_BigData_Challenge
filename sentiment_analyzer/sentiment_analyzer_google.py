import csv
import sys
import requests
import json
from nltk.tokenize import word_tokenize
import os, glob, re, itertools, HTMLParser
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import progressbar
from datetime import datetime

folder_input = 'google_input'
folder_output = 'google_output/'

def get_sentiment_textblob(text):
    """
    # @param text: blob of text
    # @return list of (sentiment, score) -> ('pos', '0.33')
    """
    blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    sentiment = blob.sentiment.classification
    score = '{0:.4f}'.format(blob.sentiment.p_pos - blob.sentiment.p_neg)
    return [sentiment, score]

def get_sentiment_vivekn(text):
    """
    # @param text: blob of text
    # @return list of (sentiment, score) -> ('pos', '0.33')
    """
    payload ={"txt":text}
    resp_json = requests.post("http://sentiment.vivekn.com/api/text/", data=payload)
    sentiment_dict = json.loads(resp_json.text)
    sentiment = sentiment_dict["result"]["sentiment"]
    score = sentiment_dict["result"]["confidence"].decode('utf8').encode('ascii','ignore')
    return [sentiment, score]

def get_storetype(store):
    store_num = int(re.findall("[0-9]+", store)[0])
    if store_num <= 11:
        return "Corporate"
    return "Authorized"

def preprocess_text(tweet):
    tweet = tweet.decode("utf8").encode('ascii', 'ignore')
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

def parse_date(date_str):
    d_str, t_str = date_str.split(" ")
    yyyy,mon,dd = [int(d) for d in d_str.split("/")]
    time_temp = [int(t) for t in t_str.split(':')]
    if yyyy < 2000:
        yyyy += 2000

    if len(time_temp) > 2:
        hh,mm,ss = time_temp
    elif len(time_temp) == 2:
        time_temp.insert(0,0)
        hh,mm,ss = time_temp

    date_parsed = datetime(yyyy,mon,dd,hh,mm,ss)
    format = "%a %b %d %H:%M:%S %Y"
    date_formatted = datetime.strftime(date_parsed, format)
    date_list = date_formatted.split(" ")
    date_list.insert(-1, "+0000")
    date_processed = ' '.join(s for s in date_list)
    return date_processed

def process_file(file_input): # pragma: no cover
    firstline = True
    try:
        with open(file_input, 'rU') as f_in:

            filepath = f_in.name.split('.')[0]
            file_out = filepath.split("/")[1]
            new_file = folder_output + file_out + '_processed.csv'
            f_out = open(new_file, 'w')
            # print "File being processed %s" % (new_file)
            reader = csv.reader(f_in)
            # Reads file line-by-line
            for row in csv.reader(f_in.read().splitlines()):

                # skip first line
                if firstline:
                    firstline = False
                    continue
                text = row[6]

                # Format store name
                store = row[0].split(" ")
                store_name  = ''.join(str(s) for s in store)
                row[0] = store_name

                # Add type of store
                store_type = get_storetype(row[0])
                row.insert(1, store_type)

                # Parse datetime to standard format
                row[6] = parse_date(row[6])

                # Get sentiment for text blob
                sentiment, score = get_sentiment_vivekn(text)
                row.insert(8, sentiment)
                row.insert(9, score)

                # Find product from text
                product = find_product(text)
                row[10] = product

                # Find service from text
                service = find_service(text)
                row.insert(11, service)

                row[13] = 'Google'


                writer = csv.writer(f_out)
                writer.writerow((row))

    except UnicodeDecodeError as e:
        pass
    except IndexError as e:
        pass

    finally:
        f_in.close()

def main(): # pragma: no cover
    # try:
    bar = progressbar.ProgressBar()
    for filename in bar(glob.glob(os.path.join(folder_input, '*.csv'))):
        if not os.path.isdir(filename):
            process_file(filename)
    # except Exception as e:
    #     print(e)

if __name__ == '__main__': # pragma: no cover
    main()
