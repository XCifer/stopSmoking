import sqlite3
import tweepy
import json
import time
import networkx as nx

G = nx.DiGraph()

with open('./twitter_credentials.json') as cred_data:
	info = json.load(cred_data)
	consumer_key = info['CONSUMER_KEY']
	consumer_secret = info['CONSUMER_SECRET']
	access_key = info['ACCESS_KEY']
	access_secret = info['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#read database
conn = sqlite3.connect("C:/tweets.db")
c = conn.cursor()
c.execute("SELECT user_id, screen_name, followers_count FROM tweets;")

ids = c.fetchmany(1000)
print(len(ids))
print(c.fetchmany(5))
follow = []
for i in range(len(ids)):
		try:
			followers = []
			print("getting ", ids[i][1],"'s followers... ")
			# a = tweepy.Cursor(api.followers_ids,screen_name=ids[i][1]).items()
			for page in tweepy.Cursor(api.followers, screen_name=ids[i][1]).items():
				followers.append(page)
				time.sleep(60)
			print(followers)
			
			print("user ",i," has ",len(followers), " followers")
			# time.sleep(60)
			for id in ids:
				if id[0] in followers:
						follow.append((id[0],ids[i][0]))
			print("follow list: ",follow)
		except tweepy.TweepError as e:
			print(e.reason," wait 60s ...")
			time.sleep(60)
			continue
print(follow)