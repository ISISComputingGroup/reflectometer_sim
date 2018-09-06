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

        self._beamline = beamline
        self._ca_server = server
        self._pvdb = pv_manager

    def read(self, reason):
        """
        Processes an incoming caget request.
        :param reason: The PV that is being read.
        :return: The value associated to this PV
        """
        if reason.startswith(PARAM_PREFIX):
            param_name = self._pvdb.get_param_name_from_pv(reason)
            param = self._beamline.parameter(param_name)
            if reason.endswith(SP_SUFFIX):
                return param.sp
            elif reason.endswith(SP_RBV_SUFFIX):
                return param.sp_rbv
            else:
                return self.getParam(reason)  # TODO return actual RBV
        elif reason.endswith("BL:MODE"):
            return self._beamline.active_mode.name
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
            if reason.endswith(MOVE_SUFFIX):
                param.move = 1
            elif reason.endswith(SP_SUFFIX):
                param.sp_no_move = value
            elif reason.endswith(SET_AND_MOVE_SUFFIX):
                param.sp = value
        elif reason == BEAMLINE_MOVE:
            self._beamline.move = 1
        elif reason == BEAMLINE_MODE:
            try:
                mode_to_set = self._beamline.get_mode_by_index(value)
                self._beamline.active_mode = mode_to_set
            except KeyError:
                print("Invalid value entered for mode.")  # TODO print list of options

        self.setParam(reason, value)
