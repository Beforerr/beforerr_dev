import polars as pl


def load(file, **kwargs):
    return pl.read_ipc(file, **kwargs)


def save(file, data: pl.DataFrame, **kwargs):
    data.write_ipc(file, **kwargs)
