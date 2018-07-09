import networkx as nx
import pandas as pd

vehicles_path = "..\\data\\vehicles.data"
points_path = "..\\data\\points15.data"
demand_path = "..\\data\\demand15.data"

# Loading of the data files.
vehicles_data = pd.read_csv(vehicles_path, sep = '\t')
points_data = pd.read_csv(points_path, sep = '\t')
demand_data = pd.read_csv(demand_path, sep = '\t')
times = demand_data[['originCode', 'destinationCode', 'Hours']]
distance = demand_data[['originCode', 'destinationCode', 'Kilometers']]
demand = demand_data[['originCode', 'destinationCode', 'parcels']]

points_set = set(points_data['code'])
aux_points_set = set(points_set)
cross_docking_points = set((280, 231))
