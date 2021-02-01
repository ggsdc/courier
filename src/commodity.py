class Commodity(object):
    """

    """
    __slots__ = ('origin', 'destination', 'value', )
    def __init__(self, origin, destination, value):
        self.origin = origin
        self.destination = destination
        self.value = value

    def __repr__(self):
        """
        Representation magic method
        """
        return 'Commodity ' + str(self.origin) + '-' + str(self.destination)