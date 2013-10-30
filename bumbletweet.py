from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import threading
import collections
import time
import json
import subprocess

from local_settings import consumer_key, consumer_secret, \
                            access_token, access_token_secret 

festival_cmd = 'echo "(SayText \\"%s\\")" | nc %s %s -q0'
tweet_deque = collections.deque()

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self):
        self.stack = []
        super(StdOutListener,self).__init__(self)
       
    def on_data(self, data):
        jd = json.loads(data)
        tweet_text = jd.get('text',None)
        if tweet_text:
            tweet_deque.append(tweet_text)
        return True

    def on_error(self, status):
        print status

class Bumble():
    def __init__(self):
        self.festival_host = "127.0.0.1" 
        self.festival_port = "1314"
        self.downtime = 0
        self.tweet = None
        self.reminder = "Make me speak. Tweet using hashtag bumble tweet"
    def say_tweet(self):
        while True:
            time.sleep(5)
            self.get_tweet()
            if self.tweet:
                self.downtime = 0
                self.clean_tweet()
                if "#roar" in self.tweet.lower():
                    self.roar()
                    s = subprocess.Popen(festival_cmd%(self.tweet,self.festival_host,self.festival_port),                                       shell=True)
                    s.wait()
                    self.tweet = None
                else:
                    s = subprocess.Popen(festival_cmd%(self.tweet,self.festival_host,self.festival_port),                                       shell=True)
                    s.wait()
                    self.tweet = None
            else:
                print "no tweets"
                if self.downtime >= 300:
                    print "time to roar"
                    self.roar()
                    s = subprocess.Popen(festival_cmd%(self.reminder,self.festival_host,self.festival_port),                                       shell=True)
                    s.wait()
                    self.downtime = 0
                else:
                    self.downtime += 5
    def get_tweet(self):
        print "getting tweet"
        try:
            self.tweet = tweet_deque.popleft()
        except IndexError:
            pass
    def clean_tweet(self):
        self.tweet =  ' '.join([w for w in self.tweet.split() 
                            if not w.startswith('http')])
        self.tweet = self.tweet.replace('"','')
        self.tweet = self.tweet.replace('\\','')
        self.tweet = self.tweet.replace('(','').replace(')','')
        self.tweet = self.tweet.replace('#bumbletweet','')
    def roar(self):
        print "roaring"
        s = subprocess.Popen('play roar.wav',shell=True)
        s.wait()

if __name__ == '__main__':
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    bumble = Bumble()

    stream = Stream(auth, l)    
    #stream.filter(track=['#bumbletweet'])

    get_tweets = threading.Thread( 
                                    target=stream.filter,
                                    kwargs={'track':['#bumbletweet']})
    say_tweets = threading.Thread(target=bumble.say_tweet)
    get_tweets.start()
    say_tweets.start()
