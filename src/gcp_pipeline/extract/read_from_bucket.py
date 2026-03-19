import pyarrow.compute as pc
import pyarrow.dataset as ds


def load_from(path: str, date: str):

    dataset = ds.dataset(path, format="parquet", partitioning="hive")

    table = dataset.to_table(filter=pc.field("date") >= date)

    return table


def load_all(path: str):

    dataset = ds.dataset(path, format="parquet", partitioning="hive")

    table = dataset.to_table()

    return table
