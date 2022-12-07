import json

class Config:
    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)

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