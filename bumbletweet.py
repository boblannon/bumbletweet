from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import threading
import collections
import time
import json
import subprocess
import unicodedata
import sys

from local_settings import consumer_key, consumer_secret, \
                            access_token, access_token_secret \
                            server_port, server_listen_addr \
                            hash_tag

festival_cmd = 'echo "" | nc %s %s -q0'
tweet_deque = collections.deque()

class StdOutListener(StreamListener):
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

class Bumble(object):
    def __init__(self):
        self.downtime = 0
        self.tweet = None
        self.reminder = "Make me speak. Tweet using hashtag "+hash_tag.replace('#','');

    def speak(self, remind=False):
        raise NotImplementedError

    def roar(self):
        raise NotImplementedError

    def say_tweet(self):
        if "#roar" in self.tweet.lower():
            self.tweet = self.tweet.lower().replace('#roar','')
            self.roar()
        self.speak()
        self.tweet = None

    def remind(self):
        self.roar()

    def watch_tweets(self):
        while True:
            time.sleep(5)
            self.get_tweet()
            if self.tweet:
                self.downtime = 0
                self.clean_tweet()
                self.say_tweet()
            else:
                #print "no tweets"
                if self.downtime >= 300:
                    #print "time to roar"
                    self.roar()
                    self.speak(remind=True)
                    self.downtime = 0
                else:
                    self.downtime += 5

    def get_tweet(self):
        #print "getting tweet"
        try:
            self.tweet = tweet_deque.popleft()
        except IndexError:
            pass

    def clean_tweet(self):
        self.tweet = unicodedata.normalize('NFKD', self.tweet).encode('ascii',
                'ignore')
        self.tweet =  ' '.join([w for w in self.tweet.split()
                            if not w.startswith('http')])
        self.tweet = self.tweet.replace('"','')
        self.tweet = self.tweet.replace('\\','')
        self.tweet = self.tweet.replace('(','').replace(')','')
        self.tweet = self.tweet.replace(hash_tag,'')


class FestivalBumble(Bumble):
    def __init__(self):
        super(FestivalBumble, self).__init__()
        self.festival_host = server_listen_addr
        self.festival_port = server_port
        self.say_cmd = 'echo "(SayText \\"{txt}\\")" | nc {host} {port} -q0'

    def speak(self, remind=False):
        if remind:
            speak_txt = self.reminder
        else:
            speak_txt = self.tweet

        #just in case, check for null tweet
        if speak_txt:
            proc_str = self.say_cmd.format(txt=speak_txt, host=self.festival_host,
                                      port=self.festival_port)
            s = subprocess.Popen(proc_str, shell=True)
            s.wait()

    def roar(self):
        #print "roaring"
        s = subprocess.Popen('play roar.wav',shell=True)
        s.wait()


class RemoteBumble(Bumble):
    def __init__(self, host=server_listen_addr, port=server_port):
        super(RemoteBumble, self).__init__()
        self.remote_host = host
        self.remote_say_port = port
        self.say_cmd = 'echo "{txt}" | nc {host} {port} -q0'
        self.remote_roar_port = str(int(port)+1)
        self.roar_cmd = 'echo "play that roar, dawg" | nc {host} {port} -q0'

    def speak(self, remind=False):
        if remind:
            speak_txt = self.reminder
        else:
            #sys.stderr.write(self.tweet+'\n')
            speak_txt = self.tweet

        #just in case, check for null tweet
        if speak_txt:
            proc_str = self.say_cmd.format(txt=speak_txt, host=self.remote_host,
                                      port=self.remote_say_port)
            s = subprocess.Popen(proc_str, shell=True)
            s.wait()

    def roar(self):
        #print "roaring"
        proc_str = self.roar_cmd.format(host=self.remote_host,
                                            port=self.remote_roar_port)
        s = subprocess.Popen(proc_str, shell=True)
        s.wait()

def main(bumble_object):
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    #stream.filter(track=['#bumbletweet'])

    get_tweets = threading.Thread(
                                    target=stream.filter,
                                    kwargs={'track':[hash_tag]})
    say_tweets = threading.Thread(target=bumble_object.watch_tweets)
    get_tweets.start()
    say_tweets.start()


if __name__ == '__main__':
    import platform
    if (platform.system() == "Linux") {
            main(FestivalBumble()) 
    } elif (platform.system() == "Darwin") { 
            main(RemoteBumble())
    } else {
            print "We only support Darwin and Linux at this time, goodbye"
    }
