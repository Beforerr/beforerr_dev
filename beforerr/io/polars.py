import polars as pl
from pathlib import Path
import polars.selectors as cs
from pydantic import validate_call


@validate_call(config=dict(arbitrary_types_allowed=True))
def save(file: Path, data: pl.DataFrame, clean: bool = False, **kwargs):
    format = file.suffix[1:]
    # check the parent directory exists
    file.parent.mkdir(parents=True, exist_ok=True)

    if clean:
        data = data.select(cs.datetime(), cs.duration(), cs.numeric())

    match format:
        case "arrow":
            data.write_ipc(file, **kwargs)
        case "csv":
            data.write_csv(file, **kwargs)
        case "parquet":
            data.write_parquet(file, **kwargs)
        case _:
            raise ValueError(f"Unsupported format: {format}")
