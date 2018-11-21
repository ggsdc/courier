import path as pa
import cycle as cy
import itinerary as it

def simple_path_generation(cross, points, times, distance, demand, idx):
    """
    Funtions to create paths of length N = 2

    Arguments
    ---------
    cross : int
        Code of the cross point that the paths have to go to.
    points : set
        Set of the rest of the points in the problem.
    times : dict
        Dictionary with the times between points
    distance : dict
        Dictionary with the distance between points
    demand : dict
        The demand dict that contains all the demand different dictionaries.
    idx : int

    Returns
    -------
        A list of instances of Paths.
    """

    # Initialize objects to be used
    paths = list()
    item = 0

    demand_dict = demand['baseDict']
    demand_origin_dict = demand['originDict']
    demand_destination_dict = demand['destinationDict']
    demand_parcels_for = demand['forDict']
    demand_parcels_from = demand['fromDict']

    # Time-window 6 hours for Madrid, 4 hours for the rest
    if cross == 280:
        timeWindow = 6
    else:
        timeWindow = 4

    # Main loop for the path generation.
    for pointA in points:
        
        # Gets the time back or continues to the next iteration.
        try:
            t1 = times[cross][pointA]
        except KeyError:
            continue

        # If the time is smaller than the timeWindow.
        if t1 > timeWindow:
            continue

       # Gets the demand generated in the point. Defaults to zero.  
        try:
            p1 = demand_origin_dict[pointA]
        except KeyError:
            p1 = 0
        
        # Gets the demand received by the point. Defaults to zero.
        try:
            p2 = demand_destination_dict[pointA]
        except KeyError:
            p2 = 0

        # In case both are zero we pass to the next iteration.
        if p1 == 0 and p2 == 0:
            continue
        
        # Gets the list of points that the point generates demand to.
        try:
            l1 = demand_parcels_for[pointA]
        except KeyError:
            l1 = list()
        
        # Gets the list of points that the point receives demand from.
        try:
            l2 = demand_parcels_from[pointA]
        except KeyError:
            l2 = list()
        
        # Gets the distance between the point and the cross-point.
        # If it not exists we pass to the next iteration.
        try:
            d1 = distance[pointA][cross]
        except KeyError:
            continue
        
        # We creae the base path with the base vehicle.
        paths.append(pa.Path(idx, pointA, cross, (cross, pointA), 1, points))
        paths[item].set_time(t1)
        paths[item].set_demand(p1,p2)
        paths[item].set_distance(d1)
        paths[item].set_points_generated(l1)
        paths[item].set_points_received(l2)
        idx = idx + 1
        item = item + 1

        # If the time is lower than 3/4 of the timeWindow then we use the truck vehicle.
        if t1 * 4/3 <= timeWindow:
            paths.append(pa.Path(idx, pointA, cross, (cross, pointA), 2, points))
            paths[item].set_time(t1 * 4/3)
            paths[item].set_demand(p1,p2)
            paths[item].set_distance(d1)
            paths[item].set_points_generated(l1)
            paths[item].set_points_received(l2)
            idx = idx + 1
            item = item + 1

        # If the time is lower that 3 hours we can use the trailers
        if t1 * 4/3 <= 4:
            paths.append(pa.Path(idx, pointA, cross, (cross, pointA), 3, points))
            paths[item].set_time(t1 * 4/3)
            paths[item].set_demand(p1,p2)
            paths[item].set_distance(d1)
            paths[item].set_points_generated(l1)
            paths[item].set_points_received(l2)
            idx = idx + 1
            item = item + 1
    
    # It returns the list of paths and the current free index for the paths.
    return paths, idx

def complex_path_generation(cross, cross_points, arcs, points, times, distance, idx):
    """"""

    arc_list = list()
    item = 0
    
    if cross == 280:
        timeWindow = 6
    else:
        timeWindow = 4

    for i in arcs:
        
        if i.origin in cross_points or i.vehicle >= 3:
            continue
        
        aux_arcs = [arc for arc in arcs if i != arc and i.vehicle == arc.vehicle]
        t1 = i.get_hours()
        d1 = i.get_distance()

        for j in aux_arcs:
                                    
            try:
                t2 = times[i.origin][j.origin]
            except KeyError:
                continue

            try:
                d2 = distance[i.origin][j.origin]
            except KeyError:
                continue

            t3 = j.get_hours()

            if t1 > t3:
                continue

            if i.vehicle==2:
                t2 = t2 * 4/3
                        
            if (t1 + t2 + 0.25 <= timeWindow):
                arc_list.append(pa.Path(idx, j.origin, cross, (cross, i.origin, j.origin), i.vehicle, points))
                
                p1, p2 = i.get_demand()
                p3, p4 = j.get_demand()

                arc_list[item].set_time(t1 + t2 + 0.25)
                arc_list[item].set_demand(p1 + p3, p2 + p4)
                arc_list[item].set_distance(d1 + d2)

                l1 = list(set(i.get_pointsGenerated() + j.get_pointsGenerated()))
                l2 = list(set(i.get_pointsReceived() + j.get_pointsReceived()))

                arc_list[item].set_points_generated(l1)
                arc_list[item].set_points_received(l2)

                idx = idx + 1
                item = item + 1

    return arc_list, idx

def cycle_generation(cross, arcs, points, idx):
    """"""

    cycles = list()
    arcs_aux = list()
    arcs_aux_2 = list()
    item = 0
    
    for i in arcs:
        
        aux_arcs = [arc for arc in arcs if i.origin == arc.origin and i.vehicle == arc.vehicle]
        d1 = i.get_generated()
        aux = item

        for j in aux_arcs:
            
            d2 = j.get_received()
            
            if d1 <= 1000 and d2 <= 1000 and i.vehicle == 2:
                continue
            elif d1 <= 1475 and d2 <= 1475 and i.vehicle == 3:
                continue

            points_order = ()
                    
            if len(i.points)==3:
                points_order = points_order + (i.points[2],)
            
            points_order = points_order + (i.points[1], i.destination, j.points[1])

            if len(j.points)==3:
                points_order = points_order + (j.points[2],)

            cycles.append(cy.Cycle(idx, i.origin, cross, points_order, i.vehicle, points))
            cycles[item].set_demand(d1, d2)
            
            if not j in arcs_aux_2:
                arcs_aux_2.append(j)
                       
            idx = idx + 1
            item = item + 1
        
        if aux < item:
            arcs_aux.append(i)

    return cycles, arcs_aux, arcs_aux_2, idx

def itinerary_generation(cross, first_arcs, second_arcs, idx):
    """"""

    itineraries = list()

    for i in first_arcs:
        l1 = i.get_pointsGenerated()
        
        second_arcs_aux = [second for second in second_arcs if i!= second and i.origin != second.origin]

        for j in second_arcs_aux:

            l2 = list(j.points)
            l2.remove(j.destination)

            if not any(x in l1 for x in l2):
                continue
              
            points_order = ()

            if len(i.points)==3:
                    points_order = points_order + (i.points[2],)
                
            points_order = points_order + (i.points[1], i.destination, j.points[1])

            if len(j.points)==3:
                points_order = points_order + (j.points[2],)

            itineraries.append(it.Itinerary(idx, points_order[0], cross, points_order[-1], points_order, i.vehicle, j.vehicle))
            idx = idx + 1
    
    return itineraries, idx

def trailer_arc_generation(points, names, demand, times, arc_idx, cycle_idx, path_idx):
    """"""

    arcs = {}
    cycles = {}
    paths = {}

    for origin in points:
        for destination in points:
            
            if origin == destination:
                continue
            
            aux1 = times[(times.originCode==origin) & (times.destinationCode==destination)]
            aux2 = demand[(demand.originCode==origin) & (demand.destinationCode==destination)]

            if len(aux1)==0 or len(aux2) == 0:
                continue

            t1 = aux1.iloc[0]['Hours']
            d1 = aux2.iloc[0]['parcels']

            if t1 * 4/3 <= 8 and d1 > 1475:
                
                arcs[arc_idx] = ca.Complex_arc(arc_idx, origin, destination, (origin, destination), 4)
                arcs[arc_idx].set_name(names)
                arcs[arc_idx].set_time(t1 * 4/3)

                cycles[cycle_idx] = cy.Cycle(cycle_idx, origin, destination, (origin, destination), 4)
                cycles[cycle_idx].set_demand(d1, 0)
                
                paths[path_idx] = pa.Path(path_idx, origin, 0, destination, (origin, destination), 4, 0)
                                
                arc_idx = arc_idx + 1
                cycle_idx = cycle_idx + 1
                path_idx = path_idx + 1

    return arcs, cycles, paths, arc_idx, cycle_idx, path_idx