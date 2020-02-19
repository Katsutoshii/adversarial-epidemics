'''
File: stepable.py
Project: simulator
File Created: Wednesday, 19th February 2020 4:12:15 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 19th February 2020 4:16:07 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

class Stepable:
    """
    Abstract class for an object that can be stepped in a
    timestep-based simulation
    """
    def step(self):
        raise NotImplementedError
