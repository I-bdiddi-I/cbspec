"""
Energy binning utilities in log10(E/eV) space.
"""

import numpy as np


def make_energy_bins(en_range):
    """
    Constructs bin edges, centers, and widths from log10(E/eV) edges
    :param en_range:
    :return:
    """
    edges = np.asarray(en_range, dtype=float)
    centers = 0.5 * (edges[1:] + edges[:-1])
    widths = edges[1:] - edges[:-1]
    return edges, centers, widths


def histogram_events(log_energy, edges):
    """
    Histogram events into energy bins.
    :param log_energy:
    :param edges:
    :return:
    """
    counts, _ = np.histogram(log_energy, bins=edges)
    return counts


def histgram_data_per_bin(mc_log_energy, dt_log_energy, mc_raw_log_energy, edges):
    """
    Histogram MC & data into the same energy bins.
    :param mc_log_energy:
    :param dt_log_energy:
    :param edges:
    :return:
    """
    mc_counts = histogram_events(mc_log_energy, edges)
    dt_counts = histogram_events(dt_log_energy, edges)
    mc_raw_counts = histogram_events(mc_raw_log_energy, edges)
    return mc_counts, dt_counts, mc_raw_counts