'''
File: Defender.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:14:26 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 23rd February 2020 4:05:24 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import networkx as nx
from dataclasses import dataclass
from random import randint, gauss
from typing import List, Callable
import math
import random

from simulator.Stepable import Stepable
from simulator.Epidemic import Epidemic
from simulator.EpidemicGraph import EpidemicGraph

@dataclass
class Defender(Stepable):
    """
    Class for defending the network in the simulation
    """
    EG: EpidemicGraph = EpidemicGraph()
    mu: float = 0.5
    sigma: float = 0.5
    n: int = 100
    m: int = 300
    gamma: float = 2.0

    def build(self, epidemic: Epidemic) -> EpidemicGraph:
        return EpidemicGraph(self.nx_graph(), epidemic)
    
    def powerlaw_sequence(self):
        """
        Return sample sequence of length n from a power law distribution.
        """
        sequence: list = [random.paretovariate(self.gamma-1) for i in range(self.n)]
        factor: float = self.m / sum(sequence)
        sequence = [round(k * factor) for k in sequence]
        return sequence
        
    # @staticmethod
    # def powerlaw_sequence(n: int, m: int, gamma: float = 2.0):
    #     pk = lambda k: k ** -gamma
    #     total_e: int = 0
    #     ks: List[int] = []
    #     k: int = 0
        
    #     while total_e < m and len(ks) < n:
    #         k += 1
    #         for _ in range(round(pk(k))):
    #             ks.append(k)
    #             if total_e >= m:
    #                 # if we hit the edge limit, just return out
    #                 break
    #             if len(ks) >= n:
    #                 # if we hit the vertex limit, we still need to add more edges
    #                 for i in range(total_e - n):
    #                     ks[i % n] += 1
    #                 break

    def nx_graph(self) -> nx.Graph:
        sequence: list = nx.random_powerlaw_tree_sequence(100, tries=5000)
        G: nx.MultiGraph = nx.configuration_model(sequence)
        G = nx.Graph(G)
        G.remove_edges_from(nx.selfloop_edges(G))
        return G
    
    def step(self):
        pass      
    
if __name__ == "__main__":
    defender: Defender = Defender()
    seq = defender.powerlaw_sequence()
    print(sorted(seq))
    print(sum(seq))
    # ep: Epidemic = Epidemic()
    
    # EG: EpidemicGraph = defender.build(ep)
    # EG.show(block=True)
    # deg: list = EG.G.degree()
    # print(sum([d[1] for d in deg]))
    