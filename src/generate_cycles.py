def create_single_cycles(id, points_set, cross_docking_points, distances):

    cycle_dict = {}
    cycle_cross_dict = {}

    for cross in cross_docking_points:
        
        print('Cruce: ', cross)
        points_set.remove(cross)
        
        for origin in points_set:
            
            aux_distance = distances[(distances.originCode == cross) & (distances.destinationCode == origin)]
            if aux_distance.iloc[0]['Hours'] <= 6:
                cycle_dict[id] = (origin, cross, origin)
                cycle_cross_dict[id] = cross
                id = id + 1

        points_set.add(cross)
    
    return cycle_dict, cycle_cross_dict, id

def create_cycle_with_one_stop(id, points_set, cross_docking_points, times):

    cycle_dict = {}
    cycle_cross_dict = {}

    for cross in cross_docking_points:

        print('Cruce: ', cross)
        points_set.remove(cross)
        aux_set = set(points_set)
        times_red = times

        while len(aux_set):

            stop = times_red.loc[times_red[times_red.originCode == cross]['Hours'].idxmin()]['destinationCode']
            time_aux = times_red.loc[times_red[times_red.originCode == cross]['Hours'].idxmin()]['Hours']
            times_aux = times_red[(times_red.originCode == stop) & (times_red.Hours + time_aux + 0.25 <= 6)]
            candidates = set(times_aux['destinationCode'])
            
            for origin in candidates:
                cycle_dict[id] = (origin, stop, cross, stop, origin)
                cycle_cross_dict[id] = cross
                id = id + 1
                cycle_dict[id] = (origin, stop, cross, origin)
                cycle_cross_dict[id] = cross
                id = id + 1
                cycle_dict[id] = (origin, cross, stop, origin)
                cycle_cross_dict[id] = cross
                id = id + 1

            times_red = times_red[(times_red.originCode != stop) & (times_red.destinationCode != stop)]
            
            aux_set.remove(stop)

        points_set.add(cross)

    return cycle_dict, cycle_cross_dict, id
