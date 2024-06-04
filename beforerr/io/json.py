from fsspec import open
import json


def load(file, **kwargs):
    with open(file, "r") as f:
        return json.load(f, **kwargs)


def save(file, data, **kwargs):
    with open(file, "w") as f:
        json.dump(data, f, **kwargs)
