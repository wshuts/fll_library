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
        self.tap_angle_pairs_lower: tuple = None
        self.tap_angle_pairs_upper: tuple = None
        self.taps_lower_reversed: tuple = None
        self.taps_upper_reversed: tuple = None
        self.taps_lower: tuple = None
        self.taps_upper: tuple = None

    def compute_sampling_time(self, index):
        return 2.0 * self.alpha / self.samps_per_sym * (index - self.half_filter_size)

    def compute_rotation_time(self, index):
        return 0.5 * (1 + self.alpha) / self.samps_per_sym * (index - self.half_filter_size)

    def normalize(self, tap):
        return tap / self.power

    @staticmethod
    def compute_tap(sample_time):
        return np.sinc(sample_time - 0.5) + np.sinc(sample_time + 0.5)

    @staticmethod
    def compute_angle_lower(rotation_time):
        return -2 * np.pi * rotation_time

    @staticmethod
    def compute_angle_upper(rotation_time):
        return 2 * np.pi * rotation_time

    @staticmethod
    def compute_rotated_tap(tap, angle):
        return tap * np.exp(1j * angle)

    def design(self):
        tap_index_range = range(0, self.filter_size)

        self.sampling_times = tuple(
            self.compute_sampling_time(index)
            for index in tap_index_range
        )

        self.bb_taps = tuple(
            self.compute_tap(sample_time)
            for sample_time in self.sampling_times
        )
        self.power = sum(self.bb_taps)
        self.bb_taps_normalized = tuple(
            self.normalize(tap)
            for tap in self.bb_taps)

        self.rotation_times = tuple(
            self.compute_rotation_time(index)
            for index in tap_index_range
        )
        self.angles_lower = tuple(
            self.compute_angle_lower(rotation_time)
            for rotation_time in self.rotation_times
        )
        self.angles_upper = tuple(
            self.compute_angle_upper(rotation_time)
            for rotation_time in self.rotation_times
        )

        self.tap_angle_pairs_lower = tuple(
            zip(self.bb_taps_normalized, self.angles_lower)
        )
        self.taps_lower = tuple(
            self.compute_rotated_tap(tap, angle)
            for (tap, angle) in self.tap_angle_pairs_lower
        )
        self.taps_lower_reversed = tuple(
            reversed(self.taps_lower)
        )

        self.tap_angle_pairs_upper = tuple(
            zip(self.bb_taps_normalized, self.angles_upper)
        )
        self.taps_upper = tuple(
            self.compute_rotated_tap(tap, angle)
            for (tap, angle) in self.tap_angle_pairs_upper
        )
        self.taps_upper_reversed = tuple(
            reversed(self.taps_upper)
        )
        return

    def dispose(self):
        return

    def print(self):
        print('Lower Band Edge Filter Taps:')
        print(list(self.taps_lower))
        print('\n')
        print('Upper Band Edge Filter Taps:')
        print(list(self.taps_upper))
        print('\n')
