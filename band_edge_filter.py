import numpy as np


class BandEdgeFilter:
    samps_per_sym: float
    filter_size: int
    alpha: float

    def __init__(self, samps_per_sym: float, filter_size: int, alpha: float):
        self.samps_per_sym = samps_per_sym
        self.filter_size = filter_size
        self.alpha = alpha
        self.symbol_times: tuple = None
        self.bb_taps: tuple = None
        self.power = 0
        self.bb_taps_normalized: tuple = None
        self.rotation_times: tuple = None
        self.taps_upper = list(range(self.filter_size))
        self.taps_lower = list(range(self.filter_size))

    def compute_symbol_time(self, index):
        m = round(self.filter_size / self.samps_per_sym)
        return (-m + index * 2.0 / self.samps_per_sym) * self.alpha

    @staticmethod
    def compute_tap(symbol_time):
        return np.sinc(symbol_time - 0.5) + np.sinc(symbol_time + 0.5)

    def compute_rotation_time(self, index):
        n = round(0.5 * (self.filter_size - 1))
        return 0.5 * (1 + self.alpha) / self.samps_per_sym * (index - n)

    def normalize(self, tap):
        return tap / self.power

    def design(self):
        tap_index_range = range(0, self.filter_size)
        self.symbol_times = tuple(self.compute_symbol_time(index) for index in tap_index_range)
        self.bb_taps = tuple(self.compute_tap(symbol_time) for symbol_time in self.symbol_times)
        self.power = sum(self.bb_taps)
        self.bb_taps_normalized = tuple(self.normalize(tap) for tap in self.bb_taps)
        self.rotation_times = tuple(self.compute_rotation_time(index) for index in tap_index_range)

        n: int = (len(self.bb_taps) - 1.0) / 2.0
        for i in tap_index_range:
            tap: float = self.bb_taps[i] / self.power

            k: float = (-n + i) * (1 + self.alpha) / (2.0 * self.samps_per_sym)

            angle_lower = -2 * np.pi * k
            angle_upper = 2 * np.pi * k

            t1: complex = tap * np.exp(1j * angle_lower)
            t2: complex = tap * np.exp(1j * angle_upper)

            self.taps_lower[self.filter_size - i - 1] = t1
            self.taps_upper[self.filter_size - i - 1] = t2

    def dispose(self):
        return

