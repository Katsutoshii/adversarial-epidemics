'''
File: EpidemicGraph.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:12:59 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 3:15:21 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from typing import List, Set, Dict
from dataclasses import dataclass, field
import networkx as nx
import matplotlib.pyplot as plt
from random import random
from copy import copy

from tools import draw_weighted_edges

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
    symptomatic: Set[int] = field(default_factory=set)
    immune: Set[int] = field(default_factory=set)
    recovered: Set[int] = field(default_factory=set)
    deceased: Set[int] = field(default_factory=set)

    # Data points for states
    susceptible_data: List[Set[int]] = field(default_factory=list)
    infected_data: List[Set[int]] = field(default_factory=list)
    symptomatic_data: List[Set[int]] = field(default_factory=list)
    immune_data: List[Set[int]] = field(default_factory=list)
    recovered_data: List[Set[int]] = field(default_factory=list)
    deceased_data: List[Set[int]] = field(default_factory=list)

    # Changes lists
    to_infect: List[int] = field(default_factory=list)
    to_symptomize: List[int] = field(default_factory=list)
    to_recover: List[int] = field(default_factory=list)
    to_decease: List[int] = field(default_factory=list)

    degrees: List[tuple] = field(default_factory=list)
    verbose: bool = False

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
        
        # initialize all unset nodes to susceptible
        for n in self.G.nodes():
            if n not in preset:
                self.susceptible.add(n)

        # if no weights are defined, default to 1
        for u, v in self.G.edges():
            if 'weight' not in self.G[u][v]:
                self.G[u][v]['weight'] = 0.1

        self.pos = nx.spring_layout(self.G) 
        self.degrees = sorted([(n, v) for n, v in nx.degree(self.G)], key=lambda nk: nk[1])
        self.record_data()
        
    def infect(self, n: int):
        """
        Infects a node
        """
        self.susceptible.remove(n)
        self.infected[n] = 0
        
        if not self.ep.incubation_period:
            self.symptomatic.add(n)

    def symptomize(self, n: int):
        """
        Makes a node show symptoms
        """
        self.symptomatic.add(n)
        
    def recover(self, n: int):
        """
        Recovers a node
        """
        self.infected.pop(n)
        self.symptomatic.remove(n)
        self.recovered.add(n)

    def decease(self, n: int):
        """
        Kills a node
        """
        self.infected.pop(n)
        self.symptomatic.remove(n)
        self.deceased.add(n)
        
    def step_susceptible(self, n: int):
        """
        Runs a timestep for a susceptible node
        """
        total_infected: int = 0
        total: int = 0
        for nn in self.G.neighbors(n):
            total += self.G[n][nn]['weight']
            if nn in self.infected:
                total_infected += self.G[n][nn]['weight']
        
        if total <= 0:
            return
            
        if total_infected / total > self.ep.spread_fraction:
            self.to_infect.append(n)

    def step_infected(self, n: int):
        """
        Runs a timestep for an infected node
        """
        self.infected[n] += 1
        if self.infected[n] > self.ep.incubation_period and n not in self.symptomatic:
            self.to_symptomize.append(n)
            
        if self.infected[n] > self.ep.recovery_period:
            if random() < self.ep.recovery_rate:
                self.to_recover.append(n)
            else:
                self.to_decease.append(n)

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

    def step_deceased(self, n: int):
        """
        Runs a timestep for a deceased node
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
        elif n in self.deceased:
            self.step_deceased(n)
        
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
        
        for n in self.to_symptomize:
            self.symptomize(n)
            
        for n in self.to_recover:
            self.recover(n)

        for n in self.to_decease:
            self.decease(n)
            
        changed: bool = bool(self.infected or self.to_infect or self.to_recover)
        
        # reset all lists
        self.to_infect = []
        self.to_recover = []
        self.to_symptomize = []
        self.to_decease = []
        
        self.record_data()
        return changed

    def percent_infected(self) -> float:
        """
        Returns the percent of infected nodes
        """
        return len(self.infected) / self.G.number_of_nodes()

    def record_data(self):
        """
        Saves current populations to data lists
        """
        self.susceptible_data.append(copy(self.susceptible))
        self.infected_data.append(copy(self.infected))
        self.symptomatic_data.append(copy(self.symptomatic))
        self.immune_data.append(copy(self.immune))
        self.recovered_data.append(copy(self.recovered))
        self.deceased_data.append(copy(self.deceased))

    def sorted_susceptible(self):
        """
        Returns sorted susceptible
        """
        return [(n, k) for n, k in self.degrees if n in self.susceptible]

    def draw_nodes(self, nodes: List[int], color: str,
            alpha: float = 0.8, size: float = 25):
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
        self.draw_nodes(self.immune, 'green')
        self.draw_nodes(self.susceptible, 'blue')
        self.draw_nodes(self.infected, 'purple')
        self.draw_nodes(self.symptomatic, 'red')
        self.draw_nodes(self.recovered, 'yellow')
        self.draw_nodes(self.deceased, 'black')

        draw_weighted_edges(self.G, self.pos)

    def plot_data(self):
        """
        Plots all trend lines for the evolution of the epidemic
        """
        plt.clf()
        x: List[int] = [i for i in range(len(self.susceptible_data))]
        plt.plot(x, [len(s) for s in self.immune_data], color="green", label="Immune")
        plt.plot(x, [len(s) for s in  self.susceptible_data], color="blue", label="Susceptible")
        plt.plot(x, [len(s) for s in self.infected_data], color="purple", label="Infected")
        plt.plot(x, [len(s) for s in self.symptomatic_data], color="red", label="Symptomatic")
        plt.plot(x, [len(s) for s in self.recovered_data], color="yellow", label="Recovered")
        plt.plot(x, [len(s) for s in self.deceased_data], color="black", label="Deceased")
        plt.legend(loc="upper right")
        plt.show()

    def show(self, block: bool = False):
        """
        Shows a figure by clearing axis and drawing
        """
        plt.clf()
        self.draw()
        plt.axis("off")
        plt.show(block=block)

    def savefig(self, filename: str, dpi: int = 400):
        """
        Saves the figure of the graph
        """
        self.show()
        plt.savefig(
            filename,
            dpi=dpi,
            bbox_inches='tight',
            pad_inches=0)

    def run(self):
        """
        Runs the simulation until the state stops changing
        """
        while True:
            self.show()
            if not self.step(): break
