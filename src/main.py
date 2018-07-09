# & c:/Users/bob_guille/Desktop/proyectos/i-d-courier/src/env/Scripts/python.exe
import pandas as pd
import datetime as datetime
import class_creation as cc
import arc_generation as generator

# Routes to the data files. This has to be changed.
vehicles_path = "..\\data\\vehicles.data"
points_path = "..\\data\\points15.data"
demand_path = "..\\data\\demand15.data"

t1 = datetime.datetime.now()

# Loading of the data files.
vehicles_data = pd.read_csv(vehicles_path, sep = '\t')
points_data = pd.read_csv(points_path, sep = '\t')
demand_data = pd.read_csv(demand_path, sep = '\t')

demand_origin \
    = demand_data.groupby('originCode', as_index = False).agg({"parcels": "sum"})

demand_destination \
    = demand_data.groupby('destinationCode', as_index = False).agg({"parcels": "sum"})

times = demand_data[['originCode', 'destinationCode', 'Hours']]
distance = demand_data[['originCode', 'destinationCode', 'Kilometers']]
demand = demand_data[['originCode', 'destinationCode', 'parcels']]
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
arc_dict = {}
temp_arcs = {}
aux_dict = {}
selected_arcs = {}
selected_arcs_2 = {}

# Cycles dictionaries - Main
cycle_dict = {}
temp_cycles = {}

# Paths dictionaries - Main
path_dict = {}
temp_paths = {}

# Indexes for the dicts
arc_idx = 1
cycle_idx = 1
path_idx = 1

t2 = datetime.datetime.now()

# Main generation loop
for cross in cross_docking_points:

    # Remove the cross from the population
    points_set.remove(cross)

    # Get the simple arcs
    temp_arcs, arc_idx \
        = generator.simple_arc_generation(cross, points_set, times, arc_idx)
    
    print(cross, ' - ', len(temp_arcs), ' Simple arcs')
        
    # Update dictionaries
    arc_dict.update(temp_arcs)
    aux_dict = temp_arcs
    
    # Get complex arcs
    temp_arcs, arc_idx \
        = generator.complex_arc_genertation(cross, temp_arcs, times, arc_idx)
    
    print(cross, ' - ', len(temp_arcs), ' Complex arcs')
    
    # Update the dictionaries
    arc_dict.update(temp_arcs)
    aux_dict.update(temp_arcs)
    
    # Generate the cycles for each cross
    temp_cycles, selected_arcs, selected_arcs_2, cycle_idx \
        = generator.cycle_generation(cross, aux_dict, demand_origin,\
            demand_destination, cycle_idx)
    
    print(cross, ' - ', len(temp_cycles), ' Cycles')
    print(cross, ' - ', len(selected_arcs), ' First selected arcs')
    print(cross, ' - ', len(selected_arcs_2), ' Second selected arcs')

    # Update the dictionaries
    cycle_dict.update(temp_cycles)
    
    # Generate the paths for each cross
    temp_paths, path_idx \
        = generator.full_path_generation(cross, selected_arcs, selected_arcs_2, demand, path_idx)
    print(cross, ' - ', len(temp_paths), ' Paths')

    # Update the dictionaries
    path_dict.update(temp_paths)
    
    # We add the cross back to the poulation
    points_set.add(cross)


t3 = datetime.datetime.now()
print(t3-t2)

t2 = datetime.datetime.now()
# We add more arcs
temp_arcs, temp_cycles, temp_paths, arc_idx, cycle_idx, path_idx \
    = generator.trailer_arc_generation(points_set, demand, times, arc_idx, cycle_idx, path_idx)
print('Número de TSR: ', len(temp_arcs))

print(t2-t3)

# We update the dictionaries
arc_dict.update(temp_arcs)
cycle_dict.update(temp_arcs)
path_dict.update(temp_paths)