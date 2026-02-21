# cbspec

**cbspec** is a modular, physics‑transparent Python package for converting 
Telescope Array **TASD** or **CBSD** (checkerboard) detector data into an 
ultra‑high‑energy cosmic‑ray (UHECR) **flux** and  **E³J(E) spectrum**. 

Basic pipeline:
- Parquet ingestion for MC and data
- Automatic tree-type detection (resTree vs. tTlfit)
- TA‑style quality cuts (fully configurable)
- Energy binning in log10(E/eV)
- MC → Data transfer function
- Aperture and exposure calculation
- Flux J(E) and E³J(E) spectrum
- Feldman–Cousins confidence intervals
- Publication‑quality plots
- Reproducible CSV outputs
- YAML-driven configuration
- text + JSON logging

## Features

### **Data ingestion & processing** 
- Reads **parquet** files for MC and data 
- Automatic **tree‑type detection** (`resTree` vs `tTlfit`) 
- TA‑style **quality cuts** (fully configurable in YAML)
- Batch‑wise parquet processing with detailed logging 
- FD energy correction and log10(E/eV) computation 
- Extraction of: - MC reconstructed log10(E) 
- MC true log10(E) 
- data reconstructed log10(E) 

### **Physics pipeline** 
- Energy binning in **log10(E/eV)** 
- MC → data transfer via:
  - reconstructed MC counts 
  - thrown MC counts 
- Aperture in the *i$^{th}$* $\log_{10}E$ bin: 

$$
\alpha_i = \frac{(N^{\text{MC}}_{\text{REC}})_i}{(N^{\text{MC}}_{\text{GEN}})_i} \, A_{\text{GEN}} \, \Omega_{\text{GEN}} 
$$ 

- Exposure in the *i$^{th}$* $\log_{10}E$ bin: 

$$ 
\lambda_i = \alpha_i \times T 
$$ 

- Flux in the *i$^{th}$* $\log_{10}E$ bin: 

$$
J_i = \frac{(N^{\text{DATA}}_{\text{REC}})_i / \Delta E_i}{\lambda_i} 
$$

- Feldman–Cousins confidence intervals via **FCpy** 
- Spectrum in the *i$^{th}$* $\log_{10}E$ bin: 
$$
S_i = E_i^3 J_i 
$$ 

### **Outputs** 
- **Plots** (saved in `output/plots/`): 
  - `full_aperture.png` 
  - `full_exposure.png` 
  - `full_flux.png` 
  - `full_spectrum.png` 
  - MC/data histograms 
  
- **Data products** (saved in `output/data/`): 
  - `full_flux.csv` 
     ``` 
    Energy, Bin_size, N_events, Exposure, J, Lower, Upper 
    ``` 
  - `full_spectrum.csv` 
    ``` 
    Energy, Spectrum, Lower, Upper 
    ``` 
  
### **Configuration & CLI** 
- YAML‑driven configuration (`config/default_config.yaml`) 
- CLI overrides:
  - `python -m cbspec --array CBSD`
  - `python -m cbspec --mc-file path/to/mc.parquet --dt-file path/to/data.parquet`
- Fully modular codebase:
  - src/cbspec/
    - binning.py 
    - exposure.py 
    - flux.py 
    - spectrum.py 
    - plotting.py 
    - process_data.py 
    - feldman_cousins.py 
    - logging_utils.py 
    - output_utils.py 
    - main.py 
    - cli.py

## Install

### 1. Create the conda environment 

```bash 
conda env create -f environment.yml 
conda activate cbspec
```

### 2. Install cbspec in editable mode
```bash
pip install -e .
```

## Running the Pipeline

```bash
python -m cbspec
```
or with overrides:
```bash
python -m cbspec \ 
  --config config/default_config.yaml \ 
  --array TASD \ 
  --mc-file /path/to/mc.parquet \ 
  --dt-file /path/to/data.parquet
```
This will:
1. Load configuration
2. Process MC + data parquet files 
3. Apply TA‑style quality cuts 
4. Build log10(E/eV) energy bins 
5. Histogram MC_reco, MC_raw, and data 
6. Compute aperture and exposure 
7. Compute Feldman–Cousins intervals 
8. Compute flux J 
9. Save:
   - `output/data/full_flux.csv` 
   - `output/data/full_spectrum.csv`
10. Produce publication‑quality plots in `output/plots/`
11. Log all steps to `output/logs/`