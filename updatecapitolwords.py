import requests
from requests_oauthlib import OAuth1
import tweepy
from pymongo import MongoClient
from datetime import datetime as dt
client = MongoClient()
capitolwords = client.dsbc.capitolwords

dates = [w['date'] for w in capitolwords.find({},{'date'})]


m = max(dates)
od = dt.strptime(m, '%Y-%m-%d')
newdate = '%i-%i-%i' % (od.year,od.month,od.day+1)
print newdate

import math
s = 'http://capitolwords.org/api/1/text.json?start_date='+newdate+'&apikey=7ef8a11e218443dcb3867207a3a9172d'

req0 = requests.get(s).json()
num = req0['num_found']
count = len(req0['results'])
try:
    pages = int(math.ceil(float(num)/count))
except ZeroDivisionError:
    pages = 1

capitol_words = []
for pg in range(pages):
    s_n= 'http://capitolwords.org/api/1/text.json?page='+str(pg)+'&start_date='+newdate+'&apikey=7ef8a11e218443dcb3867207a3a9172d'
    results = requests.get(s_n).json()['results']
    for r in results:
        print r
        capitolwords.insert(r)