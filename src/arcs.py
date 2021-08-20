"""

"""


class Arc(object):
    """
    Class defined for the arcs
    """

    def __init__(self, **data):
        self.origin = data.get("origin", None)
        self.destination = data.get("destination", None)
