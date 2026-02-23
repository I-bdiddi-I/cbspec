"""
Convert differential flux J(E) into energy-scaled spectrum:

    S(E) = E³ J(E)

This is standard representation used by Telescope Array, Auger, and HiRes
because multiplying by E³ visually flattens the spectrum and highlights
features such as the ankle and GZK suppression.

All computations are performed in log10(E/eV) space, constants with the rest
of the pipeline.

add: fitting to HiRes spectrum
"""

import numpy as np

def flux_to_spectrum(centers_log10e, flux, flux_low, flux_high):
    """
    Convert flux J(E) into spectrum S(E) = E³ J(E).

    :param centers_log10e: array-like
                           Bin centers in log10(E/eV)
    :param flux: array-like
                 Differential flux J(E) in each bin
    :param flux_low: array-like
                     Lower Feldman_Cousins bound on J(E)
    :param flux_high: array-like
                      Upper Feldman-Cousins bound on J(E)
    :return spectrum: np.ndarray
                      Energy-scaled spectrum S(E) = E³ J(E)
    :return spectrum_low: np.ndarray
                          Lower Feldman_Cousins bound in spectrum space
    :return spectrum_high: np.ndarray
                           Upper Feldman_Cousins bound in spectrum space

    Notes:
        - Convention from log10(E/eV) to E (eV):
            E = 10^(log10(E/eV))

        - Units:
            J(E)    ~ m⁻² sr⁻¹ s⁻¹ eV⁻¹
            E³J(E)  ~ eV² m⁻² sr⁻¹ s⁻¹

    These match the conventions used in TA and HiRes publications.
    """
    # Convert log10(E/eV) → E (eV)
    energies_ev = 10. ** np.asarray(centers_log10e, dtype=float)

    # Compute E³
    e3 = energies_ev**3

    # Apply scaling
    spectrum = e3 * flux
    spectrum_low = e3 * flux_low
    spectrum_high = e3 * flux_high

    return spectrum, spectrum_low, spectrum_high