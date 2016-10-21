import csv
import sys
import requests
import json
import os, glob

path = 'data_input'

def sentiment_score(file_input):
    firstline = True
    try:
        f_in = open(file_input, 'rt')
        new_file = f_in.name.split('.')[0] + '_processed.csv'
        f_out = open(new_file, 'w')
        print "File being processed %s" % (new_file)
        reader = csv.reader(f_in)
        for row in reader:
            if firstline:    # skip first line
                firstline = False
                continue
            text = row[5]
            payload = {'txt': text}
            resp = requests.post(url='http://sentiment.vivekn.com/api/text/', data=payload)
            resp_json = json.loads(resp.text)
            result = 0.0
            sign = resp_json['result']['sentiment']
            score = resp_json['result']['confidence']
            row[6] = sign 
            row.insert(7, score)
            writer = csv.writer(f_out)
            writer.writerow((row))
    finally:
        f_in.close()

def main():
    try:
        for filename in glob.glob(os.path.join(path, '*.csv')):
            if not os.path.isdir(filename):
                sentiment_score(filename)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
