"""
cbspec
------
A modular, physics‑transparent Python package for converting Telescope Array TASD or CBSD (checkerboard)
detector data into an ultra‑high‑energy cosmic‑ray spectrum.

Provides:
    - YAML-driven configuration
    - Parquet ingestion for MC and data
    - TA-style quality cuts
    - Energy binning
    - Aperture and exposure calculation
    - Flux and E³J(E) spectrum calculation
    - Feldman-Cousins intervals
    - Publication-quality plotting
    - Text + JSON logging
    - CLI: `python -m cbspec`
"""

from cbspec.main import run_pipeline