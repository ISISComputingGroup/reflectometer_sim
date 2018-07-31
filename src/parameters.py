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
        self._calc_move()
        self._sp_is_changed = False

    sp = property(None, _set_sp)  # Set point property (for OPI)
    sp_rbv = property(_sp_rbv)  # set point readback property
    sp_changed = property(_sp_changed)  # changed property
    sp_move = property(None, _sp_move)  # Set the set point and move to it (for scripts)
    move = property(None, _move)

    def _calc_move(self):
        raise NotImplemented("This must be implement in the sub class")


class Theta(BeamlineParameter):
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
        super(Theta, self).__init__()
        self._ideal_sample_point = ideal_sample_point

    def _calc_move(self):
        self._ideal_sample_point.angle = self._ideal_sample_point.incoming_beam.angle - float(self._set_point)
