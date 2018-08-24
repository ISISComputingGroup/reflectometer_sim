import unittest
from math import fabs
from mock import MagicMock, PropertyMock
from hamcrest import *

from src.components import PassiveComponent, TiltingJaws, LinearMovement, PositionAndAngle
from src.ioc_driver import HeightDriver, HeightAndTiltDriver


FLOAT_TOLERANCE = 1e-9


class TestHeightDriver(unittest.TestCase):

    def setUp(self):
        start_position = 0.0
        max_velocity = 10.0
        self.height_axis = MagicMock()
        self.height_axis.name = "JAWS:HEIGHT"
        self.height_axis.value = start_position
        self.height_axis.max_velocity = max_velocity

        self.jaws = PassiveComponent("component", movement_strategy=LinearMovement(0.0, 10.0, 90.0))
        self.jaws.set_incoming_beam(PositionAndAngle(0.0, 0.0, 0.0))

        self.jaws_driver = HeightDriver(self.jaws, self.height_axis)

    def test_GIVEN_component_with_height_setpoint_above_current_position_WHEN_calculating_move_duration_THEN_returned_duration_is_correct(self):
        target_position = 20.0
        expected = 2.0
        self.jaws.set_position_relative_to_beam(target_position)

        result = self.jaws_driver.get_max_move_duration()

        assert_that(result, is_(expected))

    def test_GIVEN_component_with_height_setpoint_below_current_position_WHEN_calculating_move_duration_THEN_returned_duration_is_correct(self):
        target_position = -20.0
        expected = 2.0
        self.jaws.set_position_relative_to_beam(target_position)

        result = self.jaws_driver.get_max_move_duration()

        assert_that(result, is_(expected))

    def test_GIVEN_move_duration_and_target_position_set_WHEN_moving_axis_THEN_computed_axis_velocity_is_correct_and_setpoint_set(self):
        target_position = 20.0
        target_duration = 4.0
        expected_velocity = 5.0
        self.jaws.set_position_relative_to_beam(target_position)

        self.jaws_driver.perform_move(target_duration)

        assert_that(self.height_axis.velocity, is_(expected_velocity))
        assert_that(self.height_axis.value, is_(target_position))


    # def test_GIVEN_component_has_not_changed_WHEN_moving_axis_THEN_no_pv_value_set(self):
    #     prop =PropertyMock(return_value=0.0)
    #     type(self.height_axis).value = prop
    #
    #     self.jaws_driver.perform_move(10.0)
    #
    #     prop.assert_not_called()
    #

class TestHeightAndTiltDriver(unittest.TestCase):
    def setUp(self):
        start_position_height = 0.0
        max_velocity_height = 10.0
        self.height_axis = MagicMock()
        self.height_axis.name = "JAWS:HEIGHT"
        self.height_axis.value = start_position_height
        self.height_axis.max_velocity = max_velocity_height

        start_position_tilt = 90.0
        max_velocity_tilt = 10.0
        self.tilt_axis = MagicMock()
        self.tilt_axis.name = "JAWS:TILT"
        self.tilt_axis.value = start_position_tilt
        self.tilt_axis.max_velocity = max_velocity_tilt

        self.tilting_jaws = TiltingJaws("component", movement_strategy=LinearMovement(0.0, 10.0, 90.0))

        self.jaws_driver = HeightAndTiltDriver(self.tilting_jaws, self.height_axis, self.tilt_axis)

    def test_GIVEN_multiple_axes_need_to_move_WHEN_computing_move_duration_THEN_maximum_duration_is_returned(self):
        beam_angle = 45.0
        expected = 4.5
        beam = PositionAndAngle(0.0, 0.0, beam_angle)
        self.tilting_jaws.set_incoming_beam(beam)
        self.tilting_jaws.set_position_relative_to_beam(0.0)  # move component into beam

        result = self.jaws_driver.get_max_move_duration()

        assert_that(result, is_(expected))

    def test_GIVEN_move_duration_and_target_position_set_WHEN_moving_multiple_axes_THEN_computed_axis_velocity_is_correct_and_setpoint_set_for_all_axes(self):
        beam_angle = 45.0
        beam = PositionAndAngle(0.0, 0.0, beam_angle)
        target_duration = 10.0
        expected_velocity_height = 1.0
        target_position_height = 10.0
        expected_velocity_tilt = 4.5
        target_position_tilt = 135.0
        self.tilting_jaws.set_incoming_beam(beam)
        self.tilting_jaws.set_position_relative_to_beam(0.0)  # move component into beam

        self.jaws_driver.perform_move(target_duration)

        assert_that(fabs(self.height_axis.velocity - expected_velocity_height) <= FLOAT_TOLERANCE)
        assert_that(fabs(self.height_axis.value - target_position_height) <= FLOAT_TOLERANCE)
        assert_that(fabs(self.tilt_axis.velocity - expected_velocity_tilt) <= FLOAT_TOLERANCE)
        assert_that(fabs(self.tilt_axis.value - target_position_tilt) <= FLOAT_TOLERANCE)

    # TODO ???
    def test_GIVEN_target_move_duration_too_short_WHEN_moving_axes_THEN_complain(self):
        pass
