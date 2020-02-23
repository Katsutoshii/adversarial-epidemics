'''
File: PACGraph.py
Project: simulator
File Created: Sunday, 23rd February 2020 4:52:53 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 23rd February 2020 4:53:09 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import networkx as nx
from dataclasses import dataclass, field
from typing import List, Tuple, Set
from random import randrange, random, sample

@dataclass
class PACGraph():
    """
    Constructs a networks using Preferential Attachment and Clustering.
    The algorithm starts with a circular graph with n vertices.
    Until there are n edges, the algorithm repeats the following:
        Pick a random vertex v and edge e = (u, w) s.t. u != v != w.
        WLOG, let deg(u) >= deg(v)
        With probability p_c, connect v to both u and w.
        With probability p_p, connect v to u, else connect v to w.
    """

    n: int = 100        # number of nodes
    m: int = 500        # number of edges
    p_p: float = 0.5    # probability of pref. attachment
    p_c: float = 0.5    # probaiblity of clustering

    G: nx.Graph = nx.Graph()
    E: Set[int] = field(default_factory=set)

    def __post_init__(self):
        self.G = nx.cycle_graph(self.n)
        self.E = set(self.G.edges)

        v: int; u: int; w: int
        while len(self.E) < self.m:
            v, u, w = self.pick_vuw()
            
            # otherwise use preferential attachment with prob. p_p
            if random() < self.p_p:
                self.add_edge(v, u)
            else:
                self.add_edge(v, w)

        for i in range(self.n * self.p_c):
            pass

    def pick_vuw(self) -> Tuple[int, int, int]:
        """
        Picks a random vertex edge e = (u, w) and vertex v such that:
            v != u != w
            deg(u) >= deg(w)
        """
        u, w = sample(self.E, k=1)[0]
        v = randrange(self.n)
        while v == u or v == w:
            v = randrange(self.n)

        if self.G.degree(u) < self.G.degree(w):
            u, w = w, u

        return v, u, w

    def add_edge(self, u: int, v: int):
        if u > v:
            u, v = v, u

        self.G.add_edge(u, v)
        self.E.add((u, v))

    def get_nxgraph(self) -> nx.Graph:
        return self.G

    def draw(self):
        nx.draw(self.G)
