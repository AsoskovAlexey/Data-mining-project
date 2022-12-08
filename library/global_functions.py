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


def create_default_scraper():
    """Returns a scraper with cookies"""
    import library.scraper as scraper
    config = read_configuration()["web"]
    default_scraper = scraper.Scraper(scroll_pause_time=0)
    default_scraper.get_page(config['url']['404_page'])
    default_scraper.add_cookies(read_json(config['cookies_file']))
    default_scraper.scroll_pause_time = 1
    return default_scraper
