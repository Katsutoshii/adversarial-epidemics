'''
File: Infector.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:16:32 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 28th February 2020 12:27:24 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from tools import gaussian_choice, sort_by_deg
from .Stepable import Stepable
from .EpidemicGraph import EpidemicGraph
from dataclasses import dataclass

@dataclass
class Infector(Stepable):
    EG: EpidemicGraph = EpidemicGraph()
    mu: float = 0.5
    sigma: float = 0.1
    
    def step(self):
        """
        Selects susceptible node to infect
        """
        sorted_susc: list = self.EG.sorted_susceptible()
        n, k = gaussian_choice(sorted_susc, mu=self.mu, sigma=self.sigma)
        self.EG.infect(n)
        print(f"Infecting {n} with degree {k}")
