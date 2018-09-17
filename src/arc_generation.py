import complex_arc as ca
import cycle as cy
import path as pa

@profile
def simple_arc_generation(cross, points, names, times, demand, idx):
    """"""

    arcs = list()
    item = 0

    demandOr \
        = demand.groupby('originCode', as_index = False).agg({"parcels": "sum"})

    demandDest \
        = demand.groupby('destinationCode', as_index = False).agg({"parcels": "sum"})

    if cross == 280:
        timeWindow = 6
    else:
        timeWindow = 4

    for pointA in points:
        try:
            t1 = times[cross][pointA]
        except KeyError:
            continue

        if t1 > timeWindow:
            continue
        
        d1 = 0
        d2 = 0
        aux = demandOr[(demandOr.originCode == pointA)]
        aux2 = demandDest[(demandDest.destinationCode == pointA)]

        if len(aux) > 0:
            d1 = aux.iloc[0]['parcels']

        if len(aux2) > 0:
            d2 = aux2.iloc[0]['parcels']

        if t1 <= timeWindow:
            arcs.append(ca.Complex_arc(idx, pointA, cross, (cross, pointA), 1, names))
            arcs[item].set_time(t1)
            arcs[item].set_demand(d1,d2)
            arcs[item].set_points_generated(demand[(demand.originCode == pointA)]['destinationCode'].tolist())
            arcs[item].set_points_received(demand[(demand.destinationCode == pointA)]['originCode'].tolist())
            idx = idx + 1
            item = item + 1

        if t1 * 4/3 <= timeWindow:
            arcs.append(ca.Complex_arc(idx, pointA, cross, (cross, pointA), 2, names))
            arcs[item].set_time(t1 * 4/3)
            arcs[item].set_demand(d1,d2)
            arcs[item].set_points_generated(demand[(demand.originCode == pointA)]['destinationCode'].tolist())
            arcs[item].set_points_received(demand[(demand.destinationCode == pointA)]['originCode'].tolist())
            idx = idx + 1
            item = item + 1

        if t1 * 4/3 <= 4:
            arcs.append(ca.Complex_arc(idx, pointA, cross, (cross, pointA), 3, names))
            arcs[item].set_time(t1 * 4/3)
            arcs[item].set_demand(d1,d2)
            arcs[item].set_points_generated(demand[(demand.originCode == pointA)]['destinationCode'].tolist())
            arcs[item].set_points_received(demand[(demand.destinationCode == pointA)]['originCode'].tolist())
            idx = idx + 1
            item = item + 1
    
    return arcs, idx

def complex_arc_genertation(cross, cross_points, arcs, names, times, idx):
    """"""

    arc_list = list()
    item = 0
    
    if cross == 280:
        timeWindow = 6
    else:
        timeWindow = 4

    for i in arcs:
        for j in arcs:
            
            if i == j or i.vehicle != j.vehicle or i.vehicle >= 3 or j.vehicle >= 3 or i.origin in cross_points:
                continue
                        
            t1 = i.get_hours()
            try:
                t2 = times[i.origin][j.origin]
            except KeyError:
                continue

            t3 = j.get_hours()

            if t1 > t3:
                continue

            if i.vehicle==2:
                t2 = t2 * 4/3
                        
            if (t1 + t2 + 0.25 <= timeWindow):
                arc_list.append(ca.Complex_arc(idx, j.origin, cross, (cross, i.origin, j.origin), i.vehicle, names))
                
                d1, d2 = i.get_demand()
                d3, d4 = j.get_demand()

                arc_list[item].set_time(t1 + t2 + 0.25)
                arc_list[item].set_demand(d1 + d3, d2 + d4)

                l1 = list()
                l2 = list()

                l1.extend(i.get_pointsGenerated())
                l2.extend(i.get_pointsReceived())

                l1.extend(x for x in j.get_pointsGenerated() if x not in l1)
                l2.extend(x for x in j.get_pointsReceived() if x not in l2)

                arc_list[item].set_points_generated(l1)
                arc_list[item].set_points_received(l2)

                #arc_list[item].set_points_generated(list(set(l1)))
                #arc_list[item].set_points_received(list(set(l2)))
                                    
                idx = idx + 1
                item = item + 1

    return arc_list, idx

def cycle_generation(cross, arcs, demandOr, demandDest, idx):
    """"""

    cycles = list()
    arcs_aux = list()
    arcs_aux_2 = list()
    item = 0

    for i in arcs:
        for j in arcs:

            if (i.origin != j.origin or i.vehicle != j.vehicle or i.destination != j.destination):
                continue
            
            d1 = i.get_generated()
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

            cycles.append(cy.Cycle(idx, i.origin, cross, points_order, i.vehicle))
            cycles[item].set_demand(d1, d2)

            try:
                aux_idx = arcs_aux.index(i)
            except ValueError:
                arcs_aux.append(i)

            try:
                aux_id = arcs_aux_2.index(j)
            except ValueError:
                arcs_aux_2.append(j)
            
            idx = idx + 1
            item = item + 1

    return cycles, arcs_aux, arcs_aux_2, idx

def full_path_generation(cross, first_arcs, second_arcs, demand, idx):
    """"""

    paths = list()

    for i in first_arcs:
        l1 = i.get_pointsGenerated()
        
        for j in second_arcs:

            if i==j or i.origin==j.origin:
                continue

            l2 = list(j.points)
            l2.remove(j.destination)

            if not set(l2)<set(l1):
                continue
              
            points_order = ()

            if len(i.points)==3:
                    points_order = points_order + (i.points[2],)
                
            points_order = points_order + (i.points[1], i.destination, j.points[1])

            if len(j.points)==3:
                points_order = points_order + (j.points[2],)

            paths.append(pa.Path(idx, points_order[0], cross, points_order[-1], points_order, i.vehicle, j.vehicle))
            idx = idx + 1
    
    return paths, idx

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