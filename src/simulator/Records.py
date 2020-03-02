'''
File: Records.py
Project: simulator
File Created: Monday, 2nd March 2020 1:46:07 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 2nd March 2020 5:28:09 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import matplotlib.pyplot as plt 
from dataclasses import dataclass, field

@dataclass
class Records():
    """
    Class for keeping, plotting and diffing recorded data
    """
    plabels: list = field(default_factory=list)
    pcolors: list = field(default_factory=list)
    records: list = field(default_factory=list)

    def __post_init__(self):
        self.records = [[] for l in self.plabels]

    def record(self, data: tuple):
        """
        Records data
        """
        for i, d in enumerate(data):
            self.records[i].append(d)

    def error(self, other, indices: list = [0]):
        """
        Diffs two records to find the error between them
        """
        total_err: float = 0
        
        for i in indices:
            for j, val in enumerate(self.records[i]):
                total_err += abs(val - other.records[i][j])

        return total_err

    def plot(self):
        """
        Plots the recorded data
        """
        plt.clf()
        
        x: list = [i for i, _ in enumerate(self.records[0])]
        for i, record in enumerate(self.records):
            plt.plot(
                x,
                record,
                color=self.pcolors[i],
                label=self.plabels[i])

        plt.legend(loc="upper right")
        plt.show()

    def get_dict(self, labels: set) -> dict:
        """
        Returns a dictionary representation of the recorded data
        """
        return {label: [int(v) for v in self.records[i]]
            for i, label in enumerate(self.plabels)
            if label in labels}
