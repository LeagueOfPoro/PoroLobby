import logging
from Lobby import Lobby
from pprint import pprint
from Config import Config

logger = logging.getLogger()
config = Config('config.json')
lobby = Lobby(logger, config)
lobby.createLobbyFromConfig()
lobby.addBotsFromConfig()