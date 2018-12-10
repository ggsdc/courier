import path as pa
import cycle as cy
import itinerary as it


def simple_path_generation(cross, points, times, distance, demand, idx):
    """
    Function to create paths of length N = 2

    Arguments
    ---------
    cross : int
        Code of the cross point that the paths have to go to.
    points : dict
        Dictionary of the points with the names
    times : dict
        Dictionary with the times between points
    distance : dict
        Dictionary with the distance between points
    demand : dict
        The demand dict that contains all the demand different dictionaries.
    idx : int

    Returns
    -------
        A list of instances of Paths and the next avalaible code (updated idx).
    """

    # Initialize objects to be used
    paths = list()
    item = 0

    # demand_dict = demand['baseDict']
    demand_origin_dict = demand['originDict']
    demand_destination_dict = demand['destinationDict']
    demand_parcels_for = demand['forDict']
    demand_parcels_from = demand['fromDict']

    # Time-window 6 hours for Madrid, 4 hours for the rest
    if cross == 280:
        time_window = 6
    else:
        time_window = 4

    # Main loop for the path generation.
    for pointA in points:
        
        # Gets the time back or continues to the next iteration.
        try:
            t1 = times[cross][pointA]
        except KeyError:
            continue

        # If the time is smaller than the timeWindow.
        if t1 > time_window:
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
        
        # We create the base path with the base vehicle.
        paths.append(pa.Path(idx, pointA, cross, (cross, pointA), 1, points))
        paths[item].set_time(t1)
        paths[item].set_demand(p1, p2)
        paths[item].set_distance(d1)
        paths[item].set_points_generated(l1)
        paths[item].set_points_received(l2)
        idx = idx + 1
        item = item + 1

        # If the time is lower than 3/4 of the timeWindow then we use the truck vehicle.
        if t1 * 4/3 <= time_window:
            paths.append(pa.Path(idx, pointA, cross, (cross, pointA), 2, points))
            paths[item].set_time(t1 * 4/3)
            paths[item].set_demand(p1, p2)
            paths[item].set_distance(d1)
            paths[item].set_points_generated(l1)
            paths[item].set_points_received(l2)
            idx = idx + 1
            item = item + 1

        # If the time is lower that 3 hours we can use the trailers
        if t1 * 4/3 <= 4:
            paths.append(pa.Path(idx, pointA, cross, (cross, pointA), 3, points))
            paths[item].set_time(t1 * 4/3)
            paths[item].set_demand(p1, p2)
            paths[item].set_distance(d1)
            paths[item].set_points_generated(l1)
            paths[item].set_points_received(l2)
            idx = idx + 1
            item = item + 1
    
    # It returns the list of paths and the current free index for the paths.
    return paths, idx


def complex_path_generation(cross, cross_points, paths, points, times, distance, idx):
    """
    Function to create paths of length N = 3

    Arguments
    ---------
    cross : int
        Code of the cross point the paths are being generated for.
    cross_points : set
        Set of all the cross points in the problem.
    paths : list
        List of already generated arcs for that cross point.
    points : dict
        Dictionary of the points with the names
    times : dict
        Dictionary of the times between points.
    distance : dict
        Dictionary of the distance between points.
    idx : int
        Free code for the path.

    Returns
    -------
        A list of the generated paths and the updated index (idx).
    """

    # Initialize the objects to be used.
    path_list = list()
    item = 0
    
    if cross == 280:
        time_window = 6
    else:
        time_window = 4

    # Iterate over the already generated arcs
    for i in paths:
        
        # If the path begins in a cross_point or the vehicle is a trailer continue to the nex iteration.
        if i.origin in cross_points or i.vehicle >= 3:
            continue
        
        # Gets the paths that are not the same path and share the same vehicle.
        aux_paths = [path for path in paths if i != path and i.vehicle == path.vehicle]
        
        # Gets the hours and distance of the first path.
        t1 = i.get_hours()
        d1 = i.get_distance()

        # Iterate over filtered paths.
        for j in aux_paths:

            # Gets the time between origin of the paths or iterates over.                 
            try:
                t2 = times[i.origin][j.origin]
            except KeyError:
                continue

            # Gets the distance between origin of the paths or iterates over.
            try:
                d2 = distance[i.origin][j.origin]
            except KeyError:
                continue

            # Gets the hours of the second path.
            t3 = j.get_hours()
            
            # If the time of the length of the first path
            if t1 > t3:
                continue

            # If the vehicle of the paths is a truck it gets the length updated.  
            if i.vehicle == 2:
                t2 = t2 * 4/3

            # If the duration of the composite path is less than the timeWindow then the path gets created.
            if t1 + t2 + 0.25 <= time_window:
                
                # The path is created
                path_list.append(pa.Path(idx, j.origin, cross, (cross, i.origin, j.origin), i.vehicle, points))
                
                # Gets the demand of both paths.
                p1, p2 = i.get_demand()
                p3, p4 = j.get_demand()

                # Sets the time, distance and demand of the path.
                path_list[item].set_time(t1 + t2 + 0.25)
                path_list[item].set_demand(p1 + p3, p2 + p4)
                path_list[item].set_distance(d1 + d2)

                # Creates the lists of the pointsGenerated and pointsReceived for the new path.
                l1 = list(set(i.get_points_generated() + j.get_points_generated()))
                l2 = list(set(i.get_points_received() + j.get_points_received()))

                # Sets the pointsGenerated and pointsReceived of the new path.
                path_list[item].set_points_generated(l1)
                path_list[item].set_points_received(l2)

                # Updates the index of the paths and the running item index.
                idx = idx + 1
                item = item + 1

    # Returns the created path list and the running index fort the paths.
    return path_list, idx


def cycle_generation(cross, arcs, points, idx):
    """

    Arguments
    ---------
    cross : int
    arcs : list
    points : dict
    idx : int

    Returns
    -------

    """

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
                    
            if len(i.points) == 3:
                points_order = points_order + (i.points[2],)
            
            points_order = points_order + (i.points[1], i.destination, j.points[1])

            if len(j.points) == 3:
                points_order = points_order + (j.points[2],)

            cycles.append(cy.Cycle(idx, i.origin, cross, points_order, i, j, i.vehicle, points))
            cycles[item].set_demand(d1, d2)
            cycles[item].set_length(i.get_distance(), j.get_distance())
            
            if j not in arcs_aux_2:
                arcs_aux_2.append(j)
                       
            idx = idx + 1
            item = item + 1
        
        if aux < item:
            arcs_aux.append(i)

    return cycles, arcs_aux, arcs_aux_2, idx


def itinerary_generation(cross, first_arcs, second_arcs, points, idx):
    """
    Arguments
    ---------
    cross : int
    first_arcs : list
    second_arcs : list
    points : dict
    idx : int

    Returns
    -------
    """

    itineraries = list()

    for i in first_arcs:
        l1 = i.get_points_generated()
        
        second_arcs_aux = [second for second in second_arcs if i != second and i.origin != second.origin]

        for j in second_arcs_aux:

            l2 = list(j.points)
            l2.remove(j.destination)

            if not any(x in l1 for x in l2):
                continue
              
            points_order = ()

            if len(i.points) == 3:
                    points_order = points_order + (i.points[2],)
                
            points_order = points_order + (i.points[1], i.destination, j.points[1])

            if len(j.points) == 3:
                points_order = points_order + (j.points[2],)

            itineraries.append(it.Itinerary(idx, points_order[0], cross, points_order[-1], points_order,
                                            i.points[::-1], i, i.vehicle, j.points, j, j.vehicle, points))
            idx = idx + 1
    
    return itineraries, idx


# def trailer_arc_generation(points, names, demand, times, arc_idx, cycle_idx, path_idx):
#     """"""
#
#     arcs = {}
#     cycles = {}
#     paths = {}
#
#     for origin in points:
#         for destination in points:
#
#             if origin == destination:
#                 continue
#
#             aux1 = times[(times.originCode == origin) & (times.destinationCode == destination)]
#             aux2 = demand[(demand.originCode == origin) & (demand.destinationCode == destination)]
#
#             if len(aux1) == 0 or len(aux2) == 0:
#                 continue
#
#             t1 = aux1.iloc[0]['Hours']
#             d1 = aux2.iloc[0]['parcels']
#
#             if t1 * 4/3 <= 8 and d1 > 1475:
#
#                 arcs[arc_idx] = ca.Complex_arc(arc_idx, origin, destination, (origin, destination), 4)
#                 arcs[arc_idx].set_name(names)
#                 arcs[arc_idx].set_time(t1 * 4/3)
#
#                 cycles[cycle_idx] = cy.Cycle(cycle_idx, origin, destination, (origin, destination), 4)
#                 cycles[cycle_idx].set_demand(d1, 0)
#
#                 paths[path_idx] = pa.Path(path_idx, origin, 0, destination, (origin, destination), 4, 0)
#
#                 arc_idx = arc_idx + 1
#                 cycle_idx = cycle_idx + 1
#                 path_idx = path_idx + 1
#
#     return arcs, cycles, paths, arc_idx, cycle_idx, path_idx
