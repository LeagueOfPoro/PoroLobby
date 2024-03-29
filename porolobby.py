import logging
from Lobby import Lobby
from pprint import pprint
from Config import Config
import argparse

parser = argparse.ArgumentParser(description='Create a practice tool or custom lobby filled with bots.')
parser.add_argument('-c', '--config', dest="configPath", default="./config.json",
                    help='Path to a config file')
parser.add_argument('-l', '--list-bots', dest="listBots", action='store_true',
                    help='List all available bots')
args = parser.parse_args()

logger = logging.getLogger()
config = Config(args.configPath, logger)
lobby = Lobby(logger, config)
if args.listBots:
    pprint(lobby.getAvailableBots())
else:
    lobby.createLobbyFromConfig()
    lobby.addBotsFromConfig()