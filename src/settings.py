from configparser import ConfigParser

class Settings:
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_config(self, section, key):
        return self.config.get(section, key)

    def set_config(self, section, key, value):
        self.config.set(section, key, value)