import unittest

from math import tan, radians
from hamcrest import *

from src.components import PositionAndAngle, PassiveComponent, ActiveComponent, VerticalMovement, Position, TiltingJaws
from src.beamline import Beamline
from src.parameters import Theta
from tests.utils import position_and_angle, position


class TestComponentBeamline(unittest.TestCase):

    def setUp(self):
        beam_start = PositionAndAngle(x=0, y=0, angle=0)
        jaws = PassiveComponent(movement_strategy=VerticalMovement(0))
        self.ideal_sample_point = ActiveComponent(movement_strategy=VerticalMovement(0))
        jaws3 = PassiveComponent(movement_strategy=VerticalMovement(20))
        theta = Theta(self.ideal_sample_point)
        self.beamline = Beamline([jaws, self.ideal_sample_point, jaws3], {"theta": theta})
        self.beamline.set_incoming_beam(beam_start)



    def test_GIVEN_beam_line_contains_multiple_component_WHEN_beam_set_THEN_each_component_has_beam_out_which_is_effected_by_each_component_in_turn(self):

        theta_set = 10.0
        self.beamline.parameter("theta").set(theta_set)

        reflection_angle = self.ideal_sample_point.get_outgoing_beam().angle - self.ideal_sample_point.incoming_beam.angle
        assert_that(reflection_angle, is_(theta_set))

if __name__ == '__main__':
    unittest.main()
