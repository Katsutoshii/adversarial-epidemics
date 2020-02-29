'''
File: analysis.py
Project: tools
File Created: Saturday, 29th February 2020 1:37:10 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 29th February 2020 2:19:05 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from typing import Dict, List, Set

from simulator import EpidemicGraph

def squared_error(EG1: EpidemicGraph, EG2: EpidemicGraph) -> float:
    """
    Calculates the squared error between two epidemic graphs
    For comparing simulation against real data
    Currently just uses symptomatic data
    """
    minlen: int = min(len(EG1.symptomatic_data), len(EG2.symptomatic_data))
    total_error: int = 0
    
    for i in range(minlen):
        total_error += (EG2.symptomatic_data[i] - EG1.symptomatic_data[i])**2

    return total_error / minlen

def squared_error_subsets(EG1: EpidemicGraph, EG2: EpidemicGraph,
        subsets: Dict[str, Set[int]]) -> float:
    """
    Calculates the squared error between two epidemic graphs
    Diffs each subset of the graph
    """
    minlen: int = min(len(EG1.symptomatic_data), len(EG2.symptomatic_data))
    total_error: int = 0
    
    for i in range(minlen):
        for name, subset in subsets.items():
            eg1_pop = len(subset.intersection(EG1.symptomatic_data[i]))
            eg2_pop = len(subset.intersection(EG2.symptomatic_data[i]))
            total_error += (eg2_pop - eg1_pop)**2

    return total_error / minlen
