import awkward as ak
import pyarrow.parquet as pq
import config
from pathlib import Path

parquet_file = pq.ParquetFile(config.CBDTINFILE)


def set_up_data_frame(infile: Path, tree_name: str):
    if tree_name == "resTree":
        s = 2
        print('Tree Type: resTree')
    if tree_name == "tTlfit":
        s = 1
        print('Tree Type: tTlfit')
    for i in parquet_file.iter_batches(batch_size=160000):
        print(f"RecordBatch {i}")
        df = i.to_pandas()
        if s == 2:
            sc = df['sc'].str[0]
            dsc = df['dsc'].str[0]
            ngsd = df['nstclust']
            bdist = df['bdist'] * 1000
        if s == 1:
            sc = df['sc']
            dsc = df['dsc']
            ngsd = df['ngsd']
            bdist = df['bdist']
            df['energy'] = df['energy_s800_p']
        en = df['energy'].str[0] / config.FDENERGYCOR  # FD energy correction
        mcen = df['mcenergy'] / config.FDENERGYCOR
        theta = df['theta'].str[s] + (1/s)  # shift correction
        dtheta = df['dtheta'].str[s]
        mctheta = df['mctheta']
        phi = df['phi'].str[s]
        dphi = df['dphi'].str[s]
        mcphi = df['mcphi']
        fs800 = dsc / sc
        ldf = df['ldfchi2'].str[0]
        gf = df['gfchi2'].str[s]
        g = df['pderr'].str[s]
        df['logen'] = np.log10(en) + 18
        df['mclogen'] = np.log10(mcen) + 18
        df['flogen'] = np.log(en / mcen)
    return df


