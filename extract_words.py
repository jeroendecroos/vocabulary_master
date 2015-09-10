import codecs
import argparse
import operator
import re

import pysrt


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('inputfiles',  nargs='+',
                   help='inputfiles = subtitles')
    parser.add_argument('outputfile',  nargs=1,
                   help='outputfile = frequency list')
    parser.add_argument('--verificationfile', 
                        default=None,
                    help='words has to be in this file')


    args = parser.parse_args()
    return args

def insert_word(freq_dict,w , verification_list=[]):
    w = re.sub('[?.;,:+=*$-_!]', '', w)
    w = w.lower()
    if not w: 
        return 0
    if w not in verification_list:
        return 0
    if w not in freq_dict:
        freq_dict[w] = 0
    freq_dict[w] += 1

def get_word_freq_dict(inputfiles, verification_list):
    freq_dict = {}
    for inputfile in inputfiles:
        print 'processing', inputfile
        subs = []
        try:
            subs = pysrt.open(inputfile)
        except UnicodeDecodeError as e:
            subs = []
        if not subs:
            for enc in ['utf8',"iso-8859-1"]:
                try:
                    print 'trying with' , enc
                    subs =  pysrt.open(inputfile, encoding=enc)
                except UnicodeDecodeError as e:
                    subs =[]
                if subs:
                    break
        if not subs:
            print 'couldnt open ', inputfile
            continue
        for sub in subs:
            words = sub.text.split()        
            for w in words:
                insert_word(freq_dict, w, verification_list)
        print len(freq_dict), sum(freq_dict.values())
    return freq_dict

def write_freq_dict(freq_dict, outputfile):
    total = 1.0 * sum(freq_dict.values())
    sorted_freq_keys = sorted(freq_dict, key=lambda x: -freq_dict[x])
    with codecs.open(outputfile, 'wb', 'utf8') as outstream:
        running_sum = 0
        for key in sorted_freq_keys:
            f = freq_dict[key]
            running_sum += f
            info_to_write = (key, f , f/total, running_sum/total)
            outstream.write('%s\t%d\t%.2f\t%.2f\n' % info_to_write)

def get_verification_list(infile):
    if infile:
        with codecs.open(infile, 'rb' ,'utf8') as instream:
            verificationlist = [l.strip() for l in instream]
        return verificationlist
    else:
        return []

if __name__ == '__main__':
    args = parse_arguments()
    verification_list = get_verification_list(args.verificationfile)
    freq_dict = get_word_freq_dict(args.inputfiles, verification_list)
    write_freq_dict(freq_dict, args.outputfile[0])


