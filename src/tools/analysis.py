'''
File: analysis.py
Project: tools
File Created: Saturday, 29th February 2020 1:37:10 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 1:43:23 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from simulator import EpidemicGraph

def squared_error(EG1: EpidemicGraph, EG2: EpidemicGraph) -> int:
    """
    Calculates the squared error between two epidemic graphs
    For comparing simulation against real data
    Currently just uses symptomatic data
    """
    minlen: int = min(len(EG1.symptomatic_data), len(EG2.symptomatic_data))
    total_error: int = 0
    
    for i in range(minlen):
        total_error += (EG2.symptomatic_data[i] - EG1.symptomatic_data[i])**2

    return total_error
