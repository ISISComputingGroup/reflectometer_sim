class Beamline(object):
    """
    The collection of all beamline components
    """
    def __init__(self, components, beamline_parameters):
        """
        The initialiser
        Args:
            components: The collection of beamline components
        """
        self._components = components
        self._beamline_parameters = beamline_parameters
        [component.set_beam_path_update_listener(self.update_beam_path) for component in components]
        self.incoming_beam = None

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

    def parameter(self, index):
        return self._beamline_parameters[index]
