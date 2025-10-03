import awkward as ak
import pyarrow.parquet as pq
import config
from pathlib import Path

parquet_file = pq.ParquetFile(config.CBDTINFILE)


def set_up_data_frame(infile: Path, tree_name: str):
    if tree_name == "resTree":
    for i in parquet_file.iter_batches(batch_size=160000):
        print(f"RecordBatch {i}")
        df = i.to_pandas()
    return df


