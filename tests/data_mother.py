from src.beamline import BeamlineMode, Beamline
from src.parameters import BeamlineParameter

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


class EmptyBeamlineParameter(BeamlineParameter):
    """
    A Bemline Parameter Stub. Counts the number of time it is asked to move
    """
    def __init__(self, name):
        super(EmptyBeamlineParameter, self).__init__(name)
        self.move_component_count = 0

    def _move_component(self):
        self.move_component_count += 1


class DataMother(object):
    """
    Test data for various tests.
    """
    BEAMLINE_MODE_NEUTRON_REFLECTION = BeamlineMode(
        "Neutron reflection",
        ["slit2height", "height", "theta", "detectorheight"])

    @staticmethod
    def beamline_with_3_empty_patameters():
        """

        Returns: a beamline with three empty parameters, all in a mode

        """
        one = EmptyBeamlineParameter("one")
        two = EmptyBeamlineParameter("two")
        three = EmptyBeamlineParameter("three")
        beamline_parameters = [one, two, three]
        beamline = Beamline([], beamline_parameters, [])
        beamline.active_mode = BeamlineMode("all", [beamline_parameter.name for beamline_parameter in beamline_parameters])
        return beamline_parameters, beamline
