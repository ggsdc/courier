"""

"""
from courier.data import Data
from courier.model import Model


def main():
    d = Data()
    d.load_data_from_json_files(
        "data/nodes.json",
        "data/distances.json",
        "data/demand.json",
        "data/vehicles.json",
    )
    print(d.nodes)
    for node in d.nodes:
        print(node.__dict__)
    print(d.vehicles)
    print(d.edges)
    model = Model(d)
    model.build_model()
    for arc in model.arcs:
        print(arc.__dict__)


if __name__ == "__main__":
    import cProfile
    import pstats

    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename="times.prof")
