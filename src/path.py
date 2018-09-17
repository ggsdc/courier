class Path(object):
    """ Class defined for the paths.

    This class will be used by the paths, defining a series of arguments and methods to be used.
    
    """
    def __init__(self, idx, origin, cross, destination, points, vehicle_first, vehicle_second):
        """Initialize magic method to create a new path.
        
        Parameters
        ----------
        idx : int
            Index of the generated path, it will be the key in the dictionary as well.
        origin : int
            Code of the origin node of the path, usually a non-crossdocking point.
        cross : int
            Code of the cross docking point of the path.
        destination : int
            Code of the destination node of the path, usually a non-crossdocking point.
        points : tuple
            List of the points in the path, the order is origin - middle points - cross - middle points - destination.
        vehicle_first : int
            Code of the vehicle that does the first stage of the path.
        vehicle_second : int
            Code of the vehicle that does the second stage of the path.

        Returns
        -------
            A new instance of the cycle object.
        """
        self.idx = idx
        self.origin = origin
        self.cross = cross
        self.destination = destination
        self.points = points
        self.vehicle_first = vehicle_first
        self.vehicle_second = vehicle_second

    def __repr__(self):
        """Representation magic method"""
        return 'Path ' + str(self.idx)

    def __str__(self):
        """Print magic method"""
        return 'Path with idx ' + str(self.idx) \
            + ' passing through the points ' + str(self.points) \
            + ' with the vehicles ' + str(self.vehicle_first) \
            + ' and ' + str(self.vehicle_second)

    def set_demand(self):
        """"""
        return True
    
    def get_demand(self):
        """"""
        return True
    
    def print_demand(self):
        """"""
        return True