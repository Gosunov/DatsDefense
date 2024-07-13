import random
from collections import defaultdict

from entities import *


def get_attacks(data: UnitResponse, world: WorldResponse) -> list[AttackCommand]:
    attacks = []
    base = data.base
    
    zombies = data.zombies
    zombies.sort(key=lambda zombie: zombie.health)
    enemy_towers = data.enemy_towers
    enemy_towers.sort(key=lambda tower: not tower.is_head) # heads tower first
    targets = zombies + enemy_towers


    damage_applied = defaultdict(int) # damage_applied[<coords>] = <damage> 
    for tower in base:
        for target in targets:
            x2 = target.x
            y2 = target.y
            target_coords = Coordinates(x2, y2)
            if damage_applied[target_coords] >= target.health:
                continue

            x1 = tower.x
            y1 = tower.y
            r  = tower.r
            if r ** 2 >= (x1 - x2) ** 2 + (y1 - y2) ** 2:
                attack = AttackCommand(tower.id, target_coords)
                attacks.append(attack)
                damage_applied[target_coords] += tower.attack
                break

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
    attacks   = get_attacks(data, world)
    builds    = get_builds(data, world)
    move_base = get_move_base(data, world)
    return Command(attacks, builds, move_base)
