class Cycle(object):
    """Class defined for the cycles.
    
    This class will be used for the cycles, defining a series of methods and arguments
    """
    def __init__(self, idx, origin, cross, points, vehicle, names):
        """
        Initialize magic method to create a new cycle.
        
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
        names : dict
            Dictionary with the names of the points to generate the full name of the cycle.

        Returns
        -------
            A new instance of the cycle object.
        """
        self.idx = idx
        self.origin = origin
        self.cross = cross
        self.points = points
        self.vehicle = vehicle
        self.name = '('
        for point in self.points:
            self.name += str(names[point]) + ', '
        
        self.name += self.name + str(self.vehicle)
        self.name += ')'

    def __repr__(self):
        """
        Representation magic method
        """
        return 'Cycle ' + str(self.idx)

    def __str__(self):
        """
        Print magic method
        """
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
        """
        Method to get the info about the demand.
        """
        return 'The points in the cycle generate ' + str(self.generated) \
            + ' parcels and receive ' + str(self.received) + ' parcels'

    def set_length(self, firstLength = 0, secondLength = 0):
        """
        Method to set the length of the cycle.
        
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
        """
        Method to get the lengths back
        
        Parameters
        ----------
            None

        Returns
        -------
            A tuple with both lengths.
        """
        return (self.firstLength, self.secondLength)

    def set_time(self, firstTime = 0, secondTime = 0):
        """
        Method to assign the time that the cycle needs to go to all points.
        
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
        """
        Method to get the time needed for the cycle both as hours and minutes
        
        Parameters
        ----------
            None

        Returns
        -------
            A tuple with first both times in hours, then in minutes.
        """
        return (self.firstTime, self.secondTime, self.firstTimeMin, self.secondTimeMin)