"""
Utils for testing
"""

from hamcrest.core.base_matcher import BaseMatcher


class IsBeam(BaseMatcher):
    """
    Matcher for the beam object

    Checks that the beam values are all the same
    """
    def __init__(self, expected_beam):
        self.expected_beam = expected_beam

    def _matches(self, beam):
        """
        Does the beam given match the expected beam
        :param beam: beam given
        :return: True if it matches; False otherwise
        """
        if not hasattr(beam, 'x') or not hasattr(beam, 'y') or not hasattr(beam, 'angle'):
            return False
        return beam.x == self.expected_beam.x and \
            beam.y == self.expected_beam.y and \
            beam.angle == self.expected_beam.angle

    def describe_to(self, description):
        """
        Describes the problem with the match.
        :param description: description to add problem with
        """
        description.append_text(self.expected_beam)


def beam(expected_beam):
    """
    Beam matcher.
    Args:
        expected_beam: expected beam to match.

    Returns: the matcher for the beam

    """
    return IsBeam(expected_beam)