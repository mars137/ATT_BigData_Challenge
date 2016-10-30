import csv
import os, glob
import progressbar


path = 'combiner_input'

def csv_combiner():
    try:
        bar = progressbar.ProgressBar()

        new_file = 'combined_dataset.csv'
        f_out = open(new_file, 'w')
        writer = csv.writer(f_out)
        for filename in bar(glob.glob(os.path.join(path, '*.csv'))):
            if not os.path.isdir(filename):
                f_in = open(filename, 'rt')
                # print "File being combined %s" % (filename)
                reader = csv.reader(f_in)
                for row in reader:
                    writer.writerow((row))
                f_in.close()
    finally:
        f_out.close()

def main():
    # try:
    csv_combiner()
    # except Exception as e:
    #    print(e)

if __name__ == '__main__':
    main()
