import pyarrow.dataset as ds


def load_all(path: str):
    dataset = ds.dataset(path, format="parquet", partitioning=["event_time"])
    return dataset.to_table().to_pandas()
