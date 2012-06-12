#!/usr/bin/python

import twython
import pickle
import re

class DataGetter(object):
    """Retrieves data from twitter search API and updates local files."""
    def __init__(self, debug=False):
        self._debug = debug
        self.api    = twython.Twython()
        self._load_tweets()
        self._dprint("%d tweets loaded from file." % len(self.tweets))
    
    def _load_tweets(self):
        """Returns a pickled file of {tweet_id:tweet}.
        Falls back to empty dictionary"""
        try:
            self._tweets=pickle.load(open('tweets'))
        except IOError:
            self._tweets=dict()
            
    @property
    def tweets(self):
        return self._tweets
   
    def _dprint(self, msg):
        if self._debug:
            print msg
 
    @property
    def amounts_filtered(self):
        return [a for a in self.amounts if 0.5 <= a <= 50]
 
    @property
    def amounts(self):
        texts=self.texts
        return sorted([texts[key][1] for key in texts])
    
    @property
    def geo(self):
        for key in self.tweets:
            if self.tweets[key]['geo']:
                print self.tweets[key]['geo']
    
    @property
    def texts(self):
        tweet_re=re.compile('^I would pay\s\$(.*)\sa month for a standalone @HBOGO subscription')
        result=dict()
        for key in self.tweets:
            text=self.tweets[key]['text']
            #print key, text, tweet_re.search(text)
            if tweet_re.search(text):
                try:
                    amount=float(tweet_re.findall(text)[0])
                    result[key]=tuple([text, amount])
                except ValueError:
                    self._dprint("FAIL(FLOAT): %s" % text)
                    pass
            else:
                self._dprint("FAIL(REGEX): %s" % text)
        return result
    
    def update_recent_tweets(self):
        page=1
        while True:
            num_existing_tweets=len(self.tweets)
            new_tweets=self.api.search(q="#takemymoneyHBO", rpp=100, page=page, result_type="recent")['results']
            self._dprint("%d tweets returned from API call." % len(new_tweets)), 
            for tweet in new_tweets:
                if tweet['id'] not in self.tweets:
                    self._tweets[tweet['id']]=tweet
            num_new_tweets=len(self.tweets)-num_existing_tweets
            if num_new_tweets==0:
                print "No new tweets."
                break
            else:
                print "%d new tweets." % num_new_tweets
                self.save_tweets()
                page+=1
        
    def save_tweets(self):
        pickle.dump(self.tweets, open('tweets', 'wb'))
        
data_getter=DataGetter(debug=False)
data_getter.update_recent_tweets()
#data_getter.save_tweets()
#print len(data_getter.tweets)
#print data_getter.texts
amounts=data_getter.amounts_filtered
amounts_size=len(amounts)
print amounts
print sum(amounts)/amounts_size
percentile=20
for i in range(1,percentile):
    loc=i*amounts_size/percentile
    print loc, amounts[loc]
    
print data_getter.geo