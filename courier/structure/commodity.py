"""

"""


class Commodity:
    """ """

    def __init__(self, data):
        self.origin = data.get("origin", None)
        self.destination = data.get("destination", None)
        self.amount = data.get("amount", None)
        self._hash = self.__hash__

    @property
    def __hash__(self):
        if self.origin is None or self.destination is None:
            return hash(None)
        return hash((self.origin.code, self.destination.code))

    def __repr__(self):
        """
        Representation magic method
        """
        return "Commodity: {}-{} ({}-{})".format(
            self.origin.name,
            self.destination.name,
            self.origin.code,
            self.destination.code,
        )
