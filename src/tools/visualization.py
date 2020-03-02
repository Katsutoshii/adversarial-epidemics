'''
File: visualization.py
Project: tools
File Created: Saturday, 29th February 2020 1:50:46 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 2nd March 2020 3:26:14 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import networkx as nx
from typing import List

def draw_weighted_edges(G: nx.Graph, pos: List[tuple],
    bins: int = 10, width_factor: float = 0.4):
    """
    Plots the network with weighted edges
    """
    edgelists: list = [[] for i in range(bins)]
    for u, v, eprops in G.edges(data=True):
        edgelists[int(bins * eprops['weight'])].append((u, v))

    for i, edges in enumerate(edgelists):
        nx.draw_networkx_edges(G, pos, edgelist=edges,
            width=i * width_factor + 0.1, alpha=0.6 + i/40)

def draw_colored_nodes(G: nx.Graph,
        pos: dict,
        attrname: str,
        color_attr: str,
        size_attr: str,
        size_factor: float = 1/10,
        y_offset: float = 0.03):
    
    colors: list = []
    sizes: list = []
    for n in G.nodes():
        red: float = getattr(G.nodes[n][attrname], color_attr)
        size: float = getattr(G.nodes[n][attrname], size_attr)
        colors.append((red, 0, 0))
        sizes.append(size * size_factor)
        
    nx.draw_networkx_nodes(G, pos, labels={n: n for n in G.nodes()}, node_color=colors, node_size=sizes)
    nx.draw_networkx_labels(G,
        {n: (p[0], p[1] - y_offset) for n, p in pos.items()},
        labels={n: n for n in G.nodes()})
    # print(nodelists)
    # for i, nodes in enumerate(nodelists):
    #     color = [(i / bins + 0.1, 0.0, 0.0)]
    #     print(f"color for {i} = {color}")
    #     nx.draw_networkx_nodes(G, pos,
    #         nodelist=nodes, label=nodes, node_color=color)
