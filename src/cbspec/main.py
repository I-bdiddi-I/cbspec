"""
Top-level orchestration of the cbspec pipeline.

This module defines `run_pipeline`, which is the central function called by:
    - python -m cbspec
    - cbspec (via pyproject.toml entry point)
    - programmatic use: from cbspec import run_pipeline

The pipeline performs:
     1. Logging + run directory setup
     2. Parquet ingestion (MC + data)
     3. Quality cuts
     4. Energy binning
     5. Histogramming (MC_recon, MC_thrown, data)
     6. Bin filtering
     7. Aperture AΩ(E)
     8. Exposure λ(E)
     9. Feldman-Cousins intervals
    10. Flux J(E)
    11. Spectrum E³J(E)
    12. CSV output (global + run-specific)
    13. Plotting (global + run-specific)
"""

from pathlib import Path
from datetime import datetime

import numpy as np

from .process_data import set_up_energy_array
from .binning import make_energy_bins, histgram_data_per_bin, filter_bins
from .exposure import compute_aperture, compute_exposure
from .feldman_cousins import feldman_cousins_vector
from .flux import compute_flux
from .spectrum import flux_to_spectrum
from .output_utils import save_flux_csv, save_spectrum_csv
from .plotting import (
    plot_aperture,
    plot_exposure,
    plot_flux,
    plot_spectrum,
    mc_recon_hist,
    mc_thrown_hist,
    dt_hist,
)
from .logging_utils import RunLogger


# Run directory helper
def _make_run_directory(output_cfg):
    """
    Create a timestamped run directory under output/runs/.
    :return run_dir: Path
                     Path to the run directory
    :return logs_dir: Path
                      Path to the logs directory inside the run directory
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_cfg.runs_dir / timestamp
    logs_dir = run_dir / "logs"

    logs_dir.mkdir(parents=True, exist_ok=True)
    return run_dir, logs_dir


# Main pipeline
def run_pipeline(array_cfg, spectrum_cfg, cuts_cfg, output_cfg):
    """
    Execute the full cbspec pipeline.
    :param array_cfg: ArrayConfig
                      Contains array type and MC/data file paths
    :param spectrum_cfg: SpectrumConfig
                         Contains energy bin edges, generated area, solid angle, and run time.
    :param cuts_cfg: QualityCuts
                     TA-style quality cuts thresholds
    :param output_cfg: OutputConfig
                       Base, plots, logs, and runs directory configuration.
    :return dict: Dictionary containing all final arrays (flux, spectrum, etc.)
    """
    # Create run directory + logger
    run_dir, logs_dir = _make_run_directory(output_cfg)
    logger = RunLogger(logs_dir)

    logger.log_text("Starting cbspec pipeline...")
    logger.log_json(event="pipeline_start", array=array_cfg.array_type)

    # Parquet ingestion (MC + data)
    logger.log_text("Reading parquet files and applying quality cuts...")
    mc_array, dt_array, mc_thrown_array = set_up_energy_array(
        infiles=[array_cfg.mc_file, array_cfg.dt_file],
        array_type=array_cfg.array_type,
        cuts=cuts_cfg,
        logger=logger,
    )

    # Energy binning
    edges, centers, widths = make_energy_bins(spectrum_cfg.en_range)

    # Histogram MC_recon, MC_thrown, data
    mc_counts, dt_counts, mc_thrown_counts = histgram_data_per_bin(
        mc_array, dt_array, mc_thrown_array, edges
    )

    # Filter bins (log10(E/eV) > 18.5, N_MC_Thrown > 1)
    (
        mask,
        mc_counts_f,
        dt_counts_f,
        mc_thrown_counts_f,
        centers_f,
    ) = filter_bins(mc_counts, dt_counts, mc_thrown_counts, centers)

    widths_f = widths[mask]

    # Aperture AΩ(E)
    aperture = compute_aperture(
        mc_counts_f,
        mc_thrown_counts_f,
        spectrum_cfg.generated_area_m2,
        spectrum_cfg.generated_solid_angle_sr,
    )

    # Exposure λ(E)
    exposure = compute_exposure(aperture, spectrum_cfg.run_time_s)

    # Feldman-Cousins intervals on counts
    fc_lower, fc_upper = feldman_cousins_vector(dt_counts_f, cl=0.68)

    # Flux J(E)
    flux = compute_flux(dt_counts_f, exposure, widths_f)
    flux_lower = compute_flux(fc_lower, exposure, widths_f)
    flux_upper = compute_flux(fc_upper, exposure, widths_f)

    # Spectrum E³J(E)
    spectrum, spectrum_lower, spectrum_upper = flux_to_spectrum(
        centers_f, flux, flux_lower, flux_upper
    )

    # Save CSV outputs (global + run-specific)
    save_flux_csv(
        global_output_dir=str(output_cfg.base_dir),
        run_output_dir=str(run_dir),
        array_type=array_cfg.array_type,
        centers=centers_f,
        widths=widths_f,
        n_events=dt_counts_f,
        exposure=exposure,
        flux=flux,
        flux_lower=flux_lower,
        flux_upper=flux_upper,
    )

    save_spectrum_csv(
        global_output_dir=str(output_cfg.base_dir),
        run_output_dir=str(run_dir),
        array_type=array_cfg.array_type,
        centers=centers_f,
        spectrum=spectrum,
        spectrum_lower=spectrum_lower,
        spectrum_upper=spectrum_upper,
    )

    # Plotting (global + run-specific)
    plot_aperture(centers_f, aperture, array_cfg.array_type, output_cfg.base_dir, run_dir)
    plot_exposure(centers_f, exposure, array_cfg.array_type, output_cfg.base_dir, run_dir)
    plot_flux(centers_f, flux, flux_lower, flux_upper, array_cfg.array_type, output_cfg.base_dir, run_dir)
    plot_spectrum(centers_f, spectrum, spectrum_lower, spectrum_upper, array_cfg.array_type,output_cfg.base_dir, run_dir)
    mc_recon_hist(mc_array,array_cfg.array_type, output_cfg.base_dir, run_dir)
    mc_thrown_hist(mc_thrown_array,array_cfg.array_type, output_cfg.base_dir, run_dir)
    dt_hist(dt_array, array_cfg.array_type, output_cfg.base_dir, run_dir)

    # Finalize
    logger.log_text("Pipeline completed successfully.")
    logger.log_json(event="pipeline_end")
    logger.close()

    return {
        "centers": centers_f,
        "widths": widths_f,
        "mc_counts": mc_counts_f,
        "dt_counts": dt_counts_f,
        "mc_thrown_counts": mc_thrown_counts_f,
        "aperture": aperture,
        "exposure": exposure,
        "flux": flux,
        "flux_lower": flux_lower,
        "flux_upper": flux_upper,
        "spectrum": spectrum,
        "spectrum_lower": spectrum_lower,
        "spectrum_upper": spectrum_upper,
    }