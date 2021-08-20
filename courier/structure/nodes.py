"""

"""


class Node:
    """
    This class represents a node in the problem that can be either a cross-docking platform
    or just a origin / destination node for the demand
    """

    def __init__(self, data):
        """

        :param dict data:
        """
        self.code = data.get("code", 0)
        self.name = data.get("name", "")
        self.cross_docking = bool(data.get("cross_docking", False))

        if self.cross_docking:
            self.capacity = data.get("capacity", 0)
            self.start = data.get("start", 0)
            self.end = data.get("end", 0)
            self.unload_docks = data.get("unload_docks", 0)
            self.load_docks = data.get("load_docks", 0)

        self._hash = self.__hash__

    @property
    def __hash__(self):
        return hash((self.code, self.name))

    def __repr__(self):
        return "Node: {} ({})".format(self.name, self.code)
