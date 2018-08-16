import math


class IocDriver(object):
    """
    Drives an actual motor IOC
    """
    def __init__(self, component):
        self._component = component

    def get_max_move_duration(self):
        """
        This should be overridden in the subclass
        Returns: the duration of the requested move for the axis with the longest duration
        """
        raise NotImplemented()

    def perform_move(self, duration):
        """
        This should be overridden in the subclass. Tells the driver to perform a move to the component setpoints within a given duration
        :param duration: The duration in which to perform this move
        """
        raise NotImplemented()


class HeightDriver(IocDriver):
    """
    Drives a component with vertical movement
    """
    def __init__(self, component, height_axis):
        super(HeightDriver, self).__init__(component)
        self._height_axis = height_axis

    def get_max_move_duration(self):
        return math.fabs(self._height_axis.value - self._component.sp_position().y) / self._height_axis.max_velocity

    def perform_move(self, duration):
        self._height_axis.velocity = math.fabs(self._height_axis.value - self._component.sp_position().y) / duration
        self._height_axis.value = self._component.sp_position().y


class TiltingJawsDriver(HeightDriver):
    """
    Drives a tilting jawset
    """
    def __init__(self, component, height_axis, angle_axis):
        super(TiltingJawsDriver, self).__init__(component, height_axis)
        self._angle_axis = angle_axis

    def get_max_move_duration(self):
        vertical_move_duration = math.fabs(self._height_axis.value - self._component.sp_position().y) / self._height_axis.max_velocity
        angular_move_duration = math.fabs(self._angle_axis.value - self._component.calculate_tilt_angle()) / self._angle_axis.max_velocity
        return max(vertical_move_duration, angular_move_duration)

    def perform_move(self, duration):
        self._height_axis.velocity = math.fabs(self._height_axis.value - self._component.sp_position().y) / duration
        self._angle_axis.velocity = math.fabs(self._angle_axis.value - self._component.sp_position().y) / duration
        self._height_axis.value = self._component.sp_position().y
        self._angle_axis.value = self._component.calculate_tilt_angle()
