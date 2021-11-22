"""

"""
from courier.structure import Commodity, CrossDockingCycle, SimpleArc
from courier.const import TIME_WINDOW


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
