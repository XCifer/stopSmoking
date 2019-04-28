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
c.execute("SELECT screen_name, in_reply_to_screen_name FROM tweets;")

items = c.fetchall()
# print(c.fetchmany(5))

G = nx.DiGraph()


for i in range(len(items)):
    G.add_node(i, screen_name = items[i][0])

for i in range(len(items)):
    if items[i][1]:
        for j in range(len(items)):
            if items[j][0] == items[i][1]:
                G.add_edge(i,j)
                print(round(i/len(items),4),"Edge from ",i," to ",j," added.")
    else :
        print(round(i/len(items),4))


G.remove_nodes_from(list(nx.isolates(G)))
nx.draw(G,with_labels=True)
plt.show()
plt.savefig('labels.png')