"""

"""

import json
from courier.structure.nodes import Node


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
        self.nodes_collection = list()

        # TODO: Distances data
        self.distances_path = distances_path

        # TODO: Demand data
        self.demand_path = demand_path
        self.edges = list()
        self.edges_collection = list()

        # TODO: Vehicle data
        self.vehicle_path = vehicle_path
        self.vehicles = list()
        self.vehicles_collection = list()

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
            self.nodes = json.load(f)

        self.nodes_collection = [Node(**data) for data in self.nodes]

    def _load_vehicles_data(self):
        pass

    def _load_edges_data(self):
        pass
