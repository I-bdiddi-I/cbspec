"""
Compute aperture and exposure.
"""

import numpy as np


# Aperture
def compute_aperture(mc_counts, mc_raw_counts, generated_area_m2, generated_solid_angle_sr):
    """
    Compute the detector aperture like in Dmitri Ivanov's thesis.

    Physics equation:
        AΩ(E) = (N_MC_reco(E) / N_MC_raw(E)) * (A_gen * Ω_gen)

    :param mc_counts: array-like
                      N_MC_reco(E) = number of reconstructed MC events in bin E
    :param mc_raw_counts: array-like
                          N_MC_raw(E) = number of thrown MC events in bin E
    :param generated_area_m2: float
                              A_gen = generated area in meters squared
    :param generated_solid_angle_sr: float
                                     Ω_gen = generated solid angle in sr
    :return aperture: np.ndarray
                      Aperture per bin [m^2 sr]
    """
    mc_counts = np.asarray(mc_counts, dtype=float)
    mc_raw_counts = np.asarray(mc_raw_counts, dtype=float)

    # Fraction of generated events that survive reconstruction + cuts
    frac = np.zeros_like(mc_counts, dtype=float)

    # Acceptance
    with np.errstate(divide='ignore', invalid='ignore'):
        mask = mc_raw_counts > 1
        frac[mask] = mc_raw_counts[mask] / mc_raw_counts[mask]

    # Multiply by generated geometry
    aperture = frac * generated_area_m2 * generated_solid_angle_sr
    return aperture


# Exposure
def compute_exposure(aperture, time_s):
    """
    Compute the exposure like in Dmitri Ivanov's thesis.

    Physics equation:
        Exposure(E) = AΩ(E) * time_s

    :param aperture: array-like
                     Aperture per bin [m^2 sr]
    :param time_s: float
                   Experimental run time in seconds
    :return exposure: np.ndarray
                      Exposure per bin [m^2 sr s]
    """
    aperture = np.asarray(aperture, dtype=float)
    return aperture * time_s