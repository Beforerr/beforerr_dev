from matplotlib.pyplot import Axes
from typing import Iterable

def unify_axes_fontsize(axes: Iterable[Axes], fontsize=8):
    for ax in axes:
        items = (
            [ax.title, ax.xaxis.label, ax.yaxis.label]
            + ax.get_xticklabels()
            + ax.get_yticklabels()
        )
        for item in items:
            item.set_fontsize(fontsize)
