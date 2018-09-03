from pcaspy import SimpleServer
from src.ChannelAccess.macros import *
from src.components import *
from src.beamline import Beamline, BeamlineMode
from src.parameters import *
from src.ChannelAccess.pv_server import ReflectometryDriver
from src.ChannelAccess.pv_manager import PVManager

STATUS_PV_FIELDS = {'type': 'enum', 'enums': ["NO", "YES"]}
FLOAT_PV_FIELDS = {'type': 'float', 'prec': 3, 'value': 0.0}
PARAMS_FIELDS = {"smenabled": STATUS_PV_FIELDS,
                 "smangle": FLOAT_PV_FIELDS,
                 "slit2pos": FLOAT_PV_FIELDS,
                 "samplepos": FLOAT_PV_FIELDS,
                 "theta": FLOAT_PV_FIELDS,
                 "slit3pos": FLOAT_PV_FIELDS,
                 "paenabled": STATUS_PV_FIELDS,
                 "slit4pos": FLOAT_PV_FIELDS,
                 "detpos": FLOAT_PV_FIELDS,
                 }

NR_INITS = {"smenabled": False, "smangle": 0.0}
PNR_INITS = {"smenabled": True, "smangle": 0.5}

NR_MODE = BeamlineMode("nr", PARAMS_FIELDS.keys(), NR_INITS)
PNR_MODE = BeamlineMode("pnr", PARAMS_FIELDS.keys(), PNR_INITS)
DISABLED_MODE = BeamlineMode("disabled", [])

MODES = [NR_MODE, PNR_MODE, DISABLED_MODE]


def create_beamline():
    beam_angle_natural = -45
    beam_start = PositionAndAngle(0.0, 0.0, beam_angle_natural)
    perp_to_floor = 90.0

    # COMPONENTS
    # s1 = PassiveComponent("s1", LinearMovement(0.0, 7.3025, perp_to_beam_angle))
    # s2 = PassiveComponent("s2", LinearMovement(0.0, 9.6885, perp_to_beam_angle))
    # s3 = PassiveComponent("s3", LinearMovement(0.0, 10.651, perp_to_beam_angle))
    # s4 = PassiveComponent("s4", LinearMovement(0.0, 11.983, perp_to_beam_angle))
    # super_mirror = ActiveComponent("sm", LinearMovement(0.0, 7.7685, perp_to_beam_angle))
    # sample = ActiveComponent("sample", LinearMovement(0.0, 10.25, perp_to_beam_angle))
    # point_det = TiltingJaws("pdet", LinearMovement(0.0, 12.113, perp_to_beam_angle))
    s1 = PassiveComponent("s1", LinearMovement(0.0, 1, perp_to_floor))
    super_mirror = ActiveComponent("sm", LinearMovement(0.0, 5, perp_to_floor))
    s2 = PassiveComponent("s2", LinearMovement(0.0, 9, perp_to_floor))
    sample = ActiveComponent("sample", LinearMovement(0.0, 10, perp_to_floor))
    s3 = PassiveComponent("s3", LinearMovement(0.0, 15, perp_to_floor))
    s4 = PassiveComponent("s4", LinearMovement(0.0, 19, perp_to_floor))
    point_det = TiltingJaws("det", LinearMovement(0.0, 20, perp_to_floor))
    comps = [s1, super_mirror, s2, sample, s3, s4, point_det]

    # BEAMLINE PARAMETERS
    sm_enabled = ComponentEnabled("smenabled", super_mirror)
    sm_angle = ReflectionAngle("smangle", super_mirror)
    slit2_pos = TrackingPosition("slit2pos", s2)
    sample_pos = TrackingPosition("samplepos", sample)
    theta = Theta("theta", sample)
    slit3_pos = TrackingPosition("slit3pos", s3)
    slit4_pos = TrackingPosition("slit4pos", s4)
    det = TrackingPosition("detpos", point_det)
    # Initialise to avoid exceptions
    # sm_enabled.sp_no_move = False
    # sm_angle.sp_no_move = 0.0
    # slit2_pos.sp_no_move = 0.0
    # sample_pos.sp_no_move = 0.0
    # theta.sp_no_move = 0.0
    # slit3_pos.sp_no_move = 0.0
    # slit4_pos.sp_no_move = 0.0
    # det.sp_no_move = 0.0
    params = [sm_enabled,
              sm_angle,
              slit2_pos,
              sample_pos,
              theta,
              slit3_pos,
              slit4_pos,
              det]

    # init beamline
    bl = Beamline(comps, params, MODES)
    bl.set_incoming_beam(beam_start)
    bl.active_mode = NR_MODE
    return bl

beamline = create_beamline()

pv_db = PVManager(PARAMS_FIELDS, [mode.name for mode in MODES])
SERVER = SimpleServer()
for pv_name in pv_db.PVDB.keys():
    print("creating pv: " + pv_name)
SERVER.createPV(REFLECTOMETRY_PREFIX, pv_db.PVDB)
DRIVER = ReflectometryDriver(SERVER, beamline, pv_db)

# Process CA transactions
while True:
    try:
        SERVER.process(0.1)
    except Exception as err:
        print(err)
        break
