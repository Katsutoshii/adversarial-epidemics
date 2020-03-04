'''
File: preprocessing.py
Project: tools
File Created: Tuesday, 3rd March 2020 9:03:41 pm
Author: Sucharita Jayanti
-----
Last Modified: Tuesday, 3rd March 2020 9:26:37 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

import numpy as np
import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from simulator import SIRD

def load_data(filepath):
    # load data into pandas dataframe
    return pd.read_csv(filepath)

# creates the global airport network (domestic and international)
def flight_graph(df):
    # Create directed graph from routes data
    G = nx.DiGraph()
    for index, row in df.iterrows(): 
        G.add_edge(row['Source ID'], row['Destination ID']) 
        
    return G


def summarize_graph(G):
    # Summary statistics about the network
    return nx.info(G)


def plot_degree_distribution(G):
    # extract degree of each airport sorted in decreasing order
    degrees = [airport[1] for airport in sorted(nx.degree(G), key=lambda x: x[1], reverse=True)]

    plt.plot(degrees)


# retrieves the country name given an ID
def country_dict(df2):
    # Get the country name from ID number
    country = dict()

    for index, row in df2.iterrows(): 
        country[row['Airport ID']] = row['Country']

    return country


# helper function to retrieve country name given an airport ID
def get_country(ID, country):
    # @return country_name - str
    if ID == "\\N" or float(ID) not in country:
        return 'No ID'

    return country[float(ID)]

# helper function used to rank countries by number of airports
def num_airports(G, country):
    num_airports = dict()

    for airport in  nx.degree(G):
        name = get_country(airport[0], country)
        if name != 'No ID':
            num_airports[name] = num_airports.get(name, 0) + 1

    names, num = [], [] 
    for name, count in sorted(num_airports.items(), key=lambda item: item[1], reverse=True):
        names.append(name)
        num.append(count)
        
    return names, num

# Main function used to generate the country graph
def create_country_graph(df, country):
    # International graph network, weighted by number of routes between two countries
    country_graph = nx.DiGraph()
    max_weight = 0
    
    for index, row in df.iterrows(): 
        source, destination = get_country(row['Source ID'],country), get_country(row['Destination ID'],country)
        if source != 'No ID' and destination != 'No ID':
            if country_graph.has_edge(source, destination):
                country_graph[source][destination]['weight'] += 1
            else:
                country_graph.add_edge(source, destination, weight=1) 

            max_weight = max(max_weight, country_graph[source][destination]['weight'])
    
    return country_graph, max_weight

def load_datasets(routes_filename: str = "../data/routes.txt",
        airports_filename: str = "../data/airports.txt"):
    df = load_data(routes_filename)
    df = df.drop(['Airline', 'Airline ID', 'Codeshare', 'Stops', 'Equipment'], axis=1)

    # Read airport data to map Airport ID -> Country
    df2 = load_data(airports_filename)
    df2 = df2.drop(['Latitude','Longitude','Altitude','Timezone','DST',
                    'database time zone','Type','Source','City','Name'], axis=1) 
    
    return df, df2

def generate_country_graph():
    # load the routes and airport csv files into pandas dataframes
    df, df2 = load_datasets()

    # create a id to country mapping
    country = country_dict(df2)

    # create country graph
    return create_country_graph(df, country)
