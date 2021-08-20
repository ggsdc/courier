import datetime
from typing import Dict, List
import commodity as cm
import cycle as cy
import itinerary as it
from path import Path
import parameter_generation as pg


# @profile
def simple_path_generation(cross: int, points: Dict, times: Dict, distance: Dict, demand: Dict, idx: int):
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
        A list of instances of Paths and the next available code (updated idx).
    """
    # Initialize objects to be used
    paths = list()
    item = 0

    # unpack the demand dicts
    # demand_dict = demand['baseDict']
    demand_origin_dict = demand['originDict']
    demand_destination_dict = demand['destinationDict']
    demand_parcels_for = demand['forDict']
    demand_parcels_from = demand['fromDict']

    # Time-window 6.228 hours for Madrid, 4 hours for the rest
    if cross == 280:
        time_window = 6.228
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

        # Gets the distance between the point and the cross-point.
        # If it not exists we pass to the next iteration.
        try:
            d1 = distance[pointA][cross]
        except KeyError:
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

        # We create the base path with the base vehicle.
        path = Path(idx, pointA, cross, (cross, pointA), 1, points)
        paths.append(path)
        paths[item].set_time(t1)
        paths[item].set_demand(p1, p2)
        paths[item].set_distance(d1)
        paths[item].set_points_generated(l1)
        paths[item].set_points_received(l2)
        idx = idx + 1
        item = item + 1

        # If the time is lower than 3/4 of the timeWindow then we use the truck vehicle.
        if t1 * 4 / 3 <= time_window:
            path = Path(idx, pointA, cross, (cross, pointA), 2, points)
            paths.append(path)
            paths[item].set_time(t1 * 4 / 3)
            paths[item].set_demand(p1, p2)
            paths[item].set_distance(d1)
            paths[item].set_points_generated(l1)
            paths[item].set_points_received(l2)
            idx = idx + 1
            item = item + 1

        # If the time is lower that 4 hours we can use the trailers
        if t1 * 4 / 3 <= 4:
            path = Path(idx, pointA, cross, (cross, pointA), 3, points)
            paths.append(path)
            paths[item].set_time(t1 * 4 / 3)
            paths[item].set_demand(p1, p2)
            paths[item].set_distance(d1)
            paths[item].set_points_generated(l1)
            paths[item].set_points_received(l2)
            idx = idx + 1
            item = item + 1

    # It returns the list of paths and the current free index for the paths.
    return paths, idx


# @profile
def complex_path_generation(cross: int, cross_points: List[int], paths: List, points: Dict, times: Dict,
                            distance: Dict, idx: int):
    """
    Function to create paths of length N = 3

    Arguments
    ---------
    cross : int
        Code of the cross point the paths are being generated for.
    cross_points : list
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
        time_window = 5.5
    else:
        time_window = 4

    # Iterate over the already generated arcs
    for i in paths:

        # If the path begins in a cross_point or the vehicle is a trailer continue to the nex iteration.
        if i.origin in cross_points or i.vehicle >= 3:
            continue

        # Gets the paths that are not the same path and share the same vehicle.
        aux_paths = [path for path in paths if i != path and i.vehicle == path.vehicle]

        # Gets the origin, vehicle, hours and distance of the first path.
        origin_i = i.origin
        vehicle_i = i.vehicle
        t1 = i.get_hours()
        d1 = i.get_distance()

        # Iterate over filtered paths.
        for j in aux_paths:

            origin_j = j.origin
            # Gets the time between origin of the paths or iterates over.                 
            try:
                t2 = times[origin_i][origin_j]
            except KeyError:
                continue

            # Gets the distance between origin of the paths or iterates over.
            try:
                d2 = distance[origin_i][origin_j]
            except KeyError:
                continue

            # Gets the hours of the second path.
            t3 = j.get_hours()

            # If the time of the length of the first path
            if t1 > t3:
                continue

            # If the vehicle of the paths is a truck it gets the length updated.  
            # if vehicle_i == 2:
            #     t2 = t2 * 4/3

            # If the duration of the composite path is less than the timeWindow then the path gets created.
            if t1 + t2 + 0.25 <= time_window:
                # The path is created
                path = Path(idx, origin_j, cross, (cross, origin_i, origin_j), vehicle_i, points)
                path_list.append(path)

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


# @profile
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

            cycle = cy.Cycle(idx, i.origin, cross, points_order, i, j, i.vehicle, points)
            cycles.append(cycle)
            cycles[item].set_demand(d1, d2)
            cycles[item].set_length(i.get_distance(), j.get_distance())

            if j not in arcs_aux_2:
                arcs_aux_2.append(j)

            idx = idx + 1
            item = item + 1

        if aux < item:
            arcs_aux.append(i)

    return cycles, arcs_aux, arcs_aux_2, idx


# @profile
def itinerary_generation(cross, first_paths, second_paths, commodities, arcs, points, idx):
    # TODO: revisar la lógica de las commodities para la creación de itinerarios
    # debería haber algún apquete de alguno de los puntos del primer camino a alguno de los puntos del segundo camino.
    """
    Arguments
    ---------
    cross : int
    first_paths : list
    second_paths : list
    points : dict
    idx : int

    Returns
    -------
    """

    itineraries = list()
    p_phi = list()
    p01_domain = dict()
    count = 0
    percentage = 25

    for i in first_paths:
        l1 = i.get_points_generated()

        second_arcs_aux = [second for second in second_paths if i != second and i.origin != second.origin]
        commodities_aux = [k for k in commodities if k.origin in i.points]

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

            itinerary = it.Itinerary(idx, points_order[0], cross, points_order[-1], points_order,
                                     i.points[::-1], i, i.vehicle, j.points, j, j.vehicle, points)

            itineraries.append(itinerary)
            idx = idx + 1

            aux_1, aux_2 = pg.parameter_phi(commodities_aux, itinerary, arcs, points)

            p_phi.extend(aux_1)
            p01_domain.update(aux_2)

        count += 1
        if count / len(first_paths) * 100 >= percentage:
            print(datetime.datetime.now(), cross, ' - ', percentage, '% of iterations for itineraries complete')
            percentage = percentage + 25

    return itineraries, p_phi, p01_domain, idx


# @profile
def arcs_generation(arcs, cycles, points):
    aux = dict()
    key = ''
    for cy in cycles:
        for p in range(0, len(cy.points)):
            try:
                key = (str(points[cy.points[p]]), str(points[cy.points[p + 1]]), cy.vehicle,)
            except IndexError:
                continue

            try:
                a = arcs[key]
                a = aux[key]
                continue
            except KeyError:
                aux[key] = dict()
                aux[key]['origin'] = points[cy.points[p]]
                aux[key]['destination'] = points[cy.points[p + 1]]
                aux[key]['vehicle'] = cy.vehicle

    return aux


# @profile
def commodities_generation(demand: Dict):
    commodities = list()
    for i in demand['baseDict']:
        for j in demand['baseDict'][i]:
            commodity = cm.Commodity(i, j, demand['baseDict'][i][j])
            commodities.append(commodity)

    return commodities
