#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("/Users/sucharitajayanti/Documents/W'20/CS 189 - Network Science and Complex Systems/finalProject/adversarial-epidemics/src")


# In[2]:


import networkx as nx
import itertools
import datapackage
import numpy as np
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
from simulator import SIRD, SIRDGraph
from preprocessing import airNet


# In[3]:


def clean_up_data(G, D, string, default_val):
    missed = np.setdiff1d(list(G.nodes()), list(D.keys()))
    if(len(missed)):
        print("missing " + string + " for the following locations:")
        print(missed)
        for i in missed:
            D[i] = default_val
    return D


# In[4]:


# Calculates what the weight should be on edge (n1,n2) n1!=n2
# Will get more complicated eventually

def get_edge_weight(base_weight, w_n1, w_n2):
    return base_weight


# In[5]:


def get_graph_with_labels(G, pop_dict, node_wreg, spread_rate, mortality_rate, recovery, infected, pos, max_weight):
    
    pop_dict = clean_up_data(G, pop_dict, "populations", 0)
    node_wreg = clean_up_data(G, node_wreg, "weight regulations", 1)
    spread_rate = clean_up_data(G, spread_rate, "b (spread rate)", 0)
    mortality_rate = clean_up_data(G, mortality_rate, "w (mortality rate)", 0)
    recovery = clean_up_data(G, recovery, "k (recovery)", 0.5)
    infected = clean_up_data(G, infected, "i (% initially infected)", 0)
    pos = clean_up_data(G, pos, "positions", (0,0))
    
    max_weight = max_weight + 0.0000000001

    nodes = [(n, SIRD(b=spread_rate[n], k=recovery[n], w=mortality_rate[n], N=pop_dict[n], i=infected[n]), pos[n]) for n in list(G.nodes())] 
    edges = [(u,v,get_edge_weight(d['weight'], node_wreg[u], node_wreg[v])/max_weight) for (u,v,d) in G.edges(data=True)]
    
    return nodes, edges
       


# In[6]:


# Population Related Functions

def get_pop_data():
    data_url = 'https://datahub.io/JohnSnowLabs/population-figures-by-country/datapackage.json'

    # to load Data Package into storage
    package = datapackage.Package(data_url)

    # to load only tabular data
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])
    return data

def pop_dict_year(data, year):
    label = 'Year_' + str(year)
    df = data[['Country',label]]
    pop_dict = {}
    for i in range(df.shape[0]):
        pop_dict[df.iloc[i][0]] = df.iloc[i][1]

    return pop_dict


# In[20]:


def temp_create_data(G, pop_dict, max_weight):
    pop_dict["Hong Kong"] = pop_dict['Hong Kong SAR, China']

    node_wreg = {k:1 for k in pop_dict}
    spread_rate = {k:0.5 for k in pop_dict}
    mortality_rate = {k:0.1 for k in pop_dict}
    recovery = {k:0.8 for k in pop_dict}
    infected = {k:0 for k in pop_dict}
    infected["Germany"] = 1
    infected["Canada"] = 8
    infected["Singapore"] = 20 
    infected["Hong Kong"] = 95
    infected["Switzerland"] = 2
    infected["Thailand"] = 1
    infected["Vietnam"] =  40
    infected["China"] = 100

    percent_infected = {n:infected[n]/pop_dict[n] for n in infected}
    pos = nx.spring_layout(G)
    
    return pop_dict, node_wreg, spread_rate, mortality_rate, recovery, infected, percent_infected, pos

def get_SIRDN_graph():
    G, max_weight = airNet.generate_country_graph()
    pop_dict = pop_dict_year(get_pop_data(), 2003)
    
    #TEMP HACK
    pop_dict, node_wreg, spread_rate, mortality_rate, recovery, infected, percent_infected, pos =  temp_create_data(G, pop_dict, max_weight)
    
    # Generate SIRDN graph
    n, e = get_graph_with_labels(G, pop_dict, node_wreg, spread_rate, mortality_rate, recovery, percent_infected, pos, max_weight)

