import sys
import codecs


infile = sys.argv[1]
outfile = sys.argv[2]

words = []
with codecs.open(infile, 'rb', 'utf8') as instream:
    words = [l.strip().split() for l in instream]


def get_answer():
    ans = None
    while not ans:
        inp = str(raw_input())
        if inp == 'y':
            ans = inp
        elif inp == 'n':
            ans = inp
        elif inp == 'r':
            ans = inp
    return ans

max_dist = 10
dist = 0
to_save = []
print 'y means unknown word; n known'
with codecs.open(outfile, 'wb', 'utf8') as outstream:
    w_n = 0
    while w_n < len(words):
        w = words[w_n]
        word = w[0]
        print (word + '\t'),
        ans = get_answer()
        if ans == 'y':
            to_save.append(w)
        if ans =='q':
            for x in to_save:
                outstream.write('\t'.join(x)+'\n')
            break
        w_n += 1
        dist  += 1
        if dist == max_dist:
            dist -= 1
            if to_save:
                save =to_save.pop(0)
                outstream.write('\t'.join(save)+'\n')
