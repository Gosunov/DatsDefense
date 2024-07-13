import random
from collections import defaultdict

from entities import *
from time import time


def get_zombies(data: UnitResponse, world: WorldResponse) -> dict[Coordinates, list[Zombie]]:
    coords_zombies = defaultdict(list)
    for zombie in data.zombies:
        coords = Coordinates(zombie.x, zombie.y)
        coords_zombies[coords].append(zombie)
    return dict(coords_zombies)


def get_enemy_towers(data: UnitResponse, world: WorldResponse) -> dict[Coordinates, EnemyTower]:
    coords_enemy_towers = dict()
    for enemy_tower in data.enemy_towers:
        coords = Coordinates(enemy_tower.x, enemy_tower.y)
        coords_enemy_towers[coords] = enemy_tower
    return coords_enemy_towers


def get_attacks(data: UnitResponse, world: WorldResponse) -> list[AttackCommand]:
    attacks = []
    base = data.base

    zombies      = get_zombies(data, world)
    enemy_towers = get_enemy_towers(data, world)

    damage_applied = defaultdict(int)
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
