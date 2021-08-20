import datetime as datetime

# This script will have the functions that allow us to create the time-space diagram
# and fit the cycles and paths to it, creating the final cycle and paths that we will
# use to solve the problem

def create_full_diagram(points, begin, end, interval):
    """"""

    # First we create a iterable object with all the time points.
    # this will be a object from begin, to end, by jumps of interval.
    time_space = dict()
    aux = begin
    for point in points:
        l = list()
        while aux <= end:
            l.append(aux)
            aux = aux + datetime.timedelta(minutes = interval)
        time_space[point] = l
        aux = begin

    return time_space