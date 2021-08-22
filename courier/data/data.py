"""

"""

import json
from courier.structure import Edge, Node, Vehicle


class Data:
    """
    This class serves to store all the data to the problem and to be passed to the different generation methods
    """

    def __init__(self, nodes_path, distances_path, demand_path, vehicle_path):
        """

        :param nodes_path:s
        :type nodes_path:
        """
        # Nodes data
        self.nodes_path = nodes_path
        self.nodes = list()
        self.nodes_collection = dict()
        self.cross_docking = list()
        self.cross_docking_collection = dict()

        self.distances_path = distances_path
        self.distances = list()

        self.demand_path = demand_path
        self.demand = list()

        self.edges = list()
        self.edges_collection = dict()

        self.vehicle_path = vehicle_path
        self.vehicles = list()
        self.vehicles_collection = dict()

        # Process data
        self._load_points_data()
        self._load_vehicles_data()
        self._load_edges_data()

    def _load_points_data(self):
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

    def _load_vehicles_data(self):
        """

        :return:
        :rtype:
        """
        with open(self.vehicle_path) as f:
            temp = json.load(f)

        self.vehicles = [Vehicle(vehicle) for vehicle in temp]
        self.vehicles_collection = {vehicle.code: vehicle for vehicle in self.vehicles}

    def _load_edges_data(self):
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
