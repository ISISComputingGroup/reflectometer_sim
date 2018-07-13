import unittest

from hamcrest import *

from src.components import Beam, TrackingComponent
from tests.utils import beam


class TestNonTiltingJawsAtFixedX(unittest.TestCase):

    def test_GIVEN_jaw_at_10_input_beam_is_at_0_deg_and_x0_y0WHEN_get_x_position_THEN_beam_output_x_position_is_10(self):
        jaws_x_position = 10
        beam_start = Beam(x=0, y=0, angle=0)
        jaws = TrackingComponent(x_position=jaws_x_position)
        jaws.set_incoming_beam(beam_start)

        result = jaws.get_outgoing_beam()

        assert_that(result, is_(beam(beam_start)))


if __name__ == '__main__':
    unittest.main()
