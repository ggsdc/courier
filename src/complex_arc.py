class Complex_arc(object):
    
    """ Class defined for the arcs

    This class will be used for the arcs, defining a series of methods and arguments

    """
    def __init__(self, idx, origin, destination, points, vehicle, names):
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
        self.name = '('
        for point in self.points:
            self.name += str(names[point]) + ', '
        
        self.name = self.name + str(self.vehicle)
        self.name += ')'

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

    def set_points_generated(self, pointsGenerated = list()):
        """"""
        self.pointsGenerated = pointsGenerated

    def set_points_received(self, pointsReceived = list()):
        """"""
        self.pointsReceived = pointsReceived

    def get_demand(self):
        """"""
        return self.generated, self.received

    def get_generated(self):
        """"""
        return self.generated

    def get_received(self):
        """"""
        return self.received

    def get_pointsGenerated(self):
        """"""
        return self.pointsGenerated

    def get_pointsReceived(self):
        """"""
        return self.pointsReceived
  
    def print_demand(self):
        """Method to print the demand info about the demand"""
        return 'The points in the arc generate ' + str(self.generated) \
            + ' parcels and receive ' + str(self.received) + ' parcels'
    
    def set_name(self):
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
        
        self.name = self.name + str(self.vehicle)
        self.name += ')'

    def print_name(self):
        return 'The arc is: ' + str(self.name)

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

    def get_hours(self):
        """"""
        return self.hours