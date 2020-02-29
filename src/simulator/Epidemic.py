'''
File: Epidemic.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:04:39 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 2:59:37 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dataclasses import dataclass

@dataclass
class Epidemic():
    """
    Holds the properties of the epidemic
    """
    spread_fraction: float = 0.01
    incubation_period: int = 0
    recovery_period: int = 0
    recovery_rate: float = 0.5      # mortality rate = 1 - recovery_rate
