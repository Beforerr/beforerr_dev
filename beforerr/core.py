# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['ifnone']

# %% ../nbs/00_core.ipynb 2
def ifnone(a, b):
    "`b` if `a` is None else `a`"
    return b if a is None else a
