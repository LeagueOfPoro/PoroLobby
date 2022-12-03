#!/usr/bin/env python3

from asyncio import gather
from random import sample
from lcu_driver import Connector

async def get_summoner(connection):
    result = await connection.request('GET', '/lol-summoner/v1/current-summoner')
    if result.status != 200:
        raise RuntimeError("Cannot request summoner profile.")
    return await result.json()

async def create_lobby(connection, game_mode, lobby_name, password, spectator_policy):
    if game_mode not in ["PRACTICETOOL", "CLASSIC"]:
        raise ValueError(f'game_mode={game_mode}')

    if spectator_policy not in ["AllAllowed", "NotAllowed"]:
        raise ValueError(f'spectator_policy={spectator_policy}')

    data = {
        "isCustom": True,
        "customGameLobby": {
            "configuration": {
                "gameMode": game_mode,
                "mapId": 11,
                "mutators": {
                    "id": 1
                },
                "spectatorPolicy": spectator_policy,
                "teamSize": 5,
            },
            "lobbyName": lobby_name,
            "lobbyPassword": password
        },
    }
    result = await connection.request('POST', '/lol-lobby/v2/lobby', data=data)
    if result.status != 200:
        raise RuntimeError("Cannot create lobby.")
    return await result.json()

async def get_available_bots(connection):
    result = await connection.request('GET', '/lol-lobby/v2/lobby/custom/available-bots')
    if result.status != 200:
        raise RuntimeError("Cannot request available bots.")
    return await result.json()

async def add_bot(connection, champion_id, team_id, difficulty):
    if team_id not in ["100", "200"]:
        raise ValueError(f'team_id={team_id}')

    if difficulty not in ["EASY", "MEDIUM"]:
        raise ValueError(f'difficulty={difficulty}')

    data = {
        "botDifficulty": difficulty,
        "championId": champion_id,
        "teamId": team_id
    }
    result = await connection.request('POST', '/lol-lobby/v1/lobby/custom/bots', data=data)
    if result.status != 204:
        raise RuntimeError(f'Cannot add bot with champion_id={champion_id} team_id={team_id} difficulty={difficulty}.')
    return await result.json()

async def add_random_bots(connection, available_bots, bot_count_red, bot_count_blue, difficulty):
    if bot_count_red > 4 or bot_count_red < 1:
        raise ValueError(f'bot_count_red={bot_count_red}')

    if bot_count_blue > 5 or bot_count_blue < 1:
        raise ValueError(f'bot_count_blue={bot_count_blue}')

    if difficulty not in ["EASY", "MEDIUM"]:
        raise ValueError(f'difficulty={difficulty}')

    bot_count = bot_count_red + bot_count_blue
    chosen_bots = sample(available_bots, bot_count)
    futures = []
    for idx, champion in enumerate(chosen_bots):
        champion_id = champion["id"]
        team_id = "100" if idx < bot_count_red else "200"
        future = add_bot(connection, champion_id, team_id, difficulty)
        futures.append(future)
    await gather(*futures)

connector = Connector()

@connector.ready
async def connect(connection):
    difficulty = ["EASY", "MEDIUM"][1]
    password = "delete yuumi"
    mode = ["CUSTOM", "PRACTICETOOL"][1]
    bot_counts = [4, 5]
    spectator_policy = ["AllAllowed", "NotAllowed"][1]

    summoner, lobby, available_bots = await gather(
        get_summoner(connection),
        create_lobby(connection, mode, "lobby", password, spectator_policy),
        get_available_bots(connection)
    )
    await add_random_bots(connection, available_bots, bot_counts[0], bot_counts[1], difficulty)

connector.start()