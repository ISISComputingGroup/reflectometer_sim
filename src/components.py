"""
Components on a beam
"""
from math import tan, radians, cos, sin


class Position(object):
    """
    The beam position and direction
    """
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Position({}, {})".format(self.x, self.y)


class PositionAndAngle(Position):
    """
    The beam position and direction
    """
    def __init__(self, x, y, angle):
        """

        Args:
            x: x position in room co-ordinates
            y: y position in room co-ordinates
            angle: clockwise angle measured from the horizon (90 to -90 with 0 pointing away from the source)
        """
        super(PositionAndAngle, self).__init__(x, y)
        self.angle = float(angle)

    def __repr__(self):
        return "PositionAndAngle({}, {}, {})".format(self.x, self.y, self.angle)


class VerticalMovement(object):
    """
    A strategy for calculating the interception of the beam with a component that can only move vertically
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
        assert beam is not None
        distance_from_incoming_beam = self._x_position - beam.x
        y = beam.y + tan(radians(-beam.angle)) * distance_from_incoming_beam
        return Position(self._x_position, y)


class ArcMovement(VerticalMovement):
    """
    A strategy for calculating the interception of the beam with a component that can only move on a radius
    """

    def __init__(self, x_centre_of_rotation):
        super(ArcMovement, self).__init__(x_centre_of_rotation)


class Component(object):
    """
    Base object for all components that can sit on a beam line
    """

    def __init__(self, movement_strategy):
        self.incoming_beam = None
        self._movement_strategy = movement_strategy
        self._beam_path_update_listener = lambda: None
        self._enabled = True

    @property
    def enabled(self):
        """
        Returns: the enabled status
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Updates the component enabled status and notifies the beam path update listener
        Args:
            enabled: The modified enabled status
        """
        self._enabled = enabled
        self._beam_path_update_listener()

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

    def set_beam_path_update_listener(self, beam_path_update_listener):
        """
        Sets a beam path update listener on this component, which is called when the beam path changes
        Args:
            beam_path_update_listener: The listener
        """
        self._beam_path_update_listener = beam_path_update_listener


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


class Bench(PassiveComponent):
    """
    Jaws which can tilt.
    """
    def __init__(self, centre_of_rotation_x, distance_from_sample_to_bench):
        super(PassiveComponent, self).__init__(ArcMovement(centre_of_rotation_x))
        self.distance_from_sample_to_bench = distance_from_sample_to_bench

    def calculate_front_position(self):
        """
        Returns: the angle to tilt so the jaws are perpendicular to the beam.
        """
        center_of_rotation = self.calculate_beam_interception()
        x = center_of_rotation.x + self.distance_from_sample_to_bench * cos(self.incoming_beam.angle)
        y = center_of_rotation.y + self.distance_from_sample_to_bench * sin(self.incoming_beam.angle)
        return Position(x, y)


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
        self._angle = 0

    @property
    def angle(self):
        """
        Returns: the angle of the component measured clockwise from the horizon in the incoming beam direction.
        """
        return self._angle

    @angle.setter
    def angle(self, angle):
        """
        Updates the component angle and notifies the beam path update listener
        Args:
            angle: The modified angle
        """
        self._angle = angle
        self._beam_path_update_listener()

    def get_outgoing_beam(self):
        """
        Returns: the outgoing beam based on the last set incoming beam and any interaction with the component
        """
        if not self._enabled:
            return self.incoming_beam

        target_position = self.calculate_beam_interception()
        angle_between_beam_and_component = (self._angle - self.incoming_beam.angle)
        angle = angle_between_beam_and_component * 2 + self.incoming_beam.angle
        return PositionAndAngle(target_position.x, target_position.y, angle)
