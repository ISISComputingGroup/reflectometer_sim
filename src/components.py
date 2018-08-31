"""
Components on a beam
"""
from math import tan, radians, cos, sin, fabs

TOLERANCE = 1e-12


class Position(object):
    """
    The beam position and direction
    """
    def __init__(self, y, z):
        self.z = float(z)
        self.y = float(y)

    def __repr__(self):
        return "Position(x, {}, {})".format(self.y, self.z)


class PositionAndAngle(Position):
    """
    The beam position and direction
    """
    def __init__(self, y, z, angle):
        """

        Args:
            z: z position in room co-ordinates
            y: y position in room co-ordinates
            angle: clockwise angle measured from the horizon (90 to -90 with 0 pointing away from the source)
        """
        super(PositionAndAngle, self).__init__(y, z)
        self.angle = float(angle)

    def __repr__(self):
        return "PositionAndAngle({}, {}, {})".format(self.z, self.y, self.angle)


class LinearMovement(object):
    """
    A strategy for calculating the interception of the beam with a component that can only move linearly in the Z Y
    plain. E.g. a slit moving vertically to the floor
    """

    def __init__(self, y_position, z_position, angle):
        self._angle_and_position = PositionAndAngle(y_position, z_position, angle)

    def calculate_interception(self, beam):
        """
        Calculate the interception point of the beam and component
        Args:
            beam(PositionAndAngle) : beam to intercept

        Returns: position of the interception

        """
        assert beam is not None
        y_m = self._angle_and_position.y
        z_m = self._angle_and_position.z
        angle_m = self._angle_and_position.angle
        y_b = beam.y
        z_b = beam.z
        angle_b = beam.angle

        if fabs(angle_b % 180.0 - angle_m % 180.0) <= TOLERANCE:
            raise ValueError("No interception between beam and movement")
        elif fabs(angle_b % 180.0) <= TOLERANCE:
            y, z = self._zero_angle(y_b, self._angle_and_position)
        elif fabs(angle_m % 180.0) <= TOLERANCE:
            y, z = self._zero_angle(y_m, beam)
        elif fabs(angle_m % 180.0 - 90) <= TOLERANCE or fabs(angle_m % 180.0 + 90) <= TOLERANCE:
            y, z = self._right_angle(z_m, beam)
        elif fabs(angle_b % 180.0 - 90) <= TOLERANCE or fabs(angle_b % 180.0 + 90) <= TOLERANCE:
            y, z = self._right_angle(z_b, self._angle_and_position)
        else:
            tan_b = tan(radians(angle_b))
            tan_m = tan(radians(angle_m))
            z = 1/(tan_m - tan_b) * (y_b - y_m + z_m * tan_m - z_b * tan_b)
            y = tan_b * tan_m / (tan_b - tan_m) * (y_m / tan_m - y_b / tan_b + z_b - z_m)

        return Position(y, z)

    def _zero_angle(self, y_zero, position_and_angle):
        """
        Calculate when one of the angles is zero but not the other
        Args:
            y_zero: the y of the item with zero angle
            position_and_angle: position and angle of other ray

        Returns: y and z of intercept

        """
        y = y_zero
        z = position_and_angle.z + (y_zero - position_and_angle.y) / tan(radians(position_and_angle.angle))
        return y, z

    def _right_angle(self, z_zero, position_and_angle):
        """
        Calculate when one of the angles is a right angle but not the other
        Args:
            z_zero: the z of the item with right angle
            position_and_angle: position and angle of other ray

        Returns: y and z of intercept
        """

        y = position_and_angle.y + (z_zero - position_and_angle.z) * tan(radians(position_and_angle.angle))
        z = z_zero
        return y, z

    def set_position_relative_to_beam(self, beam_intercept, value):
        """
        Set the position of the component relative to the beam for the given value based on its movement strategy.
        For instance this could set the height above the beam for a vertically moving component
        Args:
            beam_intercept: the current beam position of the item
            value: the value to set away from the beam, e.g. height
        """
        angle = self._angle_and_position.angle
        y_value = beam_intercept.y + value * sin(radians(angle))
        z_value = beam_intercept.z + value * cos(radians(angle))

        self._angle_and_position = PositionAndAngle(y_value, z_value, angle)

    def sp_position(self):
        """
        Returns (Position): The set point position of this component.
        """
        return Position(self._angle_and_position.y, self._angle_and_position.z)


class ArcMovement(LinearMovement):
    """
    A strategy for calculating the interception of the beam with a component that can only move on a radius
    """

    def __init__(self, y_center_of_rotation, z_centre_of_rotation):
        super(ArcMovement, self).__init__(y_center_of_rotation, z_centre_of_rotation, 0)


class Component(object):
    """
    Base object for all components that can sit on a beam line
    """

    def __init__(self, name, movement_strategy):
        """
        Initializer.
        Args:
            name (str): name of the component
            movement_strategy (VerticalMovement): strategy for calculating the interception between the movement of the
            component and the incoming beam
        """
        self.incoming_beam = None
        self._movement_strategy = movement_strategy
        self._beam_path_update_listener = lambda: None
        self._enabled = True
        self._name = name

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

    @property
    def name(self):
        """
        Returns: Name of the component
        """
        return self._name

    def set_incoming_beam(self, incoming_beam):
        """
        Set the incoming beam for the component
        Args:
            incoming_beam(PositionAndAngle): incoming beam
        """
        self.incoming_beam = incoming_beam

    def get_outgoing_beam(self):
        """
        This should be overridden in the subclass
        Returns (PositionAndAngle): the outgoing beam based on the incoming beam and any interaction with the component
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

    def __init__(self, name, movement_strategy):
        """
        Initializer.
        Args:
            name (str): name of the component
            movement_strategy: strategy encapsulating movement of the component
        """
        super(PassiveComponent, self).__init__(name, movement_strategy)

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

    def set_position_relative_to_beam(self, value):
        """
        Set the position of the component relative to the beam for the given value based on its movement strategy.
        For instance this could set the height above the beam for a vertically moving component
        Args:
            value: the value to set away from the beam, e.g. height
        """

        self._movement_strategy.set_position_relative_to_beam(self.calculate_beam_interception(), value)

    def sp_position(self):
        """
        Returns (Position): The set point position of this component.
        """
        return self._movement_strategy.sp_position()


class TiltingJaws(PassiveComponent):
    """
    Jaws which can tilt.
    """
    component_to_beam_angle = 90

    def __init__(self, name, movement_strategy):
        """
        Initializer.
        Args:
            name (str): name of the component
            movement_strategy: strategy encapsulating movement of the component
        """
        super(PassiveComponent, self).__init__(name, movement_strategy)

    def calculate_tilt_angle(self):
        """
        Returns: the angle to tilt so the jaws are perpendicular to the beam.
        """
        return self.get_outgoing_beam().angle + self.component_to_beam_angle


class Bench(PassiveComponent):
    """
    Jaws which can tilt.
    """
    def __init__(self, name, centre_of_rotation_z, distance_from_sample_to_bench):

        super(PassiveComponent, self).__init__(name, ArcMovement(centre_of_rotation_z))
        self.distance_from_sample_to_bench = distance_from_sample_to_bench

    def calculate_front_position(self):
        """
        Returns: the angle to tilt so the jaws are perpendicular to the beam.
        """
        center_of_rotation = self.calculate_beam_interception()
        x = center_of_rotation.z + self.distance_from_sample_to_bench * cos(self.incoming_beam.angle)
        y = center_of_rotation.y + self.distance_from_sample_to_bench * sin(self.incoming_beam.angle)
        return Position(y, x)


class ActiveComponent(PassiveComponent):
    """
    Active components affect the beam as it passes through them.
    """
    def __init__(self, name, movement_strategy):
        """
        Initializer.
        Args:
            name (str): name of the component
            movement_strategy: strategy encapsulating movement of the component
        """
        super(ActiveComponent, self).__init__(name, movement_strategy)
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
        return PositionAndAngle(target_position.y, target_position.z, angle)

    def set_angle_relative_to_beam(self, angle):
        """
        Set the angle of the component relative to the beamline
        Args:
            angle: angle to set the component at
        """
        self.angle = angle + self.incoming_beam.angle
