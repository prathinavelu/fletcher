import tweepy
import json
from pymongo import MongoClient
from datetime import datetime as dt
client = MongoClient()
congress = client.dsbc.congress

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = "u3YQ8gKfXGs7Uc9WcDIo8LZw4"
consumer_secret = "GDSymPoZGYdIbjJLw1Wgm7GE3p8LnQbqY1LGWPYCMs6rqeemLP"
access_token = "2828159875-jF5oTVCpmW3AyTMic26GUD6ByS6ZSskTedRepU4"
access_secret = "2X59xSlGHHlKaVTwmlbLDDnodDqakAuazIHmIRA0xmM0w"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        tweet = json.loads(data)
        d = {}
        d['id'] = tweet['id']
        d['user'] = tweet['user']['screen_name']
        d['date'] = tweet['created_at']
        d['text'] = tweet['text']
        d['favorite_count'] = tweet['favorite_count']
        d['retweet_count'] = tweet['retweet_count']
        d['followers'] = tweet['user']['followers_count']
        d['description'] = tweet['user']['description']
        d['location'] = tweet['user']['location']
        congress.insert(d)
        print d

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    congressmen_ids = []
    for person in api.list_members('cspan','members-of-congress',count=500):
        congressmen_ids.append(person.id_str)
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    print "Showing all new tweets for members of congress:"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(follow=congressmen_ids)