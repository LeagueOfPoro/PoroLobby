import json

class Config:
    def __init__(self, configFile, logger):
        try:
            with open(configFile) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logger.warning(f"The configuration file {configFile} was not found. using default values.")
            self.config = {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def getInt(self, key, default=None):
        return int(self.config.get(key, default))

    def getList(self, key, default=None):
        return self.config.get(key, default)

    def getNested(self, key1, idx):
        if key1 in self.config:
            if idx < len(self.config[key1]):
                return self.config[key1][idx]
            else:
                return None
        return None