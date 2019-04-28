import sqlite3
import json
import time
import networkx as nx
import matplotlib.pyplot as plt
import re

# read database
conn = sqlite3.connect("C:/tweets.db")
conn.text_factory = bytes
c = conn.cursor()
c.execute("SELECT user_id, screen_name, text FROM tweets;")

items = c.fetchall()
# print(c.fetchmany(5))

G = nx.DiGraph()

follow = []
for i in range(len(items)):
    G.add_node(i, user_id = items[i][0], screen_name = items[i][1])

for i in range(len(items)):
    mentions = []
    text = str(items[i][2])
    mentions = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)',text)
    # print(mentions)
    if mentions:
        for idx in range(len(items)):
            if items[idx][2] in mentions:
                G.add_edge(i,idx)
                print(i,"Edge from ",i," to ",idx," added.")
    else :
        print(i)


G.remove_nodes_from(list(nx.isolates(G)))
nx.draw(G,with_labels=True)
plt.show()
plt.savefig('labels.png')
