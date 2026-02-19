"""
This module handles YAML configuration loading and builds dataclasses.
"""

from pathlib import Path
import yaml
import numpy as np
from cbspec.data_classes import ArrayConfig, SpectrumConfig, QualityCuts

from src.cbspec.data_classes import OutputConfig


def load_config(path: Path):
    """
    Load configuration from YAML file and return ArrayConfig, SpectrumConfig,
    and QualityCuts dataclasses.
    """
    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist")

    with open(path, 'r') as f:
        cfg = yaml.safe_load(f)

    # Array configuration
    array_type = cfg["array"]["type"]

    if array_type == "TASD":
        mc_file = cfg["data"]["tasd"]["mc_file"]
        dt_file = cfg["data"]["tasd"]["dt_file"]
    elif array_type == "CBSD":
        mc_file = cfg["data"]["cbsd"]["mc_file"]
        dt_file = cfg["data"]["cbsd"]["dt_file"]
    else:
        raise TypeError(f"Array type {array_type} is not supported")

    array_cfg = ArrayConfig(
        array_type=array_type,
        mc_file=Path(mc_file),
        dt_file=Path(dt_file),
    )

    # Spectrum configuration
    spectrum_cfg = SpectrumConfig(
        en_range=np.array(cfg["energy"]["bins"], dtype=float),
        generated_area_m2=float(cfg["geometry"]["generated_area_m2"]),
        generated_solid_angle_sr=float(cfg["geometry"]["generated_solid_angle_sr"]),
        run_time_s=float(cfg["run"]["time_s"]),
    )

    # Quality cuts
    qc = cfg["quality_cuts"]
    quality_cuts = QualityCuts(
        number_of_good_sd=qc["number_of_good_sd"],
        theta_deg=qc["theta_deg"],
        boarder_dist_m=qc["boarder_dist_m"],
        geometry_chi2=qc["geometry_chi2"],
        ldf_chi2=qc["ldf_chi2"],
        ped_error=qc["ped_error"],
        frac_s800=qc["frac_s800"],
    )

    # Output configuration
    out_cfg = cfg["output"]
    output_cfg = OutputConfig(
        base_dir=Path(out_cfg["base_dir"]),
        plots_dir=Path(out_cfg["plots_dir"]),
        logs_dir=Path(out_cfg["logs_dir"]),
        runs_dir=Path(out_cfg["runs_dir"]),
    )

    return array_cfg, spectrum_cfg, quality_cuts, output_cfg