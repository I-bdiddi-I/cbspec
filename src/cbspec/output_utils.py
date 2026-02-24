"""
Utility functions for saving flux and spectrum tables to CSV files.

This module handles **both**:
    - global outputs        → output/data
    - run-specific outputs  → output/runs/<timestamp>/data/

The filenames are automatically array-tagged:
    {array_type}_flux.csv
    {array_type}_spectrum.csv

This ensures that:
    - multiple runs do not overwrite each other
    - TASD and CBSD results are easily identifiable
    - global and run-specific directories remain synchronized
"""


import os
import pandas as pd


# Directory creation helper
def ensure_dir(path: str):
    """
    Create a directory if it does not already exist.

    :param path: str
                 Path to directory to create

    Notes:
        - This function is intentionally minimal -- it is used by both global and
          run-specific output paths to ensure the directory structure exists before
          writing CSV files.
    """
    os.makedirs(path, exist_ok=True)


def save_flux_csv(
        global_output_dir: str,
        run_output_dir: str,
        array_type: str,
        centers,
        widths,
        n_events,
        exposure,
        flux,
        flux_low,
        flux_high):
    """
    Save final flux table to CSV.

    The table is written to BOTH:
        - global_output_dir/data/
        - run_output_dir/data/

    Final CSV columns:
        Energy, Bin_size, N_events, Exposure, J, Lower, Upper

    Here:
        Energy      = log10(E/eV) bin center
        Bin_size    = bin width in log10(E/eV)
        N_events    = data counts per bin
        Exposure    = exposure per bin [m^2 sr s]
        J           = flux J(E) in [m^-2 sr^-1 s^-1 eV^-1] up to a scaling by binning convention
        Lower       = lower FC flux bound
        Upper       = upper FC flux bound

    :param global_output_dir: str
                              Path to global output directory (e.g., "output")
    :param run_output_dir: str
                           Path to run-specific output directory (e.g., "output/runs/<timestamp>")
    :param array_type: str
                       "TASD" or "CBSD". Used to tag filenames
    :param centers: array-like
                    log10(E/eV) bin centers
    :param widths: array-like
                   Bin widths in log10(E/eV)
    :param n_events: array-like
                     Data counts per bin
    :param exposure: array-like
                     Exposure per bin [m² sr s]
    :param flux: array-like
                 Differential flux J(E) [m^-2 sr^-1 s^-1 eV^-1]
    :param flux_low: array-like
                     Feldman-Cousins lower bounds on J(E)
    :param flux_high: array-like
                      Feldman-Cousins upper bounds on J(E)
    :return global_path: tuple of str
                         Path to global saved CSV file
    :return run_path: tuple of str
                      Path to run-specific saved CSV file
    """
    # Global directory
    global_data_dir = os.path.join(global_output_dir, "data")
    ensure_dir(global_data_dir)

    # Run-specific directory
    run_data_dir = os.path.join(run_output_dir, "data")
    ensure_dir(run_data_dir)

    # Construct DataFrame
    df = pd.DataFrame({
        "Energy": centers,
        "Bin_size": widths,
        "N_events": n_events,
        "Exposure": exposure,
        "J": flux,
        "Lower": flux_low,
        "Upper": flux_high,
    })

    # Array-tagged filename
    filename = f"{array_type}_flux.csv"

    global_path = os.path.join(global_data_dir, filename)
    run_path = os.path.join(run_data_dir, filename)

    # Save to both locations
    df.to_csv(global_path, index=False)
    df.to_csv(run_path, index=False)

    return global_path, run_path


def save_spectrum_csv(
        global_output_dir: str,
        run_output_dir: str,
        array_type: str,
        centers,
        spectrum,
        spectrum_low,
        spectrum_high):
    """
    Save final E³J(E) spectrum table to CSV.

    The table is written to BOTH:
        - global_output_dir/data/
        - run_output_dir/data/

    Final CSV columns:
        Energy, Spectrum, Lower, Upper

    Here:
        Energy      = log10(E/eV) bin center
        Spectrum    = spectrum E^3 J(E) in [eV^2 m^-2 sr^-1 s^-1]
        Lower       = lower FC flux bound
        Upper       = upper FC flux bound

    :param global_output_dir: str
                              Path to global output directory (e.g., "output")
    :param run_output_dir: str
                           Path to run-specific output directory (e.g., "output/runs/<timestamp>")
    :param array_type: str
                       "TASD" or "CBSD". Used to tag filenames
    :param centers: array-like
                    log10(E/eV) bin centers
    :param spectrum: array-like
                     E³J(E) spectrum values
    :param spectrum_low: array-like
                         Feldman-Cousins lower bounds on J(E) in spectrum space
    :param spectrum_high: array-like
                          Feldman-Cousins upper bounds on J(E) in spectrum space
    :return global_path: tuple of str
                         Path to global saved CSV file
    :return run_path: tuple of str
                      Path to run-specific saved CSV file
    """
    # Global directory
    global_data_dir = os.path.join(global_output_dir, "data")
    ensure_dir(global_data_dir)

    # Run-specific directory
    run_data_dir = os.path.join(run_output_dir, "data")
    ensure_dir(run_data_dir)

    # Construct DataFrame
    df = pd.DataFrame({
        "Energy": centers,
        "Spectrum": spectrum,
        "Lower": spectrum_low,
        "Upper": spectrum_high,
    })

    # Array-tagged filename
    filename = f"{array_type}_spectrum.csv"

    global_path = os.path.join(global_data_dir, filename)
    run_path = os.path.join(run_data_dir, filename)

    # Save to both locations
    df.to_csv(global_path, index=False)
    df.to_csv(run_path, index=False)

    return global_path, run_path