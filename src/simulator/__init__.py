'''
File: __init__.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:04:39 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 2nd March 2020 3:18:14 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dataclasses import dataclass

from .Stepable import Stepable
from .Records import Records
from .SIRD import SIRD
from .SIRDGraph import SIRDGraph
from .PACGraph import PACGraph
from .Epidemic import Epidemic
from .EpidemicGraph import EpidemicGraph
from .Defender import Defender
from .Infector import Infector

@dataclass
class EpidemicSimulator(Stepable):
    """
    Main class for simulating a competition between an infector and a defender
    """

    EG: EpidemicGraph = EpidemicGraph()
    defender: Defender = Defender()
    infector: Infector = Infector()
    
    def __post_init__(self):
        # use the defender to construct the network
        # defender
        pass
    
    def step(self):
        pass