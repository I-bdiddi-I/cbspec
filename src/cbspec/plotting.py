"""
Publication-quality plotting utilities for the cbspec pipeline.

This module generates the following plots:
    - Aperture vs. log10(E/eV)
    - Exposure vs. log10(E/eV)
    - Flux vs. log10(E/eV)
    - Spectrum vs. log10(E/eV)
    - MC reconstructed histogram
    - MC thrown histogram
    - Data reconstructed histogram

All plots are saved to BOTH:
    - global_output_dir/plots/
    - run_output_dir/plots/

Filenames are automatically array-tagged:
    - TASD_flux.png
    - CBSD_spectrum.png
    etc.
"""


import os
import matplotlib.pyplot as plt
import numpy as np
from .output_utils import ensure_dir
from .constants import m2_to_km2, s_to_yr


def save_plot(global_output_dir, run_output_dir, filename):
    """
    Saves plots to both global and run-specific output directories.
    :param global_output_dir:
    :param run_output_dir:
    :param filename:
    :return:
    """
    global_plot_dir = os.path.join(global_output_dir, "plots")
    run_plot_dir = os.path.join(run_output_dir, "plots")
    ensure_dir(global_plot_dir)
    ensure_dir(run_plot_dir)

    plt.savefig(os.path.join(global_plot_dir, filename))
    plt.savefig(os.path.join(run_plot_dir, filename))

def plot_scatter_log_energy(centers, y_comp):
    """
    Basic structure of scatter plots vs. log10(E/eV).
    :param centers:
    :param y_comp:
    :return:
    """
    plt.figure(figsize=[8, 6])
    plt.scatter(centers, y_comp)
    plt.yscale("log")
    plt.xlim(17.8, 20.5)
    plt.xlabel(r"$\log_{10}(E/eV)$")


def plot_error_bars_log_energy(centers, y_comp, lower, upper):
    """
    Basic structure of plots needing error bars vs. log10(E/eV).
    :param centers:
    :param y_comp:
    :param lower:
    :param upper:
    :return:
    """
    yerr = [lower, upper]

    plt.figure(figsize=[8, 6])
    plt.errorbar(
        centers,
        y_comp,
        yerr=yerr,
        fmt="o",
        markersize=4,
        capsize=3,
        color="k",
        ecolor="k",
        linewidth=1,
    )
    plt.yscale("log")
    plt.xlim(17.8, 20.5)
    plt.xlabel(r"$\log_{10}(E/eV)$")


def plot_histogram(data):
    """
    Plot histogram of data.
    :param data:
    :return:
    """
    plt.figure(figsize=[8, 6])
    plt.hist(data, range=(18, 21), bins=30)
    plt.yscale("log")
    plt.xlabel(r"$\log_{10}(E/eV)$")


def plot_aperture(centers, aperture, array_type, global_output_dir, run_output_dir):
    """
    Plot aperture vs. log10(E/eV).
    :param centers:
    :param aperture:
    :param array_type:
    :param global_output_dir:
    :param run_output_dir:
    :return:
    """
    filename = f"{array_type}_aperture.png"

    # Convert aperture from [m^2 sr] to [km^2 sr]
    aperture = np.asarray(aperture, dtype=float) * m2_to_km2

    # Basic structure
    plot_scatter_log_energy(centers, aperture)

    # Aperture specific parameters
    plt.ylim(5, 5 * 10**3)
    plt.title(f"{array_type} Main Aperture")
    plt.ylabel(r"Aperture [km$^{2}$ sr]")

    save_plot(global_output_dir, run_output_dir, filename)

    plt.close()


def plot_exposure(centers, exposure, array_type, global_output_dir, run_output_dir):
    """
    Plot exposure vs. log10(E/eV).
    :param centers:
    :param exposure:
    :param array_type:
    :param global_output_dir:
    :param run_output_dir:
    :return:
    """
    filename = f"{array_type}_exposure.png"

    # Convert exposure from [m^2 sr s] to [km^2 sr yr]
    exposure = np.asarray(exposure, dtype=float) * m2_to_km2 * s_to_yr

    plot_scatter_log_energy(centers, exposure)

    # Exposure specific parameters
    plt.ylim(1, 2 * 10**4)
    plt.title(f"{array_type} Main Exposure")
    plt.ylabel(r"Exposure [km$^{2}$ sr yr]")

    save_plot(global_output_dir, run_output_dir, filename)

    plt.close()


def plot_flux(centers, flux, flux_lower, flux_upper, array_type, global_output_dir, run_output_dir):
    """
    Plot flux vs. log10(E/eV).
    :param centers:
    :param flux:
    :param flux_lower:
    :param flux_upper:
    :param array_type:
    :param global_output_dir:
    :param run_output_dir:
    :return:
    """
    filename = f"{array_type}_flux.png"

    plot_error_bars_log_energy(centers, flux, flux_lower, flux_upper)

    # Flux specific parameters
    plt.ylim(10 ** (-7), 2)
    plt.title(f"{array_type} Main Flux")
    plt.ylabel(r"J × 10$^{30}$ [eV$^{-1}$ m$^{-2}$ sr$^{-1}$ s$^{-1}$]")

    save_plot(global_output_dir, run_output_dir, filename)

    plt.close()


def plot_spectrum(centers, spectrum, spectrum_lower, spectrum_upper, array_type, global_output_dir, run_output_dir):
    """
    Plot spectrum vs. log10(E/eV).
    :param centers:
    :param spectrum:
    :param spectrum_lower:
    :param spectrum_upper:
    :param array_type:
    :param global_output_dir:
    :param run_output_dir:
    :return:
    """
    filename = f"{array_type}_spectrum.png"

    plot_error_bars_log_energy(centers, spectrum, spectrum_lower, spectrum_upper)

    # Spectrum specific parameters
    plt.ylim(4 * 10 ** (-1), 4)
    plt.title(f"{array_type} Main Spectrum")
    plt.ylabel(r"E$^{3}$ J / 10$^{24}$ [eV$^{2}$ m$^{-2}$ sr$^{-1}$ s$^{-1}$]")

    save_plot(global_output_dir, run_output_dir, filename)

    plt.close()


def mc_recon_hist(mc_array, array_type, global_output_dir, run_output_dir):
    """
    Histogram of MC reconstructed energies.
    :param mc_array:
    :param array_type:
    :param global_output_dir:
    :param run_output_dir:
    :return:
    """
    filename = f"{array_type}_MC_recon_hist.png"

    plot_histogram(mc_array)

    plt.title(f"{array_type} MC Reconstructed Energies Histogram")
    plt.ylabel("N$^{MC}_{REC}$")

    save_plot(global_output_dir, run_output_dir, filename)

    plt.close()


def mc_thrown_hist(mc_thrown_array, array_type, global_output_dir, run_output_dir):
    """
    Histogram of MC thrown energies.
    :param mc_thrown_array:
    :param array_type:
    :param global_output_dir:
    :param run_output_dir:
    :return:
    """
    filename = f"{array_type}_MC_thrown_hist.png"

    plot_histogram(mc_thrown_array)

    plt.title(f"{array_type} MC Thrown Energies Histogram")
    plt.ylabel("N$^{MC}_{GEN}$")

    save_plot(global_output_dir, run_output_dir, filename)

    plt.close()


def dt_hist(dt_array, array_type, global_output_dir, run_output_dir):
    """
    Histogram of MC thrown energies.
    :param dt_array:
    :param array_type:
    :param global_output_dir:
    :param run_output_dir:
    :return:
    """
    filename = f"{array_type}_DATA_recon_hist.png"

    plot_histogram(dt_array)

    plt.title(f"{array_type} Data Reconstructed Energies Histogram")
    plt.ylabel("N$^{DATA}_{REC}$")

    save_plot(global_output_dir, run_output_dir, filename)

    plt.close()