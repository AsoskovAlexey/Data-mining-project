import json

CONFIGURATION_FILE = "configuration.json"


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


def read_configuration(configuration_file=CONFIGURATION_FILE):
    """Returns a data from configuration.json"""
    return read_json(configuration_file)


def append_file(path, text):
    """writes text to the end of the file"""
    with open(path, "a") as file:
        file.write(text + "\n")
