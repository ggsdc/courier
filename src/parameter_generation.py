
def parameter_phi(commodities, itineraries, arcs, points):
    """

    :param commodities:
    :param itineraries:
    :param arcs:
    :param points:
    :return:
    """

    dictionary = dict()
    for k in commodities:
        aux_it = [it for it in itineraries if
                  commodities[k]['origin'] in it.points_first and commodities[k]['destination'] in it.points_second]
        for i in aux_it:
            aux_arcs = {arc: arcs[arc] for arc in i.arcs}
            check = 0
            for a in aux_arcs:
                if aux_arcs[a]['origin'] == points[commodities[k]['origin']]:
                    check = 1

                if check == 1:
                    dictionary[(k, i, a,)] = 1

                if aux_arcs[a]['destination'] == points[commodities[k]['destination']]:
                    check = 0

    return dictionary