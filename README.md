# cbspec

cbspec is a modular, physics‑transparent pipeline for converting TASD or CBSD
detector data into an ultra‑high‑energy cosmic‑ray spectrum. It follows the same
architectural philosophy as bkmodel: flat, explicit, reproducible, and easy to extend.

## Features

- Parquet ingestion for MC and data
- TA‑style quality cuts
- Energy binning in log10(E/eV)
- MC → Data transfer function
- Aperture and exposure calculation
- Flux and E³J spectrum
- Feldman–Cousins confidence intervals
- Publication‑quality plots

## Install

```bash
conda env create -f environment.yml
conda activate cbspec
pip install -e .
