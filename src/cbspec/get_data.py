import awkward as ak
import pyarrow.parquet as pq
import config
from pathlib import Path
import numpy as np
import pandas as pd

#parquet_file = pq.ParquetFile(config.CBDTINFILE)


def set_up_data_frame(infile: Path, array_type: str):
    comp_df = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

    for j in range(len(infile)):
        print(f"Input File: {infile[j]}")
        count = 0
        parquet_file = pq.ParquetFile(infile[j])
        if array_type == "TASD":
            theta_corr = 0.5
        if array_type == "CBSD":
            theta_corr = 1
        for i in parquet_file.iter_batches(batch_size=160000):
            print(f"RecordBatch {i}")
            df = i.to_pandas()
            if 'energy' in df.columns:
                print('Tree Type: resTree')
                s = 2
                en = df['energy'].str[0] / config.FDENERGYCOR
                sc = df['sc'].str[0]
                dsc = df['dsc'].str[0]
                ngsd = df['nstclust']
                bdist = df['bdist'] * 1000
                ldf = df['ldfchi2'].str[0]
                gf = df['gfchi2'].str[2]
            if 'energy_s800_p' in df.columns:
                print('Tree Type: tTlfit')
                s = 1
                df['energy'] = df['energy_s800_p']
                en = df['energy'] / config.FDENERGYCOR
                sc = df['sc']
                dsc = df['dsc']
                ngsd = df['ngsd']
                bdist = df['bdist']
                ldf = df['ldfchi2pdof']
                gf = df['gfchi2pdof'].str[1]
            mcen = df['mcenergy'] / config.FDENERGYCOR
            theta = df['theta'].str[s] + theta_corr  # shift correction
            dtheta = df['dtheta'].str[s]
            mctheta = df['mctheta']
            phi = df['phi'].str[s]
            dphi = df['dphi'].str[s]
            mcphi = df['mcphi']
            fs800 = dsc / sc
            g = df['pderr'].str[s]
            df['logen'] = np.log10(en) + 18
            df['mclogen'] = np.log10(mcen) + 18
            df['flogen'] = np.log(en / mcen)

            # uncut MC
            if j == 0:
                comp_df[-1] = pd.concat([comp_df[-1], df['mclogen']], ignore_index=True)

            # quality cuts
            cdata = df[
                (ngsd >= 5) & (theta < 45) & (bdist >= 1200) & (gf < 4) & (ldf < 4) & (g < 5) & (fs800 < 0.25)]
            count += len(cdata)
            print(
                f"Number of accepted events in current loop: {len(cdata)}\nTotal number of accepted events from {infile[j]}: {count}")
            comp_df[j] = pd.concat([comp_df[j], cdata['logen']], ignore_index=True)

    return comp_df


