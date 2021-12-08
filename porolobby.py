#! python3

from lcu_driver import Connector

connector = Connector()

# Creates 5v5 Practice Tool
async def createLobby(connection):
    data = {
        "customGameLobby": {
            "configuration": {
                "gameMode": "PRACTICETOOL",
                "gameMutator": "",
                "gameServerRegion": "",
                "mapId": 11,
                "mutators": {
                    "id": 1
                },
                "spectatorPolicy": "AllAllowed",
                "teamSize": 5,
            },
            "lobbyName": "League of Poro's Practice Tool",
            "lobbyPassword": ""
        },
        "isCustom": True,
    }
    # make the request to switch the lobby
    lobby = await connection.request('post', '/lol-lobby/v2/lobby', data=data)

    # if HTTP status code is 200 the lobby was created successfully
    if lobby.status == 200:
        print('The lobby was created correctly')
    else:
        print('Whops, Yasuo died again.')


# Contacts LCU API to add bots
async def executeAddBot(connection, data):
    res = await connection.request('post', '/lol-lobby/v1/lobby/custom/bots', data=data)
    if res.status == 204:
        print('Bot added')
    else:
        print('Whops, Yasuo died again.')

# Selects which bots to add and adds them to an existing lobby
async def addBots(connection):
    ids = [1, 3, 8, 10, 11]

    # add bots to the player's team
    for id in ids[:4]:
        data = {
            "botDifficulty": "EASY",
            "championId": id,
            "teamId": "100"
        }
        await executeAddBot(connection, data)

    # add bots to the opposite team
    for id in ids:
        data = {
            "botDifficulty": "EASY",
            "championId": id,
            "teamId": "200"
        }
        await executeAddBot(connection, data)


# fired when LCU API is ready to be used
@connector.ready
async def connect(connection):
    print('LCU API is ready to be used.')

    # check if the user is already logged into his account
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner.status != 200:
        print('Please login into your account.')
    else:
        print('Switching the lobby type.')
        await createLobby(connection)
        await addBots(connection)


# fired when League Client is closed (or disconnected from websocket)
@connector.close
async def disconnect(_):
    print('The client have been closed!')

# starts the connector
connector.start()
