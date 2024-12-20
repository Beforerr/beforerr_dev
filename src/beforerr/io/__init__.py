# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/03_io.ipynb.

# %% auto 0
__all__ = ['load', 'save', 'action']

# %% ../../../nbs/03_io.ipynb 1
from intake.readers.datatypes import recommend, JSONFile, PickleFile, Feather2
import importlib
import os
from functools import partial
from pydantic import validate_call
from pathlib import Path

# %% ../../../nbs/03_io.ipynb 2
maps = {
    JSONFile: ["beforerr.io.json"],
    PickleFile: ["beforerr.io.pickle"],
    Feather2: ["beforerr.io.arrow_ipc"],
}


def checkpath(file):
    # Placeholder implementation, replace with actual path checking logic
    pass


def query_datatype(file: str):
    """query the datatype of a file

    See also `os.path.splitext(file)` to get the file extension
    """
    datatypes = recommend(file)
    ext = os.path.splitext(file)[1]
    if JSONFile in datatypes or ext == ".json":
        return JSONFile
    if Feather2 in datatypes or ext == ".arrow":
        return Feather2
    else:
        return PickleFile


def applicable_func(datatype, func="load"):
    libraries = maps[datatype]
    lib = libraries[0]
    mod = importlib.import_module(lib)
    return getattr(mod, func)

# %% ../../../nbs/03_io.ipynb 3
@validate_call
def action(func, file: Path, *args, **kwargs):
    checkpath(file)
    dp = query_datatype(file.as_posix())
    return applicable_func(dp, func)(file, *args, **kwargs)


load = partial(action, "load")
save = partial(action, "save")
