import unittest

from math import tan, radians
from hamcrest import *

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
        expected_position = PositionAndAngle(x=jaws_x_position, y=tan(radians(beam_angle)) * distance_between, angle=150)
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

    def test_GIVEN_mirror_with_input_beam_at_60_deg_and_x0_y0_WHEN_get_beam_out_THEN_beam_output_x_is_xmirror_y_is_ymirror_angle_is_input_angle_plus_device_angle(self):
        mirror_x_position = 10
        mirror_angle = 15
        beam_angle = 60
        beam_start = PositionAndAngle(x=0, y=0, angle=beam_angle)
        expected = PositionAndAngle(x=mirror_x_position, y=tan(radians(beam_angle)) * mirror_x_position, angle= beam_angle + 2 * mirror_angle)

        mirror = ActiveComponent(movement_strategy=VerticalMovement(mirror_x_position))
        mirror.angle = mirror_angle
        mirror.set_incoming_beam(beam_start)

        result = mirror.get_outgoing_beam()

        assert_that(result, is_(position_and_angle(expected)))

    def test_GIVEN_tilting_jaw_input_beam_is_at_60_deg_WHEN_get_angle_THEN_angle_is_150_degrees(self):
        beam_angle = 60.0
        expected_angle = 60.0 + 90.0
        beam_start = PositionAndAngle(x=0, y=0, angle=beam_angle)
        jaws = TiltingJaws(movement_strategy=VerticalMovement(20))
        jaws.set_incoming_beam(beam_start)

        result = jaws.calculate_tilt_angle()

        assert_that(result, is_(expected_angle))



if __name__ == '__main__':
    unittest.main()
