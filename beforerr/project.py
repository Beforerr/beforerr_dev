# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_projects.ipynb.

# %% auto 0
__all__ = ['savename', 'append_prefix_suffix', 'projectdir', 'datadir', 'setup_run_dir', 'safesave', 'produce_or_load_file',
           'produce_or_load']

# %% ../nbs/02_projects.ipynb 1
import os
from .io import load, save
from datetime import timedelta
from pathlib import Path
from pydantic import validate_call

import warnings
from typing import Callable, Tuple, Union
from loguru import logger

# %% ../nbs/02_projects.ipynb 4
def valtostring(val, digits: Union[int, None], sigdigits: int) -> str:
    if isinstance(val, float):
        if digits is not None:
            return f"{val:.{digits}f}"
        elif sigdigits is not None:
            return f"{val:.{sigdigits}g}"
    return str(val)

# %% ../nbs/02_projects.ipynb 5
def savename(
    c: dict,
    prefix: str = "",
    suffix: str = "",
    allowedtypes: Tuple = (int, float, str, bool, timedelta),
    accesses: list[str] = [],
    ignores: list[str] = [],
    digits: int = None,
    connector: str = "_",
    equals: str = "=",
    expand: list[str] = [],
    sigdigits: int = 3,
    val2string: Callable = None,
    sort: bool = True,
) -> str:
    """
    Create a shorthand name based on the parameters in the dictionary `c`.

    Parameters
    ----------
    c : Dict
        The input dictionary containing the parameters.
    prefix : str, optional
        The prefix to start the name with.
    suffix : str, optional
        The suffix to end the name with.
    allowedtypes : Tuple, optional
        Only values of these types are included. (default: (int, float, str, bool))
    accesses : list[str], optional
        Specific keys to include in the name.
    ignores : list[str], optional
        Specific keys to ignore.
    digits : Union[int, None], optional
        Number of decimal digits for rounding floats.
    connector : str, optional
        String used to connect key-value pairs.
    equals : str, optional
        Connector between key and value.
    expand : list[str], optional
        Keys that will be expanded to their nested savename.
    sigdigits : int, optional
        Number of significant digits for rounding floats.
    val2string : Callable, optional
        Function to convert values to strings.
    sort : bool, optional
        Whether to sort the keys alphabetically.


    Returns
    -------
    str
        The generated shorthand name.
    """

    if any(sep in prefix for sep in ["/", "\\"]):
        warnings.warn(
            "Path separators in `savename` prefixes may break reproducibility on other OS. "
            "The recommended way is using `os.path.join` with `savename` (e.g. `os.path.join(datadir, savename(prefix, data))`)."
        )

    sigdigits = None if digits is not None else sigdigits
    val2string = val2string or (lambda val: valtostring(val, digits, sigdigits))

    labels = accesses or list(c.keys())
    p = (
        sorted(range(len(labels)), key=lambda k: labels[k])
        if sort
        else range(len(labels))
    )

    first = not prefix or prefix.endswith(os.path.sep)
    s = prefix
    for j in p:
        label = labels[j]
        if label in ignores:
            continue
        val = c[label]
        t = type(val)
        if any(issubclass(t, x) for x in allowedtypes):
            if label in expand:
                if not val:
                    continue
                sname = savename(
                    val,
                    connector=",",
                    digits=digits,
                    sigdigits=sigdigits,
                    equals=equals,
                )
                if not sname:
                    continue
                entry = f"{label}{equals}({sname})"
            else:
                entry = f"{label}{equals}{val2string(val)}"
            if not first:
                s += connector
            s += entry
            first = False

    if suffix:
        s += f".{suffix}"

    return s

# %% ../nbs/02_projects.ipynb 7
def append_prefix_suffix(name: str, prefix: str, suffix: str):
    if prefix:
        name = f"{prefix}_{name}"
    if suffix:
        name = f"{name}.{suffix}"
    return name

# %% ../nbs/02_projects.ipynb 9
def projectdir():
    try:
        path = Path(os.getenv("PIXI_PROJECT_ROOT"))
    except TypeError:
        path = Path().cwd()
    return path


def datadir():
    return projectdir() / "data"

# %% ../nbs/02_projects.ipynb 10
def setup_run_dir(
    c: dict, base_dir: Callable = datadir, change_dir: bool = True, **kwargs
):
    """
    Create a run directory based on the parameters in the dictionary `c`.

    Parameters
    ----------
    c
        The dictionary containing the parameters.
    base_dir
        The base directory to create the run directory in.

    Returns
    -------
    Path
        The run directory.
    """

    sub_dir = savename(c, **kwargs)
    base_dir = Path(base_dir()) if callable(base_dir) else Path(base_dir)
    directory = base_dir / sub_dir
    os.makedirs(directory, exist_ok=True)
    if change_dir:
        os.chdir(directory)
        logger.info(f"Changed directory to {directory}")

# %% ../nbs/02_projects.ipynb 12
@validate_call
def increment_backup_num(filepath: Path):
    if "_" in filepath.stem and filepath.stem.rsplit("_", 1)[-1].isdigit():
        base, num = filepath.stem.rsplit("_", 1)
        new_num = int(num) + 1
    else:
        base, new_num = filepath.stem, 1
    return filepath.with_name(f"{base}_{new_num}{filepath.suffix}")

# %% ../nbs/02_projects.ipynb 13
def safesave(file: str, data, save_func: Callable = save):
    path = Path(file)

    if path.exists():
        backup_path = increment_backup_num(path)
        while backup_path.exists():
            backup_path = increment_backup_num(backup_path)
        path.fs.mv(path, backup_path)
    return save_func(path, data)

# %% ../nbs/02_projects.ipynb 15
def produce_or_load_file(
    f: Callable,
    config: dict,
    file: Path,
    force: bool = False,
    verbose: bool = True,
    load_func: Callable = load,
    save_func: Callable = save,
    **kwargs,
):
    exist = file.is_file()
    if not force and exist:
        data = load_func(file, **kwargs)
        return data, file
    else:
        if verbose:
            force and print(f"Producing file {file} now...")
            not exist and print(f"File {file} does not exist. Producing it now...")

        data = f(**config)

        try:
            save_func(file, data, **kwargs)
            verbose and print(f"File {file} saved.")
        except Exception as e:
            print(f"Could not save file. Error: {e}")

        return data, file


def produce_or_load(
    f: Callable,
    config: dict = dict(),
    path: Path = datadir(),
    suffix: str = "pickle",
    prefix: str = None,
    force: bool = False,
    verbose: bool = True,
    action_kwargs: dict = {},
    filename: Union[Callable, str] = None,
    **kwargs,
):
    if filename is None:
        name = savename(prefix, config, suffix, **kwargs)
    elif callable(filename):
        name = filename(config)
    elif isinstance(filename, str):
        name = filename
    else:
        raise ValueError("filename must be a callable or a string.")

    name = append_prefix_suffix(filename, prefix, suffix)

    file = path / name

    return produce_or_load_file(f, config, file, force, verbose, **action_kwargs)
