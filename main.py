import json
from time import sleep, time
import random
from collections import defaultdict

from entities import *
from api import mainServerApi, testServerApi, MockApi


def get_attacks(data: UnitResponse, world: WorldResponse) -> list[AttackCommand]:
    attacks = []
    base = data.base
    zombies = data.zombies
    zombies.sort(key=lambda zombie: zombie.health)
    enemy_towers = data.enemy_towers

    damage_applied = defaultdict(int) # damage_applied[<coords>] = <damage> 
    for tower in base:
        targets = zombies + enemy_towers
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


def print_status(data: UnitResponse, 
                 world: WorldResponse, 
                 cmd: Command, 
                 resp: CommandResponse):
    points = data.player.points
    base_size = len(data.base)
    zombie_kills = data.player.zombie_kills
    gold = data.player.gold
    attacks = len(cmd.attacks)
    builds = len(cmd.builds)
    rejected = len(resp.errors)
    print(
        "points=%d,base_size=%d,zombie_kills=%d,gold=%d,attacks=%d,builds=%d,rejected=%d" % 
        (points, base_size, zombie_kills, gold, attacks, builds, rejected)
    )
    


API = MockApi()
# API = testServerApi 
# API = mainServerApi

starts_in_sec = API.participate().starts_in_sec
print('Round is starting in %ds, waiting...' % starts_in_sec)
sleep(starts_in_sec)

world = API.world()
while True:
    data = API.units()
    t1 = int(time() * 10**3)
    tleft = data.turn_ends_in_ms

    attacks   = get_attacks(data, world)
    builds    = get_builds(data, world)
    move_base = get_move_base(data, world)

    cmd = Command(attacks, builds, move_base)

    resp = API.command(cmd)
    for error in resp.errors:
        print(error)

    print_status(data, world, cmd, resp)
    t2 = int(time() * 10**3)
    tused = t2 - t1
    print("Finished turn %d in %dms" % (data.turn, tused))
    sleep((tleft - tused) / 10**6)