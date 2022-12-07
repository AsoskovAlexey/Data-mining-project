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


def read_configuration():
    "Returns a data from configuration.json"
    CONFIGURATION_FILE = "configuration.json"
    return read_json(CONFIGURATION_FILE)

def append_file(path, text):
    with open(path, "a") as file:
        file.write(text + "\n")