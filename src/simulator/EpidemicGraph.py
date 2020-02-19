'''
File: EpidemicGraph.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:12:59 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 19th February 2020 4:28:03 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from typing import List, Set, Dict
from dataclasses import dataclass, field
import networkx as nx
import matplotlib.pyplot as plt
from random import random

from .Stepable import Stepable
from .Epidemic import Epidemic

@dataclass
class EpidemicGraph(Stepable):
    """
    Class for representing an epidemic spreading over a graph
    """
    G: nx.Graph = field(default_factory=nx.Graph)
    ep: Epidemic = field(default_factory=Epidemic)
    pos: List = field(default_factory=list)

    # Subgraphs for states
    susceptible: Set[int] = field(default_factory=set)
    infected: Dict[int, int] = field(default_factory=dict)
    immune: Set[int] = field(default_factory=set)
    recovered: Set[int] = field(default_factory=set)

    # Changes lists
    to_infect: List[int] = field(default_factory=list)
    to_recover: List[int] = field(default_factory=list)

    def __post_init__(self):
        """
        Run after the init function finishes
        Set all unset nodes
        """
        preset: Set[int] = set.union(
            self.susceptible,
            self.infected,
            self.recovered,
            self.immune)
        
        for n in self.G.nodes():
            if n not in preset:
                self.susceptible.add(n)

        self.pos = nx.spring_layout(self.G) 
        
    def infect(self, n: int):
        """
        Infects a node
        """
        self.susceptible.remove(n)
        self.infected[n] = 0

    def recover(self, n: int):
        """
        Recovers a node
        """
        self.infected.pop(n)
        self.recovered.add(n)
        
    def step_susceptible(self, n: int):
        """
        Runs a timestep for a susceptible node
        """
        total_infected: int = 0
        total: int = 0
        for nn in self.G.neighbors(n):
            total += 1
            if nn in self.infected:
                total_infected += 1
        
        if total <= 0:
            return
            
        if total_infected / total > self.ep.spread_fraction:
            self.to_infect.append(n)

    def step_infected(self, n: int):
        """
        Runs a timestep for an infected node
        """
        self.infected[n] += 1
        if self.infected[n] > self.ep.recovery_period and \
                random() < self.ep.recovery_rate:
            self.to_recover.append(n)

    def step_recovered(self, n: int):
        """
        Runs a timestep for a recovered node
        """
        pass

    def step_immune(self, n: int):
        """
        Runs a timestep for an immune node
        """
        pass

    def step_node(self, n: int):
        """
        Infects a given node if too many of its neighbors have the infection
        """
        if n in self.susceptible:
            self.step_susceptible(n)
        elif n in self.infected:
            self.step_infected(n)
        elif n in self.recovered:
            self.step_recovered(n)
        elif n in self.immune:
            self.step_immune(n)
        
    def step(self) -> bool:
        """
        Runs a timestep of the simulated epidemic on the graph
        Returns True if the state has changed
        """
        for n in self.G.nodes():
            self.step_node(n)

        # process changes lists
        for n in self.to_infect:
            self.infect(n)
        
        for n in self.to_recover:
            self.recover(n)
            
        changed: bool = bool(self.to_infect or self.to_recover)
        
        # reset all lists
        self.to_infect = []
        self.to_recover = []

        return changed

    def draw_nodes(self, nodes: List[int], color: str,
            alpha = 0.8, size = 25):
        """
        Draws a subset of the nodes on the graph
        """
        nx.draw_networkx_nodes(self.G, self.pos,
            nodelist=nodes,
            node_color=color,
            node_size=size,
            alpha=alpha)

    def draw(self):
        """
        Draws all nodes and edges
        """
        self.draw_nodes(self.susceptible, 'blue')
        self.draw_nodes(self.infected, 'red')
        self.draw_nodes(self.immune, 'green')
        self.draw_nodes(self.recovered, 'yellow')
        
        nx.draw_networkx_edges(self.G, self.pos,
                edgelist=self.G.edges(),
                width=1,
                alpha=0.5,
                edge_color='black')