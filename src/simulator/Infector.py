'''
File: Infector.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:16:32 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 19th February 2020 4:17:21 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from .Stepable import Stepable
from dataclasses import dataclass

@dataclass
class Infector(Stepable):
    def step(self):
        pass
