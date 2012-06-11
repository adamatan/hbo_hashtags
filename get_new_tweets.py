#!/usr/bin/python

import twython
import pickle

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
            
    def update_recent_tweets(self):
        for page in range(1,16):
            new_tweets=self.api.search(q="#hbotakemymoney", rpp=50, p=1)['results']
            self._dprint("%d tweets returned from API call." % len(new_tweets))
            for tweet in new_tweets:
                if tweet['id'] not in self.tweets:
                    self._tweets[tweet['id']]=tweet
        
    def save_tweets(self):
        pickle.dump(self.tweets, open('tweets', 'wb'))
        
data_getter=DataGetter(debug=True)
data_getter.update_recent_tweets()
data_getter.save_tweets()
print data_getter.tweets
