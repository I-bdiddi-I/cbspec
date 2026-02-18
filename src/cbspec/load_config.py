"""
This module handles YAML configuration loading.
"""

from pathlib import Path
import yaml
import numpy as np
from cbspec.data_classes import ArrayConfig, SpectrumConfig, QualityCuts

def load_config(path: Path):
    """
    Load configuration from YAML file and return ArrayConfig, SpectrumConfig,
    and QualityCuts dataclasses.
    :param path:
    :return:
    """
    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist")

    with open(path, 'r') as f:
        cfg = yaml.safe_load(f)

    # Array configuration
    array_cfg = ArrayConfig(
        array_type=cfg["array"]["type"],
        mc_file=Path(cfg["data"]["mc_file"]),
        dt_file=Path(cfg["data"]["dt_file"]),
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

    return array_cfg, spectrum_cfg, quality_cuts