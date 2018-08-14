import unittest

from math import tan, radians, sqrt
from hamcrest import *
from parameterized import parameterized

from src.components import LinearMovement, PositionAndAngle, Position, TOLERANCE
from tests.utils import position_and_angle, position


class TestMovementIntercept(unittest.TestCase):

    def test_GIVEN_movement_and_beam_at_the_same_angle_WHEN_get_intercept_THEN_raises_calc_error(self):
        angle = 12.3
        movement = LinearMovement(1, 1, angle)
        beam = PositionAndAngle(0, 0, angle)

        assert_that(calling(movement.calculate_interception).with_args(beam), raises(ValueError))

    def test_GIVEN_movement_and_beam_at_the_same_angle_within_tolerance_WHEN_get_intercept_THEN_raises_calc_error(self):
        angle = 12.3
        tolerance = TOLERANCE
        movement = LinearMovement(1, 1, angle + tolerance * 0.99)
        beam = PositionAndAngle(0, 0, angle)

        assert_that(calling(movement.calculate_interception).with_args(beam), raises(ValueError))

    def test_GIVEN_movement_and_beam_at_the_opposite_angles_within_tolerance_WHEN_get_intercept_THEN_raises_calc_error(self):
        angle = 12.3 + 180.0
        tolerance = TOLERANCE
        movement = LinearMovement(1, 1, angle + tolerance * 0.99)
        beam = PositionAndAngle(0, 0, angle)

        assert_that(calling(movement.calculate_interception).with_args(beam), raises(ValueError))

    def test_GIVEN_movement_perpendicular_to_z_at_beam_angle_0_WHEN_get_intercept_THEN_position_is_initial_position(self):
        y = 0
        z = 10
        movement = LinearMovement(y, z, 90)
        beam = PositionAndAngle(0, 0, 0)

        result = movement.calculate_interception(beam)

        assert_that(result, is_(position(Position(y, z))))

    def test_GIVEN_movement_perpendicular_to_z_at_beam_angle_10_WHEN_get_intercept_THEN_position_is_z_as_initial_y_as_right_angle_triangle(self):
        y = 0
        z = 10
        beam_angle = 10
        movement = LinearMovement(y, z, 90)
        beam = PositionAndAngle(0, 0, beam_angle)
        expected_y = z * tan(radians(beam_angle))

        result = movement.calculate_interception(beam)

        assert_that(result, is_(position(Position(expected_y, z))))

    def test_GIVEN_movement_anti_perpendicular_to_z_at_beam_angle_10_WHEN_get_intercept_THEN_position_is_z_as_initial_y_as_right_angle_triangle(self):
        y = 0
        z = 10
        beam_angle = 10
        movement = LinearMovement(y, z, -90)
        beam = PositionAndAngle(0, 0, beam_angle)
        expected_y = z * tan(radians(beam_angle))

        result = movement.calculate_interception(beam)

        assert_that(result, is_(position(Position(expected_y, z))))

    def test_GIVEN_beam_perpendicular_to_z_at_movement_angle_10_WHEN_get_intercept_THEN_position_is_z_as_initial_y_as_right_angle_triangle(self):
        y = 0
        z = 10
        angle = 10
        movement = LinearMovement(y, z, angle)
        beam_z = 0
        beam = PositionAndAngle(1, beam_z, 90)
        expected_y = -z * tan(radians(angle))

        result = movement.calculate_interception(beam)

        assert_that(result, is_(position(Position(expected_y, beam_z))))

    @parameterized.expand([(180,), (0,)])
    def test_GIVEN_movement_45_to_z_at_beam_angle_along_z_WHEN_get_intercept_THEN_position_is_initial_position(self, angle):
        y = 0
        z = 10
        movement = LinearMovement(y, z, 45)
        beam = PositionAndAngle(0, 0, angle)

        result = movement.calculate_interception(beam)

        assert_that(result, is_(position(Position(y, z))))

    def test_GIVEN_movement_0_to_z_and_beam_angle_45_WHEN_get_intercept_THEN_position_is_on_movement_axis(self):
        y = 20
        z = 10
        movement = LinearMovement(y, z, 0)
        beam = PositionAndAngle(0, 0, 45)
        expected_y = y
        expected_z = y

        result = movement.calculate_interception(beam)

        assert_that(result, is_(position(Position(expected_y, expected_z))))

    def test_GIVEN_movement_20_to_z_and_beam_angle_45_WHEN_get_intercept_THEN_position_is_on_movement_axis(self):
        beam = PositionAndAngle(0, 0, 45)
        expected_y = 4
        expected_z = 4

        move_angle = 20
        move_z = 2
        move_y = expected_y - (expected_z - move_z) * tan(radians(move_angle))
        movement = LinearMovement(move_y, move_z, move_angle)

        result = movement.calculate_interception(beam)

        assert_that(result, is_(position(Position(expected_y, expected_z))))


class TestMovementRelativeToBeam(unittest.TestCase):

    def test_GIVEN_movement_along_y_WHEN_set_position_relative_to_beam_to_0_THEN_position_is_at_intercept(self):
        movement = LinearMovement(0, 10, 90)
        beam_intercept = Position(0, 10)
        dist = 0

        movement.set_position_relative_to_beam(beam_intercept, dist)
        result = movement.sp_position()

        assert_that(result, is_(position(Position(beam_intercept.y, beam_intercept.z))))

    def test_GIVEN_movement_along_y_WHEN_set_position_relative_to_beam_to_10_THEN_position_is_at_10_above_intercept(self):
        movement = LinearMovement(0, 10, 90)
        beam_intercept = Position(0, 10)
        dist = 10

        movement.set_position_relative_to_beam(beam_intercept, dist)
        result = movement.sp_position()

        assert_that(result, is_(position(Position(beam_intercept.y + dist , beam_intercept.z))))

    def test_GIVEN_movement_along_z_WHEN_set_position_relative_to_beam_to_10_THEN_position_is_at_10_along_intercept(self):
        movement = LinearMovement(0, 10, 0)
        beam_intercept = Position(0, 10)
        dist = 10

        movement.set_position_relative_to_beam(beam_intercept, dist)
        result = movement.sp_position()

        assert_that(result, is_(position(Position(beam_intercept.y, beam_intercept.z + dist))))

    def test_GIVEN_movement_at_30_to_z_WHEN_set_position_relative_to_beam_to_10_THEN_position_is_at_10_along_intercept(self):
        movement = LinearMovement(0, 10, 30)
        beam_intercept = Position(2, 10)
        dist = 10

        movement.set_position_relative_to_beam(beam_intercept, dist)
        result = movement.sp_position()

        assert_that(result, is_(position(Position(beam_intercept.y + dist/2.0, beam_intercept.z + dist * sqrt(3)/2.0))))

if __name__ == '__main__':
    unittest.main()
