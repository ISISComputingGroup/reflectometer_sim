import unittest

from math import tan, radians
from hamcrest import *

from src.components import PositionAndAngle, PassiveComponent, ActiveComponent, VerticalMovement, Position, TiltingJaws
from src.beamline import Beamline
from src.parameters import Theta
from tests.utils import position_and_angle, position


class TestComponentBeamline(unittest.TestCase):

    def setUp(self):
        beam_start = PositionAndAngle(x=0, y=0, angle=2.5)
        s0 = PassiveComponent("s0", movement_strategy=VerticalMovement(0))
        s1 = PassiveComponent("s1", movement_strategy=VerticalMovement(1))
        frame_overlap_mirror = ActiveComponent("FOM", movement_strategy=VerticalMovement(2))
        frame_overlap_mirror.enabled = False
        self.polerising_mirror = ActiveComponent("Poleriser", movement_strategy=VerticalMovement(3))
        self.polerising_mirror.enabled = False
        s2 = PassiveComponent("s2", movement_strategy=VerticalMovement(4))
        self.ideal_sample_point = ActiveComponent("ideal sample point", movement_strategy=VerticalMovement(5))
        s3 = PassiveComponent("s3", movement_strategy=VerticalMovement(6))
        analyser = ActiveComponent("analyser", movement_strategy=VerticalMovement(7))
        analyser.enabled = False
        s4 = PassiveComponent("s4", movement_strategy=VerticalMovement(8))
        detector = PassiveComponent("detector", movement_strategy=VerticalMovement(10))

        theta = Theta("theta", self.ideal_sample_point)
        self.beamline = Beamline(
            [s0, s1, frame_overlap_mirror, self.polerising_mirror, s2,self.ideal_sample_point, s3, analyser, s4, detector],
            [theta])
        self.beamline.set_incoming_beam(beam_start)

    def test_GIVEN_beam_line_contains_multiple_component_WHEN_set_theta_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):

        theta_set = 10.0
        self.beamline.parameter("theta").sp_move = theta_set

        reflection_angle = self.ideal_sample_point.incoming_beam.angle - self.ideal_sample_point.get_outgoing_beam().angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

    def test_GIVEN_beam_line_contains_active_super_mirror_WHEN_set_theta_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):

        theta_set = 10.0
        self.polerising_mirror.enabled = True
        self.polerising_mirror.angle = 10
        self.beamline.parameter("theta").sp_move = theta_set

        reflection_angle = self.ideal_sample_point.incoming_beam.angle - self.ideal_sample_point.get_outgoing_beam().angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

    def test_GIVEN_beam_line_contains_active_super_mirror_WHEN_angle_set_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):

        theta_set = 10.0
        self.beamline.parameter("theta").sp_move = theta_set
        self.polerising_mirror.enabled = True
        self.polerising_mirror.angle = 10

        reflection_angle = self.ideal_sample_point.incoming_beam.angle - self.ideal_sample_point.get_outgoing_beam().angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

if __name__ == '__main__':
    unittest.main()
