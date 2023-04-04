import unittest
from band_edge_filter import BandEdgeFilter


class TestBandEdgeFilter(unittest.TestCase):

    def test_constructor(self):
        band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)

        samps_per_sym = band_edge_filter.samps_per_sym
        filter_size = band_edge_filter.filter_size
        alpha = band_edge_filter.alpha

        self.assertEqual(samps_per_sym, 16.0)
        self.assertEqual(filter_size, 321)
        self.assertEqual(alpha, 0.5)

    def test_symbol_times(self):
        band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)
        band_edge_filter.design()

        newest = band_edge_filter.symbol_times[0]
        now = band_edge_filter.symbol_times[160]
        oldest = band_edge_filter.symbol_times[320]

        self.assertEqual(newest, -20.0)
        self.assertEqual(now, 0.0)
        self.assertEqual(oldest, 20.0)

    def test_bb_taps(self):
        band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)
        band_edge_filter.design()

        zero_left = band_edge_filter.bb_taps[160 - 8 - 16]
        peak_left = band_edge_filter.bb_taps[160 - 8]
        peak_right = band_edge_filter.bb_taps[160 + 8]
        zero_right = band_edge_filter.bb_taps[160 + 8 + 16]

        self.assertEqual(zero_left, 0.0)
        self.assertEqual(peak_left, 1.0)
        self.assertEqual(peak_right, 1.0)
        self.assertEqual(zero_right, 0.0)

    def test_power(self):
        band_edge_filter = BandEdgeFilter(16.0, 321, 0.5)
        band_edge_filter.design()

        power = band_edge_filter.power

        self.assertAlmostEqual(power, 32.0, 2)


if __name__ == '__main__':
    unittest.main()
