import numpy as np
from pathlib import Path

GENAREA = np.pi*(25*10**3)**2 # Generated area (Dmitri's thesis) meters squared
GENOMEGA = 3*np.pi/4 # Generated solid angle (Dmitri's thesis)

NBINS = 17
EMINLOG = 18.
EMAXLOG = 19.6
ENERGYRANGE = np.linspace(EMINLOG, EMAXLOG, NBINS)

CBMCINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/tlfptn_1850.tlsdfit.result.parquet")
CBDTINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/sddt.cb.noCuts.result.parquet")

TAMCINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/tlfptn_1850.all.tlsdfit.result.parquet")
TADTINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/sddt.main.result.parquet")