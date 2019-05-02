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
c.execute("SELECT user_id, screen_name, text FROM tweets where text like '%cigarette%' or text like '%smoking%' or text like 'smokes' or text like 'smoked';")

items = c.fetchall()
print(len(items))

G = nx.DiGraph()

for i in range(len(items)):
    G.add_node(i, user_id = items[i][0], screen_name = items[i][1], text = items[i][2])

for i in range(len(items)):
    mentions = []
    text = str(items[i][2])
    mentions = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)',text)
    # print(mentions)
    # if mentions:
    for idx in range(len(items)):
        if items[idx][1] in mentions:
            G.add_edge(i,idx)
            print(i,"Edge from ",i," to ",idx," added.")



G.remove_nodes_from(list(nx.isolates(G)))
nx.draw(G,with_labels=True,node_size =100,font_size =10,node_shape='1')
plt.show()
# plt.savefig('labels.png')
