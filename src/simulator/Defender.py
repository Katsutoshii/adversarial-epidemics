'''
File: Defender.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:14:26 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 19th February 2020 4:44:20 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import networkx as nx
from dataclasses import dataclass
from random import randint, gauss
from typing import List
from .Stepable import Stepable
from .Epidemic import Epidemic
from .EpidemicGraph import EpidemicGraph

@dataclass
class Defender(Stepable):
    EG: EpidemicGraph = EpidemicGraph()
    mu: float = 0.5
    sigma: float = 0.5

    def build(self, epidemic: Epidemic) -> EpidemicGraph:
        return EpidemicGraph(self.nx_graph(), epidemic)
    
    def nx_graph(self) -> nx.Graph:
        G: nx.Graph = nx.Graph()
        return G 
    
    def step(self):
        pass
