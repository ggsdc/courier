"""

"""


class Cycle:
    def __init__(self, data):
        self.arcs = data.get("arcs", [])
        self.before_arc = self.arcs[0]
        self.origin = self.arcs[0].origin
        self.vehicle = self.arcs[0].vehicle
        self.distance = self.arcs[0].distance

    def __hash__(self):
        pass

    def __repr__(self):
        pass


class OneArcCycle(Cycle):
    def __init__(self, data):
        super().__init__(data)


class TwoArcCycle(Cycle):
    def __init__(self, data):
        super().__init__(data)


class CrossDockingCycle(TwoArcCycle):
    # Nota - esto serían las rutas
    def __init__(self, data):
        super().__init__(data)
        self.after_arc = self.arcs[-1]
        self.cross_docking = self.arcs[0].destination
        self.destination = self.arcs[-1].destination
        # In the future the arcs do not need to have the same length so is better to be prepared for it.
        self.cost = (
            self.before_arc.distance + self.after_arc.distance
        ) * self.vehicle.cost

    def __hash__(self):
        pass

    def __repr__(self):
        return "CD Cycle: {}-{}-{} ({}-{}-{})".format(
            self.origin.name,
            self.cross_docking.name,
            self.vehicle.name,
            self.origin.code,
            self.cross_docking.code,
            self.vehicle.code,
        )


class NonCrossDockingCycle(TwoArcCycle):
    # Nota - esto serían los acercamientos.
    def __init__(self, data):
        super().__init__(data)
        self.after_arc = self.arcs[-1]
        self.destination = self.arcs[1].destination
        # In the future the arcs do not need to have the same length so is better to be prepared for it.
        self.cost = (
            self.before_arc.distance + self.after_arc.distance
        ) * self.vehicle.cost

    def __repr__(self):
        return "Non-CD Cycle: {}-{}-{} ({}-{}-{})".format(
            self.origin.name,
            self.destination.name,
            self.vehicle.name,
            self.origin.code,
            self.destination.code,
            self.vehicle.code,
        )


class NonReturnCycle(OneArcCycle):
    def __init__(self, data):
        super().__init__(data)
        self.destination = self.arcs[0].destination

    def __hash__(self):
        pass

    def __repr__(self):
        pass
