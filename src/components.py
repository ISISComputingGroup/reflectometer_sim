"""
Components on a beam
"""


class Beam(object):
    """
    The beam position and direction
    """
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def __repr__(self):
        return "Beam({}, {}, {})".format(self.x, self.y, self.angle)


class Component(object):
    """
    Base object for all components that can sit on a beam line
    """

    def __init__(self):
        self._incoming_beam = None

    def set_incoming_beam(self, incoming_beam):
        """
        Set the incoming beam for the component
        :param incoming_beam: incoming beam
        :return: nothing
        """
        self._incoming_beam = incoming_beam

    def get_outgoing_beam(self):
        """
        This should be overriden in the subclass
        :return: the outgoing beam based on the last set incoming beam and any interaction with the component
        """
        raise NotImplemented()


class TrackingComponent(Component):
    """
    A component which does not effect the beam but could track it
    """
    def __init__(self, x_position):
        super(TrackingComponent, self).__init__()
        self.x_position = x_position

    def get_outgoing_beam(self):
        """
        :return: the outgoing beam based on the last set incoming beam and any interaction with the component
        """
        return self._incoming_beam
