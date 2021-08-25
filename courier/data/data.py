"""

"""

import json
from courier.structure import Edge, Node, Vehicle
from courier.const import TIME_WINDOW


class Data:
    """
    This class serves to store all the data to the problem and to be passed to the different generation methods
    """

    def __init__(self):
        """ """
        # File routes
        self.nodes_path = None
        self.distances_path = None
        self.demand_path = None
        self.vehicle_path = None

        # Db configuration
        self.connection_string = None

        # Data: nodes, distances, demand, edges and vehicles
        self.nodes = list()
        self.nodes_collection = dict()
        self.cross_docking = list()
        self.cross_docking_collection = dict()

        self.distances = list()

        self.demand = list()

        self.edges = list()
        self.edges_collection = dict()

        self.vehicles = list()
        self.vehicles_collection = dict()

    def load_data_from_json_files(
        self, nodes_path, distances_path, demand_path, vehicle_path
    ):
        self.nodes_path = nodes_path
        self.distances_path = distances_path
        self.demand_path = demand_path
        self.vehicle_path = vehicle_path

        self._load_nodes_data_json()
        self._load_vehicles_data_json()
        self._load_edges_data_json()

    def _load_nodes_data_json(self):
        """

        :return:
        :rtype:
        """
        with open(self.nodes_path) as f:
            temp = json.load(f)

        self.nodes = [Node(node) for node in temp]
        self.nodes_collection = {node.code: node for node in self.nodes}
        self.cross_docking = [node for node in self.nodes if node.cross_docking]
        self.cross_docking_collection = {
            cross.code: cross for cross in self.cross_docking
        }

        for cross in self.cross_docking:
            cross.set_time_window(TIME_WINDOW)

    def _load_vehicles_data_json(self):
        """

        :return:
        :rtype:
        """
        with open(self.vehicle_path) as f:
            temp = json.load(f)

        self.vehicles = [Vehicle(vehicle) for vehicle in temp]
        self.vehicles_collection = {vehicle.code: vehicle for vehicle in self.vehicles}

    def _load_edges_data_json(self):
        """

        :return:
        :rtype:
        """
        with open(self.demand_path) as f:
            temp_demand = json.load(f)

        self.demand = [
            {
                **demand,
                **{
                    "origin": self.nodes_collection[demand["origin"]],
                    "destination": self.nodes_collection[demand["destination"]],
                },
            }
            for demand in temp_demand
        ]

        self.edges = [Edge(demand) for demand in self.demand]

        self.edges_collection = {
            (edge.origin.code, edge.destination.code): edge for edge in self.edges
        }

        with open(self.distances_path) as f:
            temp_distances = json.load(f)

        self.distances = [
            {
                **distance,
                **{
                    "origin": self.nodes_collection[distance["origin"]],
                    "destination": self.nodes_collection[distance["destination"]],
                },
            }
            for distance in temp_distances
        ]

        for distance in self.distances:
            if (
                distance["origin"].code,
                distance["destination"].code,
            ) in self.edges_collection.keys():

                self.edges_collection[
                    (distance["origin"].code, distance["destination"].code)
                ].set_distance_time(distance["distance"], distance["time"])
            else:
                self.edges.append(Edge(distance))
                self.edges_collection[
                    (distance["origin"].code, distance["destination"].code)
                ] = self.edges[-1]

    def load_data_from_csv_files(self):
        pass

    def load_data_from_db(self):
        pass
