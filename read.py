import sqlite3
import tweepy
import json
import time
import networkx as nx
import matplotlib.pyplot as plt

with open('./twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# read database
conn = sqlite3.connect("C:/tweets.db")
c = conn.cursor()
c.execute("SELECT user_id, screen_name, followers_count FROM tweets;")

ids = c.fetchmany(5)
print(len(ids))
print(c.fetchmany(5))

G = nx.DiGraph()
for i in range(0, len(ids)):
    G.add_node(i, userID=ids[i][0])

follow = []
for i in range(len(ids)):
    try:
        G.add_node(i, userID=ids[i][0])
        followers = []
        print("getting ", ids[i][1], "'s followers... ")
        # a = tweepy.Cursor(api.followers_ids,screen_name=ids[i][1]).items()
        for page in tweepy.Cursor(api.followers, screen_name=ids[i][1]).items():
            # print(page.id)
            followers.append(page.id)
        time.sleep(60)
        print(followers)

        print("user ", i, " has ", len(followers), " followers")
        # time.sleep(60)
        for idx in range(len(ids)):
            if ids[idx][0] in followers:
                follow.append((id[0], ids[i][0]))
                G.add_edge(idx, i)
        print("follow list: ", follow)
    except tweepy.TweepError as e:
        print(e.reason, " wait 60s ...")
        time.sleep(60)
        continue
print(follow)

nx.draw(G)
plt.show()
