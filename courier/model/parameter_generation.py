"""

"""


def parameter_phi(commodities, itinerary, arcs, points):
    """

    :param commodities:
    :param itineraries:
    :param arcs:
    :param points:
    :return:
    """

    parameter = list()
    domain = dict()
    aux_commodities = [
        k for k in commodities if k.destination in itinerary.points_second
    ]
    for k in aux_commodities:
        aux_arcs = {arc: arcs[arc] for arc in itinerary.arcs}
        key = (
            k,
            itinerary,
        )
        domain[key] = 1
        check = 0
        for a in aux_arcs:
            if aux_arcs[a]["origin"] == points[k.origin]:
                check = 1

            if check == 1:
                parameter.append(
                    (
                        k,
                        itinerary,
                        a,
                    )
                )

            if aux_arcs[a]["destination"] == points[k.destination]:
                check = 0

    return parameter, domain
