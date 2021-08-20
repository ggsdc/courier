import pandas as pd
import generate_cycles as generator
import datetime as datetime

# Routes to the data files. This has to be changed.
vehicles_path = "..\\data\\vehicles.data"
points_path = "..\\data\\points15.data"
demand_path = "..\\data\\demand15.data"

t1 = datetime.datetime.now()
# Loading of the data files.
vehicles_data = pd.read_csv(vehicles_path, sep = '\t')
points_data = pd.read_csv(points_path, sep = '\t')
demand_data = pd.read_csv(demand_path, sep = '\t')
times = demand_data[['originCode', 'destinationCode', 'Hours']]
distance = demand_data[['originCode', 'destinationCode', 'Kilometers']]
demand = demand_data[['originCode', 'destinationCode', 'parcels']]
t2 = datetime.datetime.now()
print(t2-t1)
# Set of points
points_set = set(points_data['code'])
cross_docking_points = set((280, 231))

# dictionaty of cycles.
cycles_dict = {}
cycles_cross_dict = {}
aux_dict = {}
aux_cross_dict = {}
id = 1

cycles_dict, cycles_cross_dict, id = generator.create_single_cycles(id, points_set, cross_docking_points, times)
aux_dict, aux_cross_dict, id = generator.create_cycle_with_one_stop(id, points_set, cross_docking_points, times)

cycles_dict.update(aux_dict)
cycles_cross_dict.update(aux_cross_dict)
t3 = datetime.datetime.now()
print("The number of routes is: ", id)
print(t3-t2)