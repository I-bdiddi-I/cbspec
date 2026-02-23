"""
Convert flux J(E) into spectrum S(E) = E^3 J(E) for plotting.

We work in log10(E/eV) space:
    log10E = log10(E/eV)
    E = 10^log10E eV

add: scale to HiRes spectrum
"""

import numpy as np

def flux_to_spectrum(centers_log10e, flux, flux_low, flux_high):
    """
    Convert flux J(E) into spectrum S(E) = E^3 J(E).

    :param centers_log10e: array-like
                           Bin centers in log10(E/eV)
    :param flux: array-like
                 Flux J(E)
    :param flux_low: array-like
                     Lower FC flux bound
    :param flux_high: array-like
                      Upper FC flux bound
    :return spectrum: np.ndarray
                      S(E) = E^3 J(E)
    :return spectrum_low: np.ndarray
                          Lower FC bound in spectrum space
    :return spectrum_high: np.ndarray
                           Upper FC bound in spectrum space
    """
    energies_ev = 10. ** np.asarray(centers_log10e, dtype=float)
    e3 = energies_ev**3

    spectrum = e3 * flux
    spectrum_low = e3 * flux_low
    spectrum_high = e3 * flux_high

    return spectrum, spectrum_low, spectrum_high