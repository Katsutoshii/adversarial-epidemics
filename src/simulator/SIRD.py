'''
File: SIRD.py
Project: simulator
File Created: Monday, 2nd March 2020 1:45:44 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 2nd March 2020 4:50:13 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dataclasses import dataclass, field
from simulator import Records, Stepable

@dataclass
class SIRD(Stepable):
    """
    Class for SIR model
    """
    b: float = 1/2      # contacts required for spread
    k: float = 1/4      # recovery fraction
    w: float = 1/4      # mortality rate
    N: int = 1000       # total population

    s: float = 9/10
    i: float = 1/10
    r: float = 0
    d: float = 0

    xi: float = 0       # external infection amount

    records: Records = field(default_factory=Records)

    def __post_init__(self):
        self.records = Records(
            pcolors=["blue", "red", "yellow", "black"],
            plabels=["susceptible", "cases", "recoveries", "deaths"])
            
    def infect(self, amount: float):
        self.xi = amount
        
    def step(self):
        ds: float = -self.b * self.s * self.i - self.xi
        dr: float = self.k * self.i
        di: float = -dr - ds + self.xi
        
        self.s = min(self.s + ds, 1)
        self.i = min(self.i + di, 1)
        self.r = min(self.r + dr * (1 - self.w), 1)
        self.d = min(self.d + dr * self.w, 1)

        self.record()

        self.xi = 0

    def record(self):
        self.records.record((
            self.s * self.N,
            self.i * self.N,
            self.r * self.N,
            self.d * self.N))

    def plot(self):
        self.records.plot()

    def get_dict(self, labels: set = set(["I", "R", "D"])) -> dict:
        return self.records.get_dict(labels)
