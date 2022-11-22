import json
import os


class Settings:

    def __init__(self):
        try:
            settings_config = "config.json"
            settings = json.load(open(settings_config, "r"))
            for setting_key in settings:
                setattr(self, setting_key, settings[setting_key])
        except Exception:
            print(f"Could not load settings! Please make sure, that config.json is in the directory {os.path.dirname(os.path.realpath(__file__))}")


if __name__ == '__main__':
    setting1 = Settings()
    print(setting1.XPATH_mask)
