'''
File: SIRDGraph.py
Project: simulator
File Created: Monday, 2nd March 2020 3:13:54 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Tuesday, 3rd March 2020 9:48:32 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from dataclasses import dataclass, field
import networkx as nx
import matplotlib.pyplot as plt
from simulator import SIRD, Records, Stepable
from tools import draw_weighted_edges, draw_colored_nodes
import json
from typing import Callable

def null_background():
    pass

@dataclass
class SIRDGraph(Stepable):
    nodes: list
    edges: list
    pos: dict = field(default_factory=dict)
    G: nx.Graph = nx.Graph()

    # draw settings
    font_size: int = 12
    width_factor: float = 1/2
    size_factor: float = 1/30000
    color_factor: float = 2
    y_offset: float = 0.03
    font_color: str = "black"
    labels: bool = False

    draw_background: Callable = null_background

    def __post_init__(self):
        for node, sird, pos in self.nodes:
            self.G.add_node(node)
            self.G.nodes[node]["SIRD"] = sird
            self.pos[node] = pos

        self.G.add_weighted_edges_from(self.edges)

    def draw(self):
        self.draw_background()
        draw_weighted_edges(self.G, self.pos,
            width_factor=self.width_factor)
        draw_colored_nodes(self.G, self.pos,
            attrname="SIRD", color_attr="i", size_attr="N",
            size_factor=self.size_factor,
            color_factor=self.color_factor,
            font_size=self.font_size,
            font_color=self.font_color,
            y_offset=self.y_offset,
            labels=self.labels)
    
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
