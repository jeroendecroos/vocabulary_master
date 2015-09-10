import sys
import codecs

known = sys.argv[1]
wordlist = sys.argv[2]
output = sys.argv[3]


known_words = []
with codecs.open(known, 'rb' ,'utf8') as instream:
    known_words = [x.strip() for x in instream]

with codecs.open(wordlist, 'rb', 'utf8') as instream,\
    codecs.open(output, 'wb', 'utf8') as outstream:
    total = 0
    len_total = 0
    len_known_words = 0
    known_total = 0
    for inline in instream:
        infos  = inline.split()
        w = infos[0].strip()
        n = int(infos[1].strip())
        total += n
        len_total += 1
        if w in known_words:
            known_total += n
            len_known_words +=1
            continue
        else:
            outstream.write(inline)
    print 'Fraction of words known:'
    print 1.0*known_total/total
    print known_total, total
    print "nu,ber of words"
    print 1.0* len_known_words/len_total
    print len_known_words, len_total
    
