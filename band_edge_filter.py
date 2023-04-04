import numpy as np


class BandEdgeFilter:
    samps_per_sym: float
    filter_size: int
    rolloff: float

    def __init__(self, samps_per_sym: float, filter_size: int, rolloff: float):
        self.samps_per_sym = samps_per_sym
        self.filter_size = filter_size
        self.rolloff = rolloff
        self.symbol_times: tuple = None
        self.bb_taps = []
        self.taps_upper = list(range(self.filter_size))
        self.taps_lower = list(range(self.filter_size))

    def symbol_time_mapping(self, index):
        m = round(self.filter_size / self.samps_per_sym)
        return -m + index * 2.0 / self.samps_per_sym

    def design(self):
        m = round(self.filter_size / self.samps_per_sym)
        power: float = 0

        tap_index_range = range(0, self.filter_size)
        k = map(self.symbol_time_mapping, tap_index_range)
        self.symbol_times = tuple(k)

        for i in tap_index_range:
            k = -m + i * 2.0 / self.samps_per_sym
            tap: float = np.sinc(self.rolloff * k - 0.5) + np.sinc(self.rolloff * k + 0.5)
            power += tap

            self.bb_taps.append(tap)

        n: int = (len(self.bb_taps) - 1.0) / 2.0
        for i in tap_index_range:
            tap: float = self.bb_taps[i] / power

            k: float = (-n + i) / (2.0 * self.samps_per_sym)

            angle_lower = -2 * np.pi * (1 + self.rolloff) * k
            angle_upper = 2 * np.pi * (1 + self.rolloff) * k

            t1: complex = tap * np.exp(1j * angle_lower)
            t2: complex = tap * np.exp(1j * angle_upper)

            self.taps_lower[self.filter_size - i - 1] = t1
            self.taps_upper[self.filter_size - i - 1] = t2
