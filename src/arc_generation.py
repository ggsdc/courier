import class_creation as cc

def simple_arc_generation(cross, points, names, times, idx):
    """"""

    arcs = {}
    
    if cross == 280:
        timeWindow = 6
    else:
        timeWindow = 4

    for pointA in points:
        aux = times[(times.originCode==cross) & (times.destinationCode==pointA)]
        if len(aux)==0:
            continue
        
        t1 = aux.iloc[0]['Hours']

        if t1 > timeWindow:
            continue

        if t1 <= timeWindow:
            arcs[idx] = cc.Complex_arc(idx, pointA, cross, (cross, pointA), 1)
            arcs[idx].set_name(names)
            arcs[idx].set_time(t1)
            idx = idx + 1

        if t1 * 4/3 <= timeWindow:
            arcs[idx] = cc.Complex_arc(idx, pointA, cross, (cross, pointA), 2)
            arcs[idx].set_name(names)
            arcs[idx].set_time(t1 * 4/3)
            idx = idx + 1

        if t1 * 4/3 <= 4:
            arcs[idx] = cc.Complex_arc(idx, pointA, cross, (cross, pointA), 3)
            arcs[idx].set_name(names)
            arcs[idx].set_time(t1 * 4/3)
            idx = idx + 1
    
    return arcs, idx

def complex_arc_genertation(cross, cross_points, arcs, names, times, idx):
    """"""

    arc_dict = {}
    
    if cross == 280:
        timeWindow = 6
    else:
        timeWindow = 4

    for i in arcs:
        for j in arcs:
            
            if i == j or arcs[i].vehicle != arcs[j].vehicle or arcs[i].vehicle >= 3 or arcs[j].vehicle >= 3 or arcs[i].origin in cross_points:
                continue
            
            aux1 = times[(times.originCode==cross) & (times.destinationCode==arcs[i].origin)]
            aux2 = times[(times.originCode==arcs[i].origin) & (times.destinationCode==arcs[j].origin)]
            aux3 = times[(times.originCode==cross) & (times.destinationCode==arcs[j].origin)]
            
            if (len(aux1)==0 or len(aux2)==0):
                continue

            t1 = aux1.iloc[0]['Hours']
            t2 = aux2.iloc[0]['Hours']
            t3 = aux3.iloc[0]['Hours']

            if t1 > t3:
                continue
                        
            if (t1 + t2 + 0.25 <= timeWindow and arcs[i].vehicle == 1) or ((t1 + t2) * 4/3 + 0.25 <= timeWindow and arcs[i].vehicle == 2):
                arc_dict[idx] = cc.Complex_arc(idx, arcs[j].origin, cross, (cross, arcs[i].origin, arcs[j].origin), arcs[i].vehicle)
                arc_dict[idx].set_name(names)
                if arc_dict[idx].vehicle == 1:
                    arc_dict[idx].set_time(t1 + t2 + 0.25)
                else:
                    arc_dict[idx].set_time((t1 + t2) * 4/3 + 0.25)
                    
                idx = idx + 1

    return arc_dict, idx

def cycle_generation(cross, arcs, demandOr, demandDest, idx):
    """"""

    cycles = {}
    arcs_aux = {}
    arcs_aux_2 = {}

    for i in arcs:
        for j in arcs:
            
            if (arcs[i].origin != arcs[j].origin or arcs[i].vehicle != arcs[j].vehicle):
                continue
            
            d1 = 0
            d2 = 0

            for pointA in arcs[i].points:
                
                if pointA==arcs[i].destination:
                    continue
                
                aux1 = demandOr[(demandOr.originCode == pointA)]
                
                if len(aux1) == 0:
                    continue
                
                d1 += aux1.iloc[0]['parcels']
                

            for pointB in arcs[j].points:
                
                if pointB==arcs[i].destination:
                    continue
                
                aux2 = demandDest[(demandDest.destinationCode == pointB)]
                if len(aux2) == 0:
                    continue
                
                d2 += aux2.iloc[0]['parcels']
            

            if d1 <= 1000 and d2 <= 1000 and arcs[i].vehicle == 2:
                continue
            elif d1 <= 1475 and d2 <= 1475 and arcs[j].vehicle == 3:
                continue

            points_order = ()
                    
            if len(arcs[i].points)==3:
                points_order = points_order + (arcs[i].points[2],)
            
            points_order = points_order + (arcs[i].points[1], arcs[i].destination, arcs[j].points[1])

            if len(arcs[j].points)==3:
                points_order = points_order + (arcs[j].points[2],)

            cycles[idx] = cc.Cycle(idx, arcs[i].origin, cross, points_order, arcs[i].vehicle)
            cycles[idx].set_demand(d1, d2)

            arcs_aux[arcs[i].idx] = arcs[i]
            arcs_aux_2[arcs[j].idx] = arcs[j]
            
            idx = idx + 1

    return cycles, arcs_aux, arcs_aux_2, idx

def full_path_generation(cross, first_arcs, second_arcs, demand, idx):
    """"""

    paths = {}

    for i in first_arcs:
        for j in second_arcs:

            if i==j or first_arcs[i].origin==second_arcs[j].origin:
                continue

            aux = demand[(demand.originCode==first_arcs[i].origin) & (demand.destinationCode==second_arcs[j].origin)]

            if len(aux)==0:
                continue
            else:
                d = aux.iloc[0]['parcels']
                if d == 0:
                    continue
              
            points_order = ()

            if len(first_arcs[i].points)==3:
                    points_order = points_order + (first_arcs[i].points[2],)
                
            points_order = points_order + (first_arcs[i].points[1], first_arcs[i].destination, second_arcs[j].points[1])

            if len(second_arcs[j].points)==3:
                points_order = points_order + (second_arcs[j].points[2],)

            paths[idx] = cc.Path(idx, points_order[0], cross, points_order[-1], points_order, first_arcs[i].vehicle, second_arcs[j].vehicle)
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
                
                arcs[arc_idx] = cc.Complex_arc(arc_idx, origin, destination, (origin, destination), 4)
                arcs[arc_idx].set_name(names)
                arcs[arc_idx].set_time(t1 * 4/3)

                cycles[cycle_idx] = cc.Cycle(cycle_idx, origin, destination, (origin, destination), 4)
                cycles[cycle_idx].set_demand(d1, 0)
                
                paths[path_idx] = cc.Path(path_idx, origin, 0, destination, (origin, destination), 4, 0)
                                
                arc_idx = arc_idx + 1
                cycle_idx = cycle_idx + 1
                path_idx = path_idx + 1

    return arcs, cycles, paths, arc_idx, cycle_idx, path_idx