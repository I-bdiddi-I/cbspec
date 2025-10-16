import numpy as np
from pathlib import Path

GENAREA = np.pi*(25*10**3)**2 # Generated area (Dmitri's thesis) meters squared
GENOMEGA = 3*np.pi/4 # Generated solid angle (Dmitri's thesis)
RUNTIME = 16 * 365.25 * 86400 # Expirement run time in seconds

NBINS = 17
EMINLOG = 18.
EMAXLOG = 19.6
ENERGYRANGE = np.append(np.linspace(EMINLOG, EMAXLOG, NBINS),[19.8,20.0,20.3])
FDENERGYCOR = 1.27
COENERGY = 18.5

CBMCINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/tlfptn_1850.tlsdfit.result.parquet")
CBDTINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/sddt.cb.noCuts.result.parquet")

TAMCINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/tlfptn_1850.all.tlsdfit.result.parquet")
TADTINFILE = Path("/home/r_davignon/Work/Fall_2025/cbproj/parquet_data/sddt.main.result.parquet")

#Quality Cuts:
NUMBERGOODSD = 5
THETA = 45
BOARDERDIST = 1200
GEOMFIT = 4
LDFFIT = 4
PEDERROR = 5
FRACS800 = 0.25
