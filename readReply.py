import sqlite3
import json
import time
import networkx as nx
import matplotlib.pyplot as plt
import re

def search():
    # read database
    # keyword = input("Enter a key word for searching in text: ")
    conn = sqlite3.connect("C:/tweets.db")
    conn.text_factory = bytes
    c = conn.cursor()
    c.execute("SELECT user_id, screen_name, text, in_reply_to_user_id FROM tweets where text like '%cigarette%' or text like '%smoking%' or text like 'smokes' or text like 'smoked';")
    items = c.fetchall()
    print(len(items))

    G = nx.DiGraph()


    for i in range(len(items)):
        G.add_node(i, screen_name = items[i][1], user_id=items[i][0])

    for i in range(len(items)):
        if items[i][3] != -1:
            for j in range(len(items)):
                if items[j][0] == items[i][3]:
                    G.add_edge(i,j)
                    print(round(i/len(items),4),"Edge from ",i," to ",j," added.")
        else :
            print(round(i/len(items),4))
    
    return G


   

def draw(G):
    # G2 = G.copy()
    # inde = G2.in_degree(G2)
    # outde = G2.out_degree(G2)
    # for n in G2.nodes():
    #     if inde[n]<2 and outde[n]<2:
    #         G.remove_node(n)
    G.remove_nodes_from(list(nx.isolates(G)))
    nx.draw(G,with_labels=True,node_size =100,font_size =10,node_shape='1')
    plt.show()

draw(search())