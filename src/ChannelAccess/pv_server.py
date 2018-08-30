from pcaspy import Driver
from threading import RLock
from pv_manager import *


class ReflectometryDriver(Driver):
    """
    The driver which provides an interface for the reflectometry server to channel access by creating PVs and processing
    incoming CA get and put requests.
    """
    def __init__(self, server, beamline, pv_manager):
        """
        The Constructor.
        :param server: The PCASpy server.
        :param beamline: The beamline configuration.
        :param pv_manager: The manager mapping PVs to objects in the beamline.
        """
        super(ReflectometryDriver, self).__init__()
        # Threading stuff TODO needed?
        self.monitor_lock = RLock()
        self.write_lock = RLock()
        self.write_queue = list()

        # self._beamline = BeamlineConfigReader.read("some.file")  # TODO read from config file
        self._beamline = beamline
        self._ca_server = server
        self._pvdb = pv_manager

    def read(self, reason):
        """
        Processes an incoming caget request.
        :param reason: The PV that is being read.
        :return: The value associated to this PV
        """
        if reason.endswith("BL:MODE"):
            return self._beamline.mode
        elif reason.endswith("SP"):
            param_name = self._pvdb.get_param_name_from_pv(reason)
            return self._beamline.parameter(param_name).sp_rbv
        else:
            return self.getParam(reason)

    def write(self, reason, value):
        """
        Process an incoming caput request.
        :param reason: The PV that is being written to.
        :param value: The value being written to the PV
        """
        if reason.startswith(PARAM_PREFIX):
            param_name = self._pvdb.get_param_name_from_pv(reason)
            param = self._beamline.parameter(param_name)
            if reason.endswith("MOVE"):
                self._beamline.update_beamline_parameters(param)
            elif reason.endswith("SP"):
                param.sp = value
        elif reason == BEAMLINE_MOVE:
            self._beamline.move = 1
        elif reason == BEAMLINE_MODE:
            # mode_to_set =
            self._beamline.mode = value
        else:
            # TODO stop, rbv
            pass
        self.setParam(reason, value)

