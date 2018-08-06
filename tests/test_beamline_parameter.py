import unittest
from collections import OrderedDict

from hamcrest import *

from src.beamline import Beamline, BeamlineMode
from src.components import PositionAndAngle, ActiveComponent, VerticalMovement, PassiveComponent, Position
from src.parameters import Theta, ReflectionAngle, TrackingPosition
from tests.utils import position


class TestBeamlineParameter(unittest.TestCase):

    def test_GIVEN_theta_WHEN_set_set_point_THEN_readback_is_as_set_and_sample_hasnt_moved(self):

        theta_set = 10.0
        sample = ActiveComponent("sample", movement_strategy=VerticalMovement(0))
        mirror_pos = -100
        sample.angle = mirror_pos
        theta = Theta("theta", sample)

        theta.sp = theta_set
        result = theta.sp_rbv

        assert_that(result, is_(theta_set))
        assert_that(sample.angle, is_(mirror_pos))

    def test_GIVEN_theta_WHEN_set_set_point_and_move_THEN_readback_is_as_set_and_sample_is_at_setpoint_postion(self):

        theta_set = 10.0
        expected_sample_angle = -10.0
        sample = ActiveComponent("sample", movement_strategy=VerticalMovement(0))
        sample.set_incoming_beam(PositionAndAngle(0, 0, 0))
        mirror_pos = -100
        sample.angle = mirror_pos
        theta = Theta("theta", sample)

        theta.sp = theta_set
        theta.move = 1
        result = theta.sp_rbv

        assert_that(result, is_(theta_set))
        assert_that(sample.angle, is_(expected_sample_angle))

    def test_GIVEN_theta_and_a_set_but_no_move_WHEN_get_changed_THEN_changed_is_true(self):

        theta_set = 10.0
        sample = ActiveComponent("sample", movement_strategy=VerticalMovement(0))
        theta = Theta("theta",sample)

        theta.sp = theta_set
        result = theta.sp_changed

        assert_that(result, is_(True))

    def test_GIVEN_theta_and_a_set_and_move_WHEN_get_changed_THEN_changed_is_false(self):

        theta_set = 10.0
        sample = ActiveComponent("sample", movement_strategy=VerticalMovement(0))
        sample.set_incoming_beam(PositionAndAngle(0, 0, 0))
        theta = Theta("theta",sample)

        theta.sp = theta_set
        theta.move = 1
        result = theta.sp_changed

        assert_that(result, is_(False))

    def test_GIVEN_reflection_angle_WHEN_set_set_point_and_move_THEN_readback_is_as_set_and_sample_is_at_setpoint_postion(self):

        angle_set = 10.0
        expected_sample_angle = -10.0
        sample = ActiveComponent("sample", movement_strategy=VerticalMovement(0))
        sample.set_incoming_beam(PositionAndAngle(0, 0, 0))
        mirror_pos = -100
        sample.angle = mirror_pos
        reflection_angle = ReflectionAngle("theta",sample)

        reflection_angle.sp = angle_set
        reflection_angle.move = 1
        result = reflection_angle.sp_rbv

        assert_that(result, is_(angle_set))
        assert_that(sample.angle, is_(expected_sample_angle))

    def test_GIVEN_jaw_height_WHEN_set_set_point_and_move_THEN_readback_is_as_set_and_jaws_are_at_setpoint_postion(self):

        height_set = 10.0
        beam_height = 5
        expected_height = beam_height + height_set
        jaws_x = 5
        jaws = PassiveComponent("jaws", movement_strategy=VerticalMovement(jaws_x))
        jaws.set_incoming_beam(PositionAndAngle(0, beam_height, 0))
        tracking_height = TrackingPosition("theta",jaws)

        tracking_height.sp = height_set
        tracking_height.move = 1
        result = tracking_height.sp_rbv

        assert_that(result, is_(height_set))
        assert_that(jaws.sp_position().y, is_(expected_height))
        assert_that(jaws.sp_position().x, is_(jaws_x))


class TestBeamlineModes(unittest.TestCase):

    def test_GIVEN_unpolarised_mode_and_beamline_parameters_are_set_WHEN_move_THEN_components_move_onto_beam_line(self):
        slit2 = PassiveComponent("s2", VerticalMovement(x_position=10))
        ideal_sample_point = ActiveComponent("ideal_sample_point", VerticalMovement(x_position=20))
        detector = PassiveComponent("detector", VerticalMovement(x_position=30))
        components = [slit2, ideal_sample_point, detector]

        parameters = [
            TrackingPosition("slit2height", slit2),
            TrackingPosition("height", ideal_sample_point),
            Theta("theta", ideal_sample_point),
            TrackingPosition("detectorheight", detector)]
                      #parameters["detectorAngle": TrackingAngle(detector)
        beam = PositionAndAngle(0, 0, 45)
        beamline = Beamline(components, parameters)
        beamline.mode = BeamlineMode.NEUTRON_REFLECTION
        beamline.parameter("theta").sp = 45
        beamline.parameter("height").sp = 0
        beamline.parameter("slit2height").sp = 0
        beamline.parameter("detectorheight").sp = 0
        beamline.set_incoming_beam(beam)

        beamline.move = 1

        assert_that(slit2.sp_position(), is_(position(Position(10, -10))))
        assert_that(ideal_sample_point.sp_position(), is_(position(Position(20, -20))))
        assert_that(detector.sp_position(), is_(position(Position(30, -10))))

    def test_GIVEN_a_mode_with_a_single_beamline_parameter_in_WHEN_move_THEN_beamline_parameter_is_calculated_on_move(self):
        ideal_sample_point = ActiveComponent("ideal_sample_point", VerticalMovement(x_position=20))
        theta = Theta("theta", ideal_sample_point)
        beamline_mode = BeamlineMode("mode name", [theta.name], [ideal_sample_point.name])
        beamline = Beamline([ideal_sample_point], [theta], beamline_mode)


if __name__ == '__main__':
    unittest.main()
