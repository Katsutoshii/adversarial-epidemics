'''
File: misc.py
Project: tools
File Created: Saturday, 29th February 2020 2:07:21 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 2:08:21 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import networkx as nx
from random import random, gauss
from typing import List

def random_weighted_graph(
        n: int = 20,
        k: int = 3) -> nx.Graph:
    """
    Constructs a random weighted graph
    """

    G: nx.Graph = nx.fast_gnp_random_graph(n=n, p=k/n)

    for u, v in G.edges():
        G[u][v]['weight'] = random()
    
    return G

def sort_by_deg(G: nx) -> List[tuple]:
    """
    Returns sorted list of nodes by degree
    """
    return sorted(nx.degree(G), key=lambda vk: vk[1])

def clipped_gauss(mu: float, sigma: float, lower: float, upper: float):
    """
    Returns a clipped gaussian sample
    """
    return min(max(gauss(mu, sigma), lower), upper)
    
def gaussian_choice(l: list, mu: float = 0.5, sigma: float = 0.1,
        lower: float = 0, upper: float = 1):
    """
    Picks a random item with a gaussian distribution from a sorted list
    """
    i: int = int(clipped_gauss(mu, sigma, lower, upper) * len(l))
    return l[i]
    