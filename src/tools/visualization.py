'''
File: visualization.py
Project: tools
File Created: Saturday, 29th February 2020 1:50:46 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Tuesday, 3rd March 2020 12:32:05 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import networkx as nx
from typing import List
import math

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
        color_factor: float = 1,
        size_factor: float = 1/10,
        y_offset: float = 0.03,
        font_size: int = 12,
        font_color: str = "black",
        log: bool = True,
        sqrt_color: bool = True):
    
    colors: list = []
    sizes: list = []
    for n in G.nodes():
        obj = G.nodes[n][attrname]
        red: float = color_factor * getattr(obj, color_attr)
        size: float = size_factor * getattr(obj, size_attr)
        if log and size > 0:
            size = math.log(size)
        if sqrt_color and red > 0:
            red = math.sqrt(red)
            
        colors.append((min(red, 1), 0, 0))
        sizes.append(size)
        
    nx.draw_networkx_nodes(G, pos, labels={n: n for n in G.nodes()}, node_color=colors, node_size=sizes)
    nx.draw_networkx_labels(G,
        {n: (p[0], p[1] - y_offset) for n, p in pos.items()},
        labels={n: n for n in G.nodes()},
        font_size=font_size,
        font_color=font_color)
