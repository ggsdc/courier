# & c:/Users/bob_guille/Desktop/proyectos/i-d-courier/src/venv/Scripts/python.exe
import pandas as pd
import datetime as datetime
import read_data as rd
import complex_arc as ca
import cycle as cy
import path as pa
import arc_generation as generator
import time_space as ts

# Routes to the data files. This has to be changed.
vehicles_path = "..\\data\\vehicles.data"
points_path = "..\\data\\pointsFull.data"
demand_path = "..\\data\\demandFull.data"

t1 = datetime.datetime.now()

# Loading of the data files.
vehicles_data = pd.read_csv(vehicles_path, sep = '\t')
points_data = pd.read_csv(points_path, sep = '\t')
points_names = points_data[['code', 'point']]
points_names_dict = dict(zip(points_names.code, points_names.point))

demand_data = pd.read_csv(demand_path, sep = '\t')

demand = demand_data[['originCode', 'destinationCode', 'parcels']]
demand_dict = demand.groupby('originCode').apply(lambda x: dict(zip(x['destinationCode'], x['parcels']))).to_dict()
demand_dict_aux = demand.groupby('destinationCode').apply(lambda x: dict(zip(x['originCode'], x['parcels']))).to_dict()

demand_parcels_for = dict()
demand_parcels_from = dict()

for i in demand_dict:
    laux = list()
    
    for j in demand_dict[i]:
        if demand_dict[i][j] > 0:
            laux.append(j)
    
    demand_parcels_for[i] = laux

for i in demand_dict_aux:
    laux = list()
    
    for j in demand_dict_aux[i]:
        if demand_dict[i][j] > 0:
            laux.append(j)

    demand_parcels_from[i] = laux
    

demand_origin \
    = demand_data.groupby('originCode', as_index = False).agg({"parcels": "sum"})

demand_origin_dict = dict(zip(demand_origin.originCode, demand_origin.parcels))

demand_destination \
    = demand_data.groupby('destinationCode', as_index = False).agg({"parcels": "sum"})

demand_destination_dict = dict(zip(demand_destination.destinationCode, demand_destination.parcels))

times = demand_data[['originCode', 'destinationCode', 'Hours']]
times_dict = times.groupby('originCode').apply(lambda x: dict(zip(x['destinationCode'], x['Hours']))).to_dict()

distance = demand_data[['originCode', 'destinationCode', 'Kilometers']]

t2 = datetime.datetime.now()
print(t2-t1)

# Set of points
points_set = set(points_data['code'])
cross_docking_points = set((280, 231))
# cross_docking_points = set((280, 231, 500, 930, 492, 35, 12))

# 280 - Madrid
# 231 - Bailen
# 500 - Zaragoza
# 930 - Valencia
# 492 - Benavente
# 35 - Villena
# 12 - Vitoria

# Arcs dictionaries
arc_list = list()
temp_arcs = list()
aux_list = list()
aux_list_2 = list()
selected_arcs = list()
selected_arcs_2 = list()

# Cycles dictionaries - Main
cycle_dict = list()
temp_cycles = list()

# Paths dictionaries - Main
path_dict = list()
temp_paths = list()

# Indexes for the dicts
arc_idx = 1
cycle_idx = 1
path_idx = 1

t4 = datetime.datetime.now()

# Main generation loop
for cross in cross_docking_points:

    # Remove the cross from the population
    points_set.remove(cross)
    
    t1 = datetime.datetime.now()
    # Get the simple arcs
    temp_arcs, arc_idx \
        = generator.simple_arc_generation(cross, points_set, points_names_dict, times_dict, demand_dict, arc_idx)
    t2 = datetime.datetime.now()

    print(cross, ' - ', len(temp_arcs), ' Simple arcs. Time: ', t2 - t1)
        
    # Update dictionaries
    arc_list.extend(temp_arcs)
    aux_list = temp_arcs
    
    t1 = datetime.datetime.now()
    # Get complex arcs
    temp_arcs, arc_idx \
        = generator.complex_arc_genertation(cross, cross_docking_points, temp_arcs, points_names_dict, times_dict, arc_idx)
    t2 = datetime.datetime.now()

    print(cross, ' - ', len(temp_arcs), ' Complex arcs. Time: ', t2 - t1)
    
    # Update the dictionaries
    arc_list.extend(temp_arcs)
    aux_list.extend(temp_arcs)
    
    t1 = datetime.datetime.now()
    # Generate the cycles for each cross
    temp_cycles, selected_arcs, selected_arcs_2, cycle_idx \
        = generator.cycle_generation(cross, aux_list, demand_origin,\
            demand_destination, cycle_idx)
    t2 = datetime.datetime.now()

    print(cross, ' - ', len(temp_cycles), ' Cycles. Time: ', t2 - t1)
    print(cross, ' - ', len(selected_arcs), ' First selected arcs')
    print(cross, ' - ', len(selected_arcs_2), ' Second selected arcs')

    # Update the dictionaries
    cycle_dict.extend(temp_cycles)
    
    t1 = datetime.datetime.now()
    # Generate the paths for each cross
    temp_paths, path_idx \
        = generator.full_path_generation(cross, selected_arcs, selected_arcs_2, demand, path_idx)
    t2 = datetime.datetime.now()
    
    print(cross, ' - ', len(temp_paths), ' Paths. Time: ', t2 - t1)

    # Update the dictionaries
    path_dict.extend(temp_paths)
    
    # We add the cross back to the poulation
    points_set.add(cross)

t3 = datetime.datetime.now()
print(t3-t4)

#t2 = datetime.datetime.now()
## We add more arcs
#temp_arcs, temp_cycles, temp_paths, arc_idx, cycle_idx, path_idx \
#    = generator.trailer_arc_generation(points_set, points_names, demand, times, arc_idx, cycle_idx, path_idx)
#print('Número de TSR: ', len(temp_arcs))
#
#print(t2-t3)
#
## We update the dictionaries
#arc_list.update(temp_arcs)
#cycle_dict.update(temp_arcs)
#path_dict.update(temp_paths)
#
## we get the dictionary of time-space nodes (key - tuple (point, time))
## For now to make it easier the begining time is 19.00h or 0, and the end time is 10:00 or 54000s
## with an interval of 5min or 300s.
## With the full data set and this interval we will have a maximum of 24254 time-space nodes
#time_space_dict = {}
#time_space_dict = ts.create_full_diagram(points_set, 0, 54000, 300)