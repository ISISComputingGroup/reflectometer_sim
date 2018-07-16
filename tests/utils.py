"""
Utils for testing
"""

from hamcrest.core.base_matcher import BaseMatcher


class IsPositionAndAngle(BaseMatcher):
    """
    Matcher for the beam object

    Checks that the beam values are all the same
    """
    def __init__(self, expected_beam, do_compare_angle):
        self.expected_position_and_angle = expected_beam
        self.compare_angle = do_compare_angle

    def _matches(self, beam):
        """
        Does the beam given match the expected beam
        :param beam: beam given
        :return: True if it matches; False otherwise
        """
        if not hasattr(beam, 'x') or not hasattr(beam, 'y') or (self.compare_angle and not hasattr(beam, 'angle')):
            return False
        return beam.x == self.expected_position_and_angle.x and \
            beam.y == self.expected_position_and_angle.y and \
               (not self.compare_angle or beam.angle == self.expected_position_and_angle.angle)

    def describe_to(self, description):
        """
        Describes the problem with the match.
        :param description: description to add problem with
        """
        if self.compare_angle:
            description.append_text(self.expected_position_and_angle)
        else:
            description.append_text("{} (compare position)".format(self.expected_position_and_angle))


def position_and_angle(expected_beam):
    """
    PositionAndAngle matcher.
    Args:
        expected_beam: expected beam to match.

    Returns: the matcher for the beam

    """
    return IsPositionAndAngle(expected_beam, True)

def position(expected_position):
    """
    Position matcher.
    Args:
        expected_position: expected position to match.

    Returns: the matcher for the position

    """
    return IsPositionAndAngle(expected_position, False)