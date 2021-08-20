"""

"""


class Node:
    def __init__(self, **data):
        self.code = data.get("code", 0)
        self.name = data.get("name", "")
        self.cross_docking = data.get("cross_docking", False)
        self._hash = self.__hash__

    @property
    def __hash__(self):
        return hash((self.code, self.name))
