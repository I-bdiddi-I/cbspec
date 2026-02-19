"""
Dataclasses defining the configuration structures for cbspec.
"""

import numpy as np
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ArrayConfig:
    """
    Configuration for detector array type and file paths.

    array_type  : "TASD" or "CBSD"
    mc_file     : MC parquet file path
    dt_file     : Data parquet file path
    """
    array_type: str
    mc_file: Path
    dt_file: Path

@dataclass
class SpectrumConfig:
    """
    Configuration for spectrum calculation.

    en_range                    : log10(E/EeV) bin edges
    generated_area_m2           : MC generated area from Dmitri Ivanov's thesis in m^2
    generated_solid_angel_sr    : MC generated solid angel from Dmitri Ivanov's thesis in sr
    run_time_s                  : Telescope Array detector run time in s
    """
    en_range: np.ndarray
    generated_area_m2: float
    generated_solid_angle_sr: float
    run_time_s: float

@dataclass
class QualityCuts:
    """
    Configuration for all TA-style quality cuts.
    """
    number_of_good_sd: int
    theta_deg: float
    boarder_dist_m: float
    geometry_chi2: float
    ldf_chi2: float
    ped_error: float
    frac_s800: float

@dataclass
class OutputConfig:
    """
    Configuration for output file paths.
    """
    base_dir: Path
    plots_dir: Path
    logs_dir: Path
    runs_dir: Path