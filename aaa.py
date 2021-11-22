import random


class Node:
    def __init__(self, x, y):
        self.idx = (x, y)
        self.x = x
        self.y = y


class Edge:
    def __init__(self, origin, destination):
        self.idx = (origin.idx, destination.idx)
        self.distance = 0

    def set_distance(self):
        self.distance = random.randint(1, 10)


class Grid:
    def __init__(self, nodes):
        self.nodes = nodes

    def save_grid(self):
        pass

    def filter_nodes(self):
        pass

    def calculate_edges(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
