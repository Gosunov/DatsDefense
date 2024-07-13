import random
from collections import defaultdict

from entities import *
from time import time

def get_attacks(data: UnitResponse, world: WorldResponse) -> list[AttackCommand]:
    attacks = []
    base = data.base

    targets = {} # targets[(x,y)] = (target, priority)

    zombies = data.zombies
    for zombie in zombies:
        targets[(zombie.x, zombie.y)] = (zombie, 10)

    enemy_towers = data.enemy_towers
    for e_tower in enemy_towers:
        targets[(e_tower.x, e_tower.y)] = (e_tower, 5)

    damage_applied = defaultdict(int) # damage_applied[<coords>] = <damage> 

    square_radius = 5
    for tower in base:

        attack_coord = None
        happiness = -100

        for dx in range(-square_radius, square_radius+1):
            for dy in range(-square_radius, square_radius + 1):

                x2 = tower.x + dx
                y2 = tower.y + dy

                if (x2, y2) not in targets: continue

                target_coords = Coordinates(x2, y2)
                if damage_applied[target_coords] >= targets[(x2, y2)][0].health:
                    continue

                x1 = tower.x
                y1 = tower.y
                r  = tower.r

                if r ** 2 >= (x1 - x2) ** 2 + (y1 - y2) ** 2:
                    cur_happiness = targets[(x2, y2)][1] * 100 - targets[(x2, y2)][0].health # [5 or 10] * 100 - health
                    if cur_happiness > happiness:
                        happiness = cur_happiness
                        attack_coord = target_coords
                    break

        if attack_coord is not None:
            attack = AttackCommand(tower.id, target_coords)
            attacks.append(attack)
            damage_applied[target_coords] += tower.attack

    return attacks


def get_builds(data: UnitResponse, world: WorldResponse) -> list[BuildCommand]:
    spots = set()
    base = data.base
    gold = data.player.gold

    for tower in base:
        spots.add(Coordinates(tower.x, tower.y + 1))
        spots.add(Coordinates(tower.x, tower.y - 1))
        spots.add(Coordinates(tower.x + 1, tower.y))
        spots.add(Coordinates(tower.x - 1, tower.y))

    for tower in base:
        coords = Coordinates(tower.x, tower.y)
        if coords in spots:
            spots.remove(coords)

    spots = list(spots)
    random.shuffle(spots)
    spots = spots[:gold * 2]
    builds = []

    for spot in spots:
        builds.append(BuildCommand.from_coordinates(spot))

    return builds


def get_move_base(data: UnitResponse, world: WorldResponse) -> Coordinates:
    base = data.base
    for tower in base:
        if tower.is_head:
            return Coordinates(tower.x, tower.y)
    return Coordinates(-1, -1)


def get_command(data: UnitResponse, world: WorldResponse):
    t1 = int(time() * 10 ** 3)

    attacks   = get_attacks(data, world)
    t2 = int(time() * 10 ** 3)
    print(f'{(t2 - t1)}', end=' ')

    builds    = get_builds(data, world)
    t3 = int(time() * 10 ** 3)
    print(f'{(t3 - t2)}', end=' ')

    move_base = get_move_base(data, world)
    t4 = int(time() * 10 ** 3)
    print(f'{(t4 - t3)} (att, bui, move)',)

    return Command(attacks, builds, move_base)
