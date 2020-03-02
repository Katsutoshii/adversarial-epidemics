'''
File: SIRDGraph.py
Project: simulator
File Created: Monday, 2nd March 2020 3:13:54 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 2nd March 2020 4:51:43 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from dataclasses import dataclass, field
import networkx as nx
import matplotlib.pyplot as plt
from simulator import SIRD, Records, Stepable
from tools import draw_weighted_edges, draw_colored_nodes
import json

@dataclass
class SIRDGraph(Stepable):
    nodes: list
    edges: list
    pos: dict = field(default_factory=dict)
    G: nx.Graph = nx.Graph()

    def __post_init__(self):
        for node, sird, pos in self.nodes:
            self.G.add_node(node)
            self.G.nodes[node]["SIRD"] = sird
            self.pos[node] = pos

        self.G.add_weighted_edges_from(self.edges)

    def draw(self):
        draw_weighted_edges(self.G, self.pos, width_factor=4/3)
        draw_colored_nodes(self.G, self.pos,
            attrname="SIRD", color_attr="i", size_attr="N", size_factor=1/4000)
    
    def show(self, block: bool = False):
        """
        Shows a figure by clearing axis and drawing
        """
        plt.clf()
        self.draw()
        plt.axis("off")
        plt.show(block=block)
    
    def step(self) -> bool:
        """
        Runs a timestep of the simulation
        """
        for n in self.G.nodes():
            amount: float = 0
            for nn in self.G.neighbors(n):
                nn_sird = self.G.nodes[n]["SIRD"]
                amount += self.G[n][nn]['weight'] * nn_sird.i
            
            self.G.nodes[n]["SIRD"].infect(amount)
        
        for n in self.G.nodes():
            self.G.nodes[n]["SIRD"].step()  # records data
        return True

    def get_dict(self):
        """
        Gets a dictionary representation of the recorde data
        """
        return {n: self.G.nodes[n]["SIRD"].get_dict(labels=set(["cases", "recoveries", "deaths"]))
            for n in self.G.nodes()}

    def save_dict(self):
        """
        Saves the data as a json file
        """
        data_dict: dict = self.get_dict()
        with open("../data/out/test.json", "w") as fp:
            json.dump(data_dict, fp)

    def run(self, maxsteps: int = 200):
        """
        Runs the simulation until the state stops changing
        """
        for _ in range(maxsteps):
            self.show()
            if not self.step():
                break
