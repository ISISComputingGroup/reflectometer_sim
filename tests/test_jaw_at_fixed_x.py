import unittest

from math import tan, radians, sqrt
from hamcrest import *
from parameterized import parameterized

from src.components import PositionAndAngle, PassiveComponent, ActiveComponent, VerticalMovement, Position, TiltingJaws
from tests.utils import position_and_angle, position


class TestNonTiltingJawsAtFixedX(unittest.TestCase):

    def test_GIVEN_jaw_input_beam_is_at_0_deg_and_x0_y0_WHEN_get_beam_out_THEN_beam_output_is_same_as_beam_input(self):
        jaws_x_position = 10
        beam_start = PositionAndAngle(x=0, y=0, angle=0)
        jaws = PassiveComponent(movement_strategy=VerticalMovement(jaws_x_position))
        jaws.set_incoming_beam(beam_start)

        result = jaws.get_outgoing_beam()

        assert_that(result, is_(position_and_angle(beam_start)))

    def test_GIVEN_jaw_at_10_input_beam_is_at_0_deg_and_x0_y0_WHEN_get_position_THEN_x_is_jaw_position_y_is_0(self):
        jaws_x_position = 10
        beam_start = PositionAndAngle(x=0, y=0, angle=0)
        expected_position = Position(x=jaws_x_position, y=0)
        jaws = PassiveComponent(movement_strategy=VerticalMovement(jaws_x_position))
        jaws.set_incoming_beam(beam_start)

        result = jaws.calculate_beam_interception()

        assert_that(result, is_(position(expected_position)))

    def test_GIVEN_jaw_at_10_input_beam_is_at_60_deg_and_x0_y0_WHEN_get_position_THEN_x_is_jaw_position_y_is_at_tan60_times_10(self):
        jaws_x_position = 10.0
        beam_angle = 60.0
        beam_start = PositionAndAngle(x=0, y=0, angle=beam_angle)
        expected_position = Position(x=jaws_x_position, y=tan(radians(beam_angle)) * jaws_x_position)
        jaws = PassiveComponent(movement_strategy=VerticalMovement(jaws_x_position))
        jaws.set_incoming_beam(beam_start)

        result = jaws.calculate_beam_interception()

        assert_that(result, is_(position(expected_position)))

    def test_GIVEN_jaw_at_10_input_beam_is_at_60_deg_and_x5_y30_WHEN_get_position_THEN_x_is_jaw_position_y_is_at_tan60_times_distance_between_input_beam_and_component(self):
        distance_between = 5.0
        start_x = 5.0
        start_y = 30
        beam_angle = 60.0
        jaws_x_position = distance_between + start_x
        beam_start = PositionAndAngle(x=start_x, y=start_y, angle=beam_angle)
        expected_position = Position(x=jaws_x_position, y=tan(radians(beam_angle)) * distance_between)
        jaws = PassiveComponent(movement_strategy=VerticalMovement(jaws_x_position))
        jaws.set_incoming_beam(beam_start)

        result = jaws.calculate_beam_interception()

        assert_that(result, is_(position(expected_position)))


    def test_GIVEN_mirror_with_input_beam_at_0_deg_and_x0_y0_WHEN_get_beam_out_THEN_beam_output_x_is_xmirror_y_is_ymirror_angle_is_input_angle_plus_device_angle(self):
        mirror_x_position = 10
        mirror_angle = 15
        beam_start = PositionAndAngle(x=0, y=0, angle=0)
        expected = PositionAndAngle(x=mirror_x_position, y=0, angle=2 * mirror_angle)

        mirror = ActiveComponent(movement_strategy=VerticalMovement(mirror_x_position))
        mirror.angle = mirror_angle
        mirror.set_incoming_beam(beam_start)

        result = mirror.get_outgoing_beam()

        assert_that(result, is_(position_and_angle(expected)))

    @parameterized.expand([(-30, 60, 150),
                           (0, 0, 0),
                           (30, 30, 30),
                           (0, 90, 180),
                           (-40, -30, -20)])
    def test_GIVEN_mirror_with_input_beam_at_WHEN_get_beam_out_THEN_beam_output_correct(self, beam_angle, mirror_angle, outgoing_angle):
        beam_start = PositionAndAngle(x=0, y=0, angle=beam_angle)
        expected = PositionAndAngle(x=0, y=0, angle=outgoing_angle)

        mirror = ActiveComponent(movement_strategy=VerticalMovement(0))
        mirror.angle = mirror_angle
        mirror.set_incoming_beam(beam_start)

        result = mirror.get_outgoing_beam()

        assert_that(result, is_(position_and_angle(expected)), "beam_angle: {}, mirror_angle: {}".format(beam_angle, mirror_angle))


    def test_GIVEN_tilting_jaw_input_beam_is_at_60_deg_WHEN_get_angle_THEN_angle_is_150_degrees(self):
        beam_angle = 60.0
        expected_angle = 60.0 + 90.0
        beam_start = PositionAndAngle(x=0, y=0, angle=beam_angle)
        jaws = TiltingJaws(movement_strategy=VerticalMovement(20))
        jaws.set_incoming_beam(beam_start)

        result = jaws.calculate_tilt_angle()

        assert_that(result, is_(expected_angle))

    def test_GIVEN_angled_mirror_is_disabled_WHEN_get_beam_out_THEN_outgoing_beam_is_incoming_beam(self):
        mirror_x_position = 10
        mirror_angle = 15
        beam_start = PositionAndAngle(x=0, y=0, angle=0)
        expected = beam_start

        mirror = ActiveComponent(movement_strategy=VerticalMovement(mirror_x_position))
        mirror.angle = mirror_angle
        mirror.set_incoming_beam(beam_start)
        mirror.enabled = False

        result = mirror.get_outgoing_beam()

        assert_that(result, is_(position_and_angle(expected)))



    # def test_GIVEN_bench_at_radius_10_input_beam_is_at_0_deg_and_x0_y0_WHEN_get_position_THEN_x_is_10_y_is_0(self):
    #     bench_center_of_rotation = Position(10, 0)
    #     bench_radius = 10
    #     beam_start = PositionAndAngle(x=0, y=0, angle=0)
    #     expected_position = Position(x=bench_center_of_rotation.x + bench_radius, y=0)
    #     bench = PassiveComponent(movement_strategy=ArcMovement(bench_center_of_rotation, bench_radius))
    #     bench.set_incoming_beam(beam_start)
    #
    #     result = bench.calculate_beam_interception()
    #
    #     assert_that(result, is_(position(expected_position)))
    #
    # def test_GIVEN_bench_at_radius_10_input_beam_is_at_45_deg_and_x0_y0_WHEN_get_position_THEN_x_is_10_root2_y_is_10_root2(self):
    #     bench_center_of_rotation = Position(10, 0)
    #     bench_radius = 10
    #     beam_start = PositionAndAngle(x=0, y=0, angle=0)
    #     expected_position = Position(x=(bench_center_of_rotation.x + bench_radius) * sqrt(2), y=(bench_center_of_rotation.x + bench_radius) * sqrt(2))
    #     bench = PassiveComponent(movement_strategy=ArcMovement(bench_center_of_rotation, bench_radius))
    #     bench.set_incoming_beam(beam_start)
    #
    #     result = bench.calculate_beam_interception()
    #
    #     assert_that(result, is_(position(expected_position)))


if __name__ == '__main__':
    unittest.main()
