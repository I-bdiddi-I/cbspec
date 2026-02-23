"""
Handles saving flux and spectrum data into CSV files.
"""

import os
import pandas as pd

def ensure_dir(path: str):
    """
    Create a directory if it does not already exist.
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
    Save final flux table to csv file:
        full_flux.csv

    Save it to BOTH:
        - global output/data
        - run-specific output/runs/<timestamp>/data/

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
    """
    # Global directory
    global_data_dir = os.path.join(global_output_dir, "data")
    ensure_dir(global_data_dir)

    # Run-specific directory
    run_data_dir = os.path.join(run_output_dir, "data")
    ensure_dir(run_data_dir)

    df = pd.DataFrame({
        "Energy": centers,
        "Bin_size": widths,
        "N_events": n_events,
        "Exposure": exposure,
        "J": flux,
        "Lower": flux_low,
        "Upper": flux_high,
    })

    filename = f"{array_type}_flux.csv"

    global_path = os.path.join(global_data_dir, filename)
    run_path = os.path.join(run_data_dir, filename)

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
    Save final spectrum table to csv file:
        full_spectrum.csv

    Save it to BOTH:
        - global output/data
        - run-specific output/runs/<timestamp>/data/

    Final CSV columns:
        Energy, Spectrum, Lower, Upper

    Here:
        Energy      = log10(E/eV) bin center
        Spectrum    = spectrum E^3 J(E) in [eV^2 m^-2 sr^-1 s^-1]
        Lower       = lower FC flux bound
        Upper       = upper FC flux bound
    """
    # Global directory
    global_data_dir = os.path.join(global_output_dir, "data")
    ensure_dir(global_data_dir)

    # Run-specific directory
    run_data_dir = os.path.join(run_output_dir, "data")
    ensure_dir(run_data_dir)

    df = pd.DataFrame({
        "Energy": centers,
        "Spectrum": spectrum,
        "Lower": spectrum_low,
        "Upper": spectrum_high,
    })

    filename = f"{array_type}_spectrum.csv"

    global_path = os.path.join(global_data_dir, filename)
    run_path = os.path.join(run_data_dir, filename)

    df.to_csv(global_path, index=False)
    df.to_csv(run_path, index=False)

    return global_path, run_path