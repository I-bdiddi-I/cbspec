# cbspec

cbspec is a modular, physics‑transparent Python package for converting Telescope Array TASD or CBSD (checkerboard)
detector data into an ultra‑high‑energy cosmic‑ray spectrum. 

## Features

- Parquet ingestion for MC and data
- Automatic tree-type detection (resTree vs. tTlfit)
- TA‑style quality cuts (fully configurable)
- Energy binning in log10(E/eV)
- MC → Data transfer function
- Aperture and exposure calculation
- Flux J(E) and E³J(E) spectrum
- Feldman–Cousins confidence intervals
- Publication‑quality plots
- YAML-driven configuration

## Install

```bash
conda env create -f environment.yml
conda activate cbspec
pip install -e .
