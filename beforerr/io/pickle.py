from fsspec import open
import pickle


def load(file, **kwargs):
    with open(file, "r") as f:
        return pickle.load(f, **kwargs)


def save(file, data, **kwargs):
    with open(file, "wb") as f:
        pickle.dump(data, f, **kwargs)
