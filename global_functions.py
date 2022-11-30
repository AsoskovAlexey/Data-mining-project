import json


def read_file(path):
    """Returns a file as a string"""
    try:
        with open(path) as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: No such file: {path}")


def read_json(path):
    """Returns a data from json"""
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: No such file: {path}")
