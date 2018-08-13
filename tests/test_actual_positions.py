import unittest

from math import tan, radians
from hamcrest import *

from src.components import PositionAndAngle, PassiveComponent, ActiveComponent, VerticalMovement, Position, TiltingJaws
from src.beamline import Beamline, BeamlineMode
from src.parameters import Theta, ReflectionAngle
from tests.utils import position_and_angle, position


class TestComponentBeamline(unittest.TestCase):

    def setUp(self):
        beam_start = PositionAndAngle(x=0, y=0, angle=2.5)
        s0 = PassiveComponent("s0", movement_strategy=VerticalMovement(0))
        s1 = PassiveComponent("s1", movement_strategy=VerticalMovement(1))
        frame_overlap_mirror = ActiveComponent("FOM", movement_strategy=VerticalMovement(2))
        frame_overlap_mirror.enabled = False
        self.polarising_mirror = ActiveComponent("Polariser", movement_strategy=VerticalMovement(3))
        self.polarising_mirror.enabled = False
        self.polarising_mirror.angle = 0
        s2 = PassiveComponent("s2", movement_strategy=VerticalMovement(4))
        self.ideal_sample_point = ActiveComponent("ideal sample point", movement_strategy=VerticalMovement(5))
        s3 = PassiveComponent("s3", movement_strategy=VerticalMovement(6))
        analyser = ActiveComponent("analyser", movement_strategy=VerticalMovement(7))
        analyser.enabled = False
        s4 = PassiveComponent("s4", movement_strategy=VerticalMovement(8))
        detector = PassiveComponent("detector", movement_strategy=VerticalMovement(10))

        theta = Theta("theta", self.ideal_sample_point)
        theta.sp = 0
        smangle = ReflectionAngle("smangle", self.polarising_mirror)
        smangle.sp = 0
        self.beamline = Beamline(
            [s0, s1, frame_overlap_mirror, self.polarising_mirror, s2, self.ideal_sample_point, s3, analyser, s4, detector],
            [smangle, theta])
        self.beamline.set_incoming_beam(beam_start)
        self.nr_mode = BeamlineMode("NR Mode", [theta.name])
        self.polarised_mode = BeamlineMode("NR Mode", [smangle.name, theta.name])

    def test_GIVEN_beam_line_contains_multiple_component_WHEN_set_theta_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):
        self.beamline.mode = self.nr_mode

        theta_set = 10.0
        self.beamline.parameter("theta").sp_move = theta_set

        reflection_angle = self.ideal_sample_point.incoming_beam.angle - self.ideal_sample_point.get_outgoing_beam().angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

    def test_GIVEN_beam_line_contains_active_super_mirror_WHEN_set_theta_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):
        self.beamline.mode = self.polarised_mode
        theta_set = 10.0
        self.polarising_mirror.enabled = True
        self.beamline.parameter("smangle").sp_move = 10

        self.beamline.parameter("theta").sp_move = theta_set

        reflection_angle = self.ideal_sample_point.incoming_beam.angle - self.ideal_sample_point.get_outgoing_beam().angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

    def test_GIVEN_beam_line_contains_active_super_mirror_WHEN_angle_set_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):
        self.beamline.mode = self.polarised_mode
        theta_set = 10.0
        self.beamline.parameter("theta").sp_move = theta_set
        self.polarising_mirror.enabled = True


        self.beamline.parameter("smangle").sp_move = 10

        reflection_angle = self.ideal_sample_point.incoming_beam.angle - self.ideal_sample_point.get_outgoing_beam().angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

if __name__ == '__main__':
    unittest.main()
