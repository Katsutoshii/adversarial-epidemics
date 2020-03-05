'''
File: initialization.py
Project: tools
File Created: Tuesday, 3rd March 2020 11:44:41 pm
Author: Sucharita Jayanti
'''

import numpy as np
import pandas as pd
import networkx as nx
import math

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tools import generate_country_graph
from simulator import SIRD

def clean_up_data(G, D, string, default_val):
    missed = np.setdiff1d(list(G.nodes()), list(D.keys()))
    if(len(missed)):
        print("missing " + string + " for the following locations:")
        print(missed)
        for i in missed:
            D[i] = default_val
    return D


# Calculates what the weight should be on edge (n1,n2) n1!=n2
# Will get more complicated eventually
def get_edge_weight(base_weight, w_n1, w_n2, max_weight):
    return np.sqrt(base_weight/max_weight)


def get_graph_with_labels(G, pop_dict, node_wreg, spread_rate,
    mortality_rate, recovery, infected, pos, max_weight,
    insulation=0.5):
    
    pop_dict = clean_up_data(G, pop_dict, "populations", 0)
    node_wreg = clean_up_data(G, node_wreg, "weight regulations", 1)
    spread_rate = clean_up_data(G, spread_rate, "b (spread rate)", 0)
    mortality_rate = clean_up_data(G, mortality_rate, "w (mortality rate)", 0)
    recovery = clean_up_data(G, recovery, "k (recovery)", 0.5)
    infected = clean_up_data(G, infected, "i (% initially infected)", 0)
    
    pos = clean_up_data(G, pos, "positions", (0,0))
    
    max_weight = max_weight + 0.0000000001

    nodes = [(n,
        SIRD(
            b=spread_rate[n],
            k=recovery[n],
            w=mortality_rate[n],
            N=pop_dict[n],
            i=infected[n],
            s=1-infected[n],
            insulation=insulation),
        pos[n])
        for n in list(G.nodes())]

    edges = [(u,v, get_edge_weight(d['weight'], node_wreg[u], node_wreg[v], max_weight))
        for (u,v,d) in G.edges(data=True)]
    
    return nodes, edges

def get_name_alpha3_conv():
    l_data = pd.read_csv('../data/SIRDNMetrics/Abrevs.csv')
    code_dict = {l_data['Country'][i]: l_data['Alpha3Code'][i] for i in range(l_data.shape[0])}  
    return code_dict



# POPULATION DATA RETRIEVAL

def get_pop_data(year):
    p_data = pd.read_csv('../data/SIRDNMetrics/Population.csv')
    
    code_dict = get_name_alpha3_conv()
    
    label = 'Year_' + str(year)
    df = p_data[['Country_Code',label]]
    pop_code_dict = {}
    for i in range(df.shape[0]):
        pop_code_dict[df.iloc[i][0]] = df.iloc[i][1]
    
    pop_dict = {}
    for loc in code_dict:
        if code_dict[loc] in pop_code_dict:
            pop_dict[loc] = pop_code_dict[code_dict[loc]]
            
    return pop_dict


# POPULATION DENSITY RETRIEVAL

def get_spread_rate_dict(year, max_spread_rate):
    p_data = pd.read_csv('../data/SIRDNMetrics/PopulationDensity.csv')
    
    # Country Name -> Country Code
    code_dict = get_name_alpha3_conv()
    
    label = str(year)
    df = p_data[['Country Code',label]]
    
    # Country Code -> Density
    density_code_dict = {}
    max_density = 0
    for i in range(df.shape[0]):
        density_code_dict[df.iloc[i][0]] = df.iloc[i][1]
        max_density = max(df.iloc[i][1], max_density)
        
    # Country Name -> Spread Rate
    sr_dict = {}
    for loc in code_dict:
        if code_dict[loc] in density_code_dict:
            sr_dict[loc] = np.sqrt(np.sqrt(density_code_dict[code_dict[loc]] * (max_spread_rate)/(max_density)))
            
    return sr_dict


# NODE POSITION DATA RETRIEVAL

# Convert positions to mercator map projection coordinates
def get_x(width, long):
    width = width - 200
    return int(round(math.fmod((width * (180.0 + long) / 360.0), (1.5 * width)))) + 100

def get_y(width, height, lat):
    height = height - 100
    lat_rad = lat * math.pi / 180.0
    merc = 0.5 * math.log( (1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)) )
    return int(round((height / 2) - ((width) * merc / (2 * math.pi))))+25


# Get x, y coordinates for plotting (with some correction for the way the map was trimmed
def get_pos_data():
    world_map=mpimg.imread('../data/SIRDNMetrics/worldMap.png')
    map_dim = world_map.shape
    h = world_map.shape[0]
    w = world_map.shape[1]

    pos_data = pd.read_csv('../data/SIRDNMetrics/Location.csv')
    pos = {pos_data['Country'][i]:(get_x(w, pos_data['Longitude'][i]), get_y(w, h, pos_data['Latitude'][i])+400) for i in range(pos_data.shape[0])}
    return pos

# TEMP HACK FUNCTION FOR OTHER DATA RETRIEVAL

def temp_create_data(G, pop_dict):
    node_wreg = {k:1 for k in pop_dict}
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
    return node_wreg, infected, percent_infected


# ## Graph Generation Code ##
def get_SIRDN_graph(b=0.000002, insulation=0.5, recovery=0.02, mortality=0.12):
    G, max_weight = generate_country_graph()
    pop_dict = get_pop_data(2003)#pop_dict_year(get_pop_data(), 2003)
    spread_rate = get_spread_rate_dict(2003, b)
    recovery = {k:recovery for k in pop_dict}
    pos = get_pos_data()
    
    # mortality_rate = {k:0.15 for k in pop_dict}
    mortality_rate = {k:mortality for k in pop_dict}
    #TEMP HACK
    node_wreg, infected, percent_infected =  temp_create_data(G, pop_dict)
    
    # Generate SIRDN graph
    print("spread rate")
    print(spread_rate)
    n, e = get_graph_with_labels(G, pop_dict, node_wreg, spread_rate,
        mortality_rate, recovery, percent_infected, pos, max_weight,
        insulation=insulation)
    return n, e, G, pos


# ## Visualization Code ##

# Visualization Helper
def plot_world_map(w=180, h=160):
    fig=plt.figure(figsize=(w, h))
    world_map=mpimg.imread('../data/SIRDNMetrics/worldMap.png')
    plt.imshow(world_map)
    
# takes nodes, returns nodes->labels dict
# sanatizes label list in between if necessary
def get_labels(nodes):
    code_dict = get_name_alpha3_conv()
    
    labels = {}
    for n in nodes:
        if n in code_dict:
            labels[n] = code_dict[n]
        else:
            labels[n] = 'N/A'

    return labels
