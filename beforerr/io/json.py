import json

def load(file, **kwargs):
    with open(file, "r") as file:
        return json.load(file, **kwargs)

def save(file, data, **kwargs):
    with open(file, 'w') as fp:
        json.dump(data, fp, **kwargs)
