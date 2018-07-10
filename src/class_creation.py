class Complex_arc(object):
    
    """ Class defined for the arcs

    This class will be used for the arcs, defining a series of methods and arguments

    """
    def __init__(self, idx, origin, destination, points, vehicle):
        """ Initialize magic method to create a new complex arc.

        Parameters
        ----------
        idx : int
            Index of the generated arc, it will be the key in the dictionary as well.
        origin : int
            Code of the origin node of the arc, usually a non-crossdocking point.
        destination : int
            Code of the destination of the arc, usually a crossdocking point.
        points : tuple
            List of the points in the arc, the order is destination - middle points - origin.
        vehicle : int
            Code of the vehicle that does the arc.

        Returns
        ------
            A new instance of Complex_arc

        """
        self.idx = idx
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
            Nothing, it just assigns the value.
        """
        self.generated = generated
        self.received = received
  
    def print_demand(self):
        """Method to print the demand info about the demand"""
        return 'The points in the arc generate ' + str(self.generated) \
            + ' parcels and receive ' + str(self.received) + ' parcels'
    
    def set_name(self, name):
        """Method to set up the name of the arc
        
        Parameters
        ----------
        name : data.frame
            Data frame with the codes of the locations and its names to build the name of the arc.

        Returns
        -------
            Nothing, it just assigns the value.
        """
        self.name = '('
        for point in self.points:
            self.name += str(name[(name.code==point)].iloc[0]['point']) + ', '
        
        self.name =self.name[:-2]
        self.name += ')'

    def set_time(self, hours=0):
        """Method to assign the duration of the arc
        
        Parameters
        ----------
        hours : float
            Duration of the trip in hours. Defaults to 0.

        Returns
        -------
            Nothing, it just assigns the value in hours and converts it to minutes as well.

        """
        self.hours = hours
        self.minutes = hours * 60


class Cycle(object):
    """Class defined for the cycles.
    
    This class will be used for the cycles, defining a series of methods and arguments
    """
    def __init__(self, idx, origin, cross, points, vehicle):
        """Initialize magic method to create a new cycle.
        
        Parameters
        ----------
        idx : int
            Index of the generated cycle, it will be the key in the dictionary as well.
        origin : int
            Code of the origin node of the cycle, usually a non-crossdocking point.
        cross : int
            Code of the cross docking point of the cycle.
        points : tuple
            List of the points in the cycle, the order is origin - middle points - cross - middle points - origin.
        vehicle : int
            Code of the vehicle that does the cycle.

        Returns
        -------
            A new instance of the cycle object.
        """
        self.idx = idx
        self.origin = origin
        self.cross = cross
        self.points = points
        self.vehicle = vehicle

    def __repr__(self):
        """Representation magic method"""
        return 'Cycle ' + str(self.idx)

    def __str__(self):
        """Print magic method"""
        return 'Cycle with idx ' + str(self.idx) \
            + ' passing through the points ' + str(self.points) \
            + ' with the vehicle ' + str(self.vehicle)

    def set_demand(self, generated = 0, received = 0):
        """Method to assign the demand that the cycle can give service to
        
        Parameters
        ----------
        generated : int
            Amount of parcels that have to leave the points in the cycle during the first stage. Defaults to 0.
        received : int
            Amount of parcels that have to reach the points in the cycle during the second stage. Defaults to 0.

        Returns
        -------
            Nothing, it just assigns the value.
        """
        self.generated = generated
        self.received = received

    def print_demand(self):
        """Method to get the info about the demand."""
        return 'The points in the cycle generate ' + str(self.generated) \
            + ' parcels and receive ' + str(self.received) + ' parcels'

    def set_length(self, firstLength = 0, secondLength = 0):
        """Method to set the length of the cycle.
        
        Parameters
        ----------
        firstLength : float
            Length of the trip in the first stage. Defaults to 0.
        secondLength : float
            Length of the trip in the first stage

        Returns
        -------
            Nothing it just assigns the value.
        """
        self.firstLength = firstLength
        self.secondLength = secondLength
    
    def get_length(self):
        """Method to get the lengths back
        
        Parameters
        ----------
            None

        Returns
        -------
            A tuple with both lengths.
        """
        return (self.firstLength, self.secondLength)

    def set_time(self, firstTime = 0, secondTime = 0):
        """Method to assign the time that the cycle needs to go to all points.
        
        Parameters
        ----------
        firstTime : int
            Duration of the trip in the first stage in hours. Defaults to 0.
        secondTime : int
            Duration of the trip in the second stage in hours. Defaults to 0.

        Returns
        -------
            Nothing, it just assigns the value in hours and converts it to minutes as well.
        """
        self.firstTime = firstTime
        self.secondTime = secondTime

        self.firstTimeMin = self.firstTime * 60
        self.secondTimeMin = self.secondTime * 60

    def get_time(self):
        """Method to get the time needed for the cycle both as hours and minutes
        
        Parameters
        ----------
            None

        Returns
        -------
            A tuple with first both times in hours, then in minutes.
        """
        return (self.firstTime, self.secondTime, self.firstTimeMin, self.secondTimeMin)


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
    