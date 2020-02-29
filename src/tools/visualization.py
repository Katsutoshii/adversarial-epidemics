'''
File: visualization.py
Project: tools
File Created: Saturday, 29th February 2020 1:50:46 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 1:52:58 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import networkx as nx
from typing import List

def draw_weighted_edges(G: nx.Graph, pos: List[tuple], bins: int = 10):
    """
    Plots the network with weighted edges
    """
    edgelists: list = [[] for i in range(bins)]
    for u, v, eprops in G.edges(data=True):
        edgelists[int(bins * eprops['weight'])].append((u, v))

    for i, edges in enumerate(edgelists):
        nx.draw_networkx_edges(G, pos, edgelist=edges,
            width=i * 0.3 + 0.1, alpha=0.6 + i/40)
    