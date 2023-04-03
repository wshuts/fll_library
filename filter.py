import numpy as np


#  port from GNU Radio fll_band_edge_cc_impl

# /* -*- c++ -*- */
# /*
#  * Copyright 2009-2012,2014 Free Software Foundation, Inc.
#  *
#  * This file is part of GNU Radio
#  *
#  * SPDX-License-Identifier: GPL-3.0-or-later
#  *
#  */


def design_filter(samps_per_sym: float, rolloff: float, filter_size: int):
    m = round(filter_size / samps_per_sym)
    power: float = 0
    bb_taps = []
    d_taps_lower = list(range(filter_size))
    d_taps_upper = list(range(filter_size))

    # Create the baseband filter by adding two sincs together
    tap_index = range(0, filter_size)
    for i in tap_index:
        k = -m + i * 2.0 / samps_per_sym
        tap: float = np.sinc(rolloff * k - 0.5) + np.sinc(rolloff * k + 0.5)
        power += tap

        bb_taps.append(tap)

    # Create the band edge filters by spinning the baseband
    # filter up and down to the right places in frequency.
    # Also, normalize the power in the filters
    n: int = (len(bb_taps) - 1.0) / 2.0
    tap_index = range(0, filter_size)
    for i in tap_index:
        tap: float = bb_taps[i] / power

        k: float = (-n + i) / (2.0 * samps_per_sym)

        angle_lower = -2 * np.pi * (1 + rolloff) * k
        angle_upper = 2 * np.pi * (1 + rolloff) * k

        t1: complex = tap * np.exp(1j * angle_lower)
        t2: complex = tap * np.exp(1j * angle_upper)

        # flip baseband coefficients
        d_taps_lower[filter_size - i - 1] = t1
        d_taps_upper[filter_size - i - 1] = t2

    return
