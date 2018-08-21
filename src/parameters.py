"""
Parameters that the user would interact with
"""


class BeamlineParameter(object):
    """
    General beamline parameter that can be set. Subclass must implement _calc_move to decide what to do with the
    value that is set.
    """

    def __init__(self, name):
        self._set_point = None
        self._sp_is_changed = False
        self._name = name
        self.after_move_listener = lambda x: None

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
        self._set_point = float(value)
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
        self.move_no_callback()
        self.after_move_listener(self)

    def move_no_callback(self):
        """
        Move the component but don't call a callback indicating a move has been performed.
        """
        self._move_component()
        self._sp_is_changed = False

    @property
    def name(self):
        """
        Returns: name of this beamline parameter
        """
        return self._name

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
    Angle is measure with +ve in the anti-clockwise direction)
    """

    def __init__(self, name, reflection_component):
        """
        Initializer.
        Args:
            name (str): Name of the reflection angle
            reflection_component (src.components.ActiveComponent): the active component at the reflection point
        """
        super(ReflectionAngle, self).__init__(name, )
        self._reflection_component = reflection_component

    def _move_component(self):
        self._reflection_component.set_angle_relative_to_beam(self._set_point)


class Theta(ReflectionAngle):
    """
    Twice the angle between the incoming beam and outgoing beam at the ideal sample point.
    Angle is measure with +ve in the anti-clockwise direction (opposite of room coordinates)
    """

    def __init__(self, name, ideal_sample_point):
        """
        Initializer.
        Args:
            name (str): name of theta
            ideal_sample_point (src.components.ActiveComponent): the ideal sample point active component
        """
        super(Theta, self).__init__(name, ideal_sample_point)


class TrackingPosition(BeamlineParameter):
    """
    Component which tracks the position of the beam with a single degree of freedom. E.g. slit set on a height stage
    """

    def __init__(self, name, component):
        """

        Args:
            name: Name of the variable
            component (src.components.PassiveComponent): component that the tracking is based on
        """
        super(TrackingPosition, self).__init__(name)
        self._component = component

    def _move_component(self):
        self._component.set_position_relative_to_beam(self._set_point)


class ComponentEnabled(BeamlineParameter):
    """
    Parameter which sets whether a given device is enabled (i.e. parked in beam) on the beamline.
    """

    def __init__(self, name, component):
        """
        Initializer.
        Args:
            name (str): Name of the enabled parameter
            component (src.components.PassiveComponent): the component to be enabled or disabled
        """
        super(ComponentEnabled, self).__init__(name, )
        self._component = component

    def _move_component(self):
        self._component.enabled = self._set_point
