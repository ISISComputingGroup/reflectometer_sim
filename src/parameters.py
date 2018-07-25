"""
Parameters that the user would interact with
"""


class Theta(object):
    """
    Angle measured between the incoming beam and out going beam at the ideal sample point.
    Angle is measure with +ve in the anti-clockwise direction (opposite of room coordinates)
    """

    def __init__(self, ideal_sample_point):
        self._ideal_sample_point = ideal_sample_point

    def set(self, theta):
        """
        Set Theta
        Args:
            theta:  Angle measured between the incoming beam and out going beam at the ideal sample point.
        """
        # incoming beam angle
        self._ideal_sample_point.angle = self._ideal_sample_point.incoming_beam.angle + theta/2
