'''
File: DataDriver.py
Project: simulator
File Created: Saturday, 29th February 2020 2:27:13 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 2:47:15 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dataclasses import dataclass
from typing import List
from random import sample

from .Stepable import Stepable
from .EpidemicGraph import EpidemicGraph

@dataclass
class DataDriver(Stepable):
    EG: EpidemicGraph
    timesteps: List[dict]
    t: int = 0

    def step(self):
        if self.t >= len(self.timesteps): return 
        
        actions: dict = self.timesteps[self.t]
        for country, diff in actions.items():
            for n in sample(self.EG.susceptible, k=diff["cases"]):
                self.EG.infect(n)
                