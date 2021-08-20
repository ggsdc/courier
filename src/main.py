# & c:/Users/bob_guille/Desktop/proyectos/i-d-courier/src/venv/Scripts/python.exe
import datetime as datetime
from typing import List
from sys import getsizeof

import pandas as pd
import pulp as lp

import read_data as rd
import set_generation as sg
import translate_solver as tr

# Routes to the data files. This has to be changed.
vehicles_path = "..\\data\\vehicles.data"
points_path = "..\\data\\pointsFull.data"
demand_path = "..\\data\\demandFull.data"

conflict_points = [77, 438, 719]

t1 = datetime.datetime.now()

# Loading of the data files.
vehicles_data, points_data, demand_data = rd.read_data(vehicles_path, points_path, demand_path)

points_dict = rd.process_points(points_data)
vehicles_dict = dict()
vehicles_dict['1'] = dict()
vehicles_dict['2'] = dict()
vehicles_dict['3'] = dict()
vehicles_dict['1']['capacity'] = 500
vehicles_dict['2']['capacity'] = 1475
vehicles_dict['3']['capacity'] = 2650
vehicles_dict['1']['cost'] = 0.28
vehicles_dict['2']['cost'] = 0.57
vehicles_dict['3']['cost'] = 0.76

demand_dicts, times_dict, distance_dict = rd.process_demand(demand_data)

t2 = datetime.datetime.now()
print('Time to read everything: ', t2-t1)

# Set of points
points_set = set(points_data['code'])
# cross_docking_points = [280, 231]
cross_docking_points = [231, 500, 930, 492, 35, 12, 280]

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
cycle_list = list()
temp_cycles = list()

# Arcs dictionaties - Main
arcs = dict()
aux_arcs = dict()

# Paths dictionaries - Main
itinerary_list = list()
temp_itinerary = list()

# Indexes for the dicts
path_idx = 1
cycle_idx = 1
itinerary_idx = 1

# Parameters
p_phi = list()
p_phi_aux = list()
p01_flow_domain = dict()
p01_flow_domain_aux = dict()

t3 = datetime.datetime.now()
print('Time to initialize: ', t3-t2)

# Set generation
# Commodities set
commodities = sg.commodities_generation(demand_dicts)
print(datetime.datetime.now(), 'Commodities OK')

# Main generation loop
for cross in cross_docking_points:

    # Remove the cross from the population
    points_set.remove(cross)

    t1 = datetime.datetime.now()
    # Get the simple paths
    temp_paths, path_idx \
        = sg.simple_path_generation(cross, points_dict, times_dict, distance_dict, demand_dicts, path_idx)
    t2 = datetime.datetime.now()

    # Update list
    path_list.extend(temp_paths)
    aux_list = temp_paths

    t1 = datetime.datetime.now()
    # Get complex paths
    temp_paths, path_idx \
        = sg.complex_path_generation(cross, cross_docking_points, temp_paths,
                                     points_dict, times_dict, distance_dict, path_idx)
    t2 = datetime.datetime.now()

    # Update the lists
    path_list.extend(temp_paths)
    aux_list.extend(temp_paths)

    t1 = datetime.datetime.now()
    # Generate the cycles for each cross
    temp_cycles, selected_paths, selected_paths_2, cycle_idx \
        = sg.cycle_generation(cross, aux_list, points_dict, cycle_idx)
    t2 = datetime.datetime.now()

    aux_arcs = sg.arcs_generation(arcs, temp_cycles, points_dict)
    arcs.update(aux_arcs)

    # print(cross, ' - ', len(temp_cycles), ' Cycles. Time: ', t2 - t1)
    # print(cross, ' - ', len(selected_paths), ' First selected paths')
    # print(cross, ' - ', len(selected_paths_2), ' Second selected paths')

    # Update the dictionaries
    cycle_list.extend(temp_cycles)

    t1 = datetime.datetime.now()
    # Generate the paths for each cross
    temp_itinerary, p_phi_aux, p01_flow_domain_aux, itinerary_idx \
        = sg.itinerary_generation(cross, selected_paths, selected_paths_2, commodities, arcs, points_dict, itinerary_idx)
    t2 = datetime.datetime.now()
    p_phi.extend(p_phi_aux)
    p01_flow_domain.update(p01_flow_domain_aux)
    # print(cross, ' - ', len(temp_itinerary), ' Itineraries. Time: ', t2 - t1)

    # Update the dictionaries
    itinerary_list.extend(temp_itinerary)

    # We add the cross back to the population
    points_set.add(cross)
    print(cross, ': {cycles: ', len(temp_cycles), ', itineraries: ', len(temp_itinerary),', arcs: ', len(aux_arcs) ,'}')
    print('Size of cycles: ',getsizeof(cycle_list)/1024/1024 , '. Size of itineraries: ',getsizeof(itinerary_list)/1024/1024)
    del(temp_paths, temp_cycles, temp_itinerary, p_phi_aux, p01_flow_domain_aux, aux_arcs, selected_paths,
        selected_paths_2)

t4 = datetime.datetime.now()
print('Time to generate paths, cycles and itineraries: ', t4-t3)

arcs_list = list()
for a in arcs:
    arcs_list.append(a)
print(datetime.datetime.now(), 'Arcs OK')
# Parameter (phi) if commodity k in itinerary i uses arc a
# p_phi = pg.parameter_phi(commodities=commodities, itineraries=itinerary_list, arcs=arcs, points=points_dict)
# print(datetime.datetime.now(), 'Phi OK')
# print(len(p_phi))
# Parameter (omega) if itinerary i and cycle c share arc a
p_omega = dict()
for cy in cycle_list:
    aux_arcs = [arc for arc in cy.arcs_first if arc in arcs]

    for a in aux_arcs:
        p_omega[(cy, a, )] = 1

for cy in cycle_list:
    aux_arcs = [arc for arc in cy.arcs_second if arc in arcs ]

    for a in aux_arcs:
        p_omega[(cy, a, )] = 1
print(datetime.datetime.now(), 'Omega OK')
del(aux_arcs)

t5 = datetime.datetime.now()
print('Time to generate parameters and sets: ', t5-t4)
#
# Model
model = lp.LpProblem("Courier", lp.LpMinimize)

# Objective function
v_objective_function = lp.LpVariable(name='v_objective_function', lowBound=0, cat='Continuous')
v_number_vehicles = lp.LpVariable(name='v_number_vehicles', lowBound=0, cat='Continuous')

# Cycle variable - number of vehicles per cycle
v_vehicles_cycle = lp.LpVariable.dicts("Vehicles", cycle_list, lowBound=0, cat="Integer")

# Flow variable - amount of commodity k moved in itinerary i
v_flow_itinerary = lp.LpVariable.dicts("Flow", ((k, i) for k in commodities for i in itinerary_list if (k, i, ) in p01_flow_domain.keys()), lowBound=0, cat="Continuous")

t1 = datetime.datetime.now()
test = 0
for k in commodities:
    for i in itinerary_list:
        if (k, i, ) in p01_flow_domain:
            test +=1
print(datetime.datetime.now()-t1)


print(datetime.datetime.now(), 'Variables OK')
model += lp.lpSum(v_objective_function), 'OF'

# RQ00 - Objective function
RQ00_constraints = 1
model += lp.lpSum(v_vehicles_cycle[c] * c.length * vehicles_dict[str(c.vehicle)]['cost'] for c in cycle_list) == v_objective_function, 'RQ00.1'
model += lp.lpSum(v_vehicles_cycle[c] for c in cycle_list) == v_number_vehicles, 'RQ00.2'
print(datetime.datetime.now(), 'RQ00 OK')
# RQ01 - Transport constraint
RQ01_constraints = 1
for a in arcs_list:

    aux_itineraries = [it for it in itinerary_list if a in it.arcs]

    model += lp.lpSum(v_flow_itinerary[k, i] * p_phi[(k,i,a,)] for k in commodities for i in aux_itineraries\
                      if (k, i, ) in p01_flow_domain.keys() and (k, i, a, ) in p_phi.keys())\
             <= lp.lpSum(v_vehicles_cycle[c] * vehicles_dict[str(c.vehicle)]['capacity'] * p_omega[(c, a, )] for c in cycle_list if (c, a, ) in p_omega.keys()),\
             'RQ01.' + str(RQ01_constraints)
    RQ01_constraints += 1
print(datetime.datetime.now(), 'RQ01 OK')

# RQ02 - Commodities are met
RQ02_constraints = 1
for k in commodities:
    model += lp.lpSum(v_flow_itinerary[k, i] for i in itinerary_list if (k, i, ) in p01_flow_domain.keys())\
             == k.value, 'RQ02.' + str(RQ02_constraints)
    RQ02_constraints += 1

t6 = datetime.datetime.now()
print('Time to build the model: ', t6-t5)

model.solve(lp.PULP_CBC_CMD(fracGap=0.1, msg=0))
print(model.status)
t7 = datetime.datetime.now()
print('Time to solve the model: ', t7-t6)

var_values = dict()
if model.status == 1:
    for p in model.variables():
        var_values[str(p)] = p.varValue

var_names_index = dict()
var_names_index['v_objective_function'] = (0, 'float', 1)
var_names_index['v_number_vehicles'] = (0, 'float', 1)
var_names_index['Vehicles_Cycle'] = (1, 'integer', 1)
var_names_index['Flow'] = (2, 'string', 'float', 1)

solution = tr.translate_solver(var_names_index, var_values, cycle_list, itinerary_list, commodities)

out1 = pd.DataFrame.from_dict(solution['v_objective_function'])
out2 = pd.DataFrame.from_dict(solution['v_number_vehicles'])
out3 = pd.DataFrame.from_dict(solution['Vehicles_Cycle'])
# out4 = pd.DataFrame.from_dict(solution['Flow_Itinerary'])
print('Total cost: ', out1)
print('Number of vehicles: ', out2)
out1.to_csv(path_or_buf = '..\\data\\FO.csv', sep = ';', index = False, encoding = 'utf-8')
out3.to_csv(path_or_buf = '..\\data\\vehicles.csv', sep = ';', index = False, encoding = 'utf-8')
# out4.to_csv(path_or_buf = '..\\data\\flow.csv', sep = ';', index = False, encoding = 'utf-8')

# file = open("rest.txt", "w")
# for c in model.constraints:
#     if c.__contains__('RQ01'):
#         file.write(str(model.constraints[c]))
#         file.write('\n')
# file.close()
#
# for v in var_values:
#     if var_values[v]>0:
#         print(v, var_values[v])
#
#
