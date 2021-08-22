"""

"""


class Edge:
    """
    This class represents the edge in the graph represented by two nodes.
    It stores the distance between the points, the reference time for the trip and
    the commodities that have to be moved between origin and destination

    If distance and time are 0 it means that no vehicle can do the direct trip between origin and destination
    """

    def __init__(self, data):
        self.origin = data.get("origin", None)
        self.destination = data.get("destination", None)
        self.distance = data.get("distance", 0)
        self.time = data.get("time", 0)
        self.parcels = data.get("parcels", 0)
        self._hash = self.__hash__()

    def __hash__(self):
        if self.origin is None or self.destination is None:
            return hash(None)
        return hash((self.origin.code, self.destination.code))

    def __eq__(self, other):
        return self._hash == other._hash

    def __repr__(self):
        return "Edge: {}-{} ({}-{})".format(
            self.origin.name,
            self.destination.name,
            self.origin.code,
            self.destination.code,
        )

    def set_distance_time(self, distance, time):
        self.distance = distance
        self.time = time

    def set_parcels(self, parcels):
        self.parcels = parcels
