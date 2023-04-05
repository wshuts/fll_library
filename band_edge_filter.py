import numpy as np


class BandEdgeFilter:
    samps_per_sym: float
    filter_size: int
    alpha: float

    def __init__(self, samps_per_sym: float, filter_size: int, alpha: float):
        self.samps_per_sym = samps_per_sym
        self.filter_size = filter_size
        self.alpha = alpha
        self.half_filter_size = round(0.5 * self.filter_size - 1)
        self.sampling_times: tuple = None
        self.bb_taps: tuple = None
        self.power = 0
        self.bb_taps_normalized: tuple = None
        self.rotation_times: tuple = None
        self.angles_lower: tuple = None
        self.angles_upper: tuple = None
        self.taps_upper = list(range(self.filter_size))
        self.taps_lower = list(range(self.filter_size))

    def compute_sampling_time(self, index):
        return 2.0 * self.alpha / self.samps_per_sym * (index - self.half_filter_size)

    @staticmethod
    def compute_tap(sample_time):
        return np.sinc(sample_time - 0.5) + np.sinc(sample_time + 0.5)

    def normalize(self, tap):
        return tap / self.power

    def compute_rotation_time(self, index):
        return 0.5 * (1 + self.alpha) / self.samps_per_sym * (index - self.half_filter_size)

    @staticmethod
    def compute_angle_lower(rotation_time):
        return -2 * np.pi * rotation_time

    @staticmethod
    def compute_angle_upper(rotation_time):
        return 2 * np.pi * rotation_time

    def design(self):
        tap_index_range = range(0, self.filter_size)
        self.sampling_times = tuple(self.compute_sampling_time(index) for index in tap_index_range)
        self.bb_taps = tuple(self.compute_tap(sample_time) for sample_time in self.sampling_times)
        self.power = sum(self.bb_taps)
        self.bb_taps_normalized = tuple(self.normalize(tap) for tap in self.bb_taps)
        self.rotation_times = tuple(self.compute_rotation_time(index) for index in tap_index_range)
        self.angles_lower = tuple(self.compute_angle_lower(rotation_time) for rotation_time in self.rotation_times)
        self.angles_upper = tuple(self.compute_angle_upper(rotation_time) for rotation_time in self.rotation_times)

        # t1: complex = tap * np.exp(1j * angle_lower)
        # t2: complex = tap * np.exp(1j * angle_upper)
        #
        # self.taps_lower[self.filter_size - i - 1] = t1
        # self.taps_upper[self.filter_size - i - 1] = t2

    def dispose(self):
        return
