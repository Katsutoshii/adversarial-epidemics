'''
File: SIRD.py
Project: simulator
File Created: Monday, 2nd March 2020 1:45:44 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 2nd March 2020 1:48:13 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dataclasses import dataclass, field
from simulator import Records

@dataclass
class SIRD():
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

    records: Records = Records(
        pcolors=["blue", "red", "yellow", "black"],
        plabels=["S", "I", "R", "D"])

    def step(self):
        ds: float = -self.b * self.s * self.i
        dr: float = self.k * self.i
        di: float = -dr - ds
        
        self.s += ds
        self.i += di
        self.r += dr * (1 - self.w)
        self.d += dr * self.w

        self.record()

    def record(self):
        self.records.record((
            self.s * self.N,
            self.i * self.N,
            self.r * self.N,
            self.d * self.N))

    def plot(self):
        self.records.plot()