import pyarrow.dataset as ds


def load_all(path: str):
    dataset = ds.dataset(path, format="parquet", partitioning="hive")
    return dataset.to_table().to_pandas()
