'''
File: __init__.py
Project: epidemic
File Created: Monday, 10th February 2020 4:25:50 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Thursday, 13th February 2020 9:37:27 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from typing import List, Set
from dataclasses import dataclass, field
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class Epidemic():
    spread_fraction: float = 0.5
    incubation_period: int = 0
    
@dataclass
class EpidemicGraph():
    G: nx.Graph
    ep: Epidemic
    susceptible: Set[int] = field(default_factory=set)
    infected: Set[int] = field(default_factory=set)

    def __post_init__(self):
        """
        Run after the init function finishes
        """
        for n in G.nodes():
            print(n)
        
    def step(self):
        """
        Runs a timestep of the simulated epidemic on the graph
        """
        pass

    def draw(self):
        pos = nx.spring_layout(G) # positions for all nodes
        nx.draw_networkx_nodes(G, pos,
            nodelist=self.susceptible,
            node_color='b',
            node_size=500,
            alpha=0.8)
        nx.draw_networkx_nodes(G, pos,
            nodelist=self.infected,
            node_color='r',
            node_size=500,
            alpha=0.8)

        # edges
        nx.draw_networkx_edges(G,pos,
                            edgelist=[],
                            width=8,alpha=0.5,edge_color='r')
        nx.draw_networkx_edges(G,pos,
                            edgelist=[],
                            width=8,alpha=0.5,edge_color='b')
    
if __name__ == "__main__":
    G: nx.Graph = nx.fast_gnp_random_graph(n=20, p=20)
    ep: Epidemic = Epidemic()
    EG: EpidemicGraph = EpidemicGraph(G, ep, infected=set([1]))
    EG.draw()
    plt.show()
