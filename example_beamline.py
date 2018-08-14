from src.beamline import Beamline, BeamlineMode
from src.components import PositionAndAngle, PassiveComponent, ActiveComponent, LinearMovement
from src.parameters import Theta


def create_beamline():
    perp_to_floor = 90.0
    beam_start = PositionAndAngle(y=0, z=0, angle=-2.5)
    s0 = PassiveComponent("s0", movement_strategy=LinearMovement(0, 0, perp_to_floor))
    s1 = PassiveComponent("s1", movement_strategy=LinearMovement(0, 1, perp_to_floor))
    frame_overlap_mirror = ActiveComponent("FOM", movement_strategy=LinearMovement(0, 2, perp_to_floor))
    frame_overlap_mirror.enabled = False
    polarising_mirror = ActiveComponent("Polarising mirror", movement_strategy=LinearMovement(0, 3, perp_to_floor))
    polarising_mirror.enabled = False
    s2 = PassiveComponent("s2", movement_strategy=LinearMovement(0, 4, perp_to_floor))
    ideal_sample_point = ActiveComponent("Ideal Sample Point", movement_strategy=LinearMovement(0, 5, perp_to_floor))
    s3 = PassiveComponent("s3", movement_strategy=LinearMovement(0, 6, perp_to_floor))
    analyser = ActiveComponent("analyser", movement_strategy=LinearMovement(0, 7, perp_to_floor))
    analyser.enabled = False
    s4 = PassiveComponent("s4", movement_strategy=LinearMovement(0, 8, perp_to_floor))
    detector = PassiveComponent("detector", movement_strategy=LinearMovement(0, 10, perp_to_floor))

    theta = Theta("theta", ideal_sample_point)
    beamline = Beamline(
        [s0, s1, frame_overlap_mirror, polarising_mirror, s2, ideal_sample_point, s3, analyser, s4, detector],
        [theta])
    beamline.set_incoming_beam(beam_start)
    beamline.mode = BeamlineMode("NR", ["theta"])

    return beamline


def generate_theta_movement():
    beamline = create_beamline()
    positions_z = [component.calculate_beam_interception().z for component in beamline]
    positions_z.insert(0, "z position")
    positions = [
        positions_z,
    ]
    for theta in range(0, 20, 1):
        beamline.parameter("theta").sp_move = theta * 1.0
        positions_y = [component.calculate_beam_interception().y for component in beamline]
        positions_y.insert(0, "theta {}".format(theta))
        positions.append(positions_y)

    beamline[3].enabled = True
    sm_angle = 5
    beamline[3].angle = sm_angle
    for theta in range(0, 20, 1):
        beamline.parameter("theta").sp_move = theta * 1.0
        positions_y = [component.calculate_beam_interception().y for component in beamline]
        positions_y.insert(0, "theta {} sman{}".format(theta, sm_angle))
        positions.append(positions_y)

    return positions


if __name__ == '__main__':
    thetas = generate_theta_movement()

    with open("example.csv", mode="w") as f:
        for theta in thetas:
            f.write(", ".join([str(v) for v in theta]))
            f.write("\n")
