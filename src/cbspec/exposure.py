"""
Compute aperture and exposure.
"""

import numpy as np


# Aperture
def compute_aperture(mc_counts, mc_raw_counts, centers, generated_area_m2, generated_solid_angle_sr):
    """
    Compute the detector aperture like in Dmitri Ivanov's thesis.

    Physics equation:
        AΩ(E) = (N_MC_reco(E) / N_MC_raw(E)) * (A_gen * Ω_gen)

    :param mc_counts: int
                      N_MC_reco(E) = number of reconstructed MC events in bin E
    :param mc_raw_counts: int
                          N_MC_raw(E) = number of thrown MC events in bin E
    :param centers: float
                    bin centers
    :param generated_area_m2: float
                              A_gen = generated area in meters squared
    :param generated_solid_angle_sr: float
                                     Ω_gen = generated solid angle in sr
    :return: float
    """

    # Fraction of generated events that survive reconstruction + cuts
    frac = np.zeros_like(mc_counts, dtype=float)

    # Mask: only bins with thrown MC energy > 18.5
    energy_mask = centers > 18.5

    # Mask: only bins with nonzero thrown MC counts
    raw_mask = mc_raw_counts > 1

    # Combined mask
    mask = energy_mask & raw_mask

    # Acceptance
    frac[mask] = mc_counts[mask] / mc_raw_counts[mask]

    # Multiply by generated geometry
    aperture = frac * generated_area_m2 * generated_solid_angle_sr
    return aperture


# Exposure
def compute_exposure(aperture, time_s):
    """
    Compute the exposure like in Dmitri Ivanov's thesis.

    Physics equation:
        Exposure(E) = AΩ(E) * time_s

    :param aperture: float
    :param time_s: float
    :return: float
    """
    return aperture * time_s