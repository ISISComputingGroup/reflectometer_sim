import unittest

from hamcrest import *

from src.components import PositionAndAngle, ActiveComponent, VerticalMovement
from src.parameters import Theta


class TestComponentBeamline(unittest.TestCase):

    def test_GIVEN_theta_WHEN_set_set_point_THEN_readback_is_as_set_sample_hasnt_moved(self):

        theta_set = 10.0
        sample = ActiveComponent(movement_strategy=VerticalMovement(0))
        mirror_pos = -100
        sample.angle = mirror_pos
        theta = Theta(sample)

        theta.sp = theta_set
        result = theta.sp_rbv

        assert_that(result, is_(theta_set))
        assert_that(sample.angle, is_(mirror_pos))

    def test_GIVEN_theta_WHEN_set_set_point_and_move_THEN_readback_is_as_set_sample_is_at_setpoint_postion(self):

        theta_set = 10.0
        expected_sample_angle = -10.0
        sample = ActiveComponent(movement_strategy=VerticalMovement(0))
        sample.set_incoming_beam(PositionAndAngle(0, 0, 0))
        mirror_pos = -100
        sample.angle = mirror_pos
        theta = Theta(sample)

        theta.sp = theta_set
        theta.move = 1
        result = theta.sp_rbv

        assert_that(result, is_(theta_set))
        assert_that(sample.angle, is_(expected_sample_angle))

    def test_GIVEN_theta_and_a_set_but_no_move_WHEN_get_changed_THEN_changed_is_true(self):

        theta_set = 10.0
        sample = ActiveComponent(movement_strategy=VerticalMovement(0))
        theta = Theta(sample)

        theta.sp = theta_set
        result = theta.sp_changed

        assert_that(result, is_(True))

    def test_GIVEN_theta_and_a_set_and_move_WHEN_get_changed_THEN_changed_is_false(self):

        theta_set = 10.0
        sample = ActiveComponent(movement_strategy=VerticalMovement(0))
        sample.set_incoming_beam(PositionAndAngle(0, 0, 0))
        theta = Theta(sample)

        theta.sp = theta_set
        theta.move = 1
        result = theta.sp_changed

        assert_that(result, is_(False))



if __name__ == '__main__':
    unittest.main()
