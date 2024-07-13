import random
from collections import defaultdict, deque

from entities import *
from time import time

from utils import turncache


import human_controls

def neighbours4(coords: Coordinates) -> tuple[Coordinates, Coordinates, Coordinates, Coordinates]:
    x = coords.x
    y = coords.y

    n = Coordinates(x, y + 1)
    e = Coordinates(x + 1, y)
    s = Coordinates(x, y - 1)
    w = Coordinates(x - 1, y)
    return (n, e, s, w)

def neighbours8(coords: Coordinates) -> tuple[Coordinates, Coordinates, Coordinates, Coordinates, Coordinates, Coordinates, Coordinates, Coordinates]:
    x = coords.x
    y = coords.y

    nn = Coordinates(x + 0, y + 1)
    ne = Coordinates(x + 1, y + 1)
    ee = Coordinates(x + 1, y + 0)
    se = Coordinates(x + 1, y - 1)
    ss = Coordinates(x + 0, y - 1)
    sw = Coordinates(x - 1, y - 1)
    ww = Coordinates(x - 1, y + 0)
    nw = Coordinates(x - 1, y + 1)
    return (nn, ne, ee, se, ss, sw, ww, nw)



@turncache
def get_zombies(turn: int, data: UnitResponse, world: WorldResponse) -> dict[Coordinates, list[Zombie]]:
    coords_zombies = defaultdict(list)
    for zombie in data.zombies:
        coords = Coordinates(zombie.x, zombie.y)
        coords_zombies[coords].append(zombie)
    return dict(coords_zombies)

@turncache
def get_enemy_towers(turn: int, data: UnitResponse, world: WorldResponse) -> dict[Coordinates, EnemyTower]:
    coords_enemy_towers = dict()
    for enemy_tower in data.enemy_towers:
        coords = Coordinates(enemy_tower.x, enemy_tower.y)
        coords_enemy_towers[coords] = enemy_tower
    return coords_enemy_towers

@turncache
def get_towers(turn: int, data: UnitResponse, world: WorldResponse) -> dict[Coordinates, Tower]:
    coords_towers = dict()
    for tower in data.base:
        coords = Coordinates(tower.x, tower.y)
        coords_towers[coords] = tower
    return coords_towers

@turncache
def get_head_tower(turn: int, data: UnitResponse, world: WorldResponse) -> Tower:
    for tower in data.base:
        if tower.is_head:
            return tower
    print('[ERROR]: impossible state')
    return Tower(-1, -1, -1, Coordinates(-1, -1), False, '', -1, -1)

@turncache
def get_zpots(turn: int, data: UnitResponse, world: WorldResponse) -> dict[Coordinates, Zpot]:
    coords_zpots = dict()
    for zpot in world.zpots:
        coords = Coordinates(zpot.x, zpot.y)
        coords_zpots[coords] = zpot
    return coords_zpots

@turncache
def get_damage_by_zombies(turn: int, data: UnitResponse, world: WorldResponse) -> dict[Coordinates, int]:
    towers = get_towers(turn, data, world)
    damage = defaultdict(int)

    for zombie in data.zombies:
        if zombie.wait_turns != 0:
            continue
        if zombie.type == 'normal':
            pass
        if zombie.type == 'fast':
            pass
        if zombie.type == 'bomber':
            pass
        if zombie.type == 'liner':
            pass
        if zombie.type == 'juggernaut':
            pass
        if zombie.type == 'chaos_knight':
            pass
    return dict(damage)

@turncache
def get_connected_base(turn: int, data: UnitResponse, world: WorldResponse) -> list[Tower]:
    component = []

    head = get_head_tower(turn, data, world)
    towers = get_towers(turn, data, world)

    head_coords = Coordinates(head.x, head.y)

    q = deque()
    q.append(head_coords)
    visited = set()
    visited.add(head_coords)

    while q:
        coords = q.popleft()
        if coords not in towers:
            continue
        component.append(towers[coords])

        for neighbor in neighbours4(coords):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    
    return component


def get_attacks(data: UnitResponse, world: WorldResponse) -> list[AttackCommand]:
    turn = data.turn
    attacks = []
    base = get_connected_base(turn, data, world)

    zombies      = get_zombies(turn, data, world)
    enemy_towers = get_enemy_towers(turn, data, world)

    damage_applied: defaultdict[Coordinates, int] = defaultdict(int)
    for tower in base:
        x1 = tower.x
        y1 = tower.y
        r  = tower.r

        reachable_zombies = []
        reachable_enemy_towers = []
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                x2 = x1 + dx
                y2 = y1 + dy
                if r ** 2 < (x1 - x2) ** 2 + (y1 - y2) ** 2:
                    continue

                coords = Coordinates(x2, y2) 
                if coords in zombies:
                    reachable_zombies.extend(zombies[coords])
                if coords in enemy_towers:
                    enemy_tower = enemy_towers[coords]
                    reachable_enemy_towers.append(enemy_tower)

        reachable_zombies.sort(key=lambda zombie: zombie.health)
        reachable_enemy_towers.sort(key=lambda enemy_tower: -enemy_tower.is_head)

        targets = reachable_zombies + reachable_enemy_towers
        for target in targets:
            x2 = target.x
            y2 = target.y
            target_coords = Coordinates(x2, y2)
            if damage_applied[target_coords] >= target.health:
                continue
            if r ** 2 >= (x1 - x2) ** 2 + (y1 - y2) ** 2:
                attack = AttackCommand(tower.id, target_coords)
                attacks.append(attack)
                damage_applied[target_coords] += tower.attack
                break

    return attacks


def valid_build(coords: Coordinates, data: UnitResponse, world: WorldResponse) -> bool:
    turn = data.turn

    enemy_towers = get_enemy_towers(turn, data, world)
    zombies      = get_zombies(turn, data, world)
    towers       = get_towers(turn, data, world)
    zpots        = get_zpots(turn, data, world)

    if coords in enemy_towers:
        return False
    if coords in zpots:
        return False
    if coords in zombies:
        return False
    if coords in towers:
        return False

    for neighbour in neighbours4(coords):
        if neighbour in zpots:
            return False

    for neighbour in neighbours8(coords):
        if neighbour in enemy_towers:
            return False

    return True


def get_builds(data: UnitResponse, world: WorldResponse) -> list[BuildCommand]:
    turn = data.turn

    spots = list()
    base = get_connected_base(turn, data, world)
    gold = data.player.gold

    for tower in base:
        for neighbour in neighbours4(Coordinates(tower.x, tower.y)):
            spots.append(neighbour)

    spots = list(set(spots))
    spots = filter(lambda spot: valid_build(spot, data, world), spots)
    spots = list(spots)
    random.shuffle(spots)
    spots = spots[:gold]
    
    builds = []
    for spot in spots:
        builds.append(BuildCommand.from_coordinates(spot))

    return builds


def get_move_base(data: UnitResponse, world: WorldResponse) -> Coordinates:
    base = data.base

    main_tower = (-1,-1)

    for tower in base:
        if tower.is_head:
            main_tower = (tower.x, tower.y)

    if human_controls.player_move_x is not None and human_controls.player_move_y is not None:
        if not ((human_controls.player_move_x == main_tower[0]) and (human_controls.player_move_y == main_tower[1])):
            print('Moving center to ', int(human_controls.player_move_x), int(human_controls.player_move_y))
        return Coordinates(human_controls.player_move_x, human_controls.player_move_y)

    return Coordinates(main_tower[0], main_tower[1])


def get_command(data: UnitResponse, world: WorldResponse):
    attacks   = get_attacks(data, world)
    builds    = get_builds(data, world)
    move_base = get_move_base(data, world)

    return Command(attacks, builds, move_base)
