# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_basics.ipynb.

# %% auto 0
__all__ = ['pmap']

# %% ../nbs/01_basics.ipynb 2
from pipe import select
from functools import partial

# %% ../nbs/01_basics.ipynb 3
def pmap(func, *args, **kwargs):
    """
    map with `partial`
    """
    return select(partial(func, *args, **kwargs))
