from src.beamline import Beamline
from src.components import PositionAndAngle, PassiveComponent, VerticalMovement, ActiveComponent
from src.parameters import Theta


def create_beamline():
    beam_start = PositionAndAngle(x=0, y=0, angle=2.5)
    s0 = PassiveComponent(movement_strategy=VerticalMovement(0))
    s1 = PassiveComponent(movement_strategy=VerticalMovement(1))
    frame_overlap_mirror = ActiveComponent(movement_strategy=VerticalMovement(2))
    frame_overlap_mirror.enabled = False
    polerising_mirror = ActiveComponent(movement_strategy=VerticalMovement(3))
    polerising_mirror.enabled = False
    s2 = PassiveComponent(movement_strategy=VerticalMovement(4))
    ideal_sample_point = ActiveComponent(movement_strategy=VerticalMovement(5))
    s3 = PassiveComponent(movement_strategy=VerticalMovement(6))
    analyser = ActiveComponent(movement_strategy=VerticalMovement(7))
    analyser.enabled = False
    s4 = PassiveComponent(movement_strategy=VerticalMovement(8))
    detector = PassiveComponent(movement_strategy=VerticalMovement(10))

    theta = Theta(ideal_sample_point)
    beamline = Beamline(
        [s0, s1, frame_overlap_mirror, polerising_mirror, s2, ideal_sample_point, s3, analyser, s4, detector],
        {"theta": theta})
    beamline.set_incoming_beam(beam_start)

    return beamline

def generate_theta_movement():
    beamline = create_beamline()
    positions_x = [component.calculate_beam_interception().x for component in beamline]
    positions_x.insert(0, "x position")
    positions = [
        positions_x,
    ]
    for theta in range(0, 40, 2):
        beamline.parameter("theta").set(theta * 1.0)
        positions_y = [component.calculate_beam_interception().y for component in beamline]
        positions_y.insert(0, "theta {}".format(theta))
        positions.append(positions_y)

    return positions


if __name__ == '__main__':
    thetas = generate_theta_movement()

    with open("example.csv", mode="w") as f:
        for theta in thetas:
            f.write(", ".join([str(v) for v in theta]))
            f.write("\n")
