"""

"""


class SimpleArc(object):
    """
    Class defined for the arcs
    This arcs stand for the possible services.
    This are simple arcs with no intermediate stops
    This arcs have to have a vehicle type as it is the only option to check if it is a possible service
    """

    def __init__(self, data):
        self.origin = data.get("origin", None)
        self.destination = data.get("destination", None)
        self.vehicle = data.get("vehicle", None)
        self.distance = data.get("distance", None)
        self._hash = self.__hash__()

    def __hash__(self):
        if self.origin is None or self.destination is None:
            return hash(None)
        return hash((self.origin.code, self.destination.code, self.vehicle.code))

    def __repr__(self):
        return "Simple arc: {}-{}-{} ({}-{}-{})".format(
            self.origin.name,
            self.destination.name,
            self.vehicle.name,
            self.origin.code,
            self.destination.code,
            self.vehicle.code,
        )


class ComplexArc(SimpleArc):
    def __init__(self, data):
        super().__init__(data)
        self.stops = data.get("stops", None)
