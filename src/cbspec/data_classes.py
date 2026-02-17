"""
Dataclasses defining the configuration structures for cbspec.
"""

import numpy as np
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ArrayConfig:
    """Configuration for detector array type and file paths."""
    array_type: str
    mc_file: Path
    dt_file: Path

@dataclass
class SpectrumConfig:
    """Configuration for spectrum calculation."""
    en_range: np.ndarray
    generated_area_m2: float
    generated_solid_angle_sr: float
    run_time_s: float

@dataclass
class QualityCuts:
    """Configuration for all TA-style quality cuts."""
    number_of_good_sd: int
    theta_deg: float
    boarder_dist_m: float
    geometry_chi2: float
    ldf_chi2: float
    ped_error: float
    frac_s800: float
