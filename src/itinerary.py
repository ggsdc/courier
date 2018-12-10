class Itinerary(object):
    """
    Class defined for the itineraries.

    This class will be used by the itineraries, defining a series of arguments and methods to be used.
    """

    def __init__(self, idx, origin, cross, destination, points,
                 points_first, path_first, vehicle_first, points_second, path_second, vehicle_second, names):
        """
        Initialize magic method to create a new itinerary.
        
        Parameters
        ----------
        idx : int
            Index of the generated itinerary, it will be the id to find it.
        origin : int
            Code of the origin node of the itinerary, usually a non-crossdocking point.
        cross : int
            Code of the cross docking point of the itinerary.
        destination : int
            Code of the destination node of the itinerary, usually a non-crossdocking point.
        points : tuple
            List of the points in the itinerary, the order is origin - middle points - cross - middle points - destination.
        points_first : list

        path_first : path instance

        vehicle_first : int
            Code of the vehicle that does the first stage of the itinerary.
        points_second : list

        path_second : path instance

        vehicle_second : int
            Code of the vehicle that does the second stage of the itinerary.

        Returns
        -------
            A new instance of the itinerary object.
        """
        self.idx = idx
        self.origin = origin
        self.cross = cross
        self.destination = destination
        self.points = points
        self.points_first = points_first
        self.path_first = path_first
        self.vehicle_first = vehicle_first
        self.points_second = points_second
        self.path_second = path_second
        self.vehicle_second = vehicle_second

        self.name = '('
        self.name += str(names[points_first[0]]) + ', ' + str(names[points_first[1]]) + ', '
        if len(points_first) == 3:
            self.name += str(names[points_first[-1]]) + ', '

        self.name += str(names[points_second[1]])
        if len(points_second) == 3:
            self.name += ', ' + str(names[points_second[-1]])
        self.name += ', ' + str(self.vehicle_first) + ', ' + str(self.vehicle_second) + ')'

        self.arcs = list()
        self.arcs.extend(self.path_first.arcs_reversed)
        self.arcs.extend(self.path_second.arcs)

        self.arcs_first = self.path_first.arcs_reversed
        self.arcs_second = self.path_second.arcs

    def __repr__(self):
        """
        Representation magic method
        """
        return 'Itinerary ' + str(self.idx)

    # def __str__(self):
    #     """
    #     Print magic method
    #     """
    #     return 'Itinerary with idx ' + str(self.idx) \
    #         + ' passing through the points ' + str(self.points) \
    #         + ' with the vehicles ' + str(self.vehicle_first) \
    #         + ' and ' + str(self.vehicle_second)

    def set_demand(self):
        """
        
        """
        return True
    
    def get_demand(self):
        """
        
        """
        return True
    
    def print_demand(self):
        """
        
        """
        return True