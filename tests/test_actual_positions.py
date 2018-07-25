import unittest

from math import tan, radians
from hamcrest import *

from src.components import PositionAndAngle, PassiveComponent, ActiveComponent, VerticalMovement, Position, TiltingJaws, \
    Beamline
from tests.utils import position_and_angle, position


class TestComponentBeamline(unittest.TestCase):

    def test_GIVEN_beam_line_contains_multiple_component_WHEN_beam_set_THEN_each_component_has_beam_out_which_is_effected_by_each_component_in_turn(self):
        beam_start = PositionAndAngle(x=0, y=0, angle=0)
        jaws = PassiveComponent(movement_strategy=VerticalMovement(0))
        mirror_position = 10
        mirror = ActiveComponent(movement_strategy=VerticalMovement(mirror_position))
        mirror.angle = 45
        jaws3 = PassiveComponent(movement_strategy=VerticalMovement(20))
        beamline = Beamline([jaws, mirror, jaws3])
        beamline.set_incoming_beam(beam_start)
        bounced_beam = PositionAndAngle(x=mirror_position, y=0, angle=mirror.angle * 2)
        expected_beams = [beam_start, bounced_beam, bounced_beam]


        beamline.theta.set(10)

        assert that the incoming and out beam angles == 10

        results = [component.get_outgoing_beam() for component in beamline]

        for index, (result, expected_beam) in enumerate(zip(results, expected_beams)):
            assert_that(result, position_and_angle(expected_beam), "in component {}".format(index))

if __name__ == '__main__':
    unittest.main()
