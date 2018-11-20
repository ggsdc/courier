# & c:/Users/bob_guille/Desktop/proyectos/i-d-courier/src/venv/Scripts/python.exe
import pandas as pd
import datetime as datetime
import read_data as rd
import path as pa
import cycle as cy
import itinerary as it
import set_generation as sg
import time_space as ts

# Routes to the data files. This has to be changed.
vehicles_path = "..\\data\\vehicles.data"
points_path = "..\\data\\points15.data"
demand_path = "..\\data\\demand15.data"

t1 = datetime.datetime.now()

# Loading of the data files.
vehicles_data, points_data, demand_data = rd.read_data(vehicles_path, points_path, demand_path)

points_dict = rd.process_points(points_data) 

demand_dicts, times_dict, distance_dict = rd.process_demand(demand_data)

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

# paths dictionaries
path_list = list()
temp_paths = list()
aux_list = list()
aux_list_2 = list()
selected_paths = list()
selected_paths_2 = list()

# Cycles dictionaries - Main
cycle_dict = list()
temp_cycles = list()

# Paths dictionaries - Main
itinerary_list = list()
temp_itinerary = list()

# Indexes for the dicts
path_idx = 1
cycle_idx = 1
path_idx = 1

t4 = datetime.datetime.now()

# Main generation loop
for cross in cross_docking_points:

    # Remove the cross from the population
    points_set.remove(cross)

    t1 = datetime.datetime.now()
    # Get the simple paths
    temp_paths, path_idx \
        = sg.simple_path_generation(cross, points_dict, times_dict, distance_dict, demand_dicts, path_idx)
    t2 = datetime.datetime.now()

    print(cross, ' - ', len(temp_paths), ' Simple paths. Time: ', t2 - t1)
        
    # Update dictionaries
    path_list.extend(temp_paths)
    aux_list = temp_paths

    t1 = datetime.datetime.now()
    # Get complex paths
    temp_paths, path_idx \
        = sg.complex_path_generation(cross, cross_docking_points, temp_paths, points_dict, times_dict, distance_dict, path_idx)
    t2 = datetime.datetime.now()

    print(cross, ' - ', len(temp_paths), ' Complex paths. Time: ', t2 - t1)

    # Update the dictionaries
    path_list.extend(temp_paths)
    aux_list.extend(temp_paths)

    t1 = datetime.datetime.now()
    # Generate the cycles for each cross
    temp_cycles, selected_paths, selected_paths_2, cycle_idx \
        = sg.cycle_generation(cross, aux_list, points_dict, cycle_idx)
    t2 = datetime.datetime.now()

    print(cross, ' - ', len(temp_cycles), ' Cycles. Time: ', t2 - t1)
    print(cross, ' - ', len(selected_paths), ' First selected paths')
    print(cross, ' - ', len(selected_paths_2), ' Second selected paths')

    # Update the dictionaries
    cycle_dict.extend(temp_cycles)

    t1 = datetime.datetime.now()
    # Generate the paths for each cross
    temp_itinerary, path_idx \
        = sg.itinerary_generation(cross, selected_paths, selected_paths_2, path_idx)
    t2 = datetime.datetime.now()

    print(cross, ' - ', len(temp_itinerary), ' Itineraries. Time: ', t2 - t1)

    # Update the dictionaries
    itinerary_list.extend(temp_itinerary)

    # We add the cross back to the poulation
    points_set.add(cross)

t3 = datetime.datetime.now()
print(t3-t4)

# We get the dictionary of time-space nodes (key - tuple (point, time))
# For now to make it easier the begining time is 19.00h or 0, and the end time is 10:00 or 54000s
# with an interval of 5min or 300s.
# With the full data set and this interval we will have a maximum of 24254 time-space nodes
time_space_dict = dict()
begin = datetime.datetime.combine(datetime.date.today(), datetime.time(17,0))
end = begin + datetime.timedelta(hours=17)
time_space_dict = ts.create_full_diagram(points_set, begin, end, 5)