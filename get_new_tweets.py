#!/usr/bin/python

import twython
import pickle

api=twython.Twython()

#r=api.search(q="hbotakemymoney", rpp=100, p=5)
#pickle.dump(r, open('results','wb'))
#print '\n'.join(dir(api))

r=pickle.load(open('results'))
for key in r:
    print "%-20s %s" % (key, r[key])
    
for key in r['results']:
    print key