class Complex_arc(object):
    
    """ Class defined for the arcs

    This class will be used for the arcs, defining a series of methods and arguments

    """
    def __init__(self, idx, name, origin, destination, points, vehicle):
        """ Initialize magic method to create a new complex arc.

        Parameters
        ----------
        idx : int
            Index of the generated arc, it will be the key in the dictionary as well.
        name : character
            Name of the generated arc.
        origin : int
            Code of the origin node of the arc, usually a non-crossdocking point.
        destination : int
            Code of the destination of the arc, usually a crossdocking point.
        points : list
            List of the points in the arc, the order is destination - middle points - origin.
        vehicle : int
            Code of the vehicle that does the arc.

        Returns
        ------
        A new instance of Complex_arc

        """
        self.idx = idx
        self.name = name
        self.origin = origin
        self.destination = destination
        self.points = points
        self.vehicle = vehicle

    def __repr__(self):
        """Representation magic method"""
        return 'Complex arc ' + str(self.idx)

    def __str__(self):
        """Print magic method"""
        return 'Complex arc with idx ' + str(self.idx) \
            + ' passing through the points ' + str(self.points) \
            + ' with the vehicle ' + str(self.vehicle)

    def set_time(self, hours=0):
        """Method to assign the duration of the arc
        
        Parameters
        ----------
        hours : float
            Duration of the trip in hours. Defaults to 0.
        minutes : float
            Duration of the trip in minutes. Defaults to 0.

        Returns
        -------
        Nothing, it just assigns the value

        """
        self.hours = hours
        self.minutes = hours * 60
    
    def set_demand(self, generated = 0, received = 0):
        """Method to assign the demand that the arc can give service to
        
        Parameters
        ----------
        generated : int
            Amount of parcels that have to leave the points in the arc. Defaults to 0.
        received : int
            Amount of parcels that have to reach the points in the arc. Defaults to 0.

        Returns
        -------
        Nothing, it just assigns the value
        """
        self.generated = generated
        self.received = received
    
    def print_demand(self):
        """Method to print the demand info about the demand"""
        return 'The points in the arc generate ' + str(self.generated) \
            + ' parcels and receive ' + str(self.received) + ' parcels'

class Cycle(object):
    """"""
    def __init__(self, idx, origin, cross, points, vehicle):
        """"""
        self.idx = idx
        self.origin = origin
        self.cross = cross
        self.points = points
        self.vehicle = vehicle

    def __repr__(self):
        """"""
        return 'Cycle ' + str(self.idx)

    def __str__(self):
        """"""
        return 'Cycle with idx ' + str(self.idx) \
            + ' passing through the points ' + str(self.points) \
            + ' with the vehicle ' + str(self.vehicle)

    def set_demand(self, generated = 0, received = 0):
        """"""
        self.generated = generated
        self.received = received

    def set_time(self, firstTime = 0, secondTime = 0):
        """"""
        self.firstTime = firstTime
        self.secondTime = secondTime

    def get_time(self):
        """"""
        return (self.firstTime, self.secondTime)

    def set_length(self, firstLength = 0, secondLength = 0):
        """"""
        self.firstLength = firstLength
        self.secondLength = secondLength
    
    def get_length(self):
        """"""
        return (self.firstLength, self.secondLength)
    
    def print_demand(self):
        """"""
        return 'The points in the cycle generate ' + str(self.generated) \
            + ' parcels and receive ' + str(self.received) + ' parcels'
          

class Path(object):
    """"""

    def __init__(self, idx, origin, cross, destination, points, vehicle_first, vehicle_second):
        """"""
        self.idx = idx
        self.origin = origin
        self.cross = cross
        self.destination = destination
        self.points = points
        self.vehicle_first = vehicle_first
        self.vehicle_second = vehicle_second

    def __repr__(self):
        """"""
        return 'Path ' + str(self.idx)

    def __str__(self):
        """"""
        return 'Path with idx ' + str(self.idx) \
            + ' passing through the points ' + str(self.points) \
            + ' with the vehicles ' + str(self.vehicle_first) \
            + ' and ' + str(self.vehicle_second)

    
