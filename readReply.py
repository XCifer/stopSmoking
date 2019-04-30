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
c.execute("SELECT user_id, screen_name, text FROM tweets where text like '%cigarette%';")

items = c.fetchall()
print(len(items))

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



# G2 = G.copy()
# inde = G2.in_degree(G2)
# outde = G2.out_degree(G2)
# for n in G2.nodes():
#     if inde[n]<2 and outde[n]<2:
#         G.remove_node(n)
G.remove_nodes_from(list(nx.isolates(G)))
nx.draw(G,with_labels=True)
plt.show()
plt.savefig('reply.png')