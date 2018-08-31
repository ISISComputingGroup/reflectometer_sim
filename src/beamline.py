"""
Resources at a beamline level
"""
from collections import OrderedDict


class BeamlineMode(object):
    """
    Beamline mode definition; which components and parameters are calculated on move.
    """

    def __init__(self, name, beamline_parameters_to_calculate, sp_inits=None):
        """
        Initialize.
        Args:
            name (str): name of the beam line mode
            beamline_parameters_to_calculate (list[src.parameters.BeamlineParameter]): Beamline parameters in this mode
                which should be automatically moved to whenever a preceding parameter is changed
            sp_inits: The initial beamline parameter values that should be set when switching to this mode
        """
        self.name = name.upper()
        self._beamline_parameters_to_calculate = beamline_parameters_to_calculate
        if sp_inits is None:
            self._sp_inits = {}
        else:
            self._sp_inits = sp_inits

    def has_beamline_parameter(self, beamline_parameter):
        """
        Args:
            beamline_parameter(src.parameters.BeamlineParameter): the beamline parameter

        Returns: True if beamline_parameter is in this mode.
        """
        return beamline_parameter.name in self._beamline_parameters_to_calculate

    def get_parameters_in_mode(self, beamline_parameters, first_parameter=None):
        """
        Returns, in order, all those parameters which are in this mode. Starting with the parameter after the first
        parameter
        Args:
            beamline_parameters(list[src.parameters.BeamlineParameter]): the beamline parameters which maybe in the mode
            first_parameter(src.parameters.BeamlineParameter): the parameter after which to include parameters; None for
            include all

        Returns: a list of parameters after the first parameter which are in this mode

        """
        parameters_in_mode = []
        after_first = first_parameter is None
        for beamline_parameter in beamline_parameters:
            if beamline_parameter == first_parameter:
                after_first = True
            elif after_first and beamline_parameter.name in self._beamline_parameters_to_calculate:
                parameters_in_mode.append(beamline_parameter)
        return parameters_in_mode

    @property
    def initial_setpoints(self):
        """
        Set point initial values
        Returns: the set point

        """
        return self._sp_inits


class Beamline(object):
    """
    The collection of all beamline components.
    """

    def __init__(self, components, beamline_parameters, modes):
        """
        The initializer.
        Args:
            components (list[src.components.Component]): The collection of beamline components
            beamline_parameters (list[src.parameters.BeamlineParameter]): a dictionary of parameters that characterise
            the beamline
        """
        self._components = components
        self._beamline_parameters = OrderedDict()
        self._modes = {}
        for mode in modes:
            self._modes[mode.name] = mode
        for beamline_parameter in beamline_parameters:
            if beamline_parameter.name in self._beamline_parameters:
                raise ValueError("Beamline parameters must be uniquely named. Duplicate '{}'".format(
                    beamline_parameter.name))
            self._beamline_parameters[beamline_parameter.name] = beamline_parameter
            beamline_parameter.after_move_listener = self.update_beamline_parameters

        [component.set_beam_path_update_listener(self.update_beam_path) for component in components]

        self.incoming_beam = None
        self._active_mode = None

    @property
    def active_mode(self):
        """
        Returns: the current modes
        """
        return self._active_mode

    @active_mode.setter
    def active_mode(self, mode):
        """
        Set the current mode (setting presets as expected)
        Args:
            mode (BeamlineMode): mode to set
        """
        self._active_mode = mode
        self.init_setpoints()

    @property
    def move(self):
        """
        Move the beamline.
        Returns: 0
        """
        return 0

    @move.setter
    def move(self, _):
        """
        Move to all the beamline parameters in the mode or that have changed
        Args:
            _: dummy can be anything
        """
        self.update_beamline_parameters()

    def __getitem__(self, item):
        """
        Args:
            item: the index of the component

        Returns: the indexed component
        """
        return self._components[item]

    def set_incoming_beam(self, incoming_beam):
        """
        Set the incoming beam for the component
        Args:
            incoming_beam: incoming beam
        """
        self.incoming_beam = incoming_beam
        self.update_beam_path()

    def update_beam_path(self):
        """
        Updates the beam path for all components
        """
        outgoing = self.incoming_beam
        for component in self._components:
            component.set_incoming_beam(outgoing)
            outgoing = component.get_outgoing_beam()

    def update_beamline_parameters(self, source=None):
        """
        Updates the beamline parameters in the current mode. If given a source in the mode start from this one instead
        of from the beginning of the beamline. If the source is not in the mode then don't update the beamline.
        Args:
            source: source to start the update from; None start from the beginning.

        Returns:

        """
        if source is None or self._active_mode.has_beamline_parameter(source):

            parameters_in_mode = self._active_mode.get_parameters_in_mode(self._beamline_parameters.values(), source)

            for beamline_parameter in parameters_in_mode:
                beamline_parameter.move_no_callback()

    def parameter(self, key):
        """
        Args:
            key (str): key of parameter to return

        Returns:
            src.parameters.BeamlineParameter: the beamline parameter with the given key
        """
        return self._beamline_parameters[key]

    def mode(self, key):
        """
        Args:
            key: key of parameter to return

        Returns (src.parameters.BeamlineParameter):
            the beamline parameter with the given key
        """
        return self._modes[key]

    def init_setpoints(self):
        """
        Applies the initial values set in the current beamline mode to the relevant beamline parameter setpoints.
        """
        for key, value in self._active_mode.initial_setpoints.iteritems():
            self._beamline_parameters[key].sp_no_move = value
