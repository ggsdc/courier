"""

"""


class Vehicle:
    def __init__(self, data):
        """

        :param dict data:
        """
        self.code = data.get("code", 0)
        self.name = data.get("name", "")
        self.capacity = data.get("capacity", 0)
        self.cost = data.get("cost", 0)
        self.speed = data.get("speed", 0)
        self.middle_stops = bool(data.get("middle_stops", False))

    @property
    def __hash__(self):
        return hash((self.code, self.name))

    def __repr__(self):
        return "Vehicle: {} ({})".format(self.name, self.code)
