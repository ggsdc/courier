"""

"""


def rq01_building(
    model,
    arcs,
    v_flow,
    phi,
    commodities,
    itineraries,
    domain,
    v_vehicles,
    vehicles,
    omega,
    cycles,
):
    """

    :param model:
    :type model:
    :param arcs:
    :type arcs:
    :param v_flow:
    :type v_flow:
    :param phi:
    :type phi:
    :param commodities:
    :type commodities:
    :param itineraries:
    :type itineraries:
    :param domain:
    :type domain:
    :param v_vehicles:
    :type v_vehicles:
    :param vehicles:
    :type vehicles:
    :param omega:
    :type omega:
    :param cycles:
    :type cycles:
    :return:
    :rtype:
    """
    import pulp as lp

    RQ01_constraints = 1
    for a in arcs:

        aux_itineraries = [it for it in itineraries if a in it.arcs]

        x = (
            lp.lpSum(
                v_flow[k, i]
                * phi[
                    (
                        k,
                        i,
                        a,
                    )
                ]
                for k in commodities
                for i in aux_itineraries
                if domain[
                    (
                        k,
                        i,
                    )
                ]
                == 1
                and (
                    k,
                    i,
                    a,
                )
                in phi.keys()
            )
            <= lp.lpSum(
                v_vehicles[c]
                * vehicles[str(c.vehicle)]["capacity"]
                * omega[
                    (
                        c,
                        a,
                    )
                ]
                for c in cycles
                if (
                    c,
                    a,
                )
                in omega.keys()
            ),
            "RQ01." + str(RQ01_constraints),
        )
        model += x
        RQ01_constraints += 1

    return model


def rq02_building(model, commodities, v_flow, itineraries, domain):
    """

    :param model:
    :type model:
    :param commodities:
    :type commodities:
    :param v_flow:
    :type v_flow:
    :param itineraries:
    :type itineraries:
    :param domain:
    :type domain:
    :return:
    :rtype:
    """
    import pulp as lp

    RQ02_constraints = 1

    for k in commodities:
        x = (
            lp.lpSum(
                v_flow[k, i]
                for i in itineraries
                if domain[
                    (
                        k,
                        i,
                    )
                ]
                == 1
            )
            == commodities[k]["value"],
            "RQ02.{0}" + str(RQ02_constraints),
        )
        model += x
        RQ02_constraints += 1

    return model
