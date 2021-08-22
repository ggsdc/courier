"""

"""
from courier.data import Data


def main():
    d = Data(
        "data/nodes.json",
        "data/distances.json",
        "data/demand.json",
        "data/vehicles.json",
    )
    print(d.nodes)
    print(d.vehicles)
    for key, value in d.edges_collection.items():
        print(value.__dict__)


if __name__ == "__main__":
    main()
