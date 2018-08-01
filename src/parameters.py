"""
Parameters that the user would interact with
"""


class BeamlineParameter(object):
    """
    General beamline parameter that can be set. Subclass must implement _calc_move to decide what to do with the
    value that is set.
    """

    def __init__(self):
        self._set_point = None
        self._sp_is_changed = False

    def _sp_rbv(self):
        """
        Set point read back value
        Returns: the set point

        """
        return self._set_point

    def _set_sp(self, value):
        """
        Set the set point
        Args:
            value: new set point
        """
        self._set_point = value
        self._sp_is_changed = True

    def _sp_changed(self):
        """
        Returns: if the set point has been changed since the last move
        """
        return self._sp_is_changed

    def _sp_move(self, value):
        """
        Set setpoint and move to that set point
        Args:
            value:  The new value
        """
        self._set_sp(value)
        self._move(1)

    def _move(self, _):
        """
        Move to the setpoint, no matter what the value passed is.
        """
        self._move_component()
        self._sp_is_changed = False

    sp = property(None, _set_sp)  # Set point property (for OPI)
    sp_rbv = property(_sp_rbv)  # set point readback property
    sp_changed = property(_sp_changed)
    sp_move = property(None, _sp_move)  # Set the set point and move to it (for scripts)
    move = property(None, _move)

    def _move_component(self):
        """
        Moves the component(s) associated with this parameter to the setpoint.
        """
        raise NotImplemented("This must be implement in the sub class")


class ReflectionAngle(BeamlineParameter):
    """
    The angle of the mirror measured from the incoming beam.
    Angle is measure with +ve in the anti-clockwise direction (opposite of room coordinates)
    """

    def __init__(self, reflection_component):
        """
        Initializer.
        Args:
            reflection_component (src.components.ActiveComponent): the active component at the reflection point
        """
        super(ReflectionAngle, self).__init__()
        self._reflection_component = reflection_component

    def _move_component(self):
        self._reflection_component.angle = self._reflection_component.incoming_beam.angle - float(self._set_point)


class Theta(ReflectionAngle):
    """
    Twice the angle between the incoming beam and outgoing beam at the ideal sample point.
    Angle is measure with +ve in the anti-clockwise direction (opposite of room coordinates)
    """

    def __init__(self, ideal_sample_point):
        """
        Initializer.
        Args:
            ideal_sample_point (src.components.ActiveComponent): the ideal sample point active component
        """
        super(Theta, self).__init__(ideal_sample_point)


class TrackingPosition(BeamlineParameter):
    """
    Component which tracks the position of the beam with a single degree of freedom. E.g. slit set on a height stage
    """

    def __init__(self, component):
        """

        Args:
            component (src.components.PassiveComponent):
        """
        super(TrackingPosition, self).__init__()
        self._component = component

    def _move_component(self):
        self._component.set_position_relative_to_beam(self._set_point)
