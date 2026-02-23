"""
Compute the differential flux J(E).
"""

import numpy as np


def compute_flux(n_events, exposure, bin_widths_log10e):
    """
    Compute the differential flux J(E).

    Physics (in log10(E/eV) bins):
        J(E) ≈ N / (Exposure × Δlog10E)

    :param n_events: array-like
                     Data counts per bin
    :param exposure: array-like
                     Exposure per bin [m^2 sr s]
    :param bin_widths_log10e: array-like
                              Bin widths in log10(E/eV)
    :return flux: np.ndarray
                  Differential flux J(E)
    """
    n_events = np.asarray(n_events, dtype=float)
    exposure = np.asarray(exposure, dtype=float)
    bin_widths_log10e = np.asarray(bin_widths_log10e, dtype=float)

    with np.errstate(divide='ignore', invalid='ignore'):
        flux = np.where(
            (exposure > 0) & (bin_widths_log10e > 0),
            n_events / (exposure * bin_widths_log10e),
            0.,
        )
    return flux

