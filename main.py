import requests
import json
import time
import random

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
        data = json.dumps(r.json(), indent=2)
        raise Exception('Got %d status code from server, server returned\n %s' % (r.status_code, data))
    return r.json()


def participate():
    return request('put', '/play/zombidef/participate')


def command(body):
    return request('post', '/play/zombidef/command', body)


def units():
    return request('get', '/play/zombidef/units')


def world():
    return request('get', '/play/zombidef/world')


def rounds():
    return request('get', '/rounds/zombidef')


def pprint(d):
    json_formatted_str = json.dumps(d, indent=2)
    print(json_formatted_str)


def get_zombies(data):
    zombies = data.get('zombies')
    if zombies is None:
        return []
    return zombies


def get_base(data):
    base = data.get('base')
    if base is None:
        return []
    return base


def get_enemy_blocks(data):
    enemy_blocks = data.get('enemyBlocks')
    if enemy_blocks is None:
        return []
    return enemy_blocks


def get_attack(data):
    res = []
    base = get_base(data)
    zombies = get_zombies(data)
    zombies.sort(key=lambda zombie: zombie.get('health'))
    enemy_blocks = get_enemy_blocks(data)

    for tower in base:
        for zombie in zombies:
            tx = tower.get('x')
            ty = tower.get('y')
            r = tower.get('range')
            id = tower.get('id')

            zx = zombie.get('x')
            zy = zombie.get('y')
            if r ** 2 >= (tx - zx) ** 2 + (ty - zy) ** 2:
                res.append({
                    'blockId': id,
                    'target': {
                        'x': zx,
                        'y': zy,
                    }
                })
                break
        for enemy_block in enemy_blocks:
            tx = tower.get('x')
            ty = tower.get('y')
            r = tower.get('range')
            id = tower.get('id')

            bx = enemy_block.get('x')
            by = enemy_block.get('y')
            if r ** 2 >= (tx - bx) ** 2 + (ty - by) ** 2:
                res.append({
                    'blockId': id,
                    'target': {
                        'x': bx,
                        'y': by,
                    }
                })
                break

    return res


def get_build(data):
    units_ = data

    availab_spots = set()

    X = units_['base'][0]['x']
    Y = units_['base'][0]['y']

    for unit in units_['base']:
        availab_spots.add((unit['x'], unit['y'] + 1))
        availab_spots.add((unit['x'], unit['y'] - 1))
        availab_spots.add((unit['x'] - 1, unit['y']))
        availab_spots.add((unit['x'] + 1, unit['y']))

    for unit in units_['base']:
        try:
            availab_spots.remove((unit['x'], unit['y']))
        except:
            pass

    build_com = []

    for i in range(units_['player']['gold'] * 2):
        elem = random.choice(tuple(availab_spots))
        build_com.append({'x': elem[0], 'y': elem[1]})

    return build_com


def get_move_base(data):
    base = get_base(data)
    for tower in base:
        if 'isHead' in tower:
            return {
                'x': tower.get('x'),
                'y': tower.get('y')
            }


def get_command():
    data = units()
    build = get_build(data)
    attack = get_attack(data)
    move_base = get_move_base(data)
    r = command(
        {
            'attack': attack,
            'build': build,
            'moveBase': move_base
        }
    )
    pprint(r)



while True:
    get_command()
    time.sleep(1)
