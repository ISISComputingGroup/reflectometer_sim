"""
Components on a beam
"""
from math import tan, radians


class PositionAndAngle(object):
    """
    The beam position and direction
    """
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def __repr__(self):
        return "PositionAndAngle({}, {}, {})".format(self.x, self.y, self.angle)


class Position(object):
    """
    The beam position and direction
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Position({}, {})".format(self.x, self.y)


class VerticalMovement(object):
    """
    A strategy for calculating the interception of components with the beam that can only move vertically
    """

    def __init__(self, x_position):
        self._x_position = x_position

    def calculate_interception(self, beam):
        """
        Calculate the interception point of the baem and component
        Args:
            beam: beam to intercept

        Returns: position of the interception

        """
        distance_from_incoming_beam = self._x_position - beam.x
        y = tan(radians(beam.angle)) * distance_from_incoming_beam
        return Position(self._x_position, y)


class Component(object):
    """
    Base object for all components that can sit on a beam line
    """

    def __init__(self, movement_strategy):
        self.incoming_beam = None
        self._movement_strategy = movement_strategy

    def set_incoming_beam(self, incoming_beam):
        """
        Set the incoming beam for the component
        Args:
            incoming_beam: incoming beam
        """
        self.incoming_beam = incoming_beam

    def get_outgoing_beam(self):
        """
        This should be overriden in the subclass
        :return: the outgoing beam based on the last set incoming beam and any interaction with the component
        """
        raise NotImplemented()


class PassiveComponent(Component):
    """
    A component which does not effect the beam
    """

    def __init__(self, movement_strategy):
        """
        Initializer.
        Args:
            movement_strategy: strategy encapsulating movement of the component
        """
        super(PassiveComponent, self).__init__(movement_strategy)

    def get_outgoing_beam(self):
        """
        Returns: the outgoing beam based on the last set incoming beam and any interaction with the component
        """
        return self.incoming_beam

    def calculate_beam_interception(self):
        """

        Returns: the position at the point where the components possible movement intercepts the beam

        """
        return self._movement_strategy.calculate_interception(self.incoming_beam)


class TiltingJaws(PassiveComponent):
    """
    Jaws which can tilt.
    """
    component_to_beam_angle = 90

    def __init__(self, movement_strategy):
        super(PassiveComponent, self).__init__(movement_strategy)

    def calculate_tilt_angle(self):
        """
        Returns: the angle to tilt so the jaws are perpendicular to the beam.
        """
        return self.get_outgoing_beam().angle + self.component_to_beam_angle


class ActiveComponent(PassiveComponent):
    """
    Active components affect the beam as it passes through them.
    """
    def __init__(self, movement_strategy):
        """
        Initializer.
        Args:
            movement_strategy: strategy encapsulating movement of the component
        """
        super(ActiveComponent, self).__init__(movement_strategy)
        self.angle = 0

    def get_outgoing_beam(self):
        """
        Returns: the outgoing beam based on the last set incoming beam and any interaction with the component
        """
        target_position = self.calculate_beam_interception()
        angle = self.angle*2 + self.incoming_beam.angle
        return PositionAndAngle(target_position.x, target_position.y, angle)
