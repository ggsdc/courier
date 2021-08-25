"""

"""
from ..structure import Commodity, CrossDockingCycle, SimpleArc
from ..const import TIME_WINDOW


class Model:
    def __init__(self, data):
        self.data = data
        self.arcs = list()
        self.arcs_collection = dict()
        self.arcs_complementary = dict()
        self.commodities = list()
        self.commodities_collection = dict()
        self.cycles = list()
        self.cycles_collection = dict()
        self.paths = list()
        self.paths_collection = dict()

    def build_model(self):
        self._generate_arcs()
        self._generate_commodities()
        self._generate_cycles()
        self._generate_paths()

    def _generate_arcs(self):
        """ """

        for origin in self.data.nodes:
            for destination in self.data.nodes:
                for vehicle in self.data.vehicles:
                    if origin == destination:
                        continue

                    try:
                        edge = self.data.edges_collection[
                            (destination.code, origin.code)
                        ]
                    except KeyError:
                        continue

                    if (
                        edge.time * vehicle.speed_factor > TIME_WINDOW
                        or edge.time == 0
                        or edge.distance == 0
                    ):
                        continue

                    self.arcs.append(
                        SimpleArc(
                            {
                                "origin": origin,
                                "destination": destination,
                                "vehicle": vehicle,
                                "distance": edge.distance,
                            }
                        )
                    )

                    self.arcs_collection[
                        (origin.code, destination.code, vehicle.code)
                    ] = self.arcs[-1]

        self._generate_arcs_relationships()

    def _generate_arcs_relationships(self):
        self.arcs_complementary = {
            arc: self.arcs_collection[
                (arc.destination.code, arc.origin.code, arc.vehicle.code)
            ]
            for arc in self.arcs
        }

    def _generate_commodities(self):
        """ """
        self.commodities = [
            Commodity(
                {
                    "origin": edge.origin,
                    "destination": edge.destination,
                    "amount": edge.parcels,
                }
            )
            for edge in self.data.edges
            if edge.parcels > 0
        ]

        self.commodities_collection = {
            (c.origin.code, c.destination.code): c for c in self.commodities
        }

    def _generate_cycles(self):
        """ """
        # TODO: extend to those cycles that do not have to go through a cross-docking node
        self.cycles = [
            CrossDockingCycle({"arcs": [arc, self.arcs_complementary[arc]]})
            for arc in self.arcs
            if arc.vehicle.code != 4 and arc.destination in self.data.cross_docking
        ]

    def _generate_paths(self):
        pass


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
