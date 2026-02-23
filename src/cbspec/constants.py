"""
Central location for numerical constants used throughout the cbspec pipeline.

These constants are intentionally minimal -- the physics lives in the modules
that use them. Keeping them here ensures:
    - a single source of values
    - easy modification
    - clear visibility of all global numerical factors
"""

# Fluorescence-detector energy correction factor
fd_energy_corr = 1.27

# Shift from log10(E/EeV) to log10(E/eV)
EeV_corr = 18
