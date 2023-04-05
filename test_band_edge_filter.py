import unittest
from band_edge_filter import BandEdgeFilter


class TestBandEdgeFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.samps_per_sym = 16.0
        self.filter_size = 321
        self.alpha = 0.5

        self.leftmost_index = 0
        self.center_index = round(0.5 * (self.filter_size - 1))
        self.rightmost_index = self.filter_size - 1

        self.band_edge_filter = BandEdgeFilter(self.samps_per_sym, self.filter_size, self.alpha)
        self.band_edge_filter.design()

        return

    def test_constructor(self):
        samps_per_sym_actual = self.band_edge_filter.samps_per_sym
        filter_size_actual = self.band_edge_filter.filter_size
        alpha_actual = self.band_edge_filter.alpha

        samps_per_sym_expected = self.samps_per_sym
        filter_size_expected = self.filter_size
        alpha_expected = self.alpha

        self.assertEqual(samps_per_sym_expected, samps_per_sym_actual)
        self.assertEqual(filter_size_expected, filter_size_actual)
        self.assertEqual(alpha_expected, alpha_actual)

    def test_symbol_times(self):
        leftmost_actual = self.band_edge_filter.symbol_times[self.leftmost_index]
        center_actual = self.band_edge_filter.symbol_times[self.center_index]
        rightmost_actual = self.band_edge_filter.symbol_times[self.rightmost_index]

        leftmost_expected = -1 * self.alpha * (self.filter_size - 1) / self.samps_per_sym
        center_expected = 0.0
        rightmost_expected = 1 * self.alpha * (self.filter_size - 1) / self.samps_per_sym

        self.assertEqual(leftmost_expected, leftmost_actual)
        self.assertEqual(center_expected, center_actual)
        self.assertEqual(rightmost_expected, rightmost_actual)

    def test_bb_taps(self):
        half_samps_per_sym = round(0.5 * self.samps_per_sym)
        samps_per_sym = round(self.samps_per_sym)

        zero_left_index = self.center_index - half_samps_per_sym - samps_per_sym
        peak_left_index = self.center_index - half_samps_per_sym
        peak_right_index = self.center_index + half_samps_per_sym
        zero_right_index = self.center_index + half_samps_per_sym + samps_per_sym

        zero_left = self.band_edge_filter.bb_taps[zero_left_index]
        peak_left = self.band_edge_filter.bb_taps[peak_left_index]
        peak_right = self.band_edge_filter.bb_taps[peak_right_index]
        zero_right = self.band_edge_filter.bb_taps[zero_right_index]

        self.assertEqual(0.0, zero_left)
        self.assertEqual(1.0, peak_left)
        self.assertEqual(1.0, peak_right)
        self.assertEqual(0.0, zero_right)

    def test_power(self):
        power = self.band_edge_filter.power

        self.assertAlmostEqual(32.0, power, 2)

    def test_bb_taps_normalized(self):
        half_samps_per_sym = round(0.5 * self.samps_per_sym)
        samps_per_sym = round(self.samps_per_sym)

        zero_left_index = self.center_index - half_samps_per_sym - samps_per_sym
        peak_left_index = self.center_index - half_samps_per_sym
        peak_right_index = self.center_index + half_samps_per_sym
        zero_right_index = self.center_index + half_samps_per_sym + samps_per_sym

        zero_left = self.band_edge_filter.bb_taps_normalized[zero_left_index]
        peak_left = self.band_edge_filter.bb_taps_normalized[peak_left_index]
        peak_right = self.band_edge_filter.bb_taps_normalized[peak_right_index]
        zero_right = self.band_edge_filter.bb_taps_normalized[zero_right_index]

        normalized_peak = 1.0 / self.band_edge_filter.power

        self.assertEqual(0.0, zero_left)
        self.assertEqual(normalized_peak, peak_left)
        self.assertEqual(normalized_peak, peak_right)
        self.assertEqual(0.0, zero_right)

    def tearDown(self) -> None:
        self.band_edge_filter.dispose()
        return


if __name__ == '__main__':
    unittest.main()
