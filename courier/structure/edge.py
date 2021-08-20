"""

"""


class Edge:
    """
    This class represents the edge in the graph represented by two nodes.
    It stores the distance between the points, the reference time for the trip and
    the commodities that have to be moved between origin and destination
    """

    def __init__(self, **data):
        self.origin = data.get("origin", None)
        self.destination = data.get("destination", None)
        self.distance = data.get("distance", None)
        self.time = data.get("time", None)
        self.commodity = data.get("commodity", None)
        self._hash = self.__hash__()

    def __hash__(self):
        return hash((self.origin.code, self.destination.code))
