"""
Command-line interface for cbspec pipline.

Usage:
  python -m cbspec
  python -m cbspec --config config/default_config.yaml
  python -m cbspec --array CBSD
"""

import argparse
from pathlib import Path
from cbspec.main import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Run cbspec pipeline.")
    parser.add_argument(
        "--config",
        type=str,
        default="config/default_config.yaml",
        help="YAML configuration file path.",
    )
    parser.add_argument(
        "--array",
        type=str,
        choices=["TASD", "CBSD"],
        help="Array type to use (TASD, CBSD).",
        default="TASD",
    )

    args = parser.parse_args()

    run_pipeline(
        config_path=Path(args.config),
        array_type=args.array,
    )