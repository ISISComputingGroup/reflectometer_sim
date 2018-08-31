import unittest

from hamcrest import *

from src.components import PositionAndAngle, PassiveComponent, ActiveComponent, LinearMovement
from src.beamline import Beamline, BeamlineMode
from src.parameters import Theta, ReflectionAngle


class TestComponentBeamline(unittest.TestCase):

    def setUp(self):
        beam_start = PositionAndAngle(y=0, z=0, angle=2.5)
        s0 = PassiveComponent("s0", movement_strategy=LinearMovement(0, 0, 90))
        s1 = PassiveComponent("s1", movement_strategy=LinearMovement(0, 1, 90))
        frame_overlap_mirror = ActiveComponent("FOM", movement_strategy=LinearMovement(0, 2, 90))
        frame_overlap_mirror.enabled = False
        self.polarising_mirror = ActiveComponent("Polariser", movement_strategy=LinearMovement(0, 3, 90))
        self.polarising_mirror.enabled = False
        self.polarising_mirror.angle = 0
        s2 = PassiveComponent("s2", movement_strategy=LinearMovement(0, 4, 90))
        self.ideal_sample_point = ActiveComponent("ideal sample point", movement_strategy=LinearMovement(0, 5, 90))
        s3 = PassiveComponent("s3", movement_strategy=LinearMovement(0, 6, 90))
        analyser = ActiveComponent("analyser", movement_strategy=LinearMovement(0, 7, 90))
        analyser.enabled = False
        s4 = PassiveComponent("s4", movement_strategy=LinearMovement(0, 8, 90))
        detector = PassiveComponent("detector", movement_strategy=LinearMovement(0, 10, 90))

        theta = Theta("theta", self.ideal_sample_point)
        theta.sp_no_move = 0
        smangle = ReflectionAngle("smangle", self.polarising_mirror)
        smangle.sp_no_move = 0
        self.beamline = Beamline(
            [s0, s1, frame_overlap_mirror, self.polarising_mirror, s2, self.ideal_sample_point, s3, analyser, s4, detector],
            [smangle, theta], [])
        self.beamline.set_incoming_beam(beam_start)
        self.nr_mode = BeamlineMode("NR Mode", [theta.name])
        self.polarised_mode = BeamlineMode("NR Mode", [smangle.name, theta.name])

    def test_GIVEN_beam_line_contains_multiple_component_WHEN_set_theta_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):
        self.beamline.active_mode = self.nr_mode

        theta_set = 10.0
        self.beamline.parameter("theta").sp = theta_set

        reflection_angle = self.ideal_sample_point.get_outgoing_beam().angle - self.ideal_sample_point.incoming_beam.angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

    def test_GIVEN_beam_line_contains_active_super_mirror_WHEN_set_theta_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):
        self.beamline.active_mode = self.polarised_mode
        theta_set = 10.0
        self.polarising_mirror.enabled = True
        self.beamline.parameter("smangle").sp = 10

        self.beamline.parameter("theta").sp = theta_set

        reflection_angle = self.ideal_sample_point.get_outgoing_beam().angle - self.ideal_sample_point.incoming_beam.angle
        assert_that(reflection_angle, is_(theta_set * 2.0))

    def test_GIVEN_beam_line_contains_active_super_mirror_WHEN_angle_set_THEN_angle_between_incoming_and_outgoing_beam_is_correct(self):
        self.beamline.active_mode = self.polarised_mode
        theta_set = 10.0
        self.beamline.parameter("theta").sp = theta_set
        self.polarising_mirror.enabled = True

        self.beamline.parameter("smangle").sp = 10

        reflection_angle = self.ideal_sample_point.get_outgoing_beam().angle - self.ideal_sample_point.incoming_beam.angle
        assert_that(reflection_angle, is_(theta_set * 2.0))


if __name__ == '__main__':
    unittest.main()
