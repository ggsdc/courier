# This script will have the functions that allow us to create the time-space diagram
# and fit the cycles and paths to it, creating the final cycle and paths that we will
# use to solve the problem

def create_full_diagram(points, begin, end, interval):
    """"""

    # First we create a iterable object with all the time points.
    # this will be a object from begin, to end, by jumps of interval.
    time = range(begin, end+1, interval)
    idx = 1
    diagram = {}
    for point in points:
        for instant in time:
            diagram[idx] = (point, instant)
            idx += 1


    return diagram