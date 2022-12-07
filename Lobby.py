from ConnectionManager import ConnectionManager
from exceptions.ClientNotRunningException import ClientNotRunningException
from random import choice

class Lobby:
    def __init__(self, logger, config) -> None:
        self.logger = logger
        self.config = config
        self.cm = ConnectionManager()
        self.defaultBotDifficulty = self.config.get("defaultBotDifficulty", "MEDIUM")

    def createLobby(self, gameMode="PRACTICETOOL", spectatorPolicy="AllAllowed", teamSize=5, lobbyName="League of Poro's Practice Tool", lobbyPassword=""):
        if self.cm.isConnected():
            data = {
                "customGameLobby": {
                    "configuration": {
                        "gameMode": gameMode,
                        "gameMutator": "",
                        "gameServerRegion": "",
                        "mapId": 11,
                        "mutators": {
                            "id": 1
                        },
                        "spectatorPolicy": spectatorPolicy,
                        "teamSize": teamSize,
                    },
                    "lobbyName": lobbyName,
                    "lobbyPassword": lobbyPassword
                },
                "isCustom": True,
            }

            lobby = self.cm.post('/lol-lobby/v2/lobby', data)
            if lobby.status_code == 200:
                self.logger.info('The lobby was created correctly')
            else:
                self.logger.error('Cannot create the lobby')
        else:
            self.logger.critical("Could not communicate with the client")
            raise ClientNotRunningException()

    def createLobbyFromConfig(self):
        self.createLobby(gameMode=self.config.get("gameMode", "PRACTICETOOL"), spectatorPolicy=self.config.get("spectatorPolicy", "AllAllowed"), teamSize=self.config.getInt(
            "teamSize", 5), lobbyName=self.config.get("lobbyName", "League of Poro's Practice Tool"), lobbyPassword=self.config.get("lobbyPassword", ""))

    def addBotsFromConfig(self):
        freeSlots = self.getFreeSlots()
        if self.config.getInt('maxBotsBlue', freeSlots[0]) < freeSlots[0]:
            numBotsBlue = self.config.getInt('maxBotsBlue')
        else:
            numBotsBlue = freeSlots[0]
        if self.config.getInt('maxBotsRed', freeSlots[1]) < freeSlots[1]:
            numBotsRed = self.config.getInt('maxBotsRed')
        else:
            numBotsRed = freeSlots[1]
        
        usedBots = []
        availableBots = self.getAvailableBots()
        # Add Blue bots
        for i in range(numBotsBlue):
            bot = self.config.getNested('botsBlue', i)
            if bot:
                self.addBot(100, bot["championId"], bot.get("botDifficulty", self.defaultBotDifficulty))
            else:
                usedBots.append(self.addRandomBot(100, usedBots=usedBots, availableBots=availableBots, difficulty=self.defaultBotDifficulty))

        # Add Red bots
        for i in range(numBotsRed):
            bot = self.config.getNested('botsRed', i)
            if bot:
                self.addBot(200, bot["championId"], bot.get("botDifficulty", self.defaultBotDifficulty))
            else:
                usedBots.append(self.addRandomBot(200, usedBots=usedBots, availableBots=availableBots, difficulty=self.defaultBotDifficulty))
    
    def addBot(self, teamId, championId, difficulty="MEDIUM"):
        data = {
            "botDifficulty": difficulty,
            "championId": championId,
            "teamId": str(teamId)
        }
        if self.cm.post("/lol-lobby/v1/lobby/custom/bots", data).status_code == 204:
            self.logger.info("Bot added")
        else:
            self.logger.error("Failed to add bot")
    
    def addRandomBot(self, teamId, usedBots = [], availableBots = None, difficulty="MEDIUM"):
        if not availableBots:
            availableBots = self.getAvailableBots()
        while (championId := choice(availableBots)["id"]) in usedBots:
            pass
        self.addBot(teamId, championId, difficulty)
        return championId

    def getFreeSlots(self):
        gameCfg = self.cm.get("/lol-lobby/v2/lobby").json()["gameConfig"]
        team100 = 5 - len(gameCfg["customTeam100"])
        team200 = 5 - len(gameCfg["customTeam200"])
        return (team100, team200)
    
    def getAvailableBots(self):
        return self.cm.get("/lol-lobby/v2/lobby/custom/available-bots").json()

    def testCall(self):
        return self.cm.get("/lol-lobby/v2/lobby/members").json()
