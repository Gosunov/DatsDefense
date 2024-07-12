import random

import requests
import json

TOKEN = '66912b6a10f7166912b6a10f75'
BASE_URL = 'https://games-test.datsteam.dev'

def request(method, endpoint, body=None):
    if body is None:
        body = {}
    url = BASE_URL + endpoint
    headers = {
        'X-Auth-Token': TOKEN
    }
    r = requests.request(method, url, json=body, headers=headers)
    if r.status_code != 200:
        raise Exception('Got %d status code from server, server returned %s' % (r.status_code, r.text))
    return r.json()


def participate():
    return request('put', '/play/zombidef/participate')

def command(body):
    return request('post', '/play/zombidef/command', body)

def units():
    global units_
    #units_ = request('get', '/play/zombidef/units')
    units_ = {'realmName': 'test-day1-2', 'player': {'gold': 10, 'points': 0, 'name': 'хочу макбук', 'zombieKills': 0, 'enemyBlockKills': 0, 'gameEndedAt': None}, 'base': [{'id': '0190a7c3-1f44-7551-b168-c8da18a21688', 'x': 176, 'y': 29, 'health': 100, 'attack': 10, 'range': 5, 'lastAttack': None}, {'id': '0190a7c3-1f44-753f-9127-94759d546f72', 'x': 175, 'y': 28, 'health': 300, 'attack': 40, 'range': 8, 'isHead': True, 'lastAttack': None}, {'id': '0190a7c3-1f44-754c-bc3e-a593d13dff53', 'x': 175, 'y': 29, 'health': 100, 'attack': 10, 'range': 5, 'lastAttack': None}, {'id': '0190a7c3-1f44-7547-bcac-a94c84e93bba', 'x': 176, 'y': 28, 'health': 100, 'attack': 10, 'range': 5, 'lastAttack': None}], 'zombies': [{'x': 175, 'y': 18, 'id': '1cbd05e3-3cda-4f0e-94db-b267a9a33aea', 'type': 'fast', 'health': 9, 'attack': 13, 'speed': 2, 'waitTurns': 1, 'direction': 'left'}, {'x': 171, 'y': 35, 'id': '1eea3797-69f2-4849-94fd-7bb9625272b0', 'type': 'fast', 'health': 7, 'attack': 7, 'speed': 2, 'waitTurns': 1, 'direction': 'right'}, {'x': 184, 'y': 30, 'id': '2b8da2cc-94e6-4298-bfb9-93cbdfa2855f', 'type': 'bomber', 'health': 7, 'attack': 7, 'speed': 1, 'waitTurns': 1, 'direction': 'left'}, {'x': 165, 'y': 30, 'id': 'e71d6759-0a07-46f7-bf07-dd8eb80e1541', 'type': 'normal', 'health': 9, 'attack': 13, 'speed': 1, 'waitTurns': 1, 'direction': 'right'}, {'x': 165, 'y': 33, 'id': '48fde7b4-d21f-4d7a-ab77-ac886eb42bbd', 'type': 'normal', 'health': 7, 'attack': 7, 'speed': 1, 'waitTurns': 1, 'direction': 'left'}, {'x': 172, 'y': 39, 'id': '5d08fc1d-69f7-4673-9030-c1bbaeac935e', 'type': 'chaos_knight', 'health': 7, 'attack': 7, 'speed': 3, 'waitTurns': 1, 'direction': 'left'}, {'x': 177, 'y': 38, 'id': '7b0a0577-f304-4a8c-87e2-65d2331f2983', 'type': 'liner', 'health': 9, 'attack': 13, 'speed': 1, 'waitTurns': 1, 'direction': 'right'}, {'x': 183, 'y': 18, 'id': 'b7b42574-d63b-487c-bd07-38c21038bbf9', 'type': 'fast', 'health': 9, 'attack': 13, 'speed': 2, 'waitTurns': 1, 'direction': 'right'}, {'x': 171, 'y': 30, 'id': 'b34589bd-4754-45af-b61e-fbaab46751b8', 'type': 'fast', 'health': 7, 'attack': 7, 'speed': 2, 'waitTurns': 1, 'direction': 'left'}, {'x': 181, 'y': 25, 'id': 'b8556d8d-9a1f-450d-9c74-843e106332b7', 'type': 'liner', 'health': 7, 'attack': 7, 'speed': 1, 'waitTurns': 1, 'direction': 'left'}, {'x': 171, 'y': 21, 'id': '114f8973-f619-49b9-95d7-c0f71f0e0035', 'type': 'normal', 'health': 9, 'attack': 13, 'speed': 1, 'waitTurns': 1, 'direction': 'left'}, {'x': 180, 'y': 37, 'id': '5865e7e5-a3cb-49b3-aae7-9340f143abc2', 'type': 'juggernaut', 'health': 7, 'attack': 999999, 'speed': 1, 'waitTurns': 1, 'direction': 'right'}], 'enemyBlocks': None, 'turnEndsInMs': 1391, 'turn': 27}
    return units_

def world():
    return request('get', '/play/zombidef/world')

def world():
    return request('get', '/play/zombidef/world')

def rounds():
    return request('get', '/rounds/zombidef')

units_ = {}

def build_some():
    global units_
    print(units_)

    availab_spots = set()

    X = units_['base'][0]['x']
    Y = units_['base'][0]['y']

    for unit in units_['base']:
        availab_spots.add((unit['x'], unit['y'] + 1))
        availab_spots.add((unit['x'], unit['y'] - 1))
        availab_spots.add((unit['x'] - 1, unit['y']))
        availab_spots.add((unit['x'] + 1, unit['y']))

    for unit in units_['base']:
        availab_spots.remove((unit['x'], unit['y']))

    print()

    build_com = []

    for i in range(10):

        elem = random.choice(tuple(availab_spots))

        build_com.append({'x': elem[0], 'y': elem[1]})


    print(build_com)

    return command(
        {
            'attack': [],
            'build': build_com,
            'moveBase': {},
        }
    )

def world():
    return request('get', '/play/zombidef/world')

def world():
    return request('get', '/play/zombidef/world')

def rounds():
    return request('get', '/rounds/zombidef')

def pprint(d):
    json_formatted_str = json.dumps(d, indent=2)
    print(json_formatted_str)


#pprint(rounds())

print(units())
print(build_some())
print(world())